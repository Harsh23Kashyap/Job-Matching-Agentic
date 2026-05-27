#!/usr/bin/env python3
"""Run synthetic fairness & bias audit (offline research only)."""
from __future__ import annotations

import argparse
from pathlib import Path

from config import Settings

from benchmarks.fairness_audit import (
    DEFAULT_SCORE_DELTA_THRESHOLD,
    DEFAULT_TOP_K,
    FairnessAudit,
    print_fairness_audit_summary,
    write_fairness_audit_report,
)


def main() -> None:
    settings = Settings()
    parser = argparse.ArgumentParser(
        description="Fairness audit with synthetic controlled profiles (offline only)."
    )
    parser.add_argument(
        "--profiles-path",
        default=str(settings.data_dir / "fairness_audit_profiles.json"),
    )
    parser.add_argument("--jobs-path", default=str(settings.jobs_path))
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument(
        "--score-delta-threshold",
        type=float,
        default=DEFAULT_SCORE_DELTA_THRESHOLD,
    )
    parser.add_argument("--strategy", default="composite", choices=["composite"])
    parser.add_argument(
        "--out-dir",
        default=str(settings.repo_root / "backend" / "reports"),
    )
    parser.add_argument("--prefix", default="fairness_audit")
    args = parser.parse_args()

    audit = FairnessAudit(
        settings=settings,
        profiles_path=Path(args.profiles_path),
        jobs_path=Path(args.jobs_path),
        top_k=args.top_k,
        score_delta_threshold=args.score_delta_threshold,
        strategy=args.strategy,
    )
    report = audit.run()
    print_fairness_audit_summary(report)
    paths = write_fairness_audit_report(report, Path(args.out_dir), prefix=args.prefix)
    print("\nWrote:")
    for name, path in paths.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
