#!/usr/bin/env python3
"""Run explainability evaluation on match explanations (offline research)."""
from __future__ import annotations

import argparse
from pathlib import Path

from config import Settings

from benchmarks.explainability_eval import ExplainabilityEval, print_explainability_summary, write_explainability_report


def main() -> None:
    settings = Settings()
    parser = argparse.ArgumentParser(description="Evaluate match explanation quality (offline only).")
    parser.add_argument("--data-dir", default=str(settings.data_dir))
    parser.add_argument(
        "--profiles-path",
        default=str(settings.data_dir / "fairness_audit_profiles.json"),
        help="Synthetic pairs for consistency checks",
    )
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument(
        "--modes",
        default="rules,template",
        help="Comma-separated: rules, template",
    )
    parser.add_argument("--consistency-min-jaccard", type=float, default=0.5)
    parser.add_argument(
        "--out-dir",
        default=str(settings.repo_root / "backend" / "reports"),
    )
    parser.add_argument("--prefix", default="explainability")
    args = parser.parse_args()

    eval_ = ExplainabilityEval(
        settings=settings,
        data_dir=Path(args.data_dir),
        profiles_path=Path(args.profiles_path),
        top_k=args.top_k,
        explain_modes=[m.strip() for m in args.modes.split(",") if m.strip()],
        consistency_min_jaccard=args.consistency_min_jaccard,
    )
    report = eval_.run()
    print_explainability_summary(report)
    paths = write_explainability_report(report, Path(args.out_dir), prefix=args.prefix)
    print("\nWrote:")
    for name, path in paths.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
