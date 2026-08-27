"""
Step 6: Retrieval interface (§10).

Strategy: Hybrid search (vector + BM25) with optional cross-encoder reranking.

How it works:
  1. VECTOR SEARCH — Embed the query with the same model used for chunks
     (all-MiniLM-L6-v2), then find the nearest neighbours via pgvector's
     cosine distance operator (<=>).
  2. KEYWORD SEARCH (BM25-style) — Use PostgreSQL's built-in full-text
     search (tsvector/tsquery) to find chunks matching the query terms.
     ts_rank_cd gives a relevance score analogous to BM25.
  3. RECIPROCAL RANK FUSION (RRF) — Merge the two ranked lists using
     RRF (score = 1/(k+rank)) so that a chunk ranked highly by *either*
     method surfaces to the top, while a chunk ranked highly by *both*
     gets an even stronger boost.
  4. CROSS-ENCODER RERANKING (optional) — Pass the top RRF candidates
     through a cross-encoder (cross-encoder/ms-marco-MiniLM-L-6-v2) that
     scores each (query, chunk) pair jointly, producing a more accurate
     relevance estimate than either retriever alone.

Why hybrid over pure vector:
  - Vector search excels at semantic/conceptual similarity ("models that
    route tokens to experts" finds MoE content even without the acronym).
  - Keyword search excels at exact term matching ("GRPO", "Mamba", specific
    paper titles) which embedding models can miss, especially for rare
    domain acronyms.
  - RRF combines both with no learned parameters, making it robust.

Why add a reranker:
  - The cross-encoder sees query and chunk together (not independently
    embedded), so it can detect fine-grained relevance that bi-encoder
    similarity misses.
  - At the cost of ~100ms for 20 candidates, it significantly improves
    precision in the final top-5.
  - If the reranker doesn't improve results (or adds too much latency),
    it can be disabled with --no-rerank.

Run:
    python src/retrieve.py "What are the advantages of MoE over dense models?"
    python src/retrieve.py "GRPO vs PPO" --top-k 10
    python src/retrieve.py "sliding window attention" --no-rerank

Python API:
    from src.retrieve import retrieve
    results = retrieve("What is Mamba?", top_k=5, rerank=True)

Week 2 handoff:
    Input:  Natural-language query string
    Output: List of dicts with keys: rank, text, url, title, headers,
            similarity_score (cosine), rrf_score, rerank_score (if reranked)
    Access: Python function `retrieve()` or CLI
"""

import argparse
import json
import os
import sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

DB_CONFIG = {
    "host": os.environ.get("PGHOST", "localhost"),
    "port": os.environ.get("PGPORT", "5432"),
    "dbname": os.environ.get("PGDATABASE", "ragdb"),
    "user": os.environ.get("PGUSER", "postgres"),
    "password": os.environ.get("PGPASSWORD", "pass"),
}

EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# RRF parameter: higher k smooths rank differences.
RRF_K = 60

# How many candidates to pull from each retriever before fusion.
CANDIDATE_POOL = 30

# Lazy-loaded models (initialized on first call).
_embed_model = None
_reranker_model = None


def _get_embed_model():
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer(EMBEDDING_MODEL)
    return _embed_model


def _get_reranker():
    global _reranker_model
    if _reranker_model is None:
        from sentence_transformers import CrossEncoder
        _reranker_model = CrossEncoder(RERANKER_MODEL)
    return _reranker_model


def _vector_search(cur, query_embedding: list, top_k: int) -> list[dict]:
    """Find nearest chunks by cosine similarity via pgvector."""
    cur.execute(
        """
        SELECT chunk_id, text, url, title, headers,
               1 - (embedding <=> %s::vector) AS similarity
        FROM chunks
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """,
        (query_embedding, query_embedding, top_k),
    )
    return [
        {
            "chunk_id": row[0], "text": row[1], "url": row[2],
            "title": row[3], "headers": row[4], "similarity": float(row[5]),
        }
        for row in cur.fetchall()
    ]


def _keyword_search(cur, query: str, top_k: int) -> list[dict]:
    """Find chunks by PostgreSQL full-text search (BM25-like ranking)."""
    # Build a tsquery from the natural-language query.
    # plainto_tsquery handles stemming and stop-word removal automatically.
    cur.execute(
        """
        SELECT chunk_id, text, url, title, headers,
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
            "chunk_id": row[0], "text": row[1], "url": row[2],
            "title": row[3], "headers": row[4], "bm25_score": float(row[5]),
        }
        for row in cur.fetchall()
    ]


def _rrf_fuse(vector_results: list[dict], keyword_results: list[dict], k: int = RRF_K) -> list[dict]:
    """Merge two ranked lists using Reciprocal Rank Fusion.
    RRF score = sum over lists of 1/(k + rank).
    """
    scores: dict[str, float] = {}
    chunk_data: dict[str, dict] = {}

    for rank, r in enumerate(vector_results):
        cid = r["chunk_id"]
        scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + rank + 1)
        if cid not in chunk_data:
            chunk_data[cid] = r

    for rank, r in enumerate(keyword_results):
        cid = r["chunk_id"]
        scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + rank + 1)
        if cid not in chunk_data:
            chunk_data[cid] = r

    # Sort by fused score descending.
    ranked = sorted(scores.items(), key=lambda x: -x[1])

    results = []
    for cid, rrf_score in ranked:
        entry = dict(chunk_data[cid])
        entry["rrf_score"] = rrf_score
        results.append(entry)

    return results


def retrieve(
    query: str,
    top_k: int = 5,
    rerank: bool = True,
    candidate_pool: int = CANDIDATE_POOL,
) -> list[dict]:
    """
    Retrieve relevant chunks for a natural-language query.

    Args:
        query:          Natural-language question or search terms.
        top_k:          Number of results to return.
        rerank:         If True, apply cross-encoder reranking.
        candidate_pool: How many candidates each retriever fetches before
                        fusion (only the top_k after fusion/reranking are
                        returned).

    Returns:
        List of dicts, each containing:
            rank            (int)   1-based rank
            text            (str)   chunk text
            url             (str)   source URL
            title           (str)   source document title
            headers         (dict)  section headers from the chunk
            similarity      (float) cosine similarity (vector search)
            rrf_score       (float) reciprocal rank fusion score
            rerank_score    (float) cross-encoder score (if reranked)
    """
    # 1. Embed the query
    model = _get_embed_model()
    query_vec = model.encode(query, normalize_embeddings=True).tolist()

    # 2. Dual retrieval
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    vector_results = _vector_search(cur, query_vec, candidate_pool)
    keyword_results = _keyword_search(cur, query, candidate_pool)

    cur.close()
    conn.close()

    # 3. RRF fusion
    fused = _rrf_fuse(vector_results, keyword_results)

    # Take more candidates than top_k for reranking, then trim.
    rerank_pool = fused[: max(top_k * 3, 20)]

    # 4. Optional cross-encoder reranking
    if rerank and len(rerank_pool) > 0:
        reranker = _get_reranker()
        pairs = [(query, r["text"]) for r in rerank_pool]
        scores = reranker.predict(pairs)
        for r, score in zip(rerank_pool, scores):
            r["rerank_score"] = float(score)
        rerank_pool.sort(key=lambda r: -r["rerank_score"])

    # 5. Final top_k with ranks
    final = rerank_pool[:top_k]
    for i, r in enumerate(final):
        r["rank"] = i + 1

    return final


def format_results(results: list[dict]) -> str:
    """Pretty-print results for CLI output."""
    lines = []
    for r in results:
        lines.append(f"{'='*80}")
        lines.append(f"  Rank:       {r['rank']}")
        lines.append(f"  URL:        {r.get('url', 'N/A')}")
        lines.append(f"  Title:      {r.get('title', 'N/A')}")
        if r.get("similarity") is not None:
            lines.append(f"  Cosine sim: {r['similarity']:.4f}")
        lines.append(f"  RRF score:  {r.get('rrf_score', 0):.6f}")
        if r.get("rerank_score") is not None:
            lines.append(f"  Rerank:     {r['rerank_score']:.4f}")
        lines.append(f"  Text:       {r['text'][:300]}...")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Retrieve relevant chunks from the knowledge base."
    )
    parser.add_argument("query", help="Natural-language query")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results (default: 5)")
    parser.add_argument("--no-rerank", action="store_true", help="Skip cross-encoder reranking")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of formatted text")
    args = parser.parse_args()

    results = retrieve(args.query, top_k=args.top_k, rerank=not args.no_rerank)

    if args.json:
        # Drop non-serializable fields
        for r in results:
            if "headers" in r and not isinstance(r["headers"], (dict, list, str)):
                r["headers"] = str(r["headers"])
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(f"\nQuery: {args.query}")
        print(f"Strategy: Hybrid (vector + BM25) {'+ reranker' if not args.no_rerank else '(no rerank)'}")
        print(f"Results: {len(results)}\n")
        print(format_results(results))


if __name__ == "__main__":
    main()
