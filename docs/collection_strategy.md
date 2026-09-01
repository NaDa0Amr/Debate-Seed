# Collection strategy

`src.collection` merges the legacy spider's curated seeds with query-driven
discovery. It uses Scrapling's `Fetcher` for API, index, ar5iv, and blog HTTP
requests, plus Scrapling's RAG Markdown conversion for HTML content. It keeps
the existing JSONL document contract and adds
`fetch_method` and `source_domain` to every record. A run also writes
`data/collection_report.json`, with per-domain success/failure and fetch-path
counts.

## Discovery

The shared `src.source_seeds` manifest provides a deterministic corpus
foundation, including every source referenced by the fixed qrels. Ten focused
arXiv API queries cover MoE versus dense models, efficient
attention variants, SSMs, hybrid architectures, pretraining versus reasoning
training, PPO versus GRPO, and retrieval-augmented generation. Held-out
evaluation query text is not used for discovery. Search results paginate when
the configured per-topic limit exceeds the API page size. The collector
waits roughly three seconds between arXiv API
calls. Each resulting versionless arXiv paper is expanded by one
citation-graph hop through Semantic Scholar's references and citations
endpoints. Semantic Scholar requests are paced at just under one request per
second; a 429 stops expansion cleanly.

Blog discovery is configured in one `BLOG_SOURCE_CONFIG` map, rather than
hardcoded in crawler rules. It includes Hugging Face, OpenAI, Anthropic,
Google DeepMind, Meta AI, Mistral, Qwen, Lilian Weng, Sebastian Raschka, and
Jay Alammar. Existing raw documents and new candidates are merged by canonical
URL, so a collection run does not discard prior work. OpenAI, DeepMind, Meta,
and Mistral are explicitly flagged as likely JS-rendered coverage gaps when
their static indices yield no article links; adding Playwright is the next
step for those sources.

## Full-paper fallback

For an arXiv URL, collection attempts:

1. `https://ar5iv.labs.arxiv.org/html/<id>` and converts the HTML article to
   Markdown.
2. `https://arxiv.org/pdf/<id>` and extracts text with PyMuPDF.
3. `https://arxiv.org/abs/<id>` as an abstract-only last resort.

The corresponding `fetch_method` is `ar5iv`, `pdf`, or `abstract_only`.
Non-arXiv HTML documents use `html`. Versioned `/abs/<id>vN` URLs remain
excluded by the old spider rule, while the new collector canonicalizes all
arXiv URLs to versionless `/abs/<id>` before storage.

## Cleaning and scale

`src.clean.light_clean` now removes reference/bibliography sections, common
LaTex citation and environment remnants, equation-number-only lines, and
figure/table captions. It also removes PDF page-number lines and joins broken
prose lines without joining Markdown headers or lists. The normalized
strong-term relevance filter remains the collection safety net. Chunking continues
to split Markdown headings first and then recursively into 1200-character
chunks with 300-character overlap and a 200-character minimum, so larger papers are processed as many bounded
chunks rather than oversized records.

Known limitation: PDF extraction is necessarily less structural than ar5iv;
documents that fall back to it may have fewer useful headings. The report's
fetch-method totals make that coverage visible.
