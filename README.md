# RAG Knowledge Infrastructure — Transformer Architecture Debates

A complete Retrieval-Augmented Generation (RAG) pipeline for the domain of **transformer architecture design decisions**, covering debates such as MoE vs. Dense, attention variants, hybrid architectures, and RL fine-tuning strategies (PPO vs. GRPO).

## Domain

The knowledge base covers six core debate topics in modern LLM architecture:

1. **MoE vs. Dense** — Mixture-of-Experts routing vs. dense feed-forward layers
2. **Normal vs. Linear Attention vs. SSM** — Standard softmax, linear approximations, and state-space models
3. **Sliding Window vs. Full Global Attention** — Local vs. global attention mechanisms
4. **Hybrid Architectures** — Combining attention + SSM, local + global, dense + MoE
5. **Pretraining vs. Reasoning-Oriented Training** — When to introduce reasoning objectives
6. **PPO vs. GRPO** — Reinforcement learning fine-tuning strategies

## Architecture

```
Web Sources (arXiv, HuggingFace, Lilian Weng)
        │
        ▼
[1] Spider (Scrapling SiteToMarkdownSpider)     → data/raw_docs.jsonl
        │
        ▼
[2] Clean (dedup arXiv versions, relevance)     → data/clean_docs.jsonl
        │
        ▼
[3] Chunk (Markdown header + recursive split)   → data/chunks.jsonl
        │
        ▼
[4] Embed (all-MiniLM-L6-v2, 384-dim)         → data/chunks_with_embeddings.jsonl
        │
        ▼
[5] Store (PostgreSQL + pgvector + tsvector)    → chunks table
        │
        ▼
[6] Retrieve (Hybrid: vector + BM25 + reranker) → ranked results
        │
        ▼
[7] Evaluate (7 queries, P@5/R@5/MRR)          → data/eval_results.json
```

---

## Setup

### Prerequisites

- **Python 3.10+**
- **PostgreSQL 14+** with the **pgvector** extension

### Install pgvector

```bash
# Docker (recommended for quick setup)
docker run -d --name ragdb \
  -e POSTGRES_PASSWORD=change_me \
  -e POSTGRES_DB=ragdb \
  -p 5432:5432 \
  pgvector/pgvector:pg17

# Or install pgvector on an existing PostgreSQL:
# See https://github.com/pgvector/pgvector#installation
```

### Install Python Dependencies

```bash
# Create and activate virtual environment
python -m venv qubettera
# Windows:
qubettera\Scripts\activate
# Linux/macOS:
# source qubettera/bin/activate

pip install -r requirements.txt
```

### Configure Environment

```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

---

## Running the Pipeline

### Full Pipeline (recommended)

```bash
python src/run_pipeline.py
```

This runs all steps in sequence: spider → clean → chunk → embed → store.

### Skip Scraping (use existing data)

```bash
python src/run_pipeline.py --skip-scrape
```

### Individual Steps

```bash
python src/spider.py        # Step 1: Collect documents
python src/clean.py         # Step 2: Clean and filter
python src/chunk.py         # Step 3: Chunk documents
python src/embed.py         # Step 4: Generate embeddings
python src/store.py         # Step 5: Store in PostgreSQL
```

### Run Retrieval

```bash
python src/retrieve.py "What are the advantages of Mixture of Experts?"
python src/retrieve.py "GRPO vs PPO" --top-k 10
python src/retrieve.py "sliding window attention" --no-rerank
python src/retrieve.py "Mamba SSM" --json
```

### Run Evaluation

```bash
python src/evaluate.py
# or
python src/run_pipeline.py --eval-only
```

---

## Design Decisions

### Data Collection Strategy

**Tool:** Scrapling `SiteToMarkdownSpider` — converts web pages to clean Markdown during crawl, eliminating the need for a separate HTML-to-text step.

**Sources:** 40+ seed URLs from arXiv (paper abstracts), HuggingFace Blog (explainer posts), and Lilian Weng's blog (in-depth survey posts). Links are followed only if they match on-topic URL patterns.

**Deduplication:** arXiv publishes multiple versions of the same paper (v1, v2, …). The spider's `deny` rules skip versioned URLs, and the cleaner deduplicates any remaining versions by keeping only the versionless/latest.

### Cleaning Strategy

- **arXiv boilerplate removal:** Strips navigation chrome, submission history, download links, and footer metadata via regex.
- **Relevance filtering:** Two-tier keyword matching (strong + weak keywords). A document must match ≥1 strong keyword AND ≥2 total keywords to be kept. This prevents off-topic papers that happen to mention "attention" in passing.
- **Provenance:** Each cleaned document preserves its source URL, title, relevance score, and collection timestamp.

### Chunking Strategy

**Method:** Structure-aware chunking (Markdown header split → recursive character split).

**Why:** Our documents are arXiv abstracts and blog posts with real heading structure. Splitting on headers first keeps each debate-relevant argument together as one semantic unit (e.g., an entire subsection on "GRPO vs PPO"), rather than slicing mid-argument at a fixed character count.

**Parameters:**
- Chunk size: 800 characters (~150–200 tokens)
- Chunk overlap: 100 characters
- Min chunk length: 40 characters (drops lone headers)

**Trade-off:** Larger chunks (1500 chars) preserve more context but reduce retrieval precision. 800/100 favors precision, which matters more for debate/evidence-citation than summarization.

### Embedding Model

```
Embedding model:    all-MiniLM-L6-v2
Vector dimensionality: 384
Reason for selection:
  - Local, free, no API key/cost/rate limits
  - Strong general-purpose semantic similarity (~80MB)
  - Runs on CPU quickly — no GPU dependency for reproducibility
  - Trade-off: a larger model (all-mpnet-base-v2 at 768-dim, or
    OpenAI text-embedding-3-small at 1536-dim) would likely give
    slightly better quality at higher cost/latency
```

### Database Configuration

**PostgreSQL + pgvector** with two index types:
- **IVFFlat index** (cosine distance) for approximate nearest-neighbor vector search
- **GIN index** on a generated `tsvector` column for full-text keyword search

The schema stores: chunk text, embedding vector, source URL, title, section headers (JSONB), document/chunk indices, character length, and embedding model name.

### Retrieval Strategy

**Hybrid Search + Cross-Encoder Reranking:**

1. **Vector search:** Cosine similarity via pgvector finds semantically similar chunks
2. **Keyword search:** PostgreSQL `tsvector`/`tsquery` full-text search finds exact term matches (BM25-style)
3. **Reciprocal Rank Fusion (RRF):** Merges both ranked lists — a chunk ranked highly by either method surfaces to the top; a chunk ranked by both gets an even stronger boost. `score = Σ 1/(k + rank)` with k=60.
4. **Cross-encoder reranking:** The top RRF candidates are re-scored by `cross-encoder/ms-marco-MiniLM-L-6-v2`, which sees query and chunk together for more accurate relevance estimation.

**Why hybrid:** Vector search catches conceptual similarity ("models that route tokens to experts" → MoE), while keyword search catches exact terms ("GRPO", "Mamba") that embeddings can miss for rare domain acronyms.

**Why reranker:** The cross-encoder sees query+chunk jointly rather than independently, detecting fine-grained relevance at ~100ms extra latency for 20 candidates.

### Evaluation Methodology

- **7 test queries** covering all 6 debate topics
- **Expected relevant sources** defined per query (arXiv paper IDs and blog URLs)
- **Metrics:** Precision@5, Recall@5, Mean Reciprocal Rank (MRR)
- **Comparison:** Hybrid+reranker vs. hybrid-only to quantify reranker value
- Automated interpretation/recommendation based on metric differences

---

## Retrieval Interface (Week 2 Handoff)

```
Input:
    Natural-language query (str)

Output:
    List of dicts, each containing:
      - rank (int): 1-based position
      - text (str): chunk text
      - url (str): source URL
      - title (str): document title
      - headers (dict): section headers
      - similarity (float): cosine similarity
      - rrf_score (float): RRF fusion score
      - rerank_score (float): cross-encoder score (if reranked)

Access:
    Python function: from src.retrieve import retrieve
    CLI: python src/retrieve.py "<query>"

Example:
    >>> from src.retrieve import retrieve
    >>> results = retrieve("What is Mixture of Experts?", top_k=5)
    >>> results[0]["text"]
    "Switch Transformers use a simplified MoE routing strategy..."
    >>> results[0]["url"]
    "https://arxiv.org/abs/2101.03961"
    >>> results[0]["rerank_score"]
    8.234
```

---

## Known Limitations

1. **arXiv abstracts only:** The spider collects abstract pages, not full paper PDFs. This limits the depth of information available for each paper.
2. **Embedding model size:** all-MiniLM-L6-v2 is a small model. Domain-specific or larger models would likely improve retrieval quality.
3. **Keyword search sensitivity:** PostgreSQL's `plainto_tsquery` uses English stemming, which may not handle ML-specific terms ideally (e.g., "pre-training" vs "pretraining").
4. **Static knowledge base:** The pipeline is batch-oriented. New papers require re-running the spider.
5. **Evaluation scope:** 7 queries give directional signal but not statistical significance. Production evaluation would need 50+ queries.

---

## Repository Structure

```
.
├── README.md               # This file
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
│
├── data/                   # Generated data (not in git)
│   ├── raw_docs.jsonl      # Spider output
│   ├── clean_docs.jsonl    # Cleaned + filtered
│   ├── chunks.jsonl        # Chunked documents
│   ├── chunks_with_embeddings.jsonl
│   ├── eval_results.json   # Evaluation output
│   └── raw_markdown/       # Individual page markdown files
│
├── docs/
│   └── design_decisions.md # Detailed design rationale
│
└── src/
    ├── spider.py           # Step 1: Data collection
    ├── clean.py            # Step 2: Cleaning + filtering
    ├── chunk.py            # Step 3: Chunking
    ├── embed.py            # Step 4: Embedding generation
    ├── store.py            # Step 5: PostgreSQL storage
    ├── retrieve.py         # Step 6: Hybrid retrieval + reranking
    ├── evaluate.py         # Step 7: Quantitative evaluation
    └── run_pipeline.py     # Pipeline orchestrator
```

---

## Reviewer Reproduction

```bash
# 1. Install dependencies
python -m venv qubettera
qubettera\Scripts\activate        # Windows
pip install -r requirements.txt

# 2. Start PostgreSQL (Docker)
docker run -d --name ragdb \
  -e POSTGRES_PASSWORD=change_me \
  -e POSTGRES_DB=ragdb \
  -p 5432:5432 \
  pgvector/pgvector:pg17

# 3. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 4. Run the full pipeline
python src/run_pipeline.py

# 5. Run retrieval
python src/retrieve.py "What are the advantages of MoE?"

# 6. Run evaluation
python src/evaluate.py
```
