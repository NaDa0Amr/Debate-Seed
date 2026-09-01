# Design decisions

## 1. Collection

The primary entry point is `src.collection`, not the legacy static spider. The spider's corrected curated seeds are shared through `src.source_seeds`, while ten topic-level arXiv queries and citation expansion broaden the six debate areas. The benchmark sources are part of the frozen corpus foundation; held-out evaluation query text is not used for discovery or ranking.

Each arXiv candidate is canonicalized to a versionless `/abs/<id>` URL and fetched in this order:

1. Full ar5iv HTML converted to Markdown
2. PDF text extracted with PyMuPDF
3. Abstract-only fallback

ArXiv API results are paginated when the per-topic limit exceeds the page size. One citation/reference hop through Semantic Scholar improves coverage of foundational papers. Existing raw documents are preserved by default and new documents are merged by canonical URL. Blog sources and their path rules live in `BLOG_SOURCE_CONFIG`; collection reports preserved, attempted, and newly written counts plus per-domain fetch methods to `data/collection_report.json`.

Trade-offs:

- Full papers improve evidence depth but produce far more chunks than abstracts.
- PDF fallback is robust but loses heading structure.
- Static blog indexes are reproducible and inexpensive, but JavaScript-heavy sites can remain incomplete.

## 2. Cleaning and filtering

The cleaner removes common navigation, footer, bibliography, LaTeX, caption, page-number, and whitespace noise. It deduplicates arXiv versions and normalized URLs before relevance filtering.

Relevance terms are normalized to lowercase alphanumeric tokens, so punctuation variants such as `Mixture-of-Experts` match `mixture of experts`. A title with one strong topic phrase is sufficient; body-only content needs at least two strong topic signals in the title plus first 12,000 characters. This reduces false positives caused by citations deep in full papers.

This filter is a collection safety net, not an evaluation label. Retrieval relevance is determined only by versioned qrels.

## 3. Chunking

Chunking first splits Markdown on `#`, `##`, and `###` headings and then recursively splits long sections.

| Parameter | Value | Rationale |
|---|---:|---|
| Chunk size | 1200 characters | Preserves more local evidence while keeping retrieval units bounded |
| Overlap | 300 characters | Preserves context at boundaries |
| Minimum length | 200 characters | Removes near-empty fragments and boilerplate slices |

Chunks carry URL/title provenance, heading metadata, document/chunk indexes, collection timestamp, pipeline version, and preprocessing version. Original text remains the cited evidence, while `embedding_text` prefixes the document title and section path for embedding and reranking. The source URL plus contextual text form the SHA-256 cache identity, so provenance changes force vector regeneration and identical passages from distinct sources remain independently retrievable.

## 4. Embeddings and cache identity

The default model is `all-MiniLM-L6-v2` with 384 dimensions. Model name, requested revision, dimensionality, pipeline version, and preprocessing version are configured centrally in `src.settings`.

The embedding artifact is resumable, but a cache row is reusable only when all of these agree:

- Content hash
- Embedding model
- Embedding model revision
- Embedding dimension
- Preprocessing version
- Pipeline version

Changing a model or preprocessing version therefore forces the affected vectors to be regenerated. Every output vector is converted to plain Python floats and dimension-checked before it is written.

## 5. PostgreSQL and pgvector

The `chunks` table stores chunk provenance, complete embedding identity, a pgvector column, and a generated English `tsvector`.

Publishing is atomic:

1. Validate the chunk/embedding manifests and their identity.
2. Stream embeddings into `chunks_staging` in bounded batches.
3. Build IVFFlat and GIN indexes and run `ANALYZE`.
4. Verify row counts and that model identities are uniform.
5. Swap the staging table into the live `chunks` name in the same transaction.

Any error rolls back the transaction, preserving the previous working `chunks` table.

## 6. Retrieval

Retrieval has four stages:

1. Cosine vector search through pgvector
2. PostgreSQL full-text matching scored with `ts_rank_cd`
3. Reciprocal Rank Fusion (RRF) over both ranked lists
4. Opt-in `cross-encoder/ms-marco-MiniLM-L-6-v2` reranking

`ts_rank_cd` is intentionally called a text-rank score, not BM25. RRF avoids attempting to calibrate cosine and text-rank scores onto one scale. Storage caps IVFFlat at 100 lists and retrieval currently probes all 100, making candidate search stable across index rebuilds at this corpus scale.

Before searching, retrieval verifies that the table contains exactly the configured embedding model, revision, preprocessing version, and pipeline version. This prevents query vectors from being compared with incompatible stored vectors.

Vector embedding and cross-encoder reranking use deterministic contextual text containing the document title, section path, and original chunk. Returned evidence remains the original chunk text. With the current 1200-character chunks, MiniLM can truncate some contextual inputs, so chunk size remains an evaluation-controlled trade-off.

Candidate selection allows at most two chunks per normalized source before reranking, and final output allows one. Normalization collapses arXiv versions and trailing slashes. This avoids one long paper consuming the entire top-k and makes source-level evaluation well defined.

Hybrid-only retrieval is the runtime default because the completed 30-query evaluation currently scores higher than the reranked mode (Hit@5 `0.6000` versus `0.4667`). Reranking remains available explicitly for experiments and is always measured during evaluation.

## 7. Evaluation

The 30-query evaluation uses explicit exact-source qrels (`source-qrels-v2`). Text or title hints never create relevance.

Before retrieval, a corpus audit reports:

- Unique judged sources present and missing
- Per-query available/missing sources
- Fully covered query count
- Maximum attainable source-recall ceiling

Strict evaluation stops if any judged source is missing. `--allow-incomplete-corpus` is reserved for a clearly marked end-to-end diagnostic; it does not turn missing sources into retrieval failures silently.

Metrics are computed at source level:

| Metric | Meaning |
|---|---|
| Hit@k | At least one judged source appears in the top k |
| Precision@k | Unique judged sources in the top k divided by k |
| Source recall@k | Fraction of fixed judged sources retrieved |
| MRR | Reciprocal rank of the first judged source |
| nDCG@k | Ranking gain normalized against the fixed qrels |

A duplicate source can count only once. IDCG is based on the number of fixed relevant sources, never on observed system hits.

Every run evaluates hybrid-only and hybrid-plus-reranker modes. The output records ranked chunks, scores, relevance decisions, per-query latency, corpus/model versions, qrels version, timestamp, git revision, aggregate results over all queries, and a separate aggregate over fully covered queries.

## 8. Reproducibility policy

Generated artifacts are versioned by their embedded metadata, not just filenames. A valid comparison requires the same qrels version, corpus/pipeline version, embedding model/revision, preprocessing version, candidate-pool settings, `k`, and reranker model/revision. Any difference belongs in the evaluation run manifest.
