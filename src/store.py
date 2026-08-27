"""
Step 5: Store the knowledge base in PostgreSQL + pgvector (§9).

Stores chunk text, embeddings, and metadata. Also creates a tsvector column
and GIN index for PostgreSQL full-text search, enabling hybrid retrieval
(vector similarity + BM25-style keyword matching).

Requires PostgreSQL running with the `vector` extension available
(pgvector). See README for how to start it (Docker or local install).

Configuration is read from environment variables (see .env.example) so no
credentials are hardcoded or committed.

Run:
    python src/store.py
Input:
    data/chunks_with_embeddings.jsonl
Effect:
    Creates the `chunks` table (if not present) and inserts/upserts all
    embedded chunks into it. Builds both ANN (ivfflat) and GIN (tsvector)
    indexes after population.
"""

import json
import os
from pathlib import Path

import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()  # reads .env if present; falls back to real env vars / defaults

EMBEDDED_PATH = Path("data/chunks_with_embeddings.jsonl")

DB_CONFIG = {
    "host": os.environ.get("PGHOST", "localhost"),
    "port": os.environ.get("PGPORT", "5432"),
    "dbname": os.environ.get("PGDATABASE", "ragdb"),
    "user": os.environ.get("PGUSER", "postgres"),
    "password": os.environ.get("PGPASSWORD", "pass"),
}

SCHEMA_SQL = """
CREATE EXTENSION IF NOT EXISTS vector;

DROP TABLE IF EXISTS chunks;

CREATE TABLE chunks (
    chunk_id        TEXT PRIMARY KEY,
    text            TEXT NOT NULL,
    url             TEXT,
    title           TEXT,
    headers         JSONB,
    doc_index       INTEGER,
    chunk_index     INTEGER,
    char_len        INTEGER,
    embedding_model TEXT,
    embedding       VECTOR({dim}),
    text_search     TSVECTOR GENERATED ALWAYS AS (
                        to_tsvector('english', coalesce(title, '') || ' ' || text)
                    ) STORED
);
"""

CREATE_ANN_INDEX_SQL = """
CREATE INDEX IF NOT EXISTS chunks_embedding_idx
ON chunks USING ivfflat (embedding vector_cosine_ops)
WITH (lists = {lists});
"""

CREATE_GIN_INDEX_SQL = """
CREATE INDEX IF NOT EXISTS chunks_text_search_idx
ON chunks USING gin (text_search);
"""


def load_jsonl(path: Path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def get_connection():
    """Get a psycopg2 connection using DB_CONFIG."""
    return psycopg2.connect(**DB_CONFIG)


def run():
    chunks = load_jsonl(EMBEDDED_PATH)
    print(f"Loaded {len(chunks)} embedded chunks from {EMBEDDED_PATH}")
    if not chunks:
        raise SystemExit("No chunks found — run src/embed.py first.")

    dim = chunks[0].get("embedding_dim") or len(chunks[0]["embedding"])

    # Choose number of IVFFlat lists: sqrt(n) is the recommended heuristic,
    # but at least 1 and at most 100 for our dataset size.
    import math
    n_lists = max(1, min(100, int(math.sqrt(len(chunks)))))

    schema_sql = SCHEMA_SQL.format(dim=dim)
    ann_index_sql = CREATE_ANN_INDEX_SQL.format(lists=n_lists)

    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    cur = conn.cursor()

    print("Creating pgvector extension + schema (drops old table)...")
    cur.execute(schema_sql)
    conn.commit()

    print(f"Inserting {len(chunks)} chunks...")
    rows = [
        (
            c["chunk_id"], c["text"], c.get("url"), c.get("title"),
            json.dumps(c.get("headers", {})), c.get("doc_index"),
            c.get("chunk_index"), c.get("char_len"),
            c.get("embedding_model"), c["embedding"],
        )
        for c in chunks
    ]

    execute_values(
        cur,
        """
        INSERT INTO chunks
            (chunk_id, text, url, title, headers, doc_index, chunk_index,
             char_len, embedding_model, embedding)
        VALUES %s
        """,
        rows,
        template="(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    )
    conn.commit()

    print(f"Building ANN index (ivfflat, cosine, lists={n_lists})...")
    cur.execute(ann_index_sql)
    conn.commit()

    print("Building GIN index (full-text search)...")
    cur.execute(CREATE_GIN_INDEX_SQL)
    conn.commit()

    # Acceptance criterion: stored count matches indexed chunk count.
    cur.execute("SELECT COUNT(*) FROM chunks;")
    stored_count = cur.fetchone()[0]
    print(f"Stored rows in DB: {stored_count} (expected {len(chunks)})")
    assert stored_count == len(chunks), "Row count mismatch after insert!"

    # Verify indexes
    cur.execute("""
        SELECT indexname FROM pg_indexes WHERE tablename = 'chunks';
    """)
    indexes = [row[0] for row in cur.fetchall()]
    print(f"Indexes on chunks table: {indexes}")

    cur.close()
    conn.close()
    print("Done.")


if __name__ == "__main__":
    run()
