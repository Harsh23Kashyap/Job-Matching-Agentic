#!/usr/bin/env python3
"""Run full research benchmark suite and export to docs/research/evaluation/."""
from __future__ import annotations

import argparse
from pathlib import Path

from config import Settings

from benchmarks.research_export import export_research_bundle


def main() -> None:
    settings = Settings()
    parser = argparse.ArgumentParser(
        description="Run all benchmark studies and export paper-ready research bundle."
    )
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument(
        "--from-cache",
        action="store_true",
        help="Skip re-running benchmarks; export existing backend/reports/",
    )
    parser.add_argument("--skip-cross-encoder", action="store_true")
    parser.add_argument(
        "--reports-dir",
        default=str(settings.repo_root / "backend" / "reports"),
    )
    parser.add_argument(
        "--out-dir",
        default=str(settings.repo_root / "docs" / "research" / "evaluation"),
    )
    parser.add_argument("--run-id", default=None, help="Override run folder name")
    args = parser.parse_args()

    paths = export_research_bundle(
        settings=settings,
        reports_dir=Path(args.reports_dir),
        out_root=Path(args.out_dir),
        run_id=args.run_id,
        from_cache=args.from_cache,
        skip_cross_encoder=args.skip_cross_encoder,
        top_k=args.top_k,
    )

    print("\nResearch bundle exported:")
    for name, path in paths.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
