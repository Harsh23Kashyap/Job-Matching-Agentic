#!/usr/bin/env python3
"""Report bi-encoder vs two-stage cross-encoder quality, latency, and rank changes."""
from __future__ import annotations

import argparse
from pathlib import Path

from config import Settings

from benchmarks.cross_encoder_report import print_report, run_report, write_report


def main() -> None:
    settings = Settings()
    parser = argparse.ArgumentParser(description="Cross-encoder two-stage retrieval report")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--strategy", default="composite")
    parser.add_argument("--out-dir", default=str(settings.repo_root / "backend" / "reports"))
    parser.add_argument("--prefix", default="cross_encoder")
    args = parser.parse_args()

    report = run_report(settings=settings, top_k=args.top_k, strategy=args.strategy)
    print_report(report)
    paths = write_report(report, Path(args.out_dir), prefix=args.prefix)
    print("\nWrote:")
    for name, path in paths.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
