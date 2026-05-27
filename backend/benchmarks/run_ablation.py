#!/usr/bin/env python3
"""Run composite matching ablation study and write CSV/JSON/Markdown reports."""
from __future__ import annotations

import argparse
from pathlib import Path

from config import Settings

from benchmarks.ablation import AblationStudy, print_ablation_summary, write_ablation_report


def main() -> None:
    settings = Settings()
    parser = argparse.ArgumentParser(
        description="Ablation study: single components, partial composites, full composite, RRF."
    )
    parser.add_argument("--eval-path", default=str(settings.data_dir / "eval_pairs.json"))
    parser.add_argument("--data-dir", default=str(settings.data_dir))
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--skills-mode", default="jaccard", choices=["jaccard", "embedding"])
    parser.add_argument(
        "--out-dir",
        default=str(settings.repo_root / "backend" / "reports"),
    )
    parser.add_argument("--prefix", default="ablation")
    args = parser.parse_args()

    study = AblationStudy(
        settings=settings,
        eval_path=Path(args.eval_path),
        data_dir=Path(args.data_dir),
        top_k=args.top_k,
        skills_mode=args.skills_mode,
    )
    report = study.run()
    print_ablation_summary(report)
    paths = write_ablation_report(report, Path(args.out_dir), prefix=args.prefix)
    print("\nWrote:")
    for name, path in paths.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
