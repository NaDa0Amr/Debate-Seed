"""Test fixtures that avoid pytest temporary-directory ACL issues on Windows."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def artifact_path():
    created: list[Path] = []

    def create(suffix: str = ".jsonl") -> Path:
        descriptor, raw_path = tempfile.mkstemp(prefix="qubettera-test-", suffix=suffix)
        os.close(descriptor)
        path = Path(raw_path)
        created.append(path)
        return path

    yield create

    for path in created:
        path.unlink(missing_ok=True)
