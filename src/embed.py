"""
Step 4: Embedding generation (§8).

Embedding model: sentence-transformers/all-MiniLM-L6-v2
Vector dimensionality: 384
Reason for selection:
  - Local, free, no API key/cost/rate limits — good fit for a project with
    a few hundred chunks and no production-scale latency requirement.
  - Strong general-purpose semantic similarity performance for its size
    (widely used baseline for retrieval benchmarks).
  - Small enough (~80MB) to run on CPU quickly, so no GPU/hardware
    dependency is introduced for anyone reproducing the pipeline.
  - Trade-off: a larger model (e.g. all-mpnet-base-v2, 768-dim, or an API
    model like OpenAI text-embedding-3-small, 1536-dim) would likely give
    slightly better retrieval quality, at the cost of speed/cost/an
    external dependency. Documented here as a limitation, not hidden.

Run:
    python src/embed.py
Input:
    data/chunks.jsonl
Output:
    data/chunks_with_embeddings.jsonl  (same fields as chunks.jsonl + "embedding")
"""

import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

CHUNKS_PATH = Path("data/chunks.jsonl")
EMBEDDED_PATH = Path("data/chunks_with_embeddings.jsonl")

MODEL_NAME = "all-MiniLM-L6-v2"
EXPECTED_DIM = 384
BATCH_SIZE = 64


def load_jsonl(path: Path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list):
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def run():
    chunks = load_jsonl(CHUNKS_PATH)
    print(f"Loaded {len(chunks)} chunks from {CHUNKS_PATH}")

    print(f"Loading embedding model: {MODEL_NAME} (first run downloads ~80MB)")
    model = SentenceTransformer(MODEL_NAME)

    actual_dim = model.get_sentence_embedding_dimension()
    if actual_dim != EXPECTED_DIM:
        print(f"⚠️  Model dimension is {actual_dim}, expected {EXPECTED_DIM} "
              f"— update EXPECTED_DIM/your DB schema accordingly.")

    texts = [c["text"] for c in chunks]
    print(f"Embedding {len(texts)} chunks in batches of {BATCH_SIZE}...")
    vectors = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        normalize_embeddings=True,  # so cosine similarity == dot product later
    )

    for chunk, vec in zip(chunks, vectors):
        chunk["embedding"] = vec.tolist()
        chunk["embedding_model"] = MODEL_NAME
        chunk["embedding_dim"] = len(vec)

    write_jsonl(EMBEDDED_PATH, chunks)

    # Acceptance criterion: embedding count must match chunk count.
    assert len(chunks) == len(texts) == len(vectors), "Mismatch between chunks and embeddings!"
    print(f"Wrote {len(chunks)} embedded chunks -> {EMBEDDED_PATH}")
    print(f"Embedding model: {MODEL_NAME}")
    print(f"Vector dimensionality: {actual_dim}")


if __name__ == "__main__":
    run()
