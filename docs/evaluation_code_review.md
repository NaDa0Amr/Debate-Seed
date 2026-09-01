# Repository Readiness Review

Reviewed: 2026-09-01

## Outcome

The repository is ready as a reproducible local RAG/retrieval prototype. The
pipeline completes with strict corpus coverage, publishes its PostgreSQL index
atomically, validates artifact/model identity, resumes embedding safely, and
has a passing regression suite.

This is not yet a production service: it has no HTTP API, authentication,
background scheduler, monitoring, or deployment manifest. Those are product
deployment concerns rather than correctness gaps in the current CLI pipeline.

## Verified baseline

| Check | Result |
|---|---:|
| Clean documents | 297 |
| Indexed chunks | 15,162 |
| Indexed sources | 297 |
| Judged-source coverage | 24/24 |
| Fully covered evaluation queries | 30/30 |
| Test suite | 38 passed |

Latest strict evaluation:

| Mode | Hit@5 | MRR | nDCG@5 | Precision@5 | Source recall@5 |
|---|---:|---:|---:|---:|---:|
| Hybrid | 0.6000 | 0.3522 | 0.2808 | 0.1400 | 0.3500 |
| Hybrid + reranker | 0.4667 | 0.2872 | 0.2386 | 0.1200 | 0.3000 |

Hybrid-only retrieval is therefore the runtime default. Reranking remains an
explicit option and continues to be evaluated as an ablation.

## Readiness improvements completed

- Collection rejects ar5iv conversion shells and falls back to PDF extraction.
- Quality-aware merging replaces broken persisted records while preserving
  healthy existing documents.
- Curated sources cover every fixed qrel; the stale Hugging Face Mamba URL was
  replaced with the maintained Falcon Mamba article.
- Cleaning output and chunk output use atomic JSONL replacement.
- Chunking fails clearly when no usable chunks are produced.
- Embedding cache reuse requires model, revision, dimension, preprocessing,
  pipeline, and content identity.
- Reused vectors receive current chunk metadata, preventing stale document
  indexes and timestamps from leaking through the cache.
- Storage rejects missing fields, duplicate IDs/hashes, incompatible artifact
  identities, dimension mismatches, and non-finite vectors.
- Database configuration is shared and reports missing environment variables
  clearly.
- Retrieval validates queries, candidate limits, query-vector dimensions, and
  reranker output length.
- Evaluation uses exact normalized source qrels, fixed-IDCG nDCG, source-level
  deduplication, coverage gates, run manifests, and paired reranker comparison.
- Console output is safe on legacy Windows encodings.
- Direct execution (`python src/<stage>.py`) is covered by tests.

## Remaining engineering risks

1. Approximately 60% of current contextual chunks exceed MiniLM's configured
   256-token window. A controlled token-aware chunking experiment is the most
   promising next retrieval-quality change.
2. The 30-query evaluation is suitable for regressions but too small for broad
   statistical claims or domain-general conclusions.
3. Static discovery has limited coverage for JavaScript-rendered blog indexes.
4. `plainto_tsquery` and English stemming remain imperfect for rare acronyms.
5. Collection depends on external services and can be slow or rate-limited;
   existing artifacts allow downstream stages to run independently.

## Reproduction

```powershell
python -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
# Edit PostgreSQL credentials in .env

python src\run_pipeline.py
python src\evaluate.py --require-complete-corpus
python -m pytest tests -q -p no:cacheprovider
python -m compileall -q src tests
```

For a rebuild that preserves the current raw collection:

```powershell
python src\run_pipeline.py --skip-collection
```
