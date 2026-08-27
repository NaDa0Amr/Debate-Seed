"""
Step 3: Chunking (§7).

Strategy: structure-aware chunking.
  1. Split each cleaned Markdown doc on its headers (#, ##, ###) so related
     content (e.g. an entire "MoE vs Dense" section) stays together as long
     as it fits.
  2. Within each header section, recursively split further if it's still
     too long for the embedding model's context window, with overlap so
     context isn't lost at the cut point.

Why this over plain fixed-size chunking: our docs are arXiv abstracts and
blog posts with real heading structure. Splitting on headers first keeps
each debate-relevant argument (e.g. an entire subsection on GRPO vs PPO)
together as one semantic unit, rather than slicing mid-argument at a fixed
character count.

Parameters (documented per §7 acceptance criteria):
  CHUNK_SIZE   = 800 chars  (~150-200 tokens, comfortably under every
                              common embedding model's per-input limit)
  CHUNK_OVERLAP = 100 chars  (preserves context across a cut so a chunk
                              retrieved on its own still makes sense)

Trade-off considered: larger chunks (e.g. 1500 chars) would preserve more
context per chunk but reduce retrieval precision (more irrelevant text
riding along with the relevant sentence). 800/100 favors precision, which
matters more for a debate/evidence-citation use case than for summarization.

Run:
    python src/chunk.py
Input:
    data/clean_docs.jsonl
Output:
    data/chunks.jsonl   (chunk_id, text, url, title, headers, doc_index, chunk_index)
"""

import hashlib
import json
from pathlib import Path

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

CLEAN_PATH = Path("data/clean_docs.jsonl")
CHUNKS_PATH = Path("data/chunks.jsonl")

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
MIN_CHUNK_LENGTH = 40  # drop near-empty fragments (e.g. a lone header)

HEADER_SPLITTER = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")],
    strip_headers=False,  # keep the heading text in the chunk for context
)
RECURSIVE_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", ". ", " ", ""],
)


def load_jsonl(path: Path):
    docs = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                docs.append(json.loads(line))
    return docs


def write_jsonl(path: Path, rows: list):
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def make_chunk_id(url: str, chunk_index: int) -> str:
    raw = f"{url}::{chunk_index}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def chunk_document(doc: dict, doc_index: int) -> list:
    md = doc.get("markdown", "")
    url = doc.get("url", "")
    title = doc.get("title", "")

    sections = HEADER_SPLITTER.split_text(md)
    if not sections:
        # No headers found at all — fall back to treating the whole doc
        # as a single section before recursive splitting.
        sections = [type("S", (), {"page_content": md, "metadata": {}})()]

    chunks = []
    chunk_index = 0
    for section in sections:
        pieces = RECURSIVE_SPLITTER.split_text(section.page_content)
        for piece in pieces:
            piece = piece.strip()
            if len(piece) < MIN_CHUNK_LENGTH:
                continue
            chunks.append({
                "chunk_id": make_chunk_id(url, chunk_index),
                "text": piece,
                "url": url,
                "title": title,
                "headers": section.metadata,
                "doc_index": doc_index,
                "chunk_index": chunk_index,
                "char_len": len(piece),
            })
            chunk_index += 1
    return chunks


def run():
    docs = load_jsonl(CLEAN_PATH)
    print(f"Loaded {len(docs)} cleaned docs from {CLEAN_PATH}")

    all_chunks = []
    for doc_index, doc in enumerate(docs):
        all_chunks.extend(chunk_document(doc, doc_index))

    write_jsonl(CHUNKS_PATH, all_chunks)

    lengths = [c["char_len"] for c in all_chunks]
    over_limit = [l for l in lengths if l > CHUNK_SIZE + CHUNK_OVERLAP]

    print(f"Produced {len(all_chunks)} chunks -> {CHUNKS_PATH}")
    print(f"Avg chunk length: {sum(lengths)/len(lengths):.0f} chars")
    print(f"Min/Max chunk length: {min(lengths)} / {max(lengths)} chars")
    print(f"Chunks over size budget ({CHUNK_SIZE + CHUNK_OVERLAP} chars): {len(over_limit)}")

    if len(all_chunks) < len(docs):
        print("⚠️  Fewer chunks than docs — check MIN_CHUNK_LENGTH / doc content.")


if __name__ == "__main__":
    run()