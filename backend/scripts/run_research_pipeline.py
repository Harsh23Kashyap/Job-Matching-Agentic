#!/usr/bin/env python3
"""Run the full offline research evaluation pipeline."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from config import Settings  # noqa: E402

from benchmarks.research_pipeline import PipelineConfig, make_run_dir, run_research_pipeline  # noqa: E402
from benchmarks.significance import DEFAULT_N_RESAMPLES, DEFAULT_SEED  # noqa: E402


def main() -> None:
    settings = Settings()
    parser = argparse.ArgumentParser(
        description="Full offline research pipeline — all studies into one timestamped run folder."
    )
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--data-dir", default=str(settings.data_dir))
    parser.add_argument("--eval-path", default=None, help="Defaults to <data-dir>/eval_pairs.json")
    parser.add_argument(
        "--profiles-path",
        default=None,
        help="Defaults to <data-dir>/fairness_audit_profiles.json",
    )
    parser.add_argument(
        "--reports-root",
        default=str(settings.repo_root / "backend" / "reports"),
        help="Parent directory for research_run_<timestamp>/ folders",
    )
    parser.add_argument("--run-id", default=None, help="Override folder name (default: research_run_<timestamp>)")
    parser.add_argument("--n-resamples", type=int, default=DEFAULT_N_RESAMPLES)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument(
        "--skip-cross-encoder",
        action="store_true",
        help="Skip cross-encoder reranking even if enabled in settings/env",
    )
    parser.add_argument(
        "--enable-cross-encoder",
        action="store_true",
        help="Force cross-encoder reranking step",
    )
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    eval_path = Path(args.eval_path or data_dir / "eval_pairs.json")
    profiles_path = Path(args.profiles_path or data_dir / "fairness_audit_profiles.json")
    run_dir = make_run_dir(Path(args.reports_root), args.run_id)

    config = PipelineConfig(
        settings=settings,
        run_dir=run_dir,
        data_dir=data_dir,
        eval_path=eval_path,
        profiles_path=profiles_path,
        top_k=args.top_k,
        n_resamples=args.n_resamples,
        seed=args.seed,
        skip_cross_encoder=args.skip_cross_encoder,
        enable_cross_encoder=True if args.enable_cross_encoder else None,
    )

    print(f"\nJobMatch research pipeline → {run_dir}\n")
    result = run_research_pipeline(config)

    print("\nPipeline complete:")
    print(f"  Run ID: {result.run_id}")
    print(f"  Output: {result.run_dir}")
    print(f"  Manifest: {result.manifest_path}")
    print(f"  Valid: {result.valid}\n")

    for step in result.steps:
        mark = {"ok": "OK", "skipped": "SKIP", "failed": "FAIL"}.get(step.status, step.status.upper())
        err = f" — {step.error}" if step.error else ""
        print(f"  [{mark}] {step.name} ({step.duration_sec:.1f}s){err}")

    if not result.valid:
        sys.exit(1)


if __name__ == "__main__":
    main()
