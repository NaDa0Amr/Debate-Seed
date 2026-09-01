"""Atomically build the PostgreSQL + pgvector retrieval index."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from psycopg2 import sql
from psycopg2.extras import execute_values

from src.database import connect as connect_database
from src.database import get_db_config as read_db_config
from src.jsonl import iter_jsonl
from src.settings import (
    EMBEDDING_DIM,
    EMBEDDING_MODEL,
    EMBEDDING_MODEL_REVISION,
    IVFFLAT_MAX_LISTS,
    PIPELINE_VERSION,
    PREPROCESSING_VERSION,
)

CHUNKS_PATH = Path("data/chunks.jsonl")
EMBEDDED_PATH = Path("data/chunks_with_embeddings.jsonl")
STAGING_TABLE = "chunks_staging"
PREVIOUS_TABLE = "chunks_previous"
INSERT_BATCH_SIZE = 500


def get_db_config() -> dict:
    return read_db_config(purpose="the pipeline")


def _source_hashes() -> set[str]:
    hashes: set[str] = set()
    chunk_ids: set[str] = set()
    for chunk in iter_jsonl(CHUNKS_PATH):
        chunk_id = chunk.get("chunk_id")
        content_hash = chunk.get("content_hash")
        if not chunk_id or chunk_id in chunk_ids:
            raise ValueError(f"Missing or duplicate source chunk_id: {chunk_id!r}")
        if not content_hash:
            raise ValueError(f"A source chunk is missing content_hash: {chunk_id}")
        if content_hash in hashes:
            raise ValueError(f"Duplicate source content_hash: {content_hash}")
        chunk_ids.add(chunk_id)
        hashes.add(content_hash)
    return hashes


def _scan_embeddings(source_hashes: set[str]) -> dict:
    hashes: set[str] = set()
    chunk_ids: set[str] = set()
    dimensions: set[int] = set()
    models: set[str] = set()
    revisions: set[str] = set()
    preprocessing_versions: set[str] = set()
    pipeline_versions: set[str] = set()
    count = 0

    for chunk in iter_jsonl(EMBEDDED_PATH):
        count += 1
        chunk_id = chunk.get("chunk_id")
        content_hash = chunk.get("content_hash")
        embedding = chunk.get("embedding")
        for required_field in ("chunk_id", "text", "embedding_text"):
            if not chunk.get(required_field):
                raise ValueError(
                    f"Embedded row is missing {required_field}: {chunk_id!r}"
                )
        if chunk_id in chunk_ids:
            raise ValueError(f"Duplicate embedded chunk_id: {chunk_id!r}")
        if not content_hash or content_hash in hashes:
            raise ValueError(f"Missing or duplicate embedded content_hash: {content_hash!r}")
        if not isinstance(embedding, list) or not embedding:
            raise ValueError(f"Missing embedding for chunk {chunk.get('chunk_id')}")
        try:
            numeric_embedding = [float(value) for value in embedding]
        except (TypeError, ValueError) as error:
            raise ValueError(
                f"Embedding contains a non-numeric value for chunk {chunk.get('chunk_id')}"
            ) from error
        if not all(math.isfinite(value) for value in numeric_embedding):
            raise ValueError(
                f"Embedding contains NaN or infinity for chunk {chunk.get('chunk_id')}"
            )
        declared_dim = chunk.get("embedding_dim")
        if declared_dim != len(embedding):
            raise ValueError(
                f"Embedding dimension metadata mismatch for {chunk.get('chunk_id')}: "
                f"declared {declared_dim}, actual {len(embedding)}"
            )
        hashes.add(content_hash)
        chunk_ids.add(chunk_id)
        dimensions.add(len(embedding))
        models.add(chunk.get("embedding_model"))
        revisions.add(chunk.get("embedding_model_revision"))
        preprocessing_versions.add(chunk.get("preprocessing_version"))
        pipeline_versions.add(chunk.get("pipeline_version"))

    if not count:
        raise RuntimeError("No embedded chunks found; run src/embed.py first.")
    if hashes != source_hashes:
        missing = len(source_hashes - hashes)
        stale = len(hashes - source_hashes)
        raise RuntimeError(
            "Embedded chunks are out of sync with data/chunks.jsonl "
            f"(missing={missing}, stale={stale}). Run src/embed.py first."
        )

    expected_identity = {
        "dimensions": {EMBEDDING_DIM},
        "models": {EMBEDDING_MODEL},
        "revisions": {EMBEDDING_MODEL_REVISION},
        "preprocessing_versions": {PREPROCESSING_VERSION},
        "pipeline_versions": {PIPELINE_VERSION},
    }
    actual_identity = {
        "dimensions": dimensions,
        "models": models,
        "revisions": revisions,
        "preprocessing_versions": preprocessing_versions,
        "pipeline_versions": pipeline_versions,
    }
    if actual_identity != expected_identity:
        raise RuntimeError(
            "Embedding artifact identity does not match active settings: "
            f"actual={actual_identity!r}, expected={expected_identity!r}. "
            "Re-run src/embed.py."
        )
    return {"count": count, "dimension": next(iter(dimensions))}


def get_connection():
    return connect_database(purpose="the pipeline")


def _create_staging_schema(cur, dimension: int) -> None:
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
    cur.execute(sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(STAGING_TABLE)))
    cur.execute(
        sql.SQL(
            """
            CREATE TABLE {} (
                chunk_id                 TEXT PRIMARY KEY,
                text                     TEXT NOT NULL,
                embedding_text           TEXT NOT NULL,
                url                      TEXT,
                title                    TEXT,
                headers                  JSONB,
                doc_index                INTEGER,
                chunk_index              INTEGER,
                char_len                 INTEGER,
                content_hash             TEXT NOT NULL,
                fetched_at               TIMESTAMPTZ,
                pipeline_version         TEXT NOT NULL,
                preprocessing_version    TEXT NOT NULL,
                embedding_model          TEXT NOT NULL,
                embedding_model_revision TEXT NOT NULL,
                embedding                VECTOR({}),
                text_search              TSVECTOR GENERATED ALWAYS AS (
                    to_tsvector('english', coalesce(title, '') || ' ' || text)
                ) STORED
            )
            """
        ).format(sql.Identifier(STAGING_TABLE), sql.SQL(str(dimension)))
    )


def _insert_batches(cur) -> int:
    statement = sql.SQL(
        """
        INSERT INTO {} (
            chunk_id, text, embedding_text, url, title, headers, doc_index, chunk_index,
            char_len, content_hash, fetched_at, pipeline_version,
            preprocessing_version, embedding_model, embedding_model_revision,
            embedding
        ) VALUES %s
        """
    ).format(sql.Identifier(STAGING_TABLE)).as_string(cur.connection)

    inserted = 0
    batch = []
    for chunk in iter_jsonl(EMBEDDED_PATH):
        batch.append(
            (
                chunk["chunk_id"],
                chunk["text"],
                chunk["embedding_text"],
                chunk.get("url"),
                chunk.get("title"),
                json.dumps(chunk.get("headers", {})),
                chunk.get("doc_index"),
                chunk.get("chunk_index"),
                chunk.get("char_len"),
                chunk["content_hash"],
                chunk.get("fetched_at"),
                chunk["pipeline_version"],
                chunk["preprocessing_version"],
                chunk["embedding_model"],
                chunk["embedding_model_revision"],
                chunk["embedding"],
            )
        )
        if len(batch) >= INSERT_BATCH_SIZE:
            execute_values(cur, statement, batch, page_size=INSERT_BATCH_SIZE)
            inserted += len(batch)
            batch.clear()
    if batch:
        execute_values(cur, statement, batch, page_size=INSERT_BATCH_SIZE)
        inserted += len(batch)
    return inserted


def _build_and_validate_indexes(cur, expected_count: int) -> None:
    lists = max(1, min(IVFFLAT_MAX_LISTS, int(math.sqrt(expected_count))))
    cur.execute(
        sql.SQL(
            "CREATE INDEX chunks_next_embedding_idx ON {} "
            "USING ivfflat (embedding vector_cosine_ops) WITH (lists = {})"
        ).format(sql.Identifier(STAGING_TABLE), sql.SQL(str(lists)))
    )
    cur.execute(
        sql.SQL("CREATE INDEX chunks_next_text_search_idx ON {} USING gin (text_search)").format(
            sql.Identifier(STAGING_TABLE)
        )
    )
    cur.execute(sql.SQL("ANALYZE {}").format(sql.Identifier(STAGING_TABLE)))
    cur.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(STAGING_TABLE)))
    stored_count = cur.fetchone()[0]
    if stored_count != expected_count:
        raise RuntimeError(
            f"Staging row count mismatch: stored {stored_count}, expected {expected_count}"
        )
    cur.execute(
        sql.SQL(
            """
            SELECT COUNT(DISTINCT embedding_model),
                   COUNT(DISTINCT embedding_model_revision),
                   COUNT(DISTINCT preprocessing_version),
                   COUNT(DISTINCT pipeline_version)
            FROM {}
            """
        ).format(sql.Identifier(STAGING_TABLE))
    )
    if cur.fetchone() != (1, 1, 1, 1):
        raise RuntimeError("Staging table contains mixed embedding identities")
    print(f"Built IVFFlat index with lists={lists}; staging validation passed.")


def _atomic_swap(cur) -> None:
    cur.execute(sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(PREVIOUS_TABLE)))
    cur.execute("SELECT to_regclass(current_schema() || '.chunks')")
    has_live_table = cur.fetchone()[0] is not None
    if has_live_table:
        cur.execute(
            sql.SQL("ALTER TABLE {} RENAME TO {}") .format(
                sql.Identifier("chunks"), sql.Identifier(PREVIOUS_TABLE)
            )
        )
    cur.execute(
        sql.SQL("ALTER TABLE {} RENAME TO {}") .format(
            sql.Identifier(STAGING_TABLE), sql.Identifier("chunks")
        )
    )
    if has_live_table:
        cur.execute(sql.SQL("DROP TABLE {}").format(sql.Identifier(PREVIOUS_TABLE)))
    cur.execute("ALTER INDEX chunks_next_embedding_idx RENAME TO chunks_embedding_idx")
    cur.execute("ALTER INDEX chunks_next_text_search_idx RENAME TO chunks_text_search_idx")


def run() -> None:
    source_hashes = _source_hashes()
    manifest = _scan_embeddings(source_hashes)
    print(
        f"Validated {manifest['count']} embedded chunks at dimension "
        f"{manifest['dimension']} from {EMBEDDED_PATH}"
    )

    conn = get_connection()
    conn.autocommit = False
    try:
        with conn.cursor() as cur:
            _create_staging_schema(cur, manifest["dimension"])
            inserted = _insert_batches(cur)
            if inserted != manifest["count"]:
                raise RuntimeError(
                    f"Insert count mismatch: inserted {inserted}, expected {manifest['count']}"
                )
            _build_and_validate_indexes(cur, manifest["count"])
            _atomic_swap(cur)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    print(f"Atomically published {manifest['count']} rows to the chunks table.")


if __name__ == "__main__":
    run()
