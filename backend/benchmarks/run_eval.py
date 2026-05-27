#!/usr/bin/env python3
"""Run the JobMatch research benchmark suite and write JSON/CSV reports."""
from __future__ import annotations

import argparse
from pathlib import Path

from config import Settings

from benchmarks.framework import BenchmarkFramework, print_summary_table, write_report


def main() -> None:
    settings = Settings()
    parser = argparse.ArgumentParser(
        description="Evaluate JobMatch retrieval strategies on eval_pairs.json (offline only)."
    )
    parser.add_argument("--eval-path", default=str(settings.data_dir / "eval_pairs.json"))
    parser.add_argument("--data-dir", default=str(settings.data_dir))
    parser.add_argument("--top-k", type=int, default=5, help="Cutoff K for P@K, R@K, nDCG@K")
    parser.add_argument(
        "--semantic-weight",
        type=float,
        default=0.7,
        help="Semantic weight for multimodal weighted blend strategy",
    )
    parser.add_argument(
        "--out-dir",
        default=str(settings.repo_root / "backend" / "reports"),
        help="Directory for JSON and CSV reports",
    )
    parser.add_argument(
        "--prefix",
        default="benchmark",
        help="Filename prefix for report artifacts",
    )
    args = parser.parse_args()

    framework = BenchmarkFramework(
        settings=settings,
        eval_path=Path(args.eval_path),
        data_dir=Path(args.data_dir),
        top_k=args.top_k,
        semantic_weight=args.semantic_weight,
    )
    report = framework.run()
    print_summary_table(report)
    paths = write_report(report, Path(args.out_dir), prefix=args.prefix)
    print("\nWrote:")
    for name, path in paths.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
