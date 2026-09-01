import json
import numpy as np

from src.embed import (
    EXPECTED_DIM,
    MODEL_NAME,
    MODEL_REVISION,
    PIPELINE_VERSION,
    PREPROCESSING_VERSION,
    _cache_identity_matches,
    refresh_cached_metadata,
    write_jsonl,
)


def test_write_jsonl_serializes_float32_embedding(artifact_path):
    rows = [{
        "chunk_id": "c1",
        "text": "example",
        "embedding": np.array([0.1, 0.2, 0.3], dtype=np.float32).tolist(),
    }]

    path = artifact_path()
    write_jsonl(path, rows)

    payload = json.loads(path.read_text(encoding="utf-8").strip())
    assert np.allclose(payload["embedding"], [0.1, 0.2, 0.3])
    assert all(isinstance(x, float) for x in payload["embedding"])


def test_embedding_cache_requires_full_model_and_preprocessing_identity():
    row = {
        "embedding_model": MODEL_NAME,
        "embedding_model_revision": MODEL_REVISION,
        "preprocessing_version": PREPROCESSING_VERSION,
        "pipeline_version": PIPELINE_VERSION,
        "embedding_dim": EXPECTED_DIM,
    }
    assert _cache_identity_matches(row)
    assert not _cache_identity_matches({**row, "embedding_model_revision": "other"})
    assert not _cache_identity_matches({**row, "preprocessing_version": "old"})


def test_cached_vector_uses_current_chunk_metadata():
    chunk = {
        "chunk_id": "new-id",
        "content_hash": "same-content",
        "text": "evidence",
        "doc_index": 9,
        "fetched_at": "2026-09-01T00:00:00+00:00",
    }
    cached = {
        "same-content": {
            "chunk_id": "old-id",
            "content_hash": "same-content",
            "doc_index": 1,
            "embedding": [0.0] * EXPECTED_DIM,
        }
    }
    refreshed = refresh_cached_metadata([chunk], cached)["same-content"]
    assert refreshed["chunk_id"] == "new-id"
    assert refreshed["doc_index"] == 9
    assert refreshed["embedding"] == cached["same-content"]["embedding"]
