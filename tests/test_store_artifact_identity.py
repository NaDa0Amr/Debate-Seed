import json

import pytest

import src.store as store
from src.settings import (
    EMBEDDING_DIM,
    EMBEDDING_MODEL,
    EMBEDDING_MODEL_REVISION,
    PIPELINE_VERSION,
    PREPROCESSING_VERSION,
)


def _write_jsonl(path, rows):
    path.write_text(
        "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8"
    )


def _embedded_row(**overrides):
    row = {
        "chunk_id": "c1",
        "text": "retrieval evidence",
        "embedding_text": "Document title: Test\n\nretrieval evidence",
        "content_hash": "hash-1",
        "embedding": [0.0] * EMBEDDING_DIM,
        "embedding_dim": EMBEDDING_DIM,
        "embedding_model": EMBEDDING_MODEL,
        "embedding_model_revision": EMBEDDING_MODEL_REVISION,
        "preprocessing_version": PREPROCESSING_VERSION,
        "pipeline_version": PIPELINE_VERSION,
    }
    return {**row, **overrides}


def test_store_accepts_one_consistent_artifact(monkeypatch, artifact_path):
    chunks_path = artifact_path()
    embedded_path = artifact_path()
    _write_jsonl(chunks_path, [{"chunk_id": "c1", "content_hash": "hash-1"}])
    _write_jsonl(embedded_path, [_embedded_row()])
    monkeypatch.setattr(store, "CHUNKS_PATH", chunks_path)
    monkeypatch.setattr(store, "EMBEDDED_PATH", embedded_path)

    manifest = store._scan_embeddings(store._source_hashes())
    assert manifest == {"count": 1, "dimension": EMBEDDING_DIM}


def test_store_rejects_mixed_or_stale_embedding_identity(monkeypatch, artifact_path):
    chunks_path = artifact_path()
    embedded_path = artifact_path()
    _write_jsonl(chunks_path, [{"chunk_id": "c1", "content_hash": "hash-1"}])
    _write_jsonl(embedded_path, [_embedded_row(embedding_model_revision="old")])
    monkeypatch.setattr(store, "CHUNKS_PATH", chunks_path)
    monkeypatch.setattr(store, "EMBEDDED_PATH", embedded_path)

    with pytest.raises(RuntimeError, match="identity"):
        store._scan_embeddings(store._source_hashes())


def test_store_rejects_non_finite_embedding(monkeypatch, artifact_path):
    chunks_path = artifact_path()
    embedded_path = artifact_path()
    _write_jsonl(chunks_path, [{"chunk_id": "c1", "content_hash": "hash-1"}])
    _write_jsonl(embedded_path, [_embedded_row(embedding=[float("nan")] * EMBEDDING_DIM)])
    monkeypatch.setattr(store, "CHUNKS_PATH", chunks_path)
    monkeypatch.setattr(store, "EMBEDDED_PATH", embedded_path)

    with pytest.raises(ValueError, match="NaN or infinity"):
        store._scan_embeddings(store._source_hashes())
