"""
Step 2: Cleaning + domain-relevance filtering + deduplication.

Scrapling's .markdown() already strips scripts/styles/nav-adjacent noise
during the spider step, so this script does four things:
  1. Deduplicates arXiv papers: if multiple versions of the same paper exist
     (e.g. 2312.00752, 2312.00752v1, 2312.00752v2), keep only the one with
     the highest version number (or the versionless URL).
  2. Light text normalization (collapse blank lines, drop near-empty pages).
  3. Keyword-based relevance filtering, since a crawl can still pick up
     off-topic pages that happen to sit inside an allowed domain/path.
  4. A manual spot-check helper to eyeball a random sample of the result,
     satisfying the "check at least 5 cleaned documents" requirement.

Run:
    python src/clean.py
Output:
    data/clean_docs.jsonl     (normalized, deduplicated, on-topic only)
    data/dropped_docs.jsonl   (off-topic or duplicate, kept for inspection)
"""

import json
import random
import re
from datetime import datetime, timezone
from pathlib import Path

RAW_PATH = Path("data/raw_docs.jsonl")
CLEAN_PATH = Path("data/clean_docs.jsonl")
DROPPED_PATH = Path("data/dropped_docs.jsonl")

# Terms from the Theme 4 debate seed (MoE/Dense, attention variants, SSMs,
# hybrid architectures, pretraining, PPO/GRPO). A page must mention at least
# MIN_HITS of these (case-insensitive) to be considered on-domain.
#
# Split into "strong" (specific enough to be a real signal on their own)
# and "weak" (common words like "attention" or "reasoning" that show up in
# lots of unrelated ML papers too).
STRONG_KEYWORDS = [
    "mixture of experts", "moe", "sparse routing", "expert routing",
    "linear attention", "sliding window attention", "local attention",
    "state space model", "state-space model", "mamba", "ssm",
    "hybrid architecture", "grpo", "group relative policy optimization",
    "ppo", "proximal policy optimization", "reward model",
    "flash attention", "flashattention",
    "rwkv", "dilated attention", "sparse attention",
    "cross-encoder", "reranking", "retrieval augmented",
]
WEAK_KEYWORDS = [
    "attention", "dense layer", "dense feed-forward", "transformer",
    "pretraining", "pre-training", "fine-tun", "reasoning", "rlhf",
    "policy optimization", "instruction tuning", "reinforcement learning",
    "sequence model", "language model",
]

MIN_HITS = 2
MIN_STRONG_HITS = 1   # require at least one specific/unambiguous term
MIN_LENGTH = 200  # characters; drops near-empty / boilerplate-only pages


import emoji

def light_clean(md: str) -> str:
    """Normalize whitespace and strip common arXiv/site nav boilerplate
    left over after Markdown conversion."""
    
    # Strip emojis to keep the text clean
    md = emoji.replace_emoji(md, replace="")

    # Cut arXiv's nav chrome that appears before the actual abstract.
    md = re.sub(
        r".*?(?=> ?Abstract:)", "", md, count=1, flags=re.DOTALL
    ) if "Abstract:" in md else md

    # Strip arXiv submission history block
    md = re.sub(
        r"Submission history.*?(?=\n\n|\Z)", "", md, flags=re.DOTALL | re.IGNORECASE
    )

    # Strip "Download:" link lines
    md = re.sub(r"^Download:.*$", "", md, flags=re.MULTILINE)

    # Strip arXiv footer metadata (e.g., "arXiv:XXXX.XXXXX ...")
    md = re.sub(r"^arXiv:\d+\.\d+.*$", "", md, flags=re.MULTILINE)

    md = re.sub(r"\n{3,}", "\n\n", md)   # collapse 3+ blank lines to 1
    md = re.sub(r"[ \t]+\n", "\n", md)   # trailing whitespace on lines
    return md.strip()


def is_error_page(title: str, md: str) -> bool:
    """Catch dead links (404s, removed posts) so they're not silently
    miscounted as 'low_relevance'."""
    title_lower = (title or "").lower()
    if "404" in title_lower or "page not found" in title_lower:
        return True
    if "this blog post does not exist" in md.lower():
        return True
    return False


def extract_arxiv_id(url: str) -> str | None:
    """Extract the base arXiv paper ID from a URL, stripping any version
    suffix. Returns None if the URL is not an arXiv abstract page.
    Example: 'https://arxiv.org/abs/2312.00752v2' -> '2312.00752'
    """
    m = re.search(r"arxiv\.org/abs/(\d+\.\d+)", url)
    return m.group(1) if m else None


def extract_arxiv_version(url: str) -> int:
    """Extract the version number from an arXiv URL. Returns 0 for
    versionless URLs (which serve the latest version)."""
    m = re.search(r"arxiv\.org/abs/\d+\.\d+v(\d+)", url)
    return int(m.group(1)) if m else 0


def deduplicate_arxiv(docs: list) -> tuple[list, list]:
    """Among docs sharing the same arXiv paper ID, keep only the best
    version (versionless URL preferred, else highest version number).
    Non-arXiv docs pass through unchanged."""
    arxiv_groups: dict[str, list] = {}
    non_arxiv = []

    for doc in docs:
        url = doc.get("url", "")
        paper_id = extract_arxiv_id(url)
        if paper_id:
            arxiv_groups.setdefault(paper_id, []).append(doc)
        else:
            non_arxiv.append(doc)

    kept, dropped = list(non_arxiv), []
    for paper_id, group in arxiv_groups.items():
        if len(group) == 1:
            kept.append(group[0])
            continue

        # Prefer versionless URL (version=0), else highest version number.
        # Versionless sorts first because 0 < any positive int, but we
        # want it preferred, so we sort by (has_version, -version).
        group.sort(key=lambda d: (
            extract_arxiv_version(d.get("url", "")) != 0,   # False (preferred) < True
            -extract_arxiv_version(d.get("url", "")),
        ))
        kept.append(group[0])
        for dup in group[1:]:
            dup["_drop_reason"] = f"duplicate_arxiv (kept {group[0].get('url')})"
            dropped.append(dup)

    return kept, dropped


def relevance_check(text: str) -> tuple[int, int]:
    """Returns (total_hits, strong_hits)."""
    text_lower = text.lower()
    strong = sum(1 for kw in STRONG_KEYWORDS if kw in text_lower)
    weak = sum(1 for kw in WEAK_KEYWORDS if kw in text_lower)
    return strong + weak, strong


def load_jsonl(path: Path):
    docs = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                docs.append(json.loads(line))
    return docs


def write_jsonl(path: Path, docs: list):
    with open(path, "w", encoding="utf-8") as f:
        for doc in docs:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")


def run():
    raw_docs = load_jsonl(RAW_PATH)
    print(f"Loaded {len(raw_docs)} raw docs from {RAW_PATH}")

    # Phase 1: Deduplicate arXiv versions
    deduped, dedup_dropped = deduplicate_arxiv(raw_docs)
    print(f"After arXiv dedup: {len(deduped)} kept, {len(dedup_dropped)} duplicates removed")

    # Phase 2: Clean, filter by length, and check relevance
    kept, dropped = [], list(dedup_dropped)
    collect_date = datetime.now(timezone.utc).isoformat()

    for doc in deduped:
        md = light_clean(doc.get("markdown", ""))
        title = doc.get("title", "")

        if is_error_page(title, md):
            doc["_drop_reason"] = "error_page (404 / removed)"
            dropped.append(doc)
            continue

        if len(md) < MIN_LENGTH:
            doc["_drop_reason"] = "too_short"
            dropped.append(doc)
            continue

        hits, strong_hits = relevance_check(md)
        if hits < MIN_HITS or strong_hits < MIN_STRONG_HITS:
            doc["_drop_reason"] = f"low_relevance (hits={hits}, strong={strong_hits})"
            dropped.append(doc)
            continue

        doc["markdown"] = md
        doc["_relevance_hits"] = hits
        doc["_strong_hits"] = strong_hits
        doc["_collect_date"] = collect_date
        kept.append(doc)

    write_jsonl(CLEAN_PATH, kept)
    write_jsonl(DROPPED_PATH, dropped)

    print(f"Kept:    {len(kept)}  -> {CLEAN_PATH}")
    print(f"Dropped: {len(dropped)} -> {DROPPED_PATH}")

    if len(kept) < 50:
        print(
            "\n⚠️  Fewer than 50 on-topic docs remain. Options:\n"
            "   - Lower MIN_HITS (currently "
            f"{MIN_HITS}) if too aggressive.\n"
            "   - Add more seed URLs to src/spider.py.\n"
            "   - Check data/dropped_docs.jsonl to see what got cut and why."
        )

    spot_check(kept, n=5)


def spot_check(docs: list, n: int = 5):
    """Print a random sample for manual review (§6 acceptance criterion)."""
    if not docs:
        print("Nothing to spot-check — no docs survived filtering.")
        return

    sample = random.sample(docs, min(n, len(docs)))
    print(f"\n--- Spot-check: {len(sample)} random cleaned docs ---")
    for doc in sample:
        print("=" * 80)
        print("URL:  ", doc.get("url"))
        print("Title:", doc.get("title"))
        print("Hits: ", doc.get("_relevance_hits"))
        snippet = doc["markdown"][:400].replace("\n", " ")
        print(f"{snippet} ...")


if __name__ == "__main__":
    run()