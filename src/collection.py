"""Query-driven collection with ar5iv -> PDF -> abstract arXiv fallback."""
from __future__ import annotations

import json
import logging
import re
import time
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin, urlparse

from scrapling.fetchers import Fetcher

try:
    import fitz
except ImportError:
    fitz = None

LOG = logging.getLogger(__name__)
RAW_PATH = Path("data/raw_docs.jsonl")
REPORT_PATH = Path("data/collection_report.json")
ARXIV_DELAY_SECONDS = 3.0
SEMANTIC_SCHOLAR_DELAY_SECONDS = 1.1
TOPIC_QUERIES = [
    "all:(mixture of experts dense transformer routing)",
    "all:(efficient attention linear sparse sliding window transformer)",
    "all:(state space model Mamba transformer)",
    "all:(hybrid attention state space architecture)",
    "all:(pretraining reasoning oriented training language model)",
    "all:(PPO GRPO reinforcement learning language model)",
]

# Index, pagination and article-link matching are deliberately data, rather
# than discovery logic scattered across the crawler.
BLOG_SOURCE_CONFIG = {
    "huggingface": {"base_url": "https://huggingface.co/blog", "index_path": "", "pagination_path": "/page/{page}", "pages": 3, "allow": r"^/blog/[a-z0-9][a-z0-9-]*$", "requires_js": False},
    "openai": {"base_url": "https://openai.com/research", "index_path": "", "pagination_path": "/research/page/{page}", "pages": 3, "allow": r"^/index/[^/]+/$", "requires_js": True},
    "anthropic": {"base_url": "https://www.anthropic.com/research", "index_path": "", "pagination_path": "/research?page={page}", "pages": 3, "allow": r"^/research/[^/]+$", "requires_js": False},
    "deepmind": {"base_url": "https://deepmind.google/discover/blog", "index_path": "", "pagination_path": "?page={page}", "pages": 3, "allow": r"^/discover/blog/[^/]+$", "requires_js": True},
    "meta": {"base_url": "https://ai.meta.com/blog", "index_path": "", "pagination_path": "/?page={page}", "pages": 3, "allow": r"^/blog/[^/]+/$", "requires_js": True},
    "mistral": {"base_url": "https://mistral.ai/news", "index_path": "", "pagination_path": "/page/{page}", "pages": 3, "allow": r"^/news/[^/]+$", "requires_js": True},
    "qwen": {"base_url": "https://qwenlm.github.io/blog", "index_path": "", "pagination_path": "/page{page}/", "pages": 3, "allow": r"^/blog/[^/]+/$", "requires_js": False},
    "lilian_weng": {"base_url": "https://lilianweng.github.io", "index_path": "/", "pagination_path": "/page{page}/", "pages": 3, "allow": r"^/posts/\d{4}-\d{2}-\d{2}-[^/]+/?$", "requires_js": False},
    "sebastian_raschka": {"base_url": "https://sebastianraschka.com", "index_path": "/blog", "pagination_path": "/blog/page/{page}", "pages": 3, "allow": r"^/blog/\d{4}/[^/]+/?$", "requires_js": False},
    "jalammar": {"base_url": "https://jalammar.github.io", "index_path": "/", "pagination_path": "/page{page}/", "pages": 3, "allow": r"^/[^/]+/$", "requires_js": False},
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


def discover_arxiv_papers(query: str, max_results: int, client=None) -> list[str]:
    """Discover versionless arXiv abstract URLs through the official API."""
    client = client or session()
    response = require_success(client.get("http://export.arxiv.org/api/query", params={"search_query": query, "start": 0, "max_results": max_results, "sortBy": "relevance", "sortOrder": "descending"}, timeout=30), "arXiv API")
    xml_text = response_text(response)
    root = ET.fromstring(xml_text.encode("utf-8") if isinstance(xml_text, str) else xml_text)
    namespace = {"atom": "http://www.w3.org/2005/Atom"}
    return [f"https://arxiv.org/abs/{identifier}" for entry in root.findall("atom:entry", namespace) if (identifier := arxiv_id(entry.findtext("atom:id", default="", namespaces=namespace)))]


def discover_semantic_scholar_neighbors(seed_urls: list[str], max_neighbors: int = 4, client=None) -> list[str]:
    """One-hop cited/citing arXiv expansion; honours the public 1 RPS limit."""
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
                require_success(response, endpoint := f"Semantic Scholar {relation}")
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
                if parsed.netloc == root.netloc and re.search(config["allow"], parsed.path, re.I):
                    matches.append(candidate)
        except (RuntimeError, OSError) as error:
            LOG.warning("Blog index %s failed: %s", page_url, error)
    if not matches and config.get("requires_js"):
        LOG.warning("%s needs JS rendering or an index-config update; static discovery returned zero URLs", base_url)
    return matches


def html_document(page) -> tuple[str, str]:
    """Use Scrapling's RAG Markdown conversion, including its noise removal."""
    title = page.css("meta[name='citation_title']::attr(content)").get() or page.css("title::text").get("")
    return title.strip(), page.markdown(main_content_only=True)


def abstract_only(identifier: str, client) -> tuple[str, str]:
    response = require_success(client.get(f"https://arxiv.org/abs/{identifier}", timeout=30), f"arXiv abstract {identifier}")
    title = response.css("meta[name='citation_title']::attr(content)").get("")
    return title, " ".join(response.css("blockquote.abstract::text").getall()).strip()


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
            if len(markdown.strip()) >= 500:
                return {"url": canonical, "title": title, "markdown": markdown, "fetch_method": "ar5iv"}
    except (RuntimeError, OSError) as error:
        LOG.info("ar5iv failed for %s: %s", identifier, error)
    try:
        if fitz is None:
            raise RuntimeError("PyMuPDF is unavailable")
        response = require_success(client.get(f"https://arxiv.org/pdf/{identifier}", timeout=60), f"arXiv PDF {identifier}")
        pdf = fitz.open(stream=response.body if hasattr(response, "body") else response.content, filetype="pdf")
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
    title, markdown = html_document(response)
    return {"url": url, "title": title, "markdown": markdown, "fetch_method": "html"}


def unique(urls: list[str]) -> list[str]:
    return list(dict.fromkeys(urls))


def run(max_arxiv_per_topic: int = 12, max_snowball_neighbors: int = 4) -> list[dict]:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    client = session()
    seeds = []
    for query in TOPIC_QUERIES:
        try:
            seeds.extend(discover_arxiv_papers(query, max_arxiv_per_topic, client))
        except (RuntimeError, OSError, ET.ParseError) as error:
            LOG.warning("arXiv query failed (%s): %s", query, error)
        time.sleep(ARXIV_DELAY_SECONDS)
    seeds = unique(seeds)
    blogs = [url for config in BLOG_SOURCE_CONFIG.values() for url in discover_blog_index(config["base_url"], config, client)]
    candidates = unique(seeds + discover_semantic_scholar_neighbors(seeds, max_snowball_neighbors, client) + blogs)
    docs, stats = [], {}
    for url in candidates:
        domain = urlparse(url).netloc
        stats.setdefault(domain, Counter())
        try:
            document = fetch_arxiv_full_text(url, client) if domain == "arxiv.org" else fetch_blog(url, client)
            document["source_domain"] = domain
            docs.append(document)
            stats[domain].update(("success", document["fetch_method"]))
        except (RuntimeError, ValueError, OSError) as error:
            stats[domain]["failure"] += 1
            LOG.warning("Fetch failed for %s: %s", url, error)
    RAW_PATH.parent.mkdir(exist_ok=True)
    with RAW_PATH.open("w", encoding="utf-8") as output:
        for document in docs:
            output.write(json.dumps(document, ensure_ascii=False) + "\n")
    report = {"discovered": len(candidates), "written": len(docs), "domains": {domain: dict(counts) for domain, counts in stats.items()}, "js_rendering_candidates": [config["base_url"] for config in BLOG_SOURCE_CONFIG.values() if config["requires_js"]]}
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return docs
