"""Research-grade benchmark runner for JobMatch offline evaluation."""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import Settings

from benchmarks.eval_data import cv_to_snapshot, job_to_snapshot, load_eval_labels
from benchmarks.metrics import eval_rankings
from benchmarks.strategies import BenchmarkStrategy, build_strategies


SUMMARY_CSV_FIELDS = [
    "method_key",
    "method",
    "description",
    "precision_at_k",
    "recall_at_k",
    "mrr",
    "ndcg_at_k",
    "map",
    "queries",
    "top_k",
]

PER_QUERY_CSV_FIELDS = [
    "method_key",
    "method",
    "query_id",
    "precision_at_k",
    "recall_at_k",
    "mrr",
    "ndcg_at_k",
    "map",
    "top_k",
    "predicted_ids",
]


@dataclass
class BenchmarkReport:
    meta: dict[str, Any]
    summary: list[dict[str, Any]]
    per_query: list[dict[str, Any]]


class BenchmarkFramework:
    """Exhaustive resume→jobs evaluation over eval_pairs.json."""

    def __init__(
        self,
        *,
        settings: Settings | None = None,
        eval_path: Path | None = None,
        data_dir: Path | None = None,
        top_k: int = 5,
        semantic_weight: float = 0.7,
    ) -> None:
        self.settings = settings or Settings()
        self.eval_path = Path(eval_path or self.settings.data_dir / "eval_pairs.json")
        self.data_dir = Path(data_dir or self.settings.data_dir)
        self.top_k = top_k
        self.semantic_weight = semantic_weight

    def load_corpus(self) -> tuple[dict, dict, list[dict], list[dict]]:
        resumes = json.loads((self.data_dir / "cvs.json").read_text(encoding="utf-8"))
        jobs = json.loads((self.data_dir / "jobs.json").read_text(encoding="utf-8"))
        eval_map = load_eval_labels(self.eval_path)
        return eval_map, {r["id"]: r for r in resumes}, {j["id"]: j for j in jobs}, resumes, jobs

    def build_snapshots(self, resumes: list[dict], jobs: list[dict], model_name: str):
        job_snaps = [job_to_snapshot(j, model_name) for j in jobs]
        cv_snaps = {r["id"]: cv_to_snapshot(r, model_name) for r in resumes}
        return cv_snaps, job_snaps

    def run(self, strategies: list[BenchmarkStrategy] | None = None) -> BenchmarkReport:
        eval_map, _resumes_by_id, _jobs_by_id, resumes, jobs = self.load_corpus()
        model_name = self.settings.embedding_model
        cv_snaps, job_snaps = self.build_snapshots(resumes, jobs, model_name)
        strategies = strategies or build_strategies(
            job_snaps,
            model_name=model_name,
            semantic_weight=self.semantic_weight,
            rrf_k=self.settings.rrf_k,
        )

        summary_rows: list[dict[str, Any]] = []
        per_query_rows: list[dict[str, Any]] = []

        for strategy in strategies:
            ranked = {
                qid: strategy.rank_fn(cv_snaps[qid])
                for qid in eval_map
                if qid in cv_snaps
            }
            per_query, agg = eval_rankings(eval_map, ranked, self.top_k)
            summary_rows.append(
                {
                    "method_key": strategy.key,
                    "method": strategy.label,
                    "description": strategy.description,
                    "precision_at_k": agg["avg_precision_at_k"],
                    "recall_at_k": agg["avg_recall_at_k"],
                    "mrr": agg["avg_mrr"],
                    "ndcg_at_k": agg["avg_ndcg_at_k"],
                    "map": agg["avg_map"],
                    "queries": agg["queries"],
                    "top_k": self.top_k,
                }
            )
            for row in per_query:
                per_query_rows.append(
                    {
                        "method_key": strategy.key,
                        "method": strategy.label,
                        "query_id": row["query_id"],
                        "precision_at_k": row["precision_at_k"],
                        "recall_at_k": row["recall_at_k"],
                        "mrr": row["mrr"],
                        "ndcg_at_k": row["ndcg_at_k"],
                        "map": row["map"],
                        "top_k": self.top_k,
                        "predicted_ids": row["predicted_ids"],
                    }
                )

        meta = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "task": "resume_to_jobs",
            "eval_path": str(self.eval_path),
            "data_dir": str(self.data_dir),
            "corpus": {"candidates": len(resumes), "jobs": len(jobs), "labeled_queries": len(eval_map)},
            "top_k": self.top_k,
            "embedding_model": model_name,
            "semantic_weight_multimodal": self.semantic_weight,
            "rrf_k": self.settings.rrf_k,
            "metrics": ["precision_at_k", "recall_at_k", "mrr", "ndcg_at_k", "map"],
            "strategies": [strategy.key for strategy in strategies],
        }
        return BenchmarkReport(meta=meta, summary=summary_rows, per_query=per_query_rows)


def write_report(report: BenchmarkReport, out_dir: Path, *, prefix: str = "benchmark") -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "json": out_dir / f"{prefix}_report.json",
        "summary_csv": out_dir / f"{prefix}_summary.csv",
        "per_query_csv": out_dir / f"{prefix}_per_query.csv",
    }
    payload = {
        "meta": report.meta,
        "summary": report.summary,
        "per_query": report.per_query,
    }
    paths["json"].write_text(json.dumps(payload, indent=2), encoding="utf-8")

    with paths["summary_csv"].open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=SUMMARY_CSV_FIELDS)
        writer.writeheader()
        for row in report.summary:
            writer.writerow({k: row[k] for k in SUMMARY_CSV_FIELDS})

    with paths["per_query_csv"].open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=PER_QUERY_CSV_FIELDS)
        writer.writeheader()
        for row in report.per_query:
            out = dict(row)
            out["predicted_ids"] = "|".join(out["predicted_ids"])
            writer.writerow({k: out[k] for k in PER_QUERY_CSV_FIELDS})

    return paths


def print_summary_table(report: BenchmarkReport) -> None:
    print(
        f"\nJobMatch benchmark — {report.meta['corpus']['candidates']} CVs, "
        f"{report.meta['corpus']['jobs']} jobs, "
        f"{report.meta['corpus']['labeled_queries']} queries, K={report.meta['top_k']}\n"
    )
    header = f"{'Method':<28} {'P@K':>7} {'R@K':>7} {'MRR':>7} {'nDCG@K':>8} {'MAP':>7}"
    print(header)
    print("-" * len(header))
    for row in report.summary:
        print(
            f"{row['method']:<28} "
            f"{row['precision_at_k']:7.3f} "
            f"{row['recall_at_k']:7.3f} "
            f"{row['mrr']:7.3f} "
            f"{row['ndcg_at_k']:8.3f} "
            f"{row['map']:7.3f}"
        )
