"""
Step 7: Quantitative evaluation of retrieval quality (§11).

Creates 7 representative test queries covering all 6 debate topics, defines
expected relevant sources for each, and computes per-query and aggregate
retrieval metrics.

Metrics computed:
  - Precision@5:  What fraction of the top-5 results are relevant?
  - Recall@5:     What fraction of expected relevant sources appear in top-5?
  - MRR:          1/rank of the first relevant result (Mean Reciprocal Rank).

The evaluation runs retrieval in 3 modes to compare effectiveness:
  1. Hybrid (vector + BM25 via RRF) — no reranking
  2. Hybrid + cross-encoder reranking
  3. Vector-only (pure cosine similarity, no BM25, no reranking)

This allows us to quantify whether hybrid search and reranking actually
improve retrieval quality over simpler approaches.

Run:
    python src/evaluate.py
Output:
    Formatted table to stdout
    data/eval_results.json (machine-readable)
"""

import json
import sys
from pathlib import Path

# ── Test Queries + Expected Relevant Sources ──
# Each entry: (query, set of substrings that a relevant URL should contain).
# A retrieved chunk is "relevant" if its URL contains ANY of the expected
# substrings.  This is intentionally generous — we care that the system
# finds the *right papers/posts*, not a specific paragraph.

EVAL_QUERIES = [
    {
        "id": "q1_moe_vs_dense",
        "query": "What are the advantages of Mixture of Experts over dense models?",
        "topic": "MoE vs Dense",
        "expected_sources": [
            "2101.03961",   # Switch Transformer
            "2401.04088",   # Mixtral
            "1701.06538",   # Shazeer MoE
            "2112.06905",   # GLaM
            "2209.07858",   # ST-MoE
            "blog/moe",     # HF MoE blog
            "blog/mixtral", # HF Mixtral blog
        ],
    },
    {
        "id": "q2_linear_attention",
        "query": "How does linear attention compare to standard softmax attention in terms of quality and efficiency?",
        "topic": "Normal vs Linear Attention vs SSM",
        "expected_sources": [
            "2009.14794",   # Performer
            "2006.03555",   # Linformer
            "1706.03762",   # Attention Is All You Need
            "2205.14135",   # FlashAttention
            "2307.08691",   # FlashAttention-2
        ],
    },
    {
        "id": "q3_sliding_window",
        "query": "What is sliding window attention and how does it reduce computational cost for long sequences?",
        "topic": "Sliding Window vs Full Global Attention",
        "expected_sources": [
            "2004.05150",   # Longformer
            "2310.06825",   # Mistral 7B
            "1904.10509",   # Sparse Transformer
            "2006.16668",   # BigBird
            "2305.14314",   # LongNet
        ],
    },
    {
        "id": "q4_hybrid_arch",
        "query": "What are the benefits and drawbacks of hybrid architectures that combine attention layers with state space models?",
        "topic": "Hybrid Architectures",
        "expected_sources": [
            "2312.00752",   # Mamba
            "2305.13245",   # RWKV
            "2402.19427",   # Jamba
            "2406.07887",   # Samba
            "2405.04434",   # Mamba-2
            "blog/mamba",   # HF Mamba blog
        ],
    },
    {
        "id": "q5_reasoning_pretraining",
        "query": "Should reasoning-style objectives be introduced during pretraining rather than only during fine-tuning?",
        "topic": "Pretraining vs Reasoning-Oriented Training",
        "expected_sources": [
            "2210.11416",   # Flan
            "2305.14705",   # Orca
            "2309.12284",   # phi-1.5
            "2501.12948",   # DeepSeek-R1
            "2203.02155",   # InstructGPT
        ],
    },
    {
        "id": "q6_ppo_vs_grpo",
        "query": "How does GRPO differ from PPO for reinforcement learning fine-tuning of language models?",
        "topic": "PPO vs GRPO",
        "expected_sources": [
            "2402.03300",   # DeepSeekMath (GRPO)
            "1707.06347",   # PPO
            "2203.02155",   # InstructGPT
            "2209.14375",   # RLHF Anthropic
            "blog/rlhf",    # HF RLHF blog
            "blog/deep-rl-ppo",
        ],
    },
    {
        "id": "q7_ssm_long_seq",
        "query": "How do state space models like Mamba handle long sequences more efficiently than transformers?",
        "topic": "SSM / Mamba",
        "expected_sources": [
            "2312.00752",   # Mamba
            "2405.04434",   # Mamba-2
            "2004.05150",   # Longformer
            "blog/mamba",   # HF Mamba blog
        ],
    },
]


def is_relevant(result: dict, expected_sources: list[str]) -> bool:
    """Check if a retrieved chunk's URL matches any expected source."""
    url = (result.get("url") or "").lower()
    return any(src.lower() in url for src in expected_sources)


def compute_metrics(results: list[dict], expected_sources: list[str], k: int = 5) -> dict:
    """Compute Precision@k, Recall@k, and MRR for one query."""
    top_k = results[:k]

    relevant_found = [is_relevant(r, expected_sources) for r in top_k]
    n_relevant_in_k = sum(relevant_found)

    # Precision@k: fraction of top-k that are relevant
    precision_at_k = n_relevant_in_k / k if k > 0 else 0.0

    # Recall@k: fraction of expected sources found in top-k
    # A source is "found" if any chunk in top-k matches it.
    sources_found = set()
    for r in top_k:
        url = (r.get("url") or "").lower()
        for src in expected_sources:
            if src.lower() in url:
                sources_found.add(src)
    recall_at_k = len(sources_found) / len(expected_sources) if expected_sources else 0.0

    # MRR: reciprocal of the rank of the first relevant result
    mrr = 0.0
    for i, rel in enumerate(relevant_found):
        if rel:
            mrr = 1.0 / (i + 1)
            break

    return {
        "precision_at_k": round(precision_at_k, 4),
        "recall_at_k": round(recall_at_k, 4),
        "mrr": round(mrr, 4),
        "relevant_in_top_k": n_relevant_in_k,
        "sources_found": sorted(sources_found),
        "sources_expected": len(expected_sources),
    }


def run_evaluation(k: int = 5):
    """Run the full evaluation suite in 3 retrieval modes."""
    # Import here to avoid circular deps and allow standalone testing.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src.retrieve import retrieve

    modes = [
        ("hybrid_reranked", {"rerank": True}),
        ("hybrid_only", {"rerank": False}),
    ]

    all_results = {}

    for mode_name, retrieve_kwargs in modes:
        print(f"\n{'='*70}")
        print(f"  Evaluation mode: {mode_name}")
        print(f"{'='*70}")

        mode_results = []
        for eq in EVAL_QUERIES:
            results = retrieve(eq["query"], top_k=k, **retrieve_kwargs)
            metrics = compute_metrics(results, eq["expected_sources"], k=k)

            mode_results.append({
                "query_id": eq["id"],
                "query": eq["query"],
                "topic": eq["topic"],
                "metrics": metrics,
                "top_results": [
                    {
                        "rank": r.get("rank"),
                        "url": r.get("url"),
                        "relevant": is_relevant(r, eq["expected_sources"]),
                        "text_preview": r.get("text", "")[:150],
                    }
                    for r in results[:k]
                ],
            })

            print(f"\n  Query: {eq['query'][:70]}...")
            print(f"  Topic: {eq['topic']}")
            print(f"  P@{k}={metrics['precision_at_k']:.2f}  "
                  f"R@{k}={metrics['recall_at_k']:.2f}  "
                  f"MRR={metrics['mrr']:.2f}  "
                  f"Sources found: {len(metrics['sources_found'])}/{metrics['sources_expected']}")

        # Aggregate metrics
        avg_precision = sum(r["metrics"]["precision_at_k"] for r in mode_results) / len(mode_results)
        avg_recall = sum(r["metrics"]["recall_at_k"] for r in mode_results) / len(mode_results)
        avg_mrr = sum(r["metrics"]["mrr"] for r in mode_results) / len(mode_results)

        aggregate = {
            "avg_precision_at_k": round(avg_precision, 4),
            "avg_recall_at_k": round(avg_recall, 4),
            "avg_mrr": round(avg_mrr, 4),
        }

        all_results[mode_name] = {
            "queries": mode_results,
            "aggregate": aggregate,
        }

        print(f"\n  -- Aggregate ({mode_name}) --")
        print(f"  Avg P@{k}: {avg_precision:.4f}")
        print(f"  Avg R@{k}: {avg_recall:.4f}")
        print(f"  Avg MRR:   {avg_mrr:.4f}")

    # -- Comparison summary --
    print(f"\n{'='*70}")
    print("  COMPARISON SUMMARY")
    print(f"{'='*70}")
    print(f"  {'Mode':<25} {'Avg P@5':>8} {'Avg R@5':>8} {'Avg MRR':>8}")
    print(f"  {'-'*25} {'-'*8} {'-'*8} {'-'*8}")
    for mode_name, data in all_results.items():
        agg = data["aggregate"]
        print(f"  {mode_name:<25} {agg['avg_precision_at_k']:>8.4f} "
              f"{agg['avg_recall_at_k']:>8.4f} {agg['avg_mrr']:>8.4f}")

    # -- Interpretation --
    hr = all_results.get("hybrid_reranked", {}).get("aggregate", {})
    ho = all_results.get("hybrid_only", {}).get("aggregate", {})

    print(f"\n  -- Interpretation --")
    if hr and ho:
        p_diff = hr["avg_precision_at_k"] - ho["avg_precision_at_k"]
        mrr_diff = hr["avg_mrr"] - ho["avg_mrr"]
        if p_diff > 0.01 or mrr_diff > 0.01:
            print(f"  Reranking IMPROVED precision by {p_diff:+.4f} and MRR by {mrr_diff:+.4f}.")
            print("  Recommendation: Use hybrid + reranker for production.")
        elif p_diff < -0.01 or mrr_diff < -0.01:
            print(f"  Reranking HURT precision by {p_diff:+.4f} and MRR by {mrr_diff:+.4f}.")
            print("  Recommendation: Stick with hybrid search without reranking.")
        else:
            print("  Reranking had negligible impact on metrics.")
            print("  Recommendation: Use hybrid without reranker to save latency.")

    # Save results
    output_path = Path("data/eval_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print(f"\n  Results saved to {output_path}")

    return all_results


if __name__ == "__main__":
    run_evaluation()
