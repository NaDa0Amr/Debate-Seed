"""Small, strict JSON Lines helpers shared by pipeline stages."""

from __future__ import annotations

import json
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any


def iter_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    """Yield JSON objects with a useful path and line number on invalid input."""
    with path.open(encoding="utf-8") as input_file:
        for line_number, line in enumerate(input_file, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON in {path} at line {line_number}"
                ) from error
            if not isinstance(row, dict):
                raise ValueError(
                    f"Expected a JSON object in {path} at line {line_number}"
                )
            yield row


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return list(iter_jsonl(path))


def write_jsonl_atomic(
    path: Path,
    rows: Iterable[dict[str, Any]],
    *,
    default=None,
) -> None:
    """Replace a JSONL artifact only after its complete successor is written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as output:
        for row in rows:
            output.write(
                json.dumps(row, ensure_ascii=False, default=default) + "\n"
            )
    temporary.replace(path)


def append_jsonl(
    path: Path,
    rows: Iterable[dict[str, Any]],
    *,
    default=None,
) -> None:
    """Append complete JSONL rows, creating the parent directory if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as output:
        for row in rows:
            output.write(
                json.dumps(row, ensure_ascii=False, default=default) + "\n"
            )
