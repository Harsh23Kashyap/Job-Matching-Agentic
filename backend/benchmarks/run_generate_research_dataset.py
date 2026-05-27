#!/usr/bin/env python3
"""CLI: generate synthetic research evaluation corpus under data/research/."""
from __future__ import annotations

import argparse
from pathlib import Path

from config import Settings

from benchmarks.synthetic_dataset.generator import SyntheticDatasetConfig, generate_dataset, write_dataset


def main() -> None:
    settings = Settings()
    parser = argparse.ArgumentParser(
        description="Generate synthetic research dataset (candidates, jobs, labeled pairs)."
    )
    parser.add_argument("--candidates", type=int, default=100)
    parser.add_argument("--jobs", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--out-dir",
        default=str(settings.data_dir / "research"),
    )
    parser.add_argument(
        "--sparse-labels",
        action="store_true",
        help="Label subset per candidate instead of full 100×50 matrix",
    )
    args = parser.parse_args()

    config = SyntheticDatasetConfig(
        num_candidates=args.candidates,
        num_jobs=args.jobs,
        seed=args.seed,
        full_pair_matrix=not args.sparse_labels,
    )
    dataset = generate_dataset(config)
    paths = write_dataset(Path(args.out_dir), dataset)

    manifest = dataset["manifest"]
    print(
        f"\nSynthetic research dataset: {manifest['candidates']} candidates, "
        f"{manifest['jobs']} jobs, {manifest['labeled_pairs']} labeled pairs (seed={manifest['seed']})\n"
    )
    print("Relevance distribution:", manifest["relevance_distribution"])
    print("\nRole coverage (candidates):", manifest["role_distribution_candidates"])
    print("Role coverage (jobs):", manifest["role_distribution_jobs"])
    print("\nWrote:")
    for name, path in paths.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
