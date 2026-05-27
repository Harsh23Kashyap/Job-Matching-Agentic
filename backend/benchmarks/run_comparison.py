#!/usr/bin/env python3
"""Compare lexical baselines vs embedding strategies — table-ready CSV output."""
from __future__ import annotations

import argparse
from pathlib import Path

from config import Settings

from benchmarks.comparison import ComparisonBenchmark, print_comparison_table, write_comparison_report


def main() -> None:
    settings = Settings()
    parser = argparse.ArgumentParser(
        description=(
            "Offline lexical vs embedding benchmark. "
            "Outputs method, metric, top_k, score, latency_ms — does not affect production APIs."
        )
    )
    parser.add_argument("--eval-path", default=str(settings.data_dir / "eval_pairs.json"))
    parser.add_argument("--data-dir", default=str(settings.data_dir))
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--semantic-weight", type=float, default=0.7)
    parser.add_argument(
        "--out-dir",
        default=str(settings.repo_root / "backend" / "reports"),
    )
    parser.add_argument("--prefix", default="comparison")
    parser.add_argument(
        "--embedding-only",
        action="store_true",
        help="Skip lexical baselines (embedding strategies only)",
    )
    args = parser.parse_args()

    bench = ComparisonBenchmark(
        settings=settings,
        eval_path=Path(args.eval_path),
        data_dir=Path(args.data_dir),
        top_k=args.top_k,
        semantic_weight=args.semantic_weight,
        include_lexical_baselines=not args.embedding_only,
    )
    report = bench.run()
    print_comparison_table(report)
    paths = write_comparison_report(report, Path(args.out_dir), prefix=args.prefix)
    print("\nWrote:")
    for name, path in paths.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
