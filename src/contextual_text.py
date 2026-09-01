"""Build deterministic context-enriched text for embedding and reranking."""

from __future__ import annotations

import re
from collections.abc import Iterable


def _one_line(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _header_values(headers: object) -> list[str]:
    if isinstance(headers, dict):
        preferred = [key for key in ("h1", "h2", "h3") if key in headers]
        remaining = sorted(key for key in headers if key not in preferred)
        values: Iterable[object] = [headers[key] for key in preferred + remaining]
    elif isinstance(headers, (list, tuple)):
        values = headers
    elif headers:
        values = [headers]
    else:
        values = []
    result = []
    for value in values:
        normalized = _one_line(value)
        if normalized and normalized not in result:
            result.append(normalized)
    return result


def build_contextual_text(
    text: str,
    *,
    title: str = "",
    headers: object = None,
) -> str:
    """Prefix evidence with compact document and section provenance."""
    body = (text or "").strip()
    prefix = []
    normalized_title = _one_line(title)
    if normalized_title:
        prefix.append(f"Document title: {normalized_title}")
    section_path = _header_values(headers)
    if section_path:
        prefix.append(f"Section: {' > '.join(section_path)}")
    if not prefix:
        return body
    return "\n".join(prefix) + "\n\n" + body
