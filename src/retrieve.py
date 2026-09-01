"""Hybrid retrieval against the PostgreSQL + pgvector knowledge base."""

import argparse
import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import psycopg2

from src.database import connect as connect_database
from src.database import get_db_config as read_db_config
from src.settings import (
    EMBEDDING_DIM,
    EMBEDDING_MODEL,
    EMBEDDING_MODEL_REVISION,
    IVFFLAT_PROBES as CONFIGURED_IVFFLAT_PROBES,
    PIPELINE_VERSION,
    PREPROCESSING_VERSION,
    RERANKER_MODEL,
    RERANKER_MODEL_REVISION,
)

def get_db_config() -> dict:
    return read_db_config(purpose="retrieval")


RRF_K = 30
CANDIDATE_POOL = 150
# Storage caps IVFFlat at 100 lists. Probing every list makes evaluation and
# local retrieval stable across index rebuilds at the current corpus scale.
IVFFLAT_PROBES = CONFIGURED_IVFFLAT_PROBES
RERANK_SOURCE_LIMIT = 2
FINAL_SOURCE_LIMIT = 1
_embed_model = None
_reranker_model = None


def get_connection():
    return connect_database(purpose="retrieval", statement_timeout_ms=10_000)


def _get_embed_model():
    global _embed_model
    if _embed_model is None:
        from sentence_transformers import SentenceTransformer
        try:
            _embed_model = SentenceTransformer(
                EMBEDDING_MODEL,
                revision=EMBEDDING_MODEL_REVISION,
                local_files_only=True,
            )
        except (OSError, ValueError):
            _embed_model = SentenceTransformer(
                EMBEDDING_MODEL, revision=EMBEDDING_MODEL_REVISION
            )
    return _embed_model


def _get_reranker():
    global _reranker_model
    if _reranker_model is None:
        from sentence_transformers import CrossEncoder
        try:
            _reranker_model = CrossEncoder(
                RERANKER_MODEL,
                revision=RERANKER_MODEL_REVISION,
                local_files_only=True,
            )
        except (OSError, ValueError):
            _reranker_model = CrossEncoder(
                RERANKER_MODEL, revision=RERANKER_MODEL_REVISION
            )
    return _reranker_model


def _validate_query(query: str) -> str:
    if not isinstance(query, str):
        raise TypeError("query must be a string")
    normalized = query.strip()
    if not normalized:
        raise ValueError("query must be a non-empty string")
    if len(normalized) > 512:
        raise ValueError("query is too long; limit is 512 characters")
    return normalized


def _validate_top_k(top_k: int, candidate_pool: int) -> tuple[int, int]:
    if not isinstance(top_k, int) or isinstance(top_k, bool):
        raise TypeError("top_k must be an integer")
    if not isinstance(candidate_pool, int) or isinstance(candidate_pool, bool):
        raise TypeError("candidate_pool must be an integer")
    if top_k <= 0:
        raise ValueError("top_k must be > 0")
    if candidate_pool <= 0:
        raise ValueError("candidate_pool must be > 0")
    if top_k > 50:
        raise ValueError("top_k must be <= 50")
    if candidate_pool < top_k:
        raise ValueError("candidate_pool must be >= top_k")
    if candidate_pool > 1000:
        raise ValueError("candidate_pool must be <= 1000")
    return top_k, candidate_pool


def _read_index_manifest(cur, include_urls: bool = True) -> dict:
    cur.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = current_schema() AND table_name = 'chunks'
        """
    )
    columns = {row[0] for row in cur.fetchall()}
    required = {
        "embedding_text",
        "embedding_model",
        "embedding_model_revision",
        "preprocessing_version",
        "pipeline_version",
    }
    missing_columns = sorted(required - columns)
    if "chunk_id" not in columns:
        raise RuntimeError("The chunks table is missing; run src/store.py first.")

    optional_selects = []
    for column in (
        "embedding_model",
        "embedding_model_revision",
        "preprocessing_version",
        "pipeline_version",
    ):
        if column in columns:
            optional_selects.append(f"array_remove(array_agg(DISTINCT {column}), NULL)")
        else:
            optional_selects.append("ARRAY[]::text[]")
    cur.execute(
        f"""
        SELECT COUNT(*), COUNT(DISTINCT url), {', '.join(optional_selects)}
        FROM chunks
        """
    )
    row = cur.fetchone()
    manifest = {
        "row_count": row[0],
        "source_count": row[1],
        "embedding_models": row[2] or [],
        "embedding_model_revisions": row[3] or [],
        "preprocessing_versions": row[4] or [],
        "pipeline_versions": row[5] or [],
        "missing_identity_columns": missing_columns,
    }
    if include_urls:
        cur.execute("SELECT DISTINCT url FROM chunks WHERE url IS NOT NULL")
        manifest["source_urls"] = [item[0] for item in cur.fetchall()]
    return manifest


def _validate_index_identity(manifest: dict) -> None:
    expected = {
        "embedding_models": [EMBEDDING_MODEL],
        "embedding_model_revisions": [EMBEDDING_MODEL_REVISION],
        "preprocessing_versions": [PREPROCESSING_VERSION],
        "pipeline_versions": [PIPELINE_VERSION],
    }
    mismatches = []
    if manifest.get("missing_identity_columns"):
        mismatches.append(
            "missing columns: " + ", ".join(manifest["missing_identity_columns"])
        )
    for field, wanted in expected.items():
        actual = sorted(manifest.get(field) or [])
        if actual != wanted:
            mismatches.append(f"{field}={actual!r}, expected {wanted!r}")
    if mismatches:
        raise RuntimeError(
            "The retrieval index is incompatible with the active embedding configuration ("
            + "; ".join(mismatches)
            + "). Re-run src/embed.py and src/store.py."
        )


def get_index_manifest() -> dict:
    """Return auditable corpus/model metadata and validate query-vector compatibility."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                manifest = _read_index_manifest(cur, include_urls=True)
    except psycopg2.Error as exc:
        raise RuntimeError("Database query failed while reading index metadata.") from exc
    _validate_index_identity(manifest)
    return manifest


def _vector_search(cur, query_embedding: list, top_k: int) -> list[dict]:
    cur.execute(
        """
        SELECT chunk_id, text, embedding_text, url, title, headers,
               1 - (embedding <=> %s::vector) AS similarity
        FROM chunks
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """,
        (query_embedding, query_embedding, top_k),
    )
    return [
        {
            "chunk_id": row[0],
            "text": row[1],
            "embedding_text": row[2],
            "url": row[3],
            "title": row[4],
            "headers": row[5],
            "similarity": float(row[6]),
        }
        for row in cur.fetchall()
    ]


def _keyword_search(cur, query: str, top_k: int) -> list[dict]:
    cur.execute(
        """
        SELECT chunk_id, text, embedding_text, url, title, headers,
               ts_rank_cd(text_search, plainto_tsquery('english', %s)) AS rank_score
        FROM chunks
        WHERE text_search @@ plainto_tsquery('english', %s)
        ORDER BY rank_score DESC
        LIMIT %s
        """,
        (query, query, top_k),
    )
    return [
        {
            "chunk_id": row[0],
            "text": row[1],
            "embedding_text": row[2],
            "url": row[3],
            "title": row[4],
            "headers": row[5],
            "text_rank_score": float(row[6]),
        }
        for row in cur.fetchall()
    ]


def _rrf_fuse(vector_results, keyword_results, k=RRF_K):
    scores = {}
    chunk_data = {}

    for rank, r in enumerate(vector_results):
        cid = r["chunk_id"]
        scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + rank + 1)
        chunk_data.setdefault(cid, {}).update(r)

    for rank, r in enumerate(keyword_results):
        cid = r["chunk_id"]
        scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + rank + 1)
        chunk_data.setdefault(cid, {}).update(r)

    results = []
    for cid, score in sorted(scores.items(), key=lambda x: -x[1]):
        data = chunk_data[cid]
        results.append({
            "chunk_id": cid,
            "text": data.get("text", ""),
            "embedding_text": data.get("embedding_text", data.get("text", "")),
            "url": data.get("url", ""),
            "title": data.get("title", ""),
            "headers": data.get("headers", {}),
            "rrf_score": score,
            "similarity": data.get("similarity"),   # None if missing
            "text_rank_score": data.get("text_rank_score"),
        })
    return results


def _source_key(result: dict) -> str:
    url = result.get("url") or ""
    if not url:
        return result.get("chunk_id") or ""
    parts = urlsplit(url)
    host = parts.netloc.lower()
    path = parts.path.rstrip("/").lower()
    if host in {"arxiv.org", "www.arxiv.org"} and path.startswith("/abs/"):
        host = "arxiv.org"
        path = re.sub(r"v\d+$", "", path)
    return f"{host}{path}"


def _limit_per_source(results: list[dict], limit: int) -> list[dict]:
    """Prevent overlapping chunks from a long paper consuming the whole top-k."""
    if limit <= 0:
        raise ValueError("source limit must be > 0")
    selected, counts = [], {}
    for result in results:
        source = _source_key(result)
        if counts.get(source, 0) >= limit:
            continue
        counts[source] = counts.get(source, 0) + 1
        selected.append(result)
    return selected


def retrieve(
    query: str,
    top_k: int = 20,
    rerank: bool = False,
    candidate_pool: int = CANDIDATE_POOL,
) -> list[dict]:
    query = _validate_query(query)
    top_k, candidate_pool = _validate_top_k(top_k, candidate_pool)

    try:
        model = _get_embed_model()
        query_vec = model.encode(query, normalize_embeddings=True, show_progress_bar=False, batch_size=1)
        if hasattr(query_vec, "tolist"):
            query_vec = query_vec.tolist()
        if not isinstance(query_vec, list) or len(query_vec) != EMBEDDING_DIM:
            raise ValueError(
                f"Query embedding dimension mismatch: expected {EMBEDDING_DIM}, "
                f"got {len(query_vec) if isinstance(query_vec, list) else 'non-list'}"
            )
        if not all(math.isfinite(float(value)) for value in query_vec):
            raise ValueError("Query embedding contains NaN or infinity")
    except Exception as exc:
        raise RuntimeError(f"Embedding model failed for query: {query}") from exc

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                manifest = _read_index_manifest(cur, include_urls=False)
                _validate_index_identity(manifest)
                cur.execute("SELECT set_config('ivfflat.probes', %s, true)", (str(IVFFLAT_PROBES),))
                vector_results = _vector_search(cur, query_vec, candidate_pool)
                keyword_results = _keyword_search(cur, query, candidate_pool)
    except psycopg2.Error as exc:
        raise RuntimeError("Database query failed during retrieval.") from exc

    fused = _rrf_fuse(vector_results, keyword_results)
    rerank_pool = _limit_per_source(fused, limit=RERANK_SOURCE_LIMIT)[: max(top_k * 6, 40)]

    if rerank and len(rerank_pool) > 0:
        try:
            reranker = _get_reranker()
            pairs = [(query, r["embedding_text"]) for r in rerank_pool]
            scores = reranker.predict(pairs)
            if len(scores) != len(rerank_pool):
                raise ValueError(
                    "Reranker returned a different number of scores than candidates"
                )
            for r, score in zip(rerank_pool, scores):
                r["rerank_score"] = float(score)
            rerank_pool.sort(key=lambda r: -r["rerank_score"])
        except Exception as exc:
            raise RuntimeError("Cross-encoder reranking failed.") from exc

    final = _limit_per_source(rerank_pool, limit=FINAL_SOURCE_LIMIT)[:top_k]
    for i, r in enumerate(final):
        r["rank"] = i + 1
    return final


def format_results(results: list[dict]) -> str:
    lines = []
    for r in results:
        lines.append(f"{'='*80}")
        lines.append(f"  Rank:       {r['rank']}")
        lines.append(f"  URL:        {r.get('url', 'N/A')}")
        lines.append(f"  Title:      {r.get('title', 'N/A')}")
        if r.get("similarity") is not None:
            lines.append(f"  Cosine sim: {r['similarity']:.4f}")
        if r.get("text_rank_score") is not None:
            lines.append(f"  Text rank:  {r['text_rank_score']:.4f}")
        lines.append(f"  RRF score:  {r.get('rrf_score', 0):.6f}")
        if r.get("rerank_score") is not None:
            lines.append(f"  Rerank:     {r['rerank_score']:.4f}")
        lines.append(f"  Text:       {r['text'][:300]}...")
        lines.append("")
    return "\n".join(lines)


def _console_safe(value: str) -> str:
    """Replace characters unsupported by a legacy Windows console encoding."""
    encoding = sys.stdout.encoding or "utf-8"
    return value.encode(encoding, errors="replace").decode(encoding)


def main():
    parser = argparse.ArgumentParser(description="Retrieve relevant chunks from the knowledge base.")
    parser.add_argument("query", help="Natural-language query")
    parser.add_argument("--top-k", type=int, default=20, help="Number of results (default: 20)")
    rerank_group = parser.add_mutually_exclusive_group()
    rerank_group.add_argument(
        "--rerank",
        action="store_true",
        help="Enable cross-encoder reranking (hybrid-only is the evaluated default)",
    )
    rerank_group.add_argument("--no-rerank", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of formatted text")
    args = parser.parse_args()

    rerank_enabled = args.rerank and not args.no_rerank
    results = retrieve(args.query, top_k=args.top_k, rerank=rerank_enabled)

    if args.json:
        for r in results:
            if "headers" in r and not isinstance(r["headers"], (dict, list, str)):
                r["headers"] = str(r["headers"])
        print(_console_safe(json.dumps(results, indent=2, ensure_ascii=False)))
    else:
        output = "\n".join(
            (
                f"\nQuery: {args.query}",
                f"Strategy: Hybrid (vector + PostgreSQL text rank) "
                f"{'+ reranker' if rerank_enabled else '(no rerank)'}",
                f"Results: {len(results)}\n",
                format_results(results),
            )
        )
        print(_console_safe(output))


if __name__ == "__main__":
    main()
