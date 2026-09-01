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
[1] Query-driven collection (arXiv + blogs)     → data/raw_docs.jsonl
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
[6] Retrieve (vector + text rank + reranker)     → ranked results
        │
        ▼
[7] Evaluate (30 source-qrel queries + ablation) → data/eval_results.json
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
# For development and tests:
pip install -r requirements-dev.txt
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

This runs all steps in sequence: collect → clean → chunk → embed → atomic store.

### Skip Scraping (use existing data)

```bash
python src/run_pipeline.py --skip-collection
```

### Individual Steps

```bash
python src/collection.py    # Step 1: Collect documents
# Fast benchmark-source backfill, preserving the current corpus:
python src/collection.py --curated-only
# Broader paginated discovery while preserving existing raw documents:
python src/collection.py --max-arxiv-per-topic 100
python src/clean.py         # Step 2: Clean and filter
python src/chunk.py         # Step 3: Chunk documents
python src/embed.py         # Step 4: Generate embeddings
python src/store.py         # Step 5: Store in PostgreSQL
```

### Run Retrieval

```bash
python src/retrieve.py "What are the advantages of Mixture of Experts?"
python src/retrieve.py "GRPO vs PPO" --top-k 10
python src/retrieve.py "sliding window attention" --rerank
python src/retrieve.py "Mamba SSM" --json
```

### Run Evaluation

```bash
python src/evaluate.py
# Optional strict mode: stop when any judged source is missing:
python src/evaluate.py --require-complete-corpus
# or
python src/run_pipeline.py --eval-only
```

---

## Design Decisions

### Data Collection Strategy

**Tool:** A shared curated seed set plus paginated arXiv discovery, Scrapling fetchers, and Markdown conversion. Citation-neighbor expansion uses Semantic Scholar, while configured blog indexes provide non-paper sources.

**Sources:** Curated seeds provide deterministic coverage and topic queries expand the corpus without importing held-out evaluation query text. Existing raw documents are merged by canonical URL, with broken or incomplete records automatically replaced by higher-quality fetches. arXiv collection attempts full ar5iv HTML, then PDF extraction, then an abstract-only fallback. Blog sources are configured in `src/collection.py`.

**Deduplication:** arXiv URLs are canonicalized to versionless IDs, and the cleaner deduplicates remaining arXiv versions and normalized non-arXiv URLs.

### Cleaning Strategy

- **arXiv boilerplate removal:** Strips navigation chrome, submission history, download links, and footer metadata via regex.
- **Relevance filtering:** Two-tier keyword matching (strong + weak keywords). A document must match ≥1 strong keyword AND ≥2 total keywords to be kept. This prevents off-topic papers that happen to mention "attention" in passing.
- **Provenance:** Each cleaned document preserves its source URL, title, relevance score, and collection timestamp.

### Chunking Strategy

**Method:** Structure-aware chunking (Markdown header split → recursive character split).

**Why:** Full papers and blog posts contain useful heading structure. Splitting on headers first keeps each debate-relevant argument together before bounded recursive splitting.

**Embedding context:** Each chunk keeps its original evidence text for display and adds deterministic `embedding_text` containing the document title, section path, and chunk text. The contextual form is used for vector embedding and reranking.

**Parameters:**

- Chunk size: 1200 characters
- Chunk overlap: 300 characters
- Min chunk length: 200 characters (drops near-empty fragments)

**Trade-off:** The 1200/300 configuration preserves more local evidence and reduces fragmentation, but long contextual chunks can be truncated by MiniLM's configured input window. Treat further increases as an evaluated tuning change.

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

The schema stores: original chunk text, contextual embedding text, embedding vector, source URL, title, section headers (JSONB), document/chunk indices, character length, and embedding identity.

The index is capped at 100 IVFFlat lists and the current retrieval configuration probes all 100. This favors reproducible, effectively exhaustive search for the 15k-chunk corpus; probe count can be reduced later if scale makes latency more important than exact regression stability.

### Retrieval Strategy

**Hybrid Search with Optional Cross-Encoder Reranking:**

1. **Vector search:** Cosine similarity via pgvector finds semantically similar chunks
2. **Text search:** PostgreSQL `tsvector`/`tsquery` with `ts_rank_cd` finds exact/stemmed term matches
3. **Reciprocal Rank Fusion (RRF):** Merges both ranked lists — a chunk ranked highly by either method surfaces to the top; a chunk ranked by both gets an even stronger boost. `score = Σ 1/(k + rank)` with k=30.
4. **Optional cross-encoder reranking:** With `--rerank`, the top RRF candidates are re-scored by `cross-encoder/ms-marco-MiniLM-L-6-v2`, which sees the query and contextual chunk text together.

**Why hybrid:** Vector search catches conceptual similarity ("models that route tokens to experts" → MoE), while keyword search catches exact terms ("GRPO", "Mamba") that embeddings can miss for rare domain acronyms.

**Why reranking is opt-in:** The cross-encoder sees the query, document title, section path, and chunk jointly. On the current 30-query evaluation, it reduces Hit@5 from `0.6000` to `0.4667`, so hybrid-only retrieval is the default until a better reranker or training strategy is validated.

### Evaluation Methodology

- **30 test queries** covering all 6 debate topics
- **Fixed exact-source qrels**; title/text hints never create relevance
- **Coverage reporting:** incomplete corpora produce clearly marked diagnostic results by default; `--require-complete-corpus` enables the strict coverage gate
- **Metrics:** Hit@5, Precision@5, source Recall@5, MRR, and fixed-qrel nDCG@5
- **Paired comparison:** hybrid retrieval and hybrid+reranker, including per-query ranked evidence and latency
- **Run manifest:** qrels version, timestamp, git revision, corpus/model versions, scores, and relevance decisions
- **Current corpus coverage:** 24/24 judged sources and 30/30 fully covered queries

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
      - text_rank_score (float | null): PostgreSQL full-text relevance
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
    >>> reranked = retrieve("What is Mixture of Experts?", top_k=5, rerank=True)
    >>> reranked[0]["rerank_score"]
    8.234
```

---

## Known Limitations

1. **Fallback quality:** ar5iv is preferred, but PDF and abstract-only fallbacks have less reliable structure.
2. **Embedding model size:** all-MiniLM-L6-v2 is small; a domain-specific or larger model may improve retrieval quality.
3. **Text-search sensitivity:** `plainto_tsquery` and English stemming do not handle every ML acronym or spelling variant equally.
4. **Batch updates:** new sources require rerunning collection and downstream stages.
5. **Evaluation scope:** 30 queries are useful for regression checks but remain too small for broad statistical claims.
6. **Static blog discovery:** some JavaScript-heavy sites can expose incomplete article indexes without a browser-rendered collector.
7. **Context-window truncation:** some 1200-character contextual chunks exceed MiniLM's configured 256-token window; a token-aware chunking experiment is the next quality-tuning step.

---

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest tests -q -p no:cacheprovider
python -m compileall -q src tests
```

The suite covers collection fallbacks and quality-aware merging, contextual chunk identity, resumable embedding metadata, artifact validation, exact-source evaluation metrics, retrieval guards, and direct script execution.

---

## Repository Structure

```
.
├── README.md               # This file
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
├── requirements.txt        # Runtime dependencies
├── requirements-dev.txt    # Runtime + test dependencies
│
├── data/                   # Generated data (not in git)
│   ├── raw_docs.jsonl      # Collection output
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
    ├── collection.py       # Step 1: query-driven data collection
    ├── database.py         # Shared PostgreSQL configuration
    ├── jsonl.py            # Strict atomic JSONL helpers
    ├── source_seeds.py     # Shared deterministic source seeds
    ├── spider.py           # Legacy/static collection helper
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

# 5. Verify and evaluate
python -m pytest tests -q -p no:cacheprovider
python src/evaluate.py --require-complete-corpus

# 6. Run retrieval
python src/retrieve.py "What are the advantages of MoE?"
```
