#!/usr/bin/env python3
"""Generate paper-ready Markdown/CSV/LaTeX tables from benchmark reports."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from config import Settings

from benchmarks.paper_tables.generators import generate_all_paper_tables


def main() -> None:
    settings = Settings()
    parser = argparse.ArgumentParser(
        description="Generate copy-pasteable paper tables from backend/reports/."
    )
    parser.add_argument(
        "--reports-dir",
        default=str(settings.repo_root / "backend" / "reports"),
    )
    parser.add_argument(
        "--out-dir",
        default=str(settings.repo_root / "docs" / "research" / "evaluation" / "paper_tables"),
    )
    parser.add_argument("--data-dir", default=str(settings.data_dir))
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    result = generate_all_paper_tables(
        reports_dir=Path(args.reports_dir),
        out_dir=Path(args.out_dir),
        data_dir=Path(args.data_dir),
        top_k=args.top_k,
    )

    print("\nPaper tables generated:\n")
    for key, info in result["manifest"]["tables"].items():
        if info.get("error"):
            print(f"  [SKIP] {key}: {info['error']}")
        else:
            print(f"  {info['stem']} ({info['rows']} rows) → {info['label']}")

    print(f"\nOutput: {result['out_dir']}")
    print(f"Index: {result['out_dir'] / 'README.md'}")


if __name__ == "__main__":
    main()
