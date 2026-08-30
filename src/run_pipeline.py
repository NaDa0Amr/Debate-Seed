"""
Pipeline orchestrator — runs all steps in sequence.

Usage:
    python src/run_pipeline.py               # full pipeline (scrape -> store)
    python src/run_pipeline.py --skip-scrape  # skip spider step, use existing raw data
    python src/run_pipeline.py --eval-only    # only run evaluation (assumes DB is populated)

Each step calls the corresponding module's run() function.
"""

import argparse
import sys
import time
from pathlib import Path


def timed(label: str):
    """Context manager that prints how long a step took."""
    class Timer:
        def __enter__(self):
            print(f"\n{'='*60}")
            print(f"  > {label}")
            print(f"{'='*60}")
            self.start = time.time()
            return self
        def __exit__(self, *args):
            elapsed = time.time() - self.start
            print(f"\n  [OK] {label} completed in {elapsed:.1f}s")
    return Timer()

sys.path.append(str(Path(__file__).parent.parent))


def main():
    parser = argparse.ArgumentParser(description="Run the RAG knowledge pipeline.")
    parser.add_argument("--skip-scrape", action="store_true",
                        help="Skip the spider step (use existing raw data)")
    parser.add_argument("--eval-only", action="store_true",
                        help="Only run evaluation (assumes DB is populated)")
    args = parser.parse_args()

    # Ensure data directory exists.
    Path("data").mkdir(exist_ok=True)

    if args.eval_only:
        with timed("Step 7: Evaluation"):
            from src.evaluate import run_evaluation
            run_evaluation()
        return

    if not args.skip_scrape:
        with timed("Step 1: Data collection (spider)"):
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
