"""Source-level retrieval evaluation with fixed qrels and corpus coverage gates."""

from __future__ import annotations

import argparse
import json
import math
import random
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit

QRELS_VERSION = "source-qrels-v2"

# These are explicit source-level qrels. Relevance never depends on a keyword
# appearing in a returned title or chunk. Paper IDs were checked against their
# arXiv records when this version was created.
EVAL_JUDGMENTS = [
    {"query_id": "q01", "query": "mixture of experts routing advantages over dense feedforward", "relevant_sources": ["https://arxiv.org/abs/1701.06538", "https://arxiv.org/abs/2101.03961"]},
    {"query_id": "q02", "query": "linear attention vs softmax attention quality and efficiency", "relevant_sources": ["https://arxiv.org/abs/2006.03555", "https://arxiv.org/abs/2009.14794"]},
    {"query_id": "q03", "query": "state space models handle long sequences efficiently", "relevant_sources": ["https://arxiv.org/abs/2312.00752", "https://arxiv.org/abs/2405.21060"]},
    {"query_id": "q04", "query": "sliding window attention long context reduction", "relevant_sources": ["https://arxiv.org/abs/2004.05150", "https://arxiv.org/abs/2310.06825"]},
    {"query_id": "q05", "query": "hybrid architectures combine attention and state space models", "relevant_sources": ["https://arxiv.org/abs/2403.19887", "https://arxiv.org/abs/2406.07522"]},
    {"query_id": "q06", "query": "grpo differs from ppo for reinforcement learning fine tuning", "relevant_sources": ["https://arxiv.org/abs/2402.03300", "https://arxiv.org/abs/1707.06347"]},
    {"query_id": "q07", "query": "what are the benefits of flash attention for transformer efficiency", "relevant_sources": ["https://arxiv.org/abs/2205.14135", "https://arxiv.org/abs/2307.08691"]},
    {"query_id": "q08", "query": "instruction finetuning versus standard pretraining for reasoning", "relevant_sources": ["https://arxiv.org/abs/2210.11416", "https://arxiv.org/abs/2305.14705"]},
    {"query_id": "q09", "query": "sparse routing expert load balancing in moe", "relevant_sources": ["https://arxiv.org/abs/1701.06538", "https://arxiv.org/abs/2112.06905"]},
    {"query_id": "q10", "query": "retrieval augmented generation and reranking signal", "relevant_sources": ["https://arxiv.org/abs/2004.04906", "https://arxiv.org/abs/2104.08710"]},
    {"query_id": "q11", "query": "what is sparse attention and its role in long context modeling", "relevant_sources": ["https://arxiv.org/abs/1904.10509", "https://arxiv.org/abs/2006.16668"]},
    {"query_id": "q12", "query": "dilated attention and local receptive fields", "relevant_sources": ["https://arxiv.org/abs/2004.05150", "https://arxiv.org/abs/2307.02486"]},
    {"query_id": "q13", "query": "which architectures scale better with mixture of experts", "relevant_sources": ["https://arxiv.org/abs/1701.06538", "https://arxiv.org/abs/2201.05596"]},
    {"query_id": "q14", "query": "what are the tradeoffs between linear attention and softmax attention", "relevant_sources": ["https://arxiv.org/abs/2006.04768", "https://arxiv.org/abs/2006.03555"]},
    {"query_id": "q15", "query": "how do state space models compare with transformer blocks", "relevant_sources": ["https://arxiv.org/abs/2312.00752", "https://arxiv.org/abs/2405.21060"]},
    {"query_id": "q16", "query": "why is sliding window attention useful for local context", "relevant_sources": ["https://arxiv.org/abs/2004.05150", "https://arxiv.org/abs/2310.06825"]},
    {"query_id": "q17", "query": "what does hybrid attention plus state space mean", "relevant_sources": ["https://arxiv.org/abs/2403.19887", "https://arxiv.org/abs/2406.07522"]},
    {"query_id": "q18", "query": "reasoning-oriented instruction tuning versus standard pretraining", "relevant_sources": ["https://arxiv.org/abs/2210.11416", "https://arxiv.org/abs/2305.14705"]},
    {"query_id": "q19", "query": "ppo and grpo differences in training and reward optimization", "relevant_sources": ["https://arxiv.org/abs/1707.06347", "https://arxiv.org/abs/2402.03300"]},
    {"query_id": "q20", "query": "how does flash attention reduce memory overhead", "relevant_sources": ["https://arxiv.org/abs/2205.14135", "https://arxiv.org/abs/2307.08691"]},
    {"query_id": "q21", "query": "sparse attention in long context models and efficiency gains", "relevant_sources": ["https://arxiv.org/abs/1904.10509", "https://arxiv.org/abs/2006.16668"]},
    {"query_id": "q22", "query": "why do experts require load balancing", "relevant_sources": ["https://arxiv.org/abs/1701.06538", "https://arxiv.org/abs/2112.06905"]},
    {"query_id": "q23", "query": "what is retrieval augmented generation and reranking", "relevant_sources": ["https://arxiv.org/abs/2004.04906", "https://arxiv.org/abs/2104.08710"]},
    {"query_id": "q24", "query": "comparisons of transformer attention variants", "relevant_sources": ["https://arxiv.org/abs/2004.05150", "https://arxiv.org/abs/2006.03555"]},
    {"query_id": "q25", "query": "what makes mixture of experts efficient at scale", "relevant_sources": ["https://arxiv.org/abs/1701.06538", "https://arxiv.org/abs/2112.06905"]},
    {"query_id": "q26", "query": "state space models as alternatives to attention", "relevant_sources": ["https://arxiv.org/abs/2312.00752", "https://arxiv.org/abs/2405.21060"]},
    {"query_id": "q27", "query": "how do local and global attention differ", "relevant_sources": ["https://arxiv.org/abs/2004.05150", "https://arxiv.org/abs/2006.16668"]},
    {"query_id": "q28", "query": "hybrid architectures combining attention and state space recurrence", "relevant_sources": ["https://arxiv.org/abs/2403.19887", "https://arxiv.org/abs/2406.07522"]},
    {"query_id": "q29", "query": "fine tuning with reinforcement learning and policy optimization", "relevant_sources": ["https://arxiv.org/abs/1707.06347", "https://arxiv.org/abs/2402.03300"]},
    {"query_id": "q30", "query": "long context modeling with sparse and dilated attention", "relevant_sources": ["https://arxiv.org/abs/2004.05150", "https://arxiv.org/abs/2307.02486"]},
]


def _normalize_url(url: str | None) -> str:
    """Normalize source identity, including versioned arXiv URLs."""
    if not url:
        return ""
    parts = urlsplit(url.strip())
    host = parts.netloc.lower()
    path = unquote(parts.path).rstrip("/").lower()
    if host in {"arxiv.org", "www.arxiv.org"} and path.startswith("/abs/"):
        path = re.sub(r"v\d+$", "", path)
        host = "arxiv.org"
    return f"{host}{path}"


def _expected_urls(expected: dict) -> set[str]:
    sources = expected.get("relevant_sources", [])
    normalized = (_normalize_url(url) for url in sources)
    return {url for url in normalized if url}


def _result_matches(result: dict, expected: dict) -> bool:
    """Use exact normalized source qrels; text is never a relevance label."""
    return _normalize_url(result.get("url")) in _expected_urls(expected)


def _relevance_labels(results: list[dict], expected: dict, k: int) -> list[int]:
    """Return binary source labels, counting a relevant source at most once."""
    expected_urls = _expected_urls(expected)
    seen_relevant: set[str] = set()
    labels = []
    for result in results[:k]:
        source = _normalize_url(result.get("url"))
        relevant = source in expected_urls and source not in seen_relevant
        labels.append(1 if relevant else 0)
        if relevant:
            seen_relevant.add(source)
    return labels


def _source_recall(result_list: list[dict], expected: dict) -> float:
    expected_urls = _expected_urls(expected)
    if not expected_urls:
        return 0.0
    found = {
        _normalize_url(result.get("url"))
        for result in result_list
        if _normalize_url(result.get("url")) in expected_urls
    }
    return len(found) / len(expected_urls)


def _dcg(rel_list: list[int], k: int) -> float:
    return sum((2**rel - 1) / math.log2(index + 2) for index, rel in enumerate(rel_list[:k]))


def _ndcg_at_k(results: list[dict], expected: dict, k: int = 5) -> float:
    labels = _relevance_labels(results, expected, k)
    ideal_relevant = min(k, len(_expected_urls(expected)))
    idcg = _dcg([1] * ideal_relevant, k)
    return 0.0 if idcg == 0 else _dcg(labels, k) / idcg


def compute_metrics(results: list[dict], expected: dict, k: int = 5) -> dict:
    if k <= 0:
        raise ValueError("k must be > 0")
    hits = _relevance_labels(results, expected, k)
    first_hit = next((1.0 / (index + 1) for index, hit in enumerate(hits) if hit), 0.0)
    return {
        "hit_at_k": round(1.0 if any(hits) else 0.0, 4),
        "precision_at_k": round(sum(hits) / k, 4),
        "mrr": round(first_hit, 4),
        "ndcg_at_k": round(_ndcg_at_k(results, expected, k), 4),
        "source_recall": round(_source_recall(results[:k], expected), 4),
        "relevant_in_top_k": sum(hits),
        "returned_results": min(len(results), k),
    }


def audit_corpus_coverage(judgments: list[dict], corpus_sources: list[str] | set[str]) -> dict:
    if not judgments:
        return {
            "unique_qrel_sources": 0,
            "available_qrel_sources": 0,
            "missing_qrel_sources": [],
            "fully_covered_queries": 0,
            "mean_source_recall_ceiling": 0.0,
            "queries": [],
        }
    available = {_normalize_url(url) for url in corpus_sources if _normalize_url(url)}
    unique_qrels = set().union(*(_expected_urls(item) for item in judgments))
    per_query = []
    for judgment in judgments:
        expected = _expected_urls(judgment)
        present = sorted(expected & available)
        missing = sorted(expected - available)
        per_query.append(
            {
                "query_id": judgment["query_id"],
                "expected_sources": sorted(expected),
                "available_sources": present,
                "missing_sources": missing,
                "fully_covered": not missing,
                "max_source_recall": round(len(present) / len(expected), 4) if expected else 0.0,
            }
        )
    return {
        "unique_qrel_sources": len(unique_qrels),
        "available_qrel_sources": len(unique_qrels & available),
        "missing_qrel_sources": sorted(unique_qrels - available),
        "fully_covered_queries": sum(item["fully_covered"] for item in per_query),
        "mean_source_recall_ceiling": round(
            sum(item["max_source_recall"] for item in per_query) / len(per_query), 4
        ),
        "queries": per_query,
    }


def _aggregate(query_rows: list[dict], mode: str) -> dict:
    if not query_rows:
        return {"query_count": 0}
    metric_names = ("hit_at_k", "precision_at_k", "mrr", "ndcg_at_k", "source_recall")
    aggregate = {"query_count": len(query_rows)}
    for metric in metric_names:
        aggregate[f"avg_{metric}"] = round(
            sum(row["modes"][mode]["metrics"][metric] for row in query_rows) / len(query_rows),
            4,
        )
    aggregate["avg_latency_ms"] = round(
        sum(row["modes"][mode]["latency_ms"] for row in query_rows) / len(query_rows), 2
    )
    return aggregate


def _paired_bootstrap_interval(
    query_rows: list[dict], metric: str, samples: int = 2000, seed: int = 20260901
) -> list[float]:
    """Deterministic percentile interval for the paired reranker-minus-base mean."""
    if not query_rows:
        return []
    if samples <= 0:
        raise ValueError("samples must be > 0")
    deltas = [
        row["modes"]["hybrid_rerank"]["metrics"].get(metric, row["modes"]["hybrid_rerank"].get(metric))
        - row["modes"]["hybrid"]["metrics"].get(metric, row["modes"]["hybrid"].get(metric))
        for row in query_rows
    ]
    generator = random.Random(seed)
    size = len(deltas)
    means = sorted(
        sum(deltas[generator.randrange(size)] for _ in range(size)) / size
        for _ in range(samples)
    )
    lower = means[int(0.025 * (samples - 1))]
    upper = means[int(0.975 * (samples - 1))]
    return [round(lower, 4), round(upper, 4)]


def _auditable_results(results: list[dict], expected: dict) -> list[dict]:
    fields = (
        "rank", "chunk_id", "url", "title", "headers", "text", "similarity",
        "text_rank_score", "rrf_score", "rerank_score",
    )
    return [
        {**{field: result.get(field) for field in fields}, "relevant": _result_matches(result, expected)}
        for result in results
    ]


def _git_revision() -> str | None:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"], check=True, capture_output=True,
            text=True, timeout=5,
        )
        return completed.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def _write_json_atomic(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    temporary.replace(path)


def run_evaluation(k: int = 5, allow_incomplete_corpus: bool = True) -> dict:
    if not isinstance(k, int) or isinstance(k, bool):
        raise TypeError("k must be an integer")
    if not 1 <= k <= 50:
        raise ValueError("k must be between 1 and 50")
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src.retrieve import (
        CANDIDATE_POOL,
        FINAL_SOURCE_LIMIT,
        IVFFLAT_PROBES,
        RERANK_SOURCE_LIMIT,
        RRF_K,
        get_index_manifest,
        retrieve,
    )
    from src.settings import (
        EMBEDDING_MODEL, EMBEDDING_MODEL_REVISION, RERANKER_MODEL,
        RERANKER_MODEL_REVISION,
    )

    index_manifest = get_index_manifest()
    source_urls = index_manifest.pop("source_urls")
    coverage = audit_corpus_coverage(EVAL_JUDGMENTS, source_urls)
    corpus_complete = not coverage["missing_qrel_sources"]
    if coverage["missing_qrel_sources"] and not allow_incomplete_corpus:
        raise RuntimeError(
            "Evaluation corpus is incomplete: "
            f"{len(coverage['missing_qrel_sources'])} of {coverage['unique_qrel_sources']} "
            "judged sources are missing. Rebuild the corpus or pass "
            "--allow-incomplete-corpus to record an end-to-end diagnostic run."
        )
    if not corpus_complete:
        print(
            "WARNING: Evaluation corpus is incomplete; results will be marked as "
            f"diagnostic ({coverage['available_qrel_sources']}/"
            f"{coverage['unique_qrel_sources']} judged sources available)."
        )

    coverage_by_query = {item["query_id"]: item for item in coverage["queries"]}
    per_query = []
    modes = (("hybrid", False), ("hybrid_rerank", True))
    for judgment in EVAL_JUDGMENTS:
        mode_results = {}
        for mode, use_reranker in modes:
            started = time.perf_counter()
            results = retrieve(judgment["query"], top_k=k, rerank=use_reranker)
            latency_ms = (time.perf_counter() - started) * 1000
            mode_results[mode] = {
                "metrics": compute_metrics(results, judgment, k=k),
                "latency_ms": round(latency_ms, 2),
                "results": _auditable_results(results, judgment),
            }
        per_query.append(
            {
                "query_id": judgment["query_id"],
                "query": judgment["query"],
                "relevant_sources": judgment["relevant_sources"],
                "corpus_coverage": coverage_by_query[judgment["query_id"]],
                "modes": mode_results,
            }
        )

    fully_covered = [row for row in per_query if row["corpus_coverage"]["fully_covered"]]
    aggregate = {mode: _aggregate(per_query, mode) for mode, _ in modes}
    covered_aggregate = {mode: _aggregate(fully_covered, mode) for mode, _ in modes}
    comparison_metrics = (
        "avg_hit_at_k", "avg_precision_at_k", "avg_mrr", "avg_ndcg_at_k",
        "avg_source_recall", "avg_latency_ms",
    )
    comparison = {
        name: round(aggregate["hybrid_rerank"][name] - aggregate["hybrid"][name], 4)
        for name in comparison_metrics
    }
    raw_metric_for_aggregate = {
        "avg_hit_at_k": "hit_at_k",
        "avg_precision_at_k": "precision_at_k",
        "avg_mrr": "mrr",
        "avg_ndcg_at_k": "ndcg_at_k",
        "avg_source_recall": "source_recall",
        "avg_latency_ms": "latency_ms",
    }
    comparison_with_intervals = {
        name: {
            "mean_delta": comparison[name],
            "paired_bootstrap_95_ci": _paired_bootstrap_interval(
                per_query, raw_metric_for_aggregate[name], seed=20260901 + index
            ),
        }
        for index, name in enumerate(comparison_metrics)
    }

    result = {
        "run": {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "git_revision": _git_revision(),
            "qrels_version": QRELS_VERSION,
            "k": k,
            "allow_incomplete_corpus": allow_incomplete_corpus,
            "evaluation_status": (
                "complete" if corpus_complete else "diagnostic_incomplete_corpus"
            ),
            "embedding_model": EMBEDDING_MODEL,
            "embedding_model_revision": EMBEDDING_MODEL_REVISION,
            "reranker_model": RERANKER_MODEL,
            "reranker_model_revision": RERANKER_MODEL_REVISION,
            "retrieval": {
                "candidate_pool": CANDIDATE_POOL,
                "rrf_k": RRF_K,
                "ivfflat_probes": IVFFLAT_PROBES,
                "rerank_source_limit": RERANK_SOURCE_LIMIT,
                "final_source_limit": FINAL_SOURCE_LIMIT,
            },
        },
        "corpus": {
            **index_manifest,
            "coverage": {key: value for key, value in coverage.items() if key != "queries"},
        },
        "queries": per_query,
        "aggregate": aggregate,
        "fully_covered_query_aggregate": covered_aggregate,
        "reranker_delta": comparison,
        "reranker_comparison": comparison_with_intervals,
    }
    _write_json_atomic(Path("data/eval_results.json"), result)
    print("Evaluation results (exact source qrels)")
    print(json.dumps({"aggregate": aggregate, "reranker_delta": comparison}, indent=2, sort_keys=True))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate retrieval against fixed source qrels.")
    parser.add_argument("--top-k", type=int, default=5, help="Evaluation cutoff (default: 5)")
    coverage_group = parser.add_mutually_exclusive_group()
    coverage_group.add_argument(
        "--require-complete-corpus",
        action="store_true",
        help="Stop instead of producing diagnostic results when judged sources are missing",
    )
    coverage_group.add_argument(
        "--allow-incomplete-corpus",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()
    run_evaluation(
        k=args.top_k,
        allow_incomplete_corpus=not args.require_complete_corpus,
    )


if __name__ == "__main__":
    main()
