"""Production composite scoring evaluation (offline research only)."""
from __future__ import annotations

import csv
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import Settings
from core.scoring import COMPOSITE_WEIGHTS, compute_composite

from benchmarks.eval_data import cv_to_snapshot, job_to_snapshot, load_eval_labels
from benchmarks.metrics import eval_rankings
from benchmarks.rank_utils import rank_exhaustive


SUMMARY_CSV_FIELDS = [
    "method_key",
    "method",
    "precision_at_k",
    "recall_at_k",
    "mrr",
    "ndcg_at_k",
    "map",
    "latency_ms",
    "top_k",
    "queries",
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
class CompositeEvalReport:
    meta: dict[str, Any]
    summary: dict[str, Any]
    per_query: list[dict[str, Any]]


class CompositeEval:
    """Evaluate production `compute_composite` on eval_pairs.json."""

    def __init__(
        self,
        *,
        settings: Settings | None = None,
        eval_path: Path | None = None,
        data_dir: Path | None = None,
        top_k: int = 5,
        skills_mode: str = "jaccard",
    ) -> None:
        self.settings = settings or Settings()
        self.eval_path = Path(eval_path or self.settings.data_dir / "eval_pairs.json")
        self.data_dir = Path(data_dir or self.settings.data_dir)
        self.top_k = top_k
        self.skills_mode = skills_mode

    def run(self) -> CompositeEvalReport:
        resumes = json.loads((self.data_dir / "cvs.json").read_text(encoding="utf-8"))
        jobs = json.loads((self.data_dir / "jobs.json").read_text(encoding="utf-8"))
        eval_map = load_eval_labels(self.eval_path)
        model_name = self.settings.embedding_model

        job_snaps = [job_to_snapshot(j, model_name) for j in jobs]
        cv_snaps = {r["id"]: cv_to_snapshot(r, model_name) for r in resumes}
        query_ids = [qid for qid in eval_map if qid in cv_snaps]

        score_fn = lambda c, j: compute_composite(
            c, j, metric="cosine", skills_mode=self.skills_mode, model_name=model_name
        )

        t0 = time.perf_counter()
        ranked = {
            qid: rank_exhaustive(cv_snaps[qid], job_snaps, score_fn)
            for qid in query_ids
        }
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        latency_ms = round(elapsed_ms / max(len(query_ids), 1), 3)

        per_query, agg = eval_rankings(eval_map, ranked, self.top_k)
        per_query_rows = [
            {
                "method_key": "composite",
                "method": "Production composite",
                "query_id": row["query_id"],
                "precision_at_k": row["precision_at_k"],
                "recall_at_k": row["recall_at_k"],
                "mrr": row["mrr"],
                "ndcg_at_k": row["ndcg_at_k"],
                "map": row["map"],
                "top_k": self.top_k,
                "predicted_ids": row["predicted_ids"],
            }
            for row in per_query
        ]

        summary = {
            "method_key": "composite",
            "method": "Production composite",
            "precision_at_k": agg["avg_precision_at_k"],
            "recall_at_k": agg["avg_recall_at_k"],
            "mrr": agg["avg_mrr"],
            "ndcg_at_k": agg["avg_ndcg_at_k"],
            "map": agg["avg_map"],
            "latency_ms": latency_ms,
            "top_k": self.top_k,
            "queries": agg["queries"],
        }

        meta = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "report_type": "production_composite",
            "task": "resume_to_jobs",
            "eval_path": str(self.eval_path),
            "data_dir": str(self.data_dir),
            "corpus": {"candidates": len(resumes), "jobs": len(jobs), "labeled_queries": len(eval_map)},
            "top_k": self.top_k,
            "embedding_model": model_name,
            "skills_mode": self.skills_mode,
            "composite_weights": dict(COMPOSITE_WEIGHTS),
            "strategy": "composite",
        }
        return CompositeEvalReport(meta=meta, summary=summary, per_query=per_query_rows)


def write_composite_report(report: CompositeEvalReport, out_dir: Path, *, prefix: str = "composite") -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "json": out_dir / f"{prefix}_eval_report.json",
        "summary_csv": out_dir / f"{prefix}_summary.csv",
        "per_query_csv": out_dir / f"{prefix}_per_query.csv",
    }
    payload = {"meta": report.meta, "summary": report.summary, "per_query": report.per_query}
    paths["json"].write_text(json.dumps(payload, indent=2), encoding="utf-8")

    with paths["summary_csv"].open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=SUMMARY_CSV_FIELDS)
        writer.writeheader()
        writer.writerow({k: report.summary[k] for k in SUMMARY_CSV_FIELDS})

    with paths["per_query_csv"].open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=PER_QUERY_CSV_FIELDS)
        writer.writeheader()
        for row in report.per_query:
            out = dict(row)
            out["predicted_ids"] = "|".join(out["predicted_ids"])
            writer.writerow({k: out[k] for k in PER_QUERY_CSV_FIELDS})

    return paths


def print_composite_summary(report: CompositeEvalReport) -> None:
    s = report.summary
    print(
        f"\nProduction composite: {report.meta['corpus']['labeled_queries']} queries, K={report.meta['top_k']}\n"
        f"  nDCG@K={s['ndcg_at_k']:.3f}  MRR={s['mrr']:.3f}  "
        f"P@K={s['precision_at_k']:.3f}  R@K={s['recall_at_k']:.3f}  "
        f"latency={s['latency_ms']:.2f} ms/query"
    )
