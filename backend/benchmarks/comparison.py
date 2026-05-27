"""Table-ready lexical vs embedding comparison reports (offline research only)."""
from __future__ import annotations

import csv
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import Settings

from benchmarks.baseline_strategies import build_all_strategies
from benchmarks.eval_data import cv_to_snapshot, job_to_snapshot, load_eval_labels
from benchmarks.metrics import eval_rankings


TABLE_METRICS = [
    ("precision_at_k", "Precision@K"),
    ("recall_at_k", "Recall@K"),
    ("mrr", "MRR"),
    ("ndcg_at_k", "nDCG@K"),
    ("map", "MAP"),
]

TABLE_CSV_FIELDS = ["method", "metric", "top_k", "score", "latency_ms"]


@dataclass
class ComparisonTableReport:
    meta: dict[str, Any]
    rows: list[dict[str, Any]]
    summary: list[dict[str, Any]]
    per_query: list[dict[str, Any]]


class ComparisonBenchmark:
    """Evaluate lexical baselines against embedding strategies with latency timing."""

    def __init__(
        self,
        *,
        settings: Settings | None = None,
        eval_path: Path | None = None,
        data_dir: Path | None = None,
        top_k: int = 5,
        semantic_weight: float = 0.7,
        include_lexical_baselines: bool = True,
    ) -> None:
        self.settings = settings or Settings()
        self.eval_path = Path(eval_path or self.settings.data_dir / "eval_pairs.json")
        self.data_dir = Path(data_dir or self.settings.data_dir)
        self.top_k = top_k
        self.semantic_weight = semantic_weight
        self.include_lexical_baselines = include_lexical_baselines

    def run(self) -> ComparisonTableReport:
        resumes = json.loads((self.data_dir / "cvs.json").read_text(encoding="utf-8"))
        jobs = json.loads((self.data_dir / "jobs.json").read_text(encoding="utf-8"))
        eval_map = load_eval_labels(self.eval_path)
        resumes_by_id = {r["id"]: r for r in resumes}
        model_name = self.settings.embedding_model

        job_snaps = [job_to_snapshot(j, model_name) for j in jobs]
        cv_snaps = {r["id"]: cv_to_snapshot(r, model_name) for r in resumes}

        strategies = build_all_strategies(
            jobs,
            resumes_by_id,
            job_snaps,
            model_name=model_name,
            semantic_weight=self.semantic_weight,
            rrf_k=self.settings.rrf_k,
            include_lexical_baselines=self.include_lexical_baselines,
        )

        query_ids = [qid for qid in eval_map if qid in cv_snaps]
        summary_rows: list[dict[str, Any]] = []
        table_rows: list[dict[str, Any]] = []
        per_query_rows: list[dict[str, Any]] = []

        for strategy in strategies:
            t0 = time.perf_counter()
            ranked = {qid: strategy.rank_fn(cv_snaps[qid]) for qid in query_ids}
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            latency_ms = round(elapsed_ms / max(len(query_ids), 1), 3)

            per_query, agg = eval_rankings(eval_map, ranked, self.top_k)
            summary = {
                "method_key": strategy.key,
                "method": strategy.label,
                "family": "lexical" if strategy.key in {"bm25", "tfidf_cosine", "exact_skill_overlap"} else "embedding",
                "top_k": self.top_k,
                "latency_ms": latency_ms,
                "latency_total_ms": round(elapsed_ms, 3),
                "queries": agg["queries"],
                **{name: agg[f"avg_{name}"] for name, _ in TABLE_METRICS},
            }
            summary_rows.append(summary)

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

            for field, label in TABLE_METRICS:
                table_rows.append(
                    {
                        "method": strategy.label,
                        "metric": label,
                        "top_k": self.top_k,
                        "score": round(summary[field], 6),
                        "latency_ms": latency_ms,
                    }
                )

        meta = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "report_type": "lexical_vs_embedding_comparison",
            "task": "resume_to_jobs",
            "eval_path": str(self.eval_path),
            "corpus": {"candidates": len(resumes), "jobs": len(jobs), "labeled_queries": len(eval_map)},
            "top_k": self.top_k,
            "embedding_model": model_name,
            "include_lexical_baselines": self.include_lexical_baselines,
            "strategies": [s.key for s in strategies],
            "table_columns": TABLE_CSV_FIELDS,
            "note": "Offline research only; production APIs unchanged unless BENCHMARK_LEXICAL_API is enabled.",
        }
        return ComparisonTableReport(meta=meta, rows=table_rows, summary=summary_rows, per_query=per_query_rows)


def write_comparison_report(
    report: ComparisonTableReport,
    out_dir: Path,
    *,
    prefix: str = "comparison",
) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "table_csv": out_dir / f"{prefix}_table.csv",
        "table_json": out_dir / f"{prefix}_table.json",
        "summary_json": out_dir / f"{prefix}_summary.json",
    }
    paths["table_json"].write_text(
        json.dumps({"meta": report.meta, "rows": report.rows}, indent=2),
        encoding="utf-8",
    )
    paths["summary_json"].write_text(
        json.dumps({"meta": report.meta, "summary": report.summary}, indent=2),
        encoding="utf-8",
    )
    with paths["table_csv"].open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=TABLE_CSV_FIELDS)
        writer.writeheader()
        writer.writerows(report.rows)
    return paths


def print_comparison_table(report: ComparisonTableReport) -> None:
    print(
        f"\nLexical vs embedding comparison: "
        f"{report.meta['corpus']['labeled_queries']} queries, K={report.meta['top_k']}\n"
    )
    header = f"{'Method':<32} {'Metric':<14} {'top_k':>5} {'Score':>10} {'latency_ms':>12}"
    print(header)
    print("-" * len(header))
    for row in report.rows:
        print(
            f"{row['method']:<32} "
            f"{row['metric']:<14} "
            f"{row['top_k']:5d} "
            f"{row['score']:10.4f} "
            f"{row['latency_ms']:12.3f}"
        )

    print("\nSummary by method (nDCG@K, latency_ms):")
    for s in report.summary:
        print(f"  {s['method']:<32} nDCG@K={s['ndcg_at_k']:.3f}  latency_ms={s['latency_ms']:.3f}  [{s['family']}]")
