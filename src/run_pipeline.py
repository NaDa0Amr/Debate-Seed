"""
Pipeline orchestrator that runs all stages in sequence.

Usage:
    python src/run_pipeline.py               # full pipeline (scrape -> store)
    python src/run_pipeline.py --skip-collection  # skip collection, use existing raw data
    python src/run_pipeline.py --eval-only    # only run evaluation (assumes DB is populated)

Each step calls the corresponding module's run() function.
"""

import argparse
import sys
import time
from contextlib import contextmanager
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@contextmanager
def timed(label: str):
    """Report stage duration without misreporting failed stages as successful."""
    print(f"\n{'=' * 60}")
    print(f"  > {label}")
    print(f"{'=' * 60}")
    started = time.perf_counter()
    try:
        yield
    except Exception:
        elapsed = time.perf_counter() - started
        print(f"\n  [FAILED] {label} stopped after {elapsed:.1f}s")
        raise
    else:
        elapsed = time.perf_counter() - started
        print(f"\n  [OK] {label} completed in {elapsed:.1f}s")


def main():
    parser = argparse.ArgumentParser(description="Run the RAG knowledge pipeline.")
    parser.add_argument(
        "--skip-scrape",
        "--skip-collection",
        dest="skip_scrape",
        action="store_true",
        help="Skip collection (use existing raw data)",
    )
    parser.add_argument(
        "--eval-only",
        action="store_true",
        help="Only run evaluation (assumes DB is populated)",
    )
    eval_coverage_group = parser.add_mutually_exclusive_group()
    eval_coverage_group.add_argument(
        "--require-complete-eval",
        action="store_true",
        help="Stop eval-only runs when judged sources are absent from the corpus",
    )
    eval_coverage_group.add_argument(
        "--allow-incomplete-eval",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()

    # Ensure data directory exists.
    Path("data").mkdir(exist_ok=True)

    if args.eval_only:
        with timed("Step 7: Evaluation"):
            from src.evaluate import run_evaluation
            run_evaluation(allow_incomplete_corpus=not args.require_complete_eval)
        return

    if not args.skip_scrape:
        with timed("Step 1: Query-driven data collection"):
            from src.collection import run as collect_run
            docs = collect_run()
            print(f"Collected {len(docs)} pages -> data/raw_docs.jsonl")

    with timed("Step 2: Cleaning & filtering"):
        from src.clean import run as clean_run
        clean_run()

    with timed("Step 3: Chunking"):
        from src.chunk import run as chunk_run
        chunk_run()

    with timed("Step 4: Embedding generation"):
        from src.embed import run as embed_run
        embed_run()

    with timed("Step 5: Store in PostgreSQL"):
        from src.store import run as store_run
        store_run()

    print(f"\n{'='*60}")
    print("  [OK] Pipeline complete! Knowledge base is ready.")
    print(f"{'='*60}")
    print("\nNext steps:")
    print("  python src/retrieve.py \"What are the advantages of MoE?\"")
    print("  python src/evaluate.py")


if __name__ == "__main__":
    main()
