#!/usr/bin/env python3
"""Run paired bootstrap significance tests on benchmark per-query results."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from config import Settings

from benchmarks.ablation import AblationStudy
from benchmarks.comparison import ComparisonBenchmark
from benchmarks.framework import BenchmarkFramework
from benchmarks.significance import (
    DEFAULT_N_RESAMPLES,
    DEFAULT_SEED,
    print_significance_summary,
    run_significance_analysis,
    write_significance_report,
)

SOURCE_DEFAULT_BASELINE = {
    "benchmark": "semantic_cosine",
    "comparison": "semantic_cosine",
    "ablation": "semantic_only",
}


def _load_per_query_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    for row in rows:
        if "predicted_ids" in row and row["predicted_ids"]:
            row["predicted_ids"] = row["predicted_ids"].split("|")
        for field in ("precision_at_k", "recall_at_k", "mrr", "ndcg_at_k", "map"):
            if field in row and row[field] not in ("", None):
                row[field] = float(row[field])
        if "top_k" in row and row["top_k"] not in ("", None):
            row["top_k"] = int(float(row["top_k"]))
    return rows


def _load_per_query_json(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    return payload.get("per_query") or payload.get("per_query_rows") or []


def _collect_per_query(source: str, settings: Settings, eval_path: Path, data_dir: Path, top_k: int):
    if source == "benchmark":
        fw = BenchmarkFramework(settings=settings, eval_path=eval_path, data_dir=data_dir, top_k=top_k)
        report = fw.run()
        return report.per_query, report.meta
    if source == "comparison":
        cmp = ComparisonBenchmark(settings=settings, eval_path=eval_path, data_dir=data_dir, top_k=top_k)
        report = cmp.run()
        return report.per_query, report.meta
    if source == "ablation":
        study = AblationStudy(settings=settings, eval_path=eval_path, data_dir=data_dir, top_k=top_k)
        report = study.run()
        per_query = [
            {
                "method_key": row["variant_key"],
                "method": row["variant"],
                "query_id": row["query_id"],
                "precision_at_k": row["precision_at_k"],
                "recall_at_k": row["recall_at_k"],
                "mrr": row["mrr"],
                "ndcg_at_k": row["ndcg_at_k"],
                "map": row["map"],
                "predicted_ids": row.get("predicted_ids", []),
                "top_k": top_k,
            }
            for row in report.per_query
        ]
        return per_query, report.meta
    raise ValueError(f"Unknown source: {source}")


def main() -> None:
    settings = Settings()
    parser = argparse.ArgumentParser(
        description="Paired bootstrap significance (nDCG@K, MRR) vs baseline."
    )
    parser.add_argument("--eval-path", default=str(settings.data_dir / "eval_pairs.json"))
    parser.add_argument("--data-dir", default=str(settings.data_dir))
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument(
        "--baseline",
        default=None,
        help="method_key / variant_key (default depends on --source)",
    )
    parser.add_argument(
        "--source",
        default="benchmark",
        choices=["benchmark", "comparison", "ablation", "file"],
    )
    parser.add_argument("--per-query-csv", help="Existing per-query CSV (--source file)")
    parser.add_argument("--per-query-json", help="Existing per-query JSON (--source file)")
    parser.add_argument("--method-key-field", default="method_key")
    parser.add_argument("--method-label-field", default="method")
    parser.add_argument("--n-resamples", type=int, default=DEFAULT_N_RESAMPLES)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument(
        "--out-dir",
        default=str(settings.repo_root / "backend" / "reports"),
    )
    parser.add_argument("--prefix", default="significance")
    args = parser.parse_args()

    eval_path = Path(args.eval_path)
    data_dir = Path(args.data_dir)
    source = args.source

    if args.per_query_csv or args.per_query_json:
        source = "file"
        per_query = (
            _load_per_query_csv(Path(args.per_query_csv))
            if args.per_query_csv
            else _load_per_query_json(Path(args.per_query_json))
        )
        meta = {"task": "resume_to_jobs", "top_k": args.top_k}
    else:
        per_query, meta = _collect_per_query(source, settings, eval_path, data_dir, args.top_k)

    baseline = args.baseline or SOURCE_DEFAULT_BASELINE.get(source, "semantic_cosine")
    if source == "ablation" and args.baseline is None:
        args.method_key_field = "method_key"
        args.method_label_field = "method"

    report = run_significance_analysis(
        per_query,
        baseline_key=baseline,
        n_resamples=args.n_resamples,
        seed=args.seed,
        method_key_field=args.method_key_field,
        method_label_field=args.method_label_field,
        top_k=meta.get("top_k", args.top_k),
        task=meta.get("task", "resume_to_jobs"),
    )
    report.meta["eval_path"] = str(eval_path)
    report.meta["data_source"] = source

    print_significance_summary(report)
    paths = write_significance_report(report, Path(args.out_dir), prefix=args.prefix)
    print("\nWrote:")
    for name, path in paths.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
