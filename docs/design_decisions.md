# Design Decisions

This document explains the rationale behind each major architectural and technical decision in the RAG knowledge pipeline.

---

## 1. Data Collection

### Source Selection

**Decision:** Seed the spider with 40+ specific URLs from arXiv, HuggingFace Blog, and Lilian Weng's blog.

**Why:** Rather than broad crawling (e.g., "crawl all of arxiv.org"), we use targeted seeding because:
- It ensures high-quality, on-topic content from the start
- It avoids the noise of general-purpose crawling (e.g., arXiv listing pages, random CS papers)
- The allowed `follow` patterns let the crawler discover related papers linked from our seeds
- Lilian Weng's posts are dense survey-style articles that reference many papers, making them excellent starting points for link discovery

**Trade-off:** We sacrifice breadth (some relevant papers won't be discovered) for precision (nearly everything collected is on-topic).

### arXiv Version Deduplication

**Decision:** The spider's `deny` rules skip versioned arXiv URLs (`/abs/1706.03762v1`, `v2`, etc.).

**Why:** arXiv publishes each revision as a separate URL. Without deduplication, a single paper with 7 versions becomes 7 near-identical documents, inflating chunk counts and degrading retrieval precision (the same content appears in multiple chunks). The versionless URL (`/abs/1706.03762`) always serves the latest revision.

### Scraping Tool

**Decision:** Scrapling `SiteToMarkdownSpider`.

**Why:** Scrapling's `SiteToMarkdownSpider` template converts pages to clean Markdown during the crawl itself, handling HTML parsing, script/style removal, and structural conversion in one step. This eliminates the need for a separate HTML-to-Markdown tool and ensures consistent conversion quality.

---

## 2. Data Cleaning

### Relevance Filtering

**Decision:** Two-tier keyword filtering with "strong" and "weak" keyword lists.

**Why:** A simple keyword count (`text.count("attention") >= 1`) produces too many false positives — "attention" appears in papers about computer vision, psychology, and many unrelated fields. By requiring at least 1 strong keyword (e.g., "mixture of experts", "mamba", "grpo") AND ≥2 total keyword hits, we ensure documents are genuinely about our debate topics.

**Trade-off:** Some borderline papers may be dropped. We log dropped documents with reasons to `data/dropped_docs.jsonl` for manual inspection.

### arXiv Boilerplate Removal

**Decision:** Regex-based removal of arXiv navigation chrome, submission history, and download links.

**Why:** Even after Markdown conversion, arXiv pages contain structured boilerplate (submission dates, version history tables, navigation links) that adds noise to chunks without contributing information. Since this boilerplate follows predictable patterns across all arXiv pages, regex is reliable here.

---

## 3. Chunking Strategy

### Method: Structure-Aware (Markdown Header Split → Recursive Character Split)

**Decision:** First split on Markdown headers (#, ##, ###), then recursively split oversized sections.

**Why:** Our documents have real structural headings (paper sections, blog post headers). Splitting on headers preserves semantic coherence — an entire "MoE vs Dense" subsection stays together as one chunk when it fits, rather than being cut mid-argument at an arbitrary character boundary.

**Alternative considered:** Fixed-size chunking (simpler but loses structural context). Semantic chunking (embedding-based boundary detection — interesting but overkill for documents with explicit headers).

### Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Chunk size | 800 chars | ~150-200 tokens, well within all-MiniLM-L6-v2's 256-token input limit. Favors retrieval precision over context preservation. |
| Chunk overlap | 100 chars | Ensures context isn't lost at cut boundaries. A sentence split across two chunks will appear in both. |
| Min chunk length | 40 chars | Drops fragments that are just a header with no body text. |

---

## 4. Embedding Model

### Model: `all-MiniLM-L6-v2`

| Property | Value |
|----------|-------|
| Dimensions | 384 |
| Model size | ~80 MB |
| Max tokens | 256 |
| License | Apache 2.0 |

**Why:**
- **Free and local:** No API key, no cost per embedding, no rate limits. Important for a reproducible project.
- **Fast on CPU:** Embeds ~4800 chunks in under 30 seconds without a GPU.
- **Proven quality:** Widely used baseline in retrieval benchmarks (MTEB). While not SOTA, it's "good enough" for ~200 documents.

**Trade-offs documented:**
- `all-mpnet-base-v2` (768-dim): ~2x better retrieval quality on MTEB, but 3x larger and slower.
- OpenAI `text-embedding-3-small` (1536-dim): Higher quality, but introduces API cost and external dependency.
- Domain-specific models: Could improve on ML-specific terminology, but none are readily available for this narrow domain.

---

## 5. Database Configuration

### PostgreSQL + pgvector

**Decision:** Use PostgreSQL with the pgvector extension for vector storage, and PostgreSQL's built-in full-text search for keyword matching.

**Why:** PostgreSQL is required by the project. pgvector adds native vector operations. Using the same database for both vector and keyword search avoids the complexity of managing a separate search engine (e.g., Elasticsearch).

### Schema Design

The `chunks` table stores everything needed for retrieval and provenance:

```sql
CREATE TABLE chunks (
    chunk_id        TEXT PRIMARY KEY,
    text            TEXT NOT NULL,
    url             TEXT,
    title           TEXT,
    headers         JSONB,
    doc_index       INTEGER,
    chunk_index     INTEGER,
    char_len        INTEGER,
    embedding_model TEXT,
    embedding       VECTOR(384),
    text_search     TSVECTOR GENERATED ALWAYS AS (
        to_tsvector('english', coalesce(title, '') || ' ' || text)
    ) STORED
);
```

Key decisions:
- **`text_search` as a generated column:** Automatically maintained by PostgreSQL on insert/update. No application code needed to keep it in sync.
- **`headers` as JSONB:** Preserves the section hierarchy from the Markdown header split, which is useful for displaying context in retrieval results.
- **IVFFlat index:** Approximate nearest-neighbor index for fast vector search. Lists count = sqrt(n) following the pgvector recommendation.
- **GIN index:** Standard index type for full-text search on tsvector columns.

---

## 6. Retrieval Strategy

### Hybrid Search (Vector + BM25) + Cross-Encoder Reranking

This is a three-stage retrieval pipeline:

```
Query
  │
  ├─→ Vector Search (pgvector cosine) ──→ Top 30 by similarity
  │                                           │
  ├─→ Keyword Search (tsvector/tsquery) ─→ Top 30 by BM25 rank
  │                                           │
  └─→ Reciprocal Rank Fusion (RRF) ─────→ Merged top ~40 candidates
                                              │
                                              ▼
                                    Cross-Encoder Reranker
                                    (ms-marco-MiniLM-L-6-v2)
                                              │
                                              ▼
                                    Final Top-K results
```

### Why Hybrid Over Pure Vector

Vector search alone misses:
- **Exact term matches:** The query "GRPO" should retrieve chunks containing that exact acronym, but a 384-dim embedding may not represent rare domain acronyms precisely.
- **Keyword-heavy queries:** "PPO vs GRPO reinforcement learning" has clear keyword signals that BM25 captures perfectly.

Keyword search alone misses:
- **Semantic similarity:** "Models that route tokens to a subset of experts" should retrieve MoE content even though it doesn't mention "MoE" or "Mixture of Experts."

### Reciprocal Rank Fusion (RRF)

**Formula:** `score(d) = Σ 1/(k + rank_i(d))` across all retriever lists, with k=60.

**Why RRF:**
- No learned parameters — works out of the box
- Score-agnostic — doesn't need calibrated similarity/BM25 scores
- Symmetric — treats both retrievers equally unless their rank distributions differ naturally

### Cross-Encoder Reranking

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Why:** A bi-encoder (used for initial retrieval) embeds query and document independently, so it can't model fine-grained interactions between them. A cross-encoder processes (query, document) as a single input, allowing it to detect whether a specific question is actually answered by a specific passage.

**Trade-off:** Adds ~100ms of latency for 20 candidates. Acceptable for this use case (not real-time search). Can be disabled with `--no-rerank` if latency matters.

---

## 7. Evaluation Methodology

### Test Queries

7 queries covering all 6 debate topics, plus one cross-cutting (SSM/Mamba). Each query has a set of expected relevant source URLs (arXiv paper IDs and blog URLs).

### Metrics

| Metric | What it measures | Why we use it |
|--------|-----------------|---------------|
| Precision@5 | Fraction of top-5 that are relevant | "How noisy are the results?" |
| Recall@5 | Fraction of expected sources found in top-5 | "How much relevant content are we finding?" |
| MRR | 1/rank of the first relevant result | "How quickly does the user see something relevant?" |

### Comparison Modes

We evaluate in two modes to quantify the value of each pipeline stage:
1. **Hybrid + Reranker** — full pipeline
2. **Hybrid Only** — no cross-encoder reranking

This lets us make a data-driven recommendation about whether the reranker justifies its latency cost.
