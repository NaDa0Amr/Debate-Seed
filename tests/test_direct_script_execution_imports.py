"""Regression tests for running package files through ``python src/<file>.py``."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"


@pytest.mark.parametrize(
    "script_name",
    [
        "clean.py",
        "collection.py",
        "spider.py",
        "chunk.py",
        "embed.py",
        "retrieve.py",
        "evaluate.py",
        "store.py",
        "run_pipeline.py",
    ],
)
def test_direct_script_can_import_package_settings(script_name: str):
    script_path = SRC_ROOT / script_name
    # run_name is deliberately not __main__: this verifies direct-script import
    # semantics without starting collection, embedding, retrieval, or storage.
    code = (
        "import runpy, sys; "
        f"sys.path = [{str(SRC_ROOT)!r}] + [p for p in sys.path if p]; "
        f"runpy.run_path({str(script_path)!r}, run_name='direct_import_check')"
    )
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert completed.returncode == 0, completed.stderr
