"""Query-driven collection with ar5iv -> PDF -> abstract arXiv fallback."""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import time
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scrapling.fetchers import Fetcher

from src.jsonl import load_jsonl, write_jsonl_atomic
from src.source_seeds import CURATED_SOURCE_URLS

try:
    import pymupdf
except ImportError:
    pymupdf = None

LOG = logging.getLogger(__name__)
RAW_PATH = Path("data/raw_docs.jsonl")
REPORT_PATH = Path("data/collection_report.json")
ARXIV_DELAY_SECONDS = 3.0
SEMANTIC_SCHOLAR_DELAY_SECONDS = 1.1
# These are concepts, not hand-maintained paper URLs. Short focused queries
# retrieve canonical work more reliably than one long query dominated by
# recent variants.
TOPIC_QUERIES = [
    "all:(mixture of experts) AND all:(routing OR load balancing)",
    "all:(switch transformer OR sparse expert routing)",
    "all:(linear attention OR linformer OR performer)",
    "all:(sparse attention OR longformer OR bigbird OR longnet)",
    "all:(sliding window attention OR flashattention)",
    "all:(state space model OR mamba)",
    "all:(hybrid attention state space OR jamba OR samba)",
    "all:(reasoning pretraining OR instruction finetuning)",
    "all:(reinforcement learning fine tuning OR PPO OR GRPO)",
    "all:(retrieval augmented generation OR dense retrieval reranking)",
]

# Index, pagination and article-link matching are deliberately data, rather
# than discovery logic scattered across the crawler.
BLOG_SOURCE_CONFIG = {
    "huggingface": {"base_url": "https://huggingface.co/blog", "index_path": "", "pagination_path": "/page/{page}", "pages": 3, "allow": r"^/blog/(?!rss(?:$|/))(?!feed(?:$|/))(?!tag(?:s)?(?:$|/))(?!page(?:$|/))[a-z0-9][a-z0-9-]*$", "requires_js": False},
    "openai": {"base_url": "https://openai.com", "index_path": "/research", "pagination_path": "/research/page/{page}", "pages": 3, "allow": r"^/research/(?!rss(?:$|/))(?!feed(?:$|/))(?!tag(?:s)?(?:$|/))(?!page(?:$|/))[a-z0-9][a-z0-9-]*/?$", "requires_js": True},
    "anthropic": {"base_url": "https://www.anthropic.com", "index_path": "/research", "pagination_path": "/research?page={page}", "pages": 3, "allow": r"^/research/(?!rss(?:$|/))(?!feed(?:$|/))(?!tag(?:s)?(?:$|/))(?!page(?:$|/))[a-z0-9][a-z0-9-]*/?$", "requires_js": False},
    "deepmind": {"base_url": "https://deepmind.google/blog", "index_path": "", "pagination_path": "?page={page}", "pages": 3, "allow": r"^/blog/(?!rss(?:$|/))(?!feed(?:$|/))(?!tag(?:s)?(?:$|/))(?!page(?:$|/))[a-z0-9][a-z0-9-]+/?$", "requires_js": False},
    "meta": {"base_url": "https://ai.meta.com/blog", "index_path": "", "pagination_path": "/?page={page}", "pages": 3, "allow": r"^/blog/(?!rss(?:$|/))(?!feed(?:$|/))(?!tag(?:s)?(?:$|/))(?!page(?:$|/))[a-z0-9][a-z0-9-]*/?$", "requires_js": True},
    "mistral": {"base_url": "https://mistral.ai/news", "index_path": "", "pagination_path": "/page/{page}", "pages": 3, "allow": r"^/news/(?!rss(?:$|/))(?!feed(?:$|/))(?!tag(?:s)?(?:$|/))(?!page(?:$|/))[a-z0-9][a-z0-9-]+/?$", "requires_js": True},
    "qwen": {"base_url": "https://qwenlm.github.io/blog", "index_path": "", "pagination_path": "/page{page}/", "pages": 3, "allow": r"^/blog/(?!rss(?:$|/))(?!feed(?:$|/))(?!tag(?:s)?(?:$|/))(?!page(?:$|/))[a-z0-9][a-z0-9-]+/?$", "requires_js": False},
    "lilian_weng": {"base_url": "https://lilianweng.github.io", "index_path": "/", "pagination_path": "/page{page}/", "pages": 3, "allow": r"^/posts/\d{4}-\d{2}-\d{2}-[^/]+/?$", "requires_js": False},
    "sebastian_raschka": {"base_url": "https://sebastianraschka.com", "index_path": "/blog", "pagination_path": "/blog/page/{page}", "pages": 3, "allow": r"^/blog/\d{4}/[^/]+/?$", "requires_js": False},
    "jalammar": {"base_url": "https://jalammar.github.io", "index_path": "/", "pagination_path": "/page{page}/", "pages": 3, "allow": r"^/(?!rss(?:$|/))(?!feed(?:$|/))(?!tag(?:s)?(?:$|/))(?!page(?:$|/))[a-z0-9][a-z0-9-]*/?$", "requires_js": False},
}
ALLOWED_DOMAINS = {"arxiv.org", "ar5iv.labs.arxiv.org"} | {urlparse(c["base_url"]).netloc for c in BLOG_SOURCE_CONFIG.values()}


def session():
    """Return Scrapling's static fetcher; it supplies browser-like headers."""
    return Fetcher


def response_status(response) -> int | None:
    """Support both Scrapling and requests-style response objects."""
    return getattr(response, "status", getattr(response, "status_code", None))


def response_text(response) -> str:
    """Return body text from either Scrapling or requests-style responses."""
    if hasattr(response, "body"):
        body = response.body
        if isinstance(body, (bytes, bytearray)):
            return body.decode("utf-8", errors="replace")
        if isinstance(body, str):
            return body
    if hasattr(response, "text"):
        text = response.text
        if isinstance(text, str):
            return text
    if hasattr(response, "content"):
        content = response.content
        if isinstance(content, (bytes, bytearray)):
            return content.decode("utf-8", errors="replace")
        if isinstance(content, str):
            return content
    return ""


def require_success(response, url: str, allowed: tuple[int, ...] = (200,)):
    status = response_status(response)
    if status not in allowed:
        raise RuntimeError(f"HTTP {status} for {url}")
    return response


def arxiv_id(value: str) -> str | None:
    found = re.search(r"(\d{4}\.\d{4,5})(?:v\d+)?", value)
    return found.group(1) if found else None


def discover_arxiv_papers(
    query: str,
    max_results: int,
    client=None,
    page_size: int = 50,
) -> list[str]:
    """Discover versionless arXiv URLs, paging beyond the first result set."""
    if max_results <= 0:
        return []
    if page_size <= 0:
        raise ValueError("page_size must be > 0")
    client = client or session()
    namespace = {"atom": "http://www.w3.org/2005/Atom"}
    discovered = []
    for start in range(0, max_results, page_size):
        requested = min(page_size, max_results - start)
        response = require_success(
            client.get(
                "http://export.arxiv.org/api/query",
                params={
                    "search_query": query,
                    "start": start,
                    "max_results": requested,
                    "sortBy": "relevance",
                    "sortOrder": "descending",
                },
                timeout=30,
            ),
            "arXiv API",
        )
        xml_text = response_text(response)
        root = ET.fromstring(
            xml_text.encode("utf-8") if isinstance(xml_text, str) else xml_text
        )
        entries = root.findall("atom:entry", namespace)
        discovered.extend(
            f"https://arxiv.org/abs/{identifier}"
            for entry in entries
            if (
                identifier := arxiv_id(
                    entry.findtext("atom:id", default="", namespaces=namespace)
                )
            )
        )
        if len(entries) < requested:
            break
    return unique(discovered)


def discover_semantic_scholar_neighbors(seed_urls: list[str], max_neighbors: int = 4, client=None) -> list[str]:
    """One-hop cited/citing arXiv expansion; honours the public 1 RPS limit."""
    if max_neighbors <= 0:
        return []
    client = client or session()
    neighbors = []
    for seed in seed_urls:
        if not (identifier := arxiv_id(seed)):
            continue
        for relation in ("references", "citations"):
            try:
                response = client.get(f"https://api.semanticscholar.org/graph/v1/paper/ARXIV:{identifier}/{relation}", params={"limit": max_neighbors, "fields": "externalIds"}, timeout=30)
                if response_status(response) == 429:
                    LOG.warning("Semantic Scholar rate limited; ending citation expansion")
                    return neighbors
                require_success(response, f"Semantic Scholar {relation}")
                payload = response.json() if hasattr(response, "json") else json.loads(response_text(response))
                for item in payload.get("data", []):
                    paper = item.get("citingPaper") or item.get("citedPaper") or item
                    arxiv = (paper.get("externalIds") or {}).get("ArXiv")
                    if arxiv and (neighbor := arxiv_id(arxiv)):
                        neighbors.append(f"https://arxiv.org/abs/{neighbor}")
            except (RuntimeError, ValueError, OSError, TypeError, json.JSONDecodeError) as error:
                LOG.warning("Semantic Scholar %s lookup for %s failed: %s", relation, identifier, error)
            time.sleep(SEMANTIC_SCHOLAR_DELAY_SECONDS)
    return neighbors


def discover_blog_index(base_url: str, config: dict, client=None) -> list[str]:
    """Find matching articles in a static index; warns where JS is required."""
    client = client or session()
    root = urlparse(base_url)
    paths = [config.get("index_path", "")] + [config["pagination_path"].format(page=page) for page in range(2, config.get("pages", 1) + 1)]
    matches = []
    for path in paths:
        page_url = urljoin(base_url + "/", path.lstrip("/"))
        try:
            response = require_success(client.get(page_url, timeout=30), page_url)
            for href in response.css("a::attr(href)").getall():
                candidate = urljoin(page_url, href).split("#", 1)[0]
                parsed = urlparse(candidate)
                if parsed.netloc != root.netloc:
                    continue
                candidate_path = parsed.path or "/"
                if re.search(r"(?i)(?:^|/)(?:rss|feed|tag|tags|page|author|category|categories|search)(?:/|$)", candidate_path):
                    continue
                if re.search(config["allow"], candidate_path, re.I):
                    matches.append(candidate)
        except (RuntimeError, OSError) as error:
            LOG.warning("Blog index %s failed: %s", page_url, error)
    if not matches and config.get("requires_js"):
        LOG.warning("%s needs JS rendering or an index-config update; static discovery returned zero URLs", base_url)
    return matches


def html_document(page) -> tuple[str, str]:
    """Use Scrapling's RAG Markdown conversion, including its noise removal."""
    title = page.css("meta[name='citation_title']::attr(content)").get() or page.css("title::text").get("")
    markdown = page.markdown(main_content_only=True)
    lowered = markdown.lower()
    if "<?xml" in lowered or "<rss" in lowered or "<feed" in lowered:
        raise ValueError("RSS/XML feed content detected instead of HTML article content")
    content_type = ""
    headers = getattr(page, "headers", {}) or {}
    if isinstance(headers, dict):
        content_type = headers.get("content-type", "")
    if content_type and "text/html" not in content_type.lower():
        raise ValueError(f"Unexpected response content-type: {content_type}")
    if not title.strip() and not re.search(r"^\s{0,3}#{1,6}\s+\S", markdown, flags=re.MULTILINE):
        raise ValueError("HTML content lacks an article title or heading")
    return title.strip(), markdown


def abstract_only(identifier: str, client) -> tuple[str, str]:
    response = require_success(client.get(f"https://arxiv.org/abs/{identifier}", timeout=30), f"arXiv abstract {identifier}")
    title = response.css("meta[name='citation_title']::attr(content)").get("")
    return title, " ".join(response.css("blockquote.abstract::text").getall()).strip()


def ar5iv_document_is_usable(title: str, markdown: str) -> bool:
    """Reject ar5iv conversion shells so collection falls back to the PDF."""
    normalized_title = re.sub(r"\s+", " ", (title or "").strip().lower())
    normalized_markdown = re.sub(r"\s+", " ", (markdown or "").strip().lower())
    if len(normalized_markdown) < 500:
        return False
    if not normalized_title or "untitled document" in normalized_title:
        return False

    # A failed LaTeXML conversion can return HTTP 200 with a long navigation
    # shell. It contains no paper text but used to pass the length check.
    conversion_shell_markers = (
        "see pages 1-last of <ppo-min.pdf>",
        "see pages 1-last of ppo-min.pdf",
    )
    return not any(marker in normalized_markdown for marker in conversion_shell_markers)


def fetch_arxiv_full_text(url: str, client=None) -> dict:
    """Use ar5iv HTML, PDF extraction, then abstract-only fallback."""
    client = client or session()
    identifier = arxiv_id(url)
    if not identifier:
        raise ValueError(f"Invalid arXiv URL: {url}")
    canonical = f"https://arxiv.org/abs/{identifier}"
    try:
        response = client.get(f"https://ar5iv.labs.arxiv.org/html/{identifier}", timeout=45)
        if response_status(response) != 404:
            require_success(response, f"ar5iv {identifier}")
            title, markdown = html_document(response)
            if ar5iv_document_is_usable(title, markdown):
                return {"url": canonical, "title": title, "markdown": markdown, "fetch_method": "ar5iv"}
            LOG.info("ar5iv returned a conversion shell for %s; trying PDF", identifier)
    except (RuntimeError, ValueError, OSError) as error:
        LOG.info("ar5iv failed for %s: %s", identifier, error)
    try:
        if pymupdf is None:
            raise RuntimeError("PyMuPDF is unavailable")
        response = require_success(client.get(f"https://arxiv.org/pdf/{identifier}", timeout=60), f"arXiv PDF {identifier}")
        pdf_bytes = response.body if hasattr(response, "body") else response.content
        with pymupdf.open(stream=pdf_bytes, filetype="pdf") as pdf:
            markdown = "\n\n".join(page.get_text("text") for page in pdf)
        if len(markdown.strip()) >= 500:
            title, _ = abstract_only(identifier, client)
            return {"url": canonical, "title": title, "markdown": markdown, "fetch_method": "pdf"}
    except (RuntimeError, ValueError, OSError) as error:
        LOG.info("PDF failed for %s: %s", identifier, error)
    title, markdown = abstract_only(identifier, client)
    return {"url": canonical, "title": title, "markdown": markdown, "fetch_method": "abstract_only"}


def fetch_blog(url: str, client=None) -> dict:
    client = client or session()
    response = require_success(client.get(url, timeout=30), url)
    headers = getattr(response, "headers", {}) or {}
    content_type = headers.get("content-type", "") if isinstance(headers, dict) else ""
    if content_type and "text/html" not in content_type.lower():
        raise ValueError(f"Non-HTML response for {url}: {content_type}")
    title, markdown = html_document(response)
    return {"url": url, "title": title, "markdown": markdown, "fetch_method": "html"}


def unique(urls: list[str]) -> list[str]:
    return list(dict.fromkeys(urls))


def canonical_source_url(url: str) -> str:
    """Return a stable identity for merging crawls and arXiv revisions."""
    parsed = urlparse((url or "").strip())
    if not parsed.scheme or not parsed.netloc:
        return ""
    if parsed.netloc.lower() in {
        "arxiv.org",
        "www.arxiv.org",
        "ar5iv.labs.arxiv.org",
    } and (identifier := arxiv_id(url)):
        return f"https://arxiv.org/abs/{identifier}"
    path = parsed.path.rstrip("/") or "/"
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", "", ""))


def load_existing_documents(path: Path = RAW_PATH) -> list[dict]:
    if not path.exists():
        return []
    return load_jsonl(path)


def document_quality(document: dict) -> tuple[int, int]:
    """Rank duplicate records by usable full-text quality, then body length."""
    title = str(document.get("title", ""))
    markdown = str(document.get("markdown", ""))
    method = str(document.get("fetch_method", ""))
    normalized_title = re.sub(r"\s+", " ", title.strip().lower())

    if "untitled document" in normalized_title or len(markdown.strip()) < 500:
        return (0, len(markdown))
    if method == "ar5iv" and not ar5iv_document_is_usable(title, markdown):
        return (0, len(markdown))

    method_quality = {
        "ar5iv": 4,
        "pdf": 3,
        "html": 3,
        "abstract_only": 1,
    }.get(method, 2)
    return (method_quality, len(markdown))


def document_needs_refresh(document: dict) -> bool:
    """Return true for a persisted record that should be fetched again."""
    return document_quality(document)[0] == 0


def merge_documents(existing: list[dict], additions: list[dict]) -> list[dict]:
    """Keep the best available record for each canonical source URL."""
    merged = []
    source_indexes = {}
    for document in existing + additions:
        source = canonical_source_url(document.get("url", ""))
        if not source:
            continue
        if source not in source_indexes:
            source_indexes[source] = len(merged)
            merged.append(document)
            continue

        index = source_indexes[source]
        if document_quality(document) > document_quality(merged[index]):
            merged[index] = document
    return merged


def write_documents_atomic(path: Path, documents: list[dict]) -> None:
    write_jsonl_atomic(path, documents)


def run(
    max_arxiv_per_topic: int = 50,
    max_snowball_neighbors: int = 2,
    arxiv_page_size: int = 50,
    preserve_existing: bool = True,
    curated_only: bool = False,
) -> list[dict]:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    client = session()
    existing_docs = load_existing_documents() if preserve_existing else []
    existing_by_source = {
        canonical_source_url(document.get("url", "")): document
        for document in existing_docs
        if canonical_source_url(document.get("url", ""))
    }
    seeds = []
    # Evaluation queries are deliberately excluded: corpus construction must
    # remain independent from held-out retrieval tests.
    if not curated_only:
        for query in TOPIC_QUERIES:
            try:
                seeds.extend(
                    discover_arxiv_papers(
                        query,
                        max_arxiv_per_topic,
                        client,
                        page_size=arxiv_page_size,
                    )
                )
            except (RuntimeError, OSError, ET.ParseError) as error:
                LOG.warning("arXiv query failed (%s): %s", query, error)
            time.sleep(ARXIV_DELAY_SECONDS)
    seeds = unique(seeds)
    blogs = (
        [
            url
            for config in BLOG_SOURCE_CONFIG.values()
            for url in discover_blog_index(config["base_url"], config, client)
        ]
        if not curated_only
        else []
    )
    expansion_seeds = unique(CURATED_SOURCE_URLS + seeds)
    neighbors = (
        discover_semantic_scholar_neighbors(
            expansion_seeds, max_snowball_neighbors, client
        )
        if not curated_only
        else []
    )
    candidates = unique(
        CURATED_SOURCE_URLS
        + seeds
        + neighbors
        + blogs
    )
    missing_candidates = [
        url for url in candidates if canonical_source_url(url) not in existing_by_source
    ]
    refresh_candidates = [
        url
        for url in candidates
        if (
            canonical_source_url(url) in existing_by_source
            and document_needs_refresh(
                existing_by_source[canonical_source_url(url)]
            )
        )
    ]
    pending = unique(missing_candidates + refresh_candidates)
    additions, stats = [], {}
    for index, url in enumerate(pending):
        domain = urlparse(url).netloc
        if domain not in ALLOWED_DOMAINS:
            LOG.warning("Skipping out-of-policy candidate %s because %s is not in ALLOWED_DOMAINS", url, domain)
            continue
        stats.setdefault(domain, Counter())
        try:
            if index:
                time.sleep(1.2)
            document = fetch_arxiv_full_text(url, client) if domain == "arxiv.org" else fetch_blog(url, client)
            document["source_domain"] = domain
            additions.append(document)
            stats[domain].update(("success", document["fetch_method"]))
        except (RuntimeError, ValueError, OSError) as error:
            stats[domain]["failure"] += 1
            LOG.warning("Fetch failed for %s: %s", url, error)
    docs = merge_documents(existing_docs, additions)
    merged_sources = {
        canonical_source_url(document.get("url", "")) for document in docs
    }
    replacement_count = sum(
        canonical_source_url(document.get("url", "")) in existing_by_source
        for document in additions
    )
    new_source_count = sum(
        canonical_source_url(document.get("url", "")) not in existing_by_source
        and canonical_source_url(document.get("url", "")) in merged_sources
        for document in additions
    )
    if not curated_only:
        for config in BLOG_SOURCE_CONFIG.values():
            domain = urlparse(config["base_url"]).netloc
            if config.get("requires_js") and not any(doc.get("source_domain") == domain for doc in docs):
                raise RuntimeError(f"Configured JS-rendered source {domain} contributed zero documents; static discovery or fetch path is broken")
    write_documents_atomic(RAW_PATH, docs)
    report = {
        "mode": "curated_only" if curated_only else "curated_plus_discovery",
        "curated_seeds": len(CURATED_SOURCE_URLS),
        "discovered": len(candidates),
        "preserved": len(existing_docs),
        "already_present": len(candidates) - len(missing_candidates) - len(refresh_candidates),
        "refresh_attempted": len(refresh_candidates),
        "attempted": len(pending),
        "fetched_success": len(additions),
        "new_sources_written": new_source_count,
        "replacements_written": replacement_count,
        "written": len(docs),
        "domains": {domain: dict(counts) for domain, counts in stats.items()},
        "js_rendering_candidates": [config["base_url"] for config in BLOG_SOURCE_CONFIG.values() if config["requires_js"]],
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return docs


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Collect curated seeds plus query/citation discoveries."
    )
    parser.add_argument(
        "--max-arxiv-per-topic",
        type=int,
        default=50,
        help="Maximum arXiv results per topic (default: 50)",
    )
    parser.add_argument(
        "--arxiv-page-size",
        type=int,
        default=50,
        help="arXiv API page size (default: 50)",
    )
    parser.add_argument(
        "--max-snowball-neighbors",
        type=int,
        default=2,
        help="References/citations requested per seed (default: 2)",
    )
    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help="Discard existing raw documents instead of merging with them",
    )
    parser.add_argument(
        "--curated-only",
        action="store_true",
        help="Backfill missing curated seeds without broad search or citation expansion",
    )
    args = parser.parse_args()
    if args.max_arxiv_per_topic < 0:
        parser.error("--max-arxiv-per-topic must be >= 0")
    if args.arxiv_page_size <= 0:
        parser.error("--arxiv-page-size must be > 0")
    if args.max_snowball_neighbors < 0:
        parser.error("--max-snowball-neighbors must be >= 0")
    run(
        max_arxiv_per_topic=args.max_arxiv_per_topic,
        max_snowball_neighbors=args.max_snowball_neighbors,
        arxiv_page_size=args.arxiv_page_size,
        preserve_existing=not args.replace_existing,
        curated_only=args.curated_only,
    )


if __name__ == "__main__":
    main()
