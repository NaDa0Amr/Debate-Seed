"""
Step 1: Data collection.

Crawls a seeded list of URLs known to be on-topic (transformer architecture /
training-strategy content: MoE, attention variants, SSMs, PPO/GRPO) and
converts each page to clean Markdown.

Kept shallow on purpose: we seed with specific known-good pages rather than
letting the crawler wander through an entire domain, which is what was
pulling in off-topic content before.

Key enhancement: deny versioned arXiv URLs (e.g. /abs/1706.03762v1..v7) to
avoid near-duplicate documents. The versionless URL (/abs/1706.03762) always
points to the latest revision.

Run:
    python src/spider.py
Output:
    Delegates to src.collection, merging curated seeds and discovered sources
    into data/raw_docs.jsonl without overwriting existing documents by default.
"""

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scrapling.spiders import SiteToMarkdownSpider, CrawlRule, LinkExtractor

from src.source_seeds import CURATED_SOURCE_URLS


class TransformerDocsSpider(SiteToMarkdownSpider):
    name = "transformer_docs"

    # --- Seed with pages you already know are on-topic. ---
    # Built from targeted searches (arXiv search, Google Scholar,
    # "site:huggingface.co/blog moe", etc.).
    start_urls = CURATED_SOURCE_URLS

    # Legacy Scrapling entry point. The pipeline now uses src.collection,
    # whose full-text fallback includes ar5iv; retain this allow-list entry
    # for callers that still instantiate this spider directly.
    allowed_domains = {"arxiv.org", "ar5iv.labs.arxiv.org", "huggingface.co", "lilianweng.github.io"}
    output_dir = "data/raw_markdown"
    max_pages = 300         # headroom above the 50-doc minimum
    main_content_only = True

    def rules(self):
        return [
            CrawlRule(
                LinkExtractor(
                    # Only follow further links that still look on-topic.
                    allow=[
                        r"/abs/\d+\.\d+$",       # arXiv abstracts (versionless only)
                        r"/blog/[a-z0-9\-]*(moe|mixtral|mamba|attention|rlhf|grpo|ppo|reasoning)",
                        r"/posts/\d{4}-\d{2}-\d{2}",  # Lilian Weng blog posts
                    ],
                    deny=[
                        r"/abs/\d+\.\d+v\d+",   # SKIP versioned arXiv pages (v1, v2, ...)
                        r"/pdf/", r"/list/", r"\?",
                        r"/tags/", r"/page/\d+/",
                        r"/html/",               # arXiv HTML renderings
                    ],
                ),
                callback=self.parse,
            )
        ]


if __name__ == "__main__":
    # Keep the historical command working, but route it through the merged
    # collector so it preserves existing documents and uses full-text fallbacks.
    from src.collection import main as collection_main

    print("src/spider.py now delegates to the merged src/collection.py workflow.")
    collection_main()
