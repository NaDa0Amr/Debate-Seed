"""Shared, versioned settings for chunking, embedding, and retrieval."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


def _positive_int_env(name: str, default: int) -> int:
    raw_value = os.environ.get(name, str(default))
    try:
        value = int(raw_value)
    except ValueError as error:
        raise RuntimeError(f"{name} must be an integer, got {raw_value!r}") from error
    if value <= 0:
        raise RuntimeError(f"{name} must be > 0, got {value}")
    return value

PIPELINE_VERSION = os.environ.get(
    "PIPELINE_VERSION", "rag-pipeline-2026.09.01-context-v1"
)
PREPROCESSING_VERSION = os.environ.get(
    "PREPROCESSING_VERSION", "clean-v2-chunk-v3-context"
)

EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
EMBEDDING_MODEL_REVISION = os.environ.get("EMBEDDING_MODEL_REVISION", "main")
EMBEDDING_DIM = _positive_int_env("EMBEDDING_DIM", 384)

RERANKER_MODEL = os.environ.get(
    "RERANKER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2"
)
RERANKER_MODEL_REVISION = os.environ.get("RERANKER_MODEL_REVISION", "main")

IVFFLAT_MAX_LISTS = _positive_int_env("IVFFLAT_MAX_LISTS", 100)
IVFFLAT_PROBES = _positive_int_env("IVFFLAT_PROBES", 100)
