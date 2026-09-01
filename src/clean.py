"""
Step 2: Cleaning + domain-relevance filtering + deduplication.

Scrapling's .markdown() already strips scripts/styles/nav-adjacent noise
during collection, so this script does four things:
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

import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.jsonl import load_jsonl, write_jsonl_atomic

try:
    import emoji
except ImportError:  # pragma: no cover - runtime compatibility for minimal envs
    class _EmojiFallback:
        @staticmethod
        def replace_emoji(text: str, replace: str = "") -> str:
            return text

    emoji = _EmojiFallback()

RAW_PATH = Path("data/raw_docs.jsonl")
CLEAN_PATH = Path("data/clean_docs.jsonl")
DROPPED_PATH = Path("data/dropped_docs.jsonl")

# Terms from the Theme 4 debate seed (MoE/Dense, attention variants, SSMs,
# hybrid architectures, pretraining, PPO/GRPO). A page must mention at least
# enough strong signals from these terms to be considered on-domain.
#
# Split into "strong" (specific enough to be a real signal on their own)
# and "weak" (common words like "attention" or "reasoning" that show up in
# lots of unrelated ML papers too).
STRONG_KEYWORDS = [
    "mixture of experts", "moe", "sparse routing", "load balancing",
    "switch transformer", "expert choice routing", "sparse mixture",
    "linear attention", "linformer", "performer", "sliding window attention",
    "flashattention", "flash attention", "longformer", "longnet", "bigbird", "big bird", "mistral 7b",
    "sparse transformer", "sparse attention",
    "state space model", "ssm", "mamba",
    "hybrid architecture", "jamba", "samba",
    "instruction finetuning", "instruction-finetuned", "chain-of-thought",
    "reasoning oriented pretraining", "reasoning-oriented",
    "grpo", "group relative policy optimization",
    "ppo", "proximal policy optimization", "retrieval augmented generation",
    "dense retrieval", "dense passage retrieval", "reranking", "realm"
]
WEAK_KEYWORDS = []   # no weak fallback
# A body-only single match is often a citation to another paper. A single
# match is sufficient only when it appears in the title; otherwise require
# two independent topic signals.
MIN_STRONG_HITS = 2
MIN_LENGTH = 200
# Keyword matches in a full paper's bibliography are not evidence that the
# paper itself is about the topic. Abstracts and introductions appear first.
RELEVANCE_WINDOW_CHARS = 12_000
# Precompiled patterns keep the cleaner fast enough for large crawls without
# re-creating the same regex objects for every document.
NAV_LINK_BLOCK_RE = re.compile(
    r"(?:^|\n)\s*(?:[*+-]|\d+\.)\s*(?:\[[^\]]+\]\([^)]+\)|[^\n]*?(?:https?://|/)[^\n]*)"
    r"(?:\s*\n\s*(?:[*+-]|\d+\.)\s*(?:\[[^\]]+\]\([^)]+\)|[^\n]*?(?:https?://|/)[^\n]*))*\s*\n*",
    flags=re.IGNORECASE | re.MULTILINE,
)
SITE_HEADER_RE = re.compile(
    r"(?:\[\s*skip\s+to\s+(?:main|footer)\s+(?:content|page)\s*\]\([^)]+\)|"
    r"\[\s*skip\s+to\s+(?:main|footer)\s*\]\([^)]+\)|"
    r"skip\s+to\s+(?:main|footer)(?:\s+(?:content|page))?|"
    r"menu\s+products?\s+solutions?|"
    r"(?:log in|log in to continue|sign in|sign up|register|create account|join now)\b|"
    r"\b(?:home|products?|solutions?|pricing|docs?|blog|about|contact)\b(?:\s*\|\s*\b(?:home|products?|solutions?|pricing|docs?|blog|about|contact)\b)+)",
    flags=re.IGNORECASE,
)
REFERENCE_RE = re.compile(
    r"^\s{0,3}#{1,6}\s*(?:references|bibliography|works cited)\s*(?:\n\s*[-=]{3,}\s*)?$|"
    r"^\s*(?:references|bibliography|works cited)\s*(?:\n\s*[-=]{3,}\s*)?$",
    flags=re.IGNORECASE | re.MULTILINE,
)
LATEX_CMD_RE = re.compile(r"\\(?:cite|citet|citep|ref|eqref)\{[^}]*\}|\\(?:begin|end)\{[^}]*\}|\\(?:label|tag)\{[^}]*\}")
NUMBERED_LINE_RE = re.compile(r"^\s*(?:\(?\d+(?:\.\d+)*\)?|\[\d+\])\s*$", flags=re.MULTILINE)
CAPTION_RE = re.compile(r"^\s*(?:\*\*)?(?:figure|fig\.|table)\s*\d+[\.:].*$", flags=re.IGNORECASE | re.MULTILINE)
PAGE_RE = re.compile(r"^\s*(?:page\s+)?\d+\s*$", flags=re.MULTILINE)
# Keep this intentionally narrow so it does not consume normal prose wrapping
# a single dollar sign or a block of text between paragraphs.
MATH_RE = re.compile(r"(?:\$\$.*?\$\$|\$[^\n$]*\$)", flags=re.DOTALL)
FOOTER_RE = re.compile(
    r"^\s*(?:terms\s*&\s*policies|privacy\s+policy|cookie\s+policy|copyright\s+\d{4}|\u00a9\s*\d{4})\s*$",
    flags=re.IGNORECASE | re.MULTILINE,
)


def light_clean(md: str) -> str:
    """Normalize whitespace and strip common site/nav boilerplate left over
    after Markdown conversion."""
    md = emoji.replace_emoji(md, replace="")
    md = md.replace("\r\n", "\n").replace("\r", "\n")

    # Strip leading chrome when a page starts with a dense block of short links.
    # This catches header/footer nav and breadcrumb rows that don't contain real prose.
    leading = md.lstrip()
    if leading:
        first_lines = leading.splitlines()[:12]
        link_line_count = 0
        link_char_count = 0
        for line in first_lines:
            if re.search(r"\[[^\]]+\]\([^)]*\)", line):
                link_line_count += 1
                link_char_count += len(line)
        if link_line_count >= 2 and link_char_count >= 120:
            md = "\n".join(leading.splitlines()[link_line_count:])

    # Remove markdown-only navigation blocks that contain a list of links,
    # which are common in scraped sites (header/footer navigation, side menus).
    md = NAV_LINK_BLOCK_RE.sub("\n", md)

    # Remove common site chrome and login prompts that appear before the content.
    md = SITE_HEADER_RE.sub("", md)

    # Full paper renders often retain a complete bibliography. It is nearly all
    # author/title repetition, weakens retrieval, and has no useful body context.
    md = REFERENCE_RE.split(md, maxsplit=1)[0]

    # ar5iv / LaTeX remnants and display-equation numbering.
    md = LATEX_CMD_RE.sub("", md)
    md = NUMBERED_LINE_RE.sub("", md)

    # Captions are normally detached from their evidence after conversion.
    md = CAPTION_RE.sub("", md)

    # Remove math content before keyword matching so notation and equation
    # fragments do not distort the relevance signal.
    md = MATH_RE.sub(" ", md)

    # Cut arXiv's nav chrome that appears before the actual abstract.
    if "Abstract:" in md:
        md = re.sub(r".*?(?=> ?Abstract:)", "", md, count=1, flags=re.DOTALL)

    # Strip arXiv submission history block, download lines, and footer metadata.
    md = re.sub(r"Submission history.*?(?=\n\n|\Z)", "", md, flags=re.DOTALL | re.IGNORECASE)
    md = re.sub(r"^Download:.*$", "", md, flags=re.MULTILINE)
    md = re.sub(r"^arXiv:\d+\.\d+.*$", "", md, flags=re.MULTILINE)

    # Truncate standard corporate footer boilerplate once a legal/footer block
    # is encountered. This must happen before collapsing line breaks so the
    # footer is still recognized as a standalone line.
    md = FOOTER_RE.split(md, maxsplit=1)[0].rstrip()

    # Remove page-number lines and collapse single newlines; preserve paragraph
    # breaks by only collapsing a newline when the next line is not blank.
    md = PAGE_RE.sub("", md)
    md = re.sub(r"(?<!\n)\n(?!\n)", " ", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"[ \t]+\n", "\n", md)

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


def normalize_url(url: str) -> str:
    """Normalize a URL for duplicate detection by stripping query strings and
    fragments and collapsing trailing slashes; this catches common crawl
    duplicates such as ?utm_source=... or #comments."""
    candidate = (url or "").strip()
    if not candidate:
        return ""

    parts = urlsplit(candidate)
    if not parts.scheme and not parts.netloc:
        return ""

    path = unquote(parts.path.rstrip("/") or "/")
    normalized = urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, "", ""))
    return normalized


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
        # Versionless sorts first because 0 < any positive int, but we want it
        # preferred, so we sort by (has_version, -version).
        group.sort(key=lambda d: (
            extract_arxiv_version(d.get("url", "")) != 0,
            -extract_arxiv_version(d.get("url", "")),
        ))
        kept.append(group[0])
        for dup in group[1:]:
            dup["_drop_reason"] = f"duplicate_arxiv (kept {group[0].get('url')})"
            dropped.append(dup)

    return kept, dropped


def deduplicate_urls(docs: list) -> tuple[list, list]:
    """Drop non-arXiv docs that share a normalized URL with an earlier doc."""
    kept, dropped = [], []
    seen: set[str] = set()

    for doc in docs:
        url = doc.get("url", "")
        normalized = normalize_url(url)

        if not normalized:
            kept.append(doc)
            continue

        if normalized in seen:
            doc["_drop_reason"] = "duplicate_url"
            dropped.append(doc)
            continue

        seen.add(normalized)
        kept.append(doc)

    return kept, dropped


def relevance_check(text: str) -> tuple[int, int]:
    """Returns (total_hits, strong_hits)."""
    # Treat punctuation and hyphen variants as token boundaries. This makes
    # titles such as "Mixture-of-Experts" match "mixture of experts" without
    # weakening whole-token matching for short terms such as SSM and PPO.
    normalized = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    padded = f" {normalized} "

    def matches_keyword(keyword: str) -> bool:
        normalized_keyword = re.sub(r"[^a-z0-9]+", " ", keyword.lower()).strip()
        return bool(normalized_keyword) and f" {normalized_keyword} " in padded

    strong = sum(1 for kw in STRONG_KEYWORDS if matches_keyword(kw))
    weak = sum(1 for kw in WEAK_KEYWORDS if matches_keyword(kw))
    return strong + weak, strong


def run():
    raw_docs = load_jsonl(RAW_PATH)
    print(f"Loaded {len(raw_docs)} raw docs from {RAW_PATH}")

    # Phase 1: Deduplicate arXiv versions.
    deduped, dedup_dropped = deduplicate_arxiv(raw_docs)
    print(f"After arXiv dedup: {len(deduped)} kept, {len(dedup_dropped)} duplicates removed")

    # Phase 2: Deduplicate generic URLs so repeated pages from different crawls
    # or non-arXiv sites do not survive multiple times.
    deduped, url_dropped = deduplicate_urls(deduped)
    print(f"After URL dedup: {len(deduped)} kept, {len(url_dropped)} duplicates removed")

    # Phase 3: Clean, filter by length, and check relevance.
    kept, dropped = [], list(dedup_dropped) + list(url_dropped)
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

        # Title metadata is high-signal and protects relevant papers when the
        # full-text conversion is imperfect or names a key concept only once.
        _, title_strong_hits = relevance_check(title)
        hits, strong_hits = relevance_check(f"{title}\n{md[:RELEVANCE_WINDOW_CHARS]}")
        if strong_hits < MIN_STRONG_HITS and title_strong_hits < 1:
            doc["_drop_reason"] = f"low_relevance (hits={hits}, strong={strong_hits})"
            dropped.append(doc)
            continue

        doc["markdown"] = md
        doc["_relevance_hits"] = hits
        doc["_strong_hits"] = strong_hits
        doc["_collect_date"] = collect_date
        kept.append(doc)

    write_jsonl_atomic(CLEAN_PATH, kept)
    write_jsonl_atomic(DROPPED_PATH, dropped)

    print(f"Kept:    {len(kept)}  -> {CLEAN_PATH}")
    print(f"Dropped: {len(dropped)} -> {DROPPED_PATH}")

    if len(kept) < 50:
        print(
            "\nWARNING: Fewer than 50 on-topic docs remain. Options:\n"
            "   - Lower MIN_STRONG_HITS (currently "
            f"{MIN_STRONG_HITS}) if too aggressive.\n"
            "   - Expand topic discovery in src/collection.py.\n"
            "   - Check data/dropped_docs.jsonl to see what got cut and why."
        )

    spot_check(kept, n=5)


def spot_check(docs: list, n: int = 5):
    """Print a random sample for manual review."""
    if not docs:
        print("Nothing to spot-check; no docs survived filtering.")
        return

    sample = random.sample(docs, min(n, len(docs)))
    encoding = sys.stdout.encoding or "utf-8"

    def console_safe(value) -> str:
        return str(value or "").encode(encoding, errors="replace").decode(encoding)

    print(f"\n--- Spot-check: {len(sample)} random cleaned docs ---")
    for doc in sample:
        print("=" * 80)
        print("URL:  ", console_safe(doc.get("url")))
        print("Title:", console_safe(doc.get("title")))
        print("Hits: ", doc.get("_relevance_hits"))
        snippet = doc["markdown"][:400].replace("\n", " ")
        # Windows' legacy console cannot encode all scraped Unicode text.
        print(f"{snippet} ...".encode(encoding, errors="replace").decode(encoding))


if __name__ == "__main__":
    run()
