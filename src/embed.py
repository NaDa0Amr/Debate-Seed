"""
Step 4: Embedding generation.

Generates embeddings incrementally and resumably:
  - Each chunk's content_hash is computed up front (before embedding), so
    progress can be tracked independent of when embedding actually happens.
  - Chunks already present in EMBEDDED_PATH (by content_hash) are skipped on
    re-run, so a crash mid-run does not require re-embedding everything.
  - Output is appended batch-by-batch (not rewritten in full each time), so
    writes stay O(n) over a long run instead of O(n^2).
  - Embedding dimension is verified for every row before it's written, not
    just the first one.

Run:
    python src/embed.py
Input:
    data/chunks.jsonl
Output:
    data/chunks_with_embeddings.jsonl   (appended to; safe to resume)
"""

import hashlib
import json
import sys
from pathlib import Path

# When this file is invoked as ``python src/embed.py``, Python adds ``src``
# rather than the repository root to sys.path. Add the root before importing
# the package; module execution (``python -m src.embed``) needs no adjustment.
if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.settings import (
    EMBEDDING_DIM,
    EMBEDDING_MODEL,
    EMBEDDING_MODEL_REVISION,
    PIPELINE_VERSION,
    PREPROCESSING_VERSION,
)
from src.contextual_text import build_contextual_text
from src.jsonl import (
    append_jsonl as append_jsonl_rows,
    load_jsonl,
    write_jsonl_atomic,
)

CHUNKS_PATH = Path("data/chunks.jsonl")
EMBEDDED_PATH = Path("data/chunks_with_embeddings.jsonl")

MODEL_NAME = EMBEDDING_MODEL
MODEL_REVISION = EMBEDDING_MODEL_REVISION
EXPECTED_DIM = EMBEDDING_DIM
BATCH_SIZE = 64


def _json_default(value):
    """Fallback for json.dumps to handle numpy scalar/array leftovers
    (e.g. float32, int64) that can end up in chunk metadata from upstream
    numpy-touched fields."""
    if hasattr(value, "tolist"):
        return value.tolist()
    if hasattr(value, "item"):
        try:
            return value.item()
        except ValueError:
            pass
    return str(value)


def _serialize_jsonl_row(row):
    return json.loads(json.dumps(row, default=_json_default, ensure_ascii=False))


def write_jsonl(path: Path, rows: list):
    """Write rows to a JSONL file, normalizing numpy-style values into plain
    Python types for deterministic on-disk serialization."""
    write_jsonl_atomic(
        path,
        (_serialize_jsonl_row(row) for row in rows),
    )


def append_jsonl(path: Path, rows: list):
    """Append rows to a jsonl file, creating it if needed. Never truncates
    existing content, so previously-written batches survive a crash and a
    resumed run."""
    append_jsonl_rows(
        path,
        (_serialize_jsonl_row(row) for row in rows),
    )


def compute_content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _cache_identity_matches(row: dict) -> bool:
    """Return whether a cached vector was built with the active configuration."""
    return (
        row.get("embedding_model") == MODEL_NAME
        and row.get("embedding_model_revision") == MODEL_REVISION
        and row.get("preprocessing_version") == PREPROCESSING_VERSION
        and row.get("pipeline_version") == PIPELINE_VERSION
        and row.get("embedding_dim") == EXPECTED_DIM
    )


def current_embeddings(path: Path, chunks: list[dict]) -> dict[str, dict]:
    """Return cached embeddings only for the current chunk manifest.

    The embedding file is a cache, not an archive. Filtering by current
    content hashes prevents a later store run from loading stale chunks.
    """
    if not path.exists():
        return {}
    valid_hashes = {chunk["content_hash"] for chunk in chunks}
    cached = {}
    for row in load_jsonl(path):
        content_hash = row.get("content_hash")
        embedding = row.get("embedding")
        if (
            content_hash in valid_hashes
            and isinstance(embedding, list)
            and len(embedding) == EXPECTED_DIM
            and _cache_identity_matches(row)
        ):
            cached[content_hash] = row
    return cached


def refresh_cached_metadata(
    chunks: list[dict], cached_rows: dict[str, dict]
) -> dict[str, dict]:
    """Combine reusable vectors with metadata from the current chunk manifest."""
    refreshed = {}
    for chunk in chunks:
        content_hash = chunk["content_hash"]
        cached = cached_rows.get(content_hash)
        if cached is None:
            continue
        refreshed[content_hash] = {
            **chunk,
            "embedding": cached["embedding"],
            "embedding_model": MODEL_NAME,
            "embedding_model_revision": MODEL_REVISION,
            "embedding_dim": EXPECTED_DIM,
            "pipeline_version": PIPELINE_VERSION,
            "preprocessing_version": PREPROCESSING_VERSION,
        }
    return refreshed


def encode_batch(model, texts: list[str]):
    """Encode in the model-owning thread to avoid PyTorch worker deadlocks."""
    return model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=False,
        normalize_embeddings=True,
    )


def load_embedding_model():
    """Prefer an existing Hugging Face cache and download only when absent."""
    from sentence_transformers import SentenceTransformer

    try:
        return SentenceTransformer(
            MODEL_NAME,
            revision=MODEL_REVISION,
            local_files_only=True,
        )
    except (OSError, ValueError):
        print("Embedding model is not complete in the local cache; downloading it now.")
        return SentenceTransformer(MODEL_NAME, revision=MODEL_REVISION)


def run():
    chunks = load_jsonl(CHUNKS_PATH)
    print(f"Loaded {len(chunks)} chunks from {CHUNKS_PATH}")
    if not chunks:
        raise SystemExit("No chunks found; run src/chunk.py first.")

    # Rebuild the contextual input and its hash so metadata changes cannot
    # silently reuse a vector generated for stale title/section provenance.
    for chunk in chunks:
        chunk["embedding_text"] = build_contextual_text(
            chunk["text"],
            title=chunk.get("title", ""),
            headers=chunk.get("headers"),
        )
        chunk["content_hash"] = compute_content_hash(
            f"{chunk.get('url', '')}\n{chunk['embedding_text']}"
        )

    # Cached vectors remain valid by content/configuration identity, but all
    # non-vector metadata must come from the current chunk manifest. This keeps
    # doc indexes, timestamps, and provenance fresh after collection changes.
    cached_rows = refresh_cached_metadata(
        chunks,
        current_embeddings(EMBEDDED_PATH, chunks),
    )
    done_hashes = set(cached_rows)
    if done_hashes:
        print(f"Found {len(done_hashes)} already-embedded chunks in {EMBEDDED_PATH}; resuming")

    pending = [c for c in chunks if c["content_hash"] not in done_hashes]
    print(f"{len(pending)} chunks remaining to embed (of {len(chunks)} total)")

    if not pending:
        write_jsonl(EMBEDDED_PATH, [cached_rows[c["content_hash"]] for c in chunks])
        print("All current chunks are embedded; compacted the embedding cache.")
        return

    print(f"Loading embedding model: {MODEL_NAME} (first run downloads ~80MB)")
    model = load_embedding_model()
    get_dimension = getattr(model, "get_embedding_dimension", None)
    actual_dim = (
        get_dimension()
        if get_dimension is not None
        else model.get_sentence_embedding_dimension()
    )
    if actual_dim != EXPECTED_DIM:
        raise ValueError(
            f"Model dimension mismatch: model reports {actual_dim}, expected {EXPECTED_DIM}."
        )

    total_batches = (len(pending) + BATCH_SIZE - 1) // BATCH_SIZE
    embedded_count = 0

    for batch_num, start in enumerate(range(0, len(pending), BATCH_SIZE), start=1):
        batch = pending[start:start + BATCH_SIZE]
        text_batch = [c["embedding_text"] for c in batch]

        vectors = encode_batch(model, text_batch)

        if len(vectors) != len(batch):
            raise ValueError("Embedding batch length mismatch for the current chunk batch.")

        batch_rows = []
        for chunk, vec in zip(batch, vectors):
            vec = [float(v) for v in list(vec)]
            if len(vec) != EXPECTED_DIM:
                raise ValueError(
                    f"Embedding dimension mismatch: expected {EXPECTED_DIM}, got "
                    f"{len(vec)} for chunk {chunk.get('chunk_id')}"
                )
            chunk["embedding"] = vec
            chunk["embedding_model"] = MODEL_NAME
            chunk["embedding_model_revision"] = MODEL_REVISION
            chunk["embedding_dim"] = len(vec)
            chunk["pipeline_version"] = PIPELINE_VERSION
            chunk["preprocessing_version"] = PREPROCESSING_VERSION
            batch_rows.append(chunk)

        # The first write removes stale cache rows; subsequent batches remain
        # append-only so interrupted runs still resume safely.
        if batch_num == 1:
            retained = [cached_rows[c["content_hash"]] for c in chunks if c["content_hash"] in cached_rows]
            write_jsonl(EMBEDDED_PATH, retained + batch_rows)
        else:
            append_jsonl(EMBEDDED_PATH, batch_rows)
        embedded_count += len(batch_rows)
        print(f"Wrote batch {batch_num} of {total_batches} ({embedded_count} chunks so far) -> {EMBEDDED_PATH}")

    # Compact after all batches succeed so the output is exactly the current
    # chunk manifest, even when it started as a resumed partial cache.
    completed = {}
    for row in load_jsonl(EMBEDDED_PATH):
        if row.get("content_hash"):
            completed[row["content_hash"]] = row
    if len(completed) != len(chunks) or any(chunk["content_hash"] not in completed for chunk in chunks):
        raise RuntimeError("Embedding output does not contain every current chunk after generation.")
    write_jsonl(EMBEDDED_PATH, [completed[chunk["content_hash"]] for chunk in chunks])
    print(f"\nDone. Embedded {embedded_count} new chunks -> {EMBEDDED_PATH}")
    print(f"Embedding model: {MODEL_NAME}")
    print(f"Embedding model revision: {MODEL_REVISION}")
    print(f"Vector dimensionality: {actual_dim}")
    print(f"Total chunks now in {EMBEDDED_PATH}: {len(chunks)}")


if __name__ == "__main__":
    run()
