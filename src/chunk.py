"""
Step 3: Chunking.

Strategy: structure-aware chunking.
  1. Split each cleaned Markdown doc on its headers (#, ##, ###) so related
     content (e.g. an entire "MoE vs Dense" section) stays together as long
     as it fits.
  2. Within each header section, recursively split further if it's still
     too long for the embedding model's context window, with overlap so
     context isn't lost at the cut point.

Why this over plain fixed-size chunking: full papers and blog posts retain
useful heading structure. Splitting on headers first keeps
each debate-relevant argument (e.g. an entire subsection on GRPO vs PPO)
together as one semantic unit, rather than slicing mid-argument at a fixed
character count.

Parameters:
  CHUNK_SIZE    = 1200 chars (uses more local evidence per retrieval unit)
  CHUNK_OVERLAP = 300 chars  (preserves context across a cut so a chunk
                               retrieved on its own still makes sense)
  MIN_CHUNK_LENGTH = 200 chars (drops near-empty/boilerplate fragments)

Trade-off considered: 1200/300 preserves more local evidence and reduces
fragmentation, but the configured MiniLM models may truncate long contextual
chunks. Evaluation should be used before increasing this further.

Run:
    python src/chunk.py
Input:
    data/clean_docs.jsonl
Output:
    data/chunks.jsonl   (chunk_id, text, embedding_text, URL/title/section provenance)
"""

import hashlib
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from src.contextual_text import build_contextual_text
from src.jsonl import load_jsonl, write_jsonl_atomic
from src.settings import PIPELINE_VERSION, PREPROCESSING_VERSION

CLEAN_PATH = Path("data/clean_docs.jsonl")
CHUNKS_PATH = Path("data/chunks.jsonl")

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 300
MIN_CHUNK_LENGTH = 200  # drop near-empty fragments and short boilerplate-only slices

HEADER_SPLITTER = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")],
    strip_headers=False,  # keep the heading text in the chunk for context
)
RECURSIVE_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", ". ", " ", ""],
)


def make_chunk_id(url: str, chunk_index: int, text: str | None = None) -> str:
    raw = f"{url}::{chunk_index}::{text or ''}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def chunk_document(doc: dict, doc_index: int) -> list[dict]:
    md = doc.get("markdown", "")
    url = doc.get("url", "")
    title = doc.get("title", "")

    sections = HEADER_SPLITTER.split_text(md)
    if not sections:
        sections = [type("S", (), {"page_content": md, "metadata": {}})()]

    chunks = []
    seen_hashes: set[str] = set()
    chunk_index = 0
    for section in sections:
        pieces = RECURSIVE_SPLITTER.split_text(section.page_content)
        for piece in pieces:
            piece = piece.strip()
            if len(piece) < MIN_CHUNK_LENGTH:
                continue
            embedding_text = build_contextual_text(
                piece,
                title=title,
                headers=section.metadata,
            )
            cache_identity = f"{url}\n{embedding_text}"
            content_hash = hashlib.sha256(cache_identity.encode("utf-8")).hexdigest()
            if content_hash in seen_hashes:
                continue
            seen_hashes.add(content_hash)
            chunks.append({
                "chunk_id": make_chunk_id(url, chunk_index, piece),
                "text": piece,
                "embedding_text": embedding_text,
                "url": url,
                "title": title,
                "headers": section.metadata,
                "doc_index": doc_index,
                "chunk_index": chunk_index,
                "char_len": len(piece),
                "content_hash": content_hash,
                "pipeline_version": PIPELINE_VERSION,
                "preprocessing_version": PREPROCESSING_VERSION,
                "fetched_at": doc.get("_collect_date"),
            })
            chunk_index += 1
    return chunks


def run():
    docs = load_jsonl(CLEAN_PATH)
    print(f"Loaded {len(docs)} cleaned docs from {CLEAN_PATH}")

    all_chunks = []
    seen_hashes: set[str] = set()
    for doc_index, doc in enumerate(docs):
        for chunk in chunk_document(doc, doc_index):
            h = chunk.get("content_hash")
            if h in seen_hashes:
                continue
            seen_hashes.add(h)
            all_chunks.append(chunk)

    if not all_chunks:
        raise RuntimeError(
            "Chunking produced no output. Check data/clean_docs.jsonl and "
            "MIN_CHUNK_LENGTH before embedding."
        )

    write_jsonl_atomic(CHUNKS_PATH, all_chunks)

    lengths = [c["char_len"] for c in all_chunks]
    over_limit = [l for l in lengths if l > CHUNK_SIZE + CHUNK_OVERLAP]

    print(f"Produced {len(all_chunks)} chunks -> {CHUNKS_PATH}")
    print(f"Avg chunk length: {sum(lengths)/len(lengths):.0f} chars")
    print(f"Min/Max chunk length: {min(lengths)} / {max(lengths)} chars")
    print(f"Chunks over size budget ({CHUNK_SIZE + CHUNK_OVERLAP} chars): {len(over_limit)}")

    if len(all_chunks) < len(docs):
        print("WARNING: Fewer chunks than docs; check MIN_CHUNK_LENGTH and document content.")


if __name__ == "__main__":
    run()
