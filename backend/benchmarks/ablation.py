"""Ablation study runner; component-wise matching quality on eval_pairs.json."""
from __future__ import annotations

import csv
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from config import Settings
from contracts.matching import ScoreBreakdown
from contracts.snapshots import CandidateSnapshot, JobSnapshot

from benchmarks.ablation_scoring import (
    compensation_only,
    experience_only,
    full_composite,
    location_only,
    semantic_only,
    semantic_skills,
    semantic_skills_experience,
    skills_only,
)
from benchmarks.eval_data import cv_to_snapshot, job_to_snapshot, load_eval_labels
from benchmarks.metrics import eval_rankings
from benchmarks.rank_utils import rank_exhaustive, rrf_fuse_lists
from benchmarks.strategies import BenchmarkStrategy


METRIC_FIELDS = [
    ("precision_at_k", "Precision@K"),
    ("recall_at_k", "Recall@K"),
    ("mrr", "MRR"),
    ("ndcg_at_k", "nDCG@K"),
    ("map", "MAP"),
]

SUMMARY_CSV_FIELDS = [
    "variant_key",
    "variant",
    "category",
    "components",
    "precision_at_k",
    "recall_at_k",
    "mrr",
    "ndcg_at_k",
    "map",
    "latency_ms",
    "top_k",
    "queries",
]

TABLE_CSV_FIELDS = ["variant", "metric", "top_k", "score", "latency_ms"]


@dataclass
class AblationReport:
    meta: dict[str, Any]
    summary: list[dict[str, Any]]
    table_rows: list[dict[str, Any]]
    per_query: list[dict[str, Any]]


def build_ablation_strategies(
    job_snaps: list[JobSnapshot],
    *,
    model_name: str,
    skills_mode: str = "jaccard",
    rrf_k: int = 60,
) -> list[BenchmarkStrategy]:
    """Nine ablation variants for resume→jobs ranking."""

    def exhaustive(
        score_fn: Callable[..., ScoreBreakdown],
        *,
        metric: str = "cosine",
    ):
        return lambda snap: rank_exhaustive(
            snap,
            job_snaps,
            lambda c, j: score_fn(c, j, metric=metric, skills_mode=skills_mode, model_name=model_name),
        )

    singles: list[BenchmarkStrategy] = [
        BenchmarkStrategy(
            key="semantic_only",
            label="Semantic only",
            description="Bi-encoder cosine similarity.",
            rank_fn=exhaustive(semantic_only),
            contributes_to_rrf=True,
        ),
        BenchmarkStrategy(
            key="skills_only",
            label="Skills only",
            description="Jaccard overlap on required skills.",
            rank_fn=exhaustive(skills_only),
            contributes_to_rrf=True,
        ),
        BenchmarkStrategy(
            key="experience_only",
            label="Experience only",
            description="Experience years vs job requirement.",
            rank_fn=exhaustive(experience_only),
            contributes_to_rrf=True,
        ),
        BenchmarkStrategy(
            key="compensation_only",
            label="Compensation only",
            description="Salary expectation vs job budget.",
            rank_fn=exhaustive(compensation_only),
            contributes_to_rrf=True,
        ),
        BenchmarkStrategy(
            key="location_only",
            label="Location only",
            description="Remote preference vs job remote policy.",
            rank_fn=exhaustive(location_only),
            contributes_to_rrf=True,
        ),
    ]

    partials: list[BenchmarkStrategy] = [
        BenchmarkStrategy(
            key="semantic_skills",
            label="Semantic + skills",
            description="Renormalized composite weights over semantic (40%) + skills (30%).",
            rank_fn=exhaustive(semantic_skills),
            contributes_to_rrf=False,
        ),
        BenchmarkStrategy(
            key="semantic_skills_experience",
            label="Semantic + skills + experience",
            description="Renormalized weights over semantic, skills, experience.",
            rank_fn=exhaustive(semantic_skills_experience),
            contributes_to_rrf=False,
        ),
        BenchmarkStrategy(
            key="full_composite",
            label="Full composite",
            description="Production composite: 40/30/15/10/5% over all five signals.",
            rank_fn=exhaustive(full_composite),
            contributes_to_rrf=False,
        ),
    ]

    def rrf_rank(snap: CandidateSnapshot) -> list[tuple[str, float]]:
        lists = [s.rank_fn(snap) for s in singles]
        return rrf_fuse_lists(lists, k=rrf_k)

    ensemble = BenchmarkStrategy(
        key="rrf_ensemble",
        label="RRF ensemble",
        description=f"RRF (k={rrf_k}) over the five single-component rankers.",
        rank_fn=rrf_rank,
        contributes_to_rrf=False,
    )

    return singles + partials + [ensemble]


ABLATION_META: dict[str, dict[str, Any]] = {
    "semantic_only": {"category": "single", "components": "semantic"},
    "skills_only": {"category": "single", "components": "skills"},
    "experience_only": {"category": "single", "components": "experience"},
    "compensation_only": {"category": "single", "components": "compensation"},
    "location_only": {"category": "single", "components": "location"},
    "semantic_skills": {"category": "partial", "components": "semantic+skills"},
    "semantic_skills_experience": {"category": "partial", "components": "semantic+skills+experience"},
    "full_composite": {"category": "full", "components": "semantic+skills+experience+compensation+location"},
    "rrf_ensemble": {"category": "ensemble", "components": "RRF(semantic,skills,experience,compensation,location)"},
}


class AblationStudy:
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

    def run(self) -> AblationReport:
        resumes = json.loads((self.data_dir / "cvs.json").read_text(encoding="utf-8"))
        jobs = json.loads((self.data_dir / "jobs.json").read_text(encoding="utf-8"))
        eval_map = load_eval_labels(self.eval_path)
        model_name = self.settings.embedding_model

        job_snaps = [job_to_snapshot(j, model_name) for j in jobs]
        cv_snaps = {r["id"]: cv_to_snapshot(r, model_name) for r in resumes}
        strategies = build_ablation_strategies(
            job_snaps,
            model_name=model_name,
            skills_mode=self.skills_mode,
            rrf_k=self.settings.rrf_k,
        )

        query_ids = [qid for qid in eval_map if qid in cv_snaps]
        summary: list[dict[str, Any]] = []
        table_rows: list[dict[str, Any]] = []
        per_query: list[dict[str, Any]] = []

        for strategy in strategies:
            meta = ABLATION_META[strategy.key]
            t0 = time.perf_counter()
            ranked = {qid: strategy.rank_fn(cv_snaps[qid]) for qid in query_ids}
            latency_ms = round((time.perf_counter() - t0) * 1000.0 / max(len(query_ids), 1), 3)

            pq, agg = eval_rankings(eval_map, ranked, self.top_k)
            row = {
                "variant_key": strategy.key,
                "variant": strategy.label,
                "category": meta["category"],
                "components": meta["components"],
                "precision_at_k": agg["avg_precision_at_k"],
                "recall_at_k": agg["avg_recall_at_k"],
                "mrr": agg["avg_mrr"],
                "ndcg_at_k": agg["avg_ndcg_at_k"],
                "map": agg["avg_map"],
                "latency_ms": latency_ms,
                "top_k": self.top_k,
                "queries": agg["queries"],
            }
            summary.append(row)

            for field, label in METRIC_FIELDS:
                table_rows.append(
                    {
                        "variant": strategy.label,
                        "metric": label,
                        "top_k": self.top_k,
                        "score": round(row[field], 6),
                        "latency_ms": latency_ms,
                    }
                )

            for item in pq:
                per_query.append(
                    {
                        "variant_key": strategy.key,
                        "variant": strategy.label,
                        **item,
                    }
                )

        report_meta = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "report_type": "ablation_study",
            "task": "resume_to_jobs",
            "eval_path": str(self.eval_path),
            "corpus": {
                "candidates": len(resumes),
                "jobs": len(jobs),
                "labeled_queries": len(eval_map),
            },
            "top_k": self.top_k,
            "skills_mode": self.skills_mode,
            "embedding_model": model_name,
            "composite_weights": {
                "semantic": 0.40,
                "skills": 0.30,
                "experience": 0.15,
                "compensation": 0.10,
                "location": 0.05,
            },
            "variants": [s.key for s in strategies],
            "best_ndcg": max(summary, key=lambda r: r["ndcg_at_k"])["variant"],
        }
        return AblationReport(meta=report_meta, summary=summary, table_rows=table_rows, per_query=per_query)


def write_ablation_report(
    report: AblationReport,
    out_dir: Path,
    *,
    prefix: str = "ablation",
) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "summary_json": out_dir / f"{prefix}_summary.json",
        "table_csv": out_dir / f"{prefix}_table.csv",
        "summary_csv": out_dir / f"{prefix}_summary.csv",
        "per_query_csv": out_dir / f"{prefix}_per_query.csv",
        "report_json": out_dir / f"{prefix}_report.json",
        "markdown": out_dir / f"{prefix}_summary.md",
    }

    paths["report_json"].write_text(
        json.dumps(
            {
                "meta": report.meta,
                "summary": report.summary,
                "table_rows": report.table_rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    paths["summary_json"].write_text(
        json.dumps({"meta": report.meta, "summary": report.summary}, indent=2),
        encoding="utf-8",
    )

    with paths["summary_csv"].open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=SUMMARY_CSV_FIELDS)
        writer.writeheader()
        for row in report.summary:
            writer.writerow({k: row[k] for k in SUMMARY_CSV_FIELDS})

    with paths["table_csv"].open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=TABLE_CSV_FIELDS)
        writer.writeheader()
        writer.writerows(report.table_rows)

    per_query_fields = [
        "variant_key",
        "variant",
        "query_id",
        "precision_at_k",
        "recall_at_k",
        "mrr",
        "ndcg_at_k",
        "map",
        "predicted_ids",
    ]
    with paths["per_query_csv"].open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=per_query_fields)
        writer.writeheader()
        for row in report.per_query:
            out = dict(row)
            out["predicted_ids"] = "|".join(out.get("predicted_ids", []))
            writer.writerow({k: out.get(k) for k in per_query_fields})

    paths["markdown"].write_text(render_ablation_markdown(report), encoding="utf-8")
    return paths


def render_ablation_markdown(report: AblationReport) -> str:
    meta = report.meta
    k = meta["top_k"]
    lines = [
        "# Ablation Study: Composite Matching Components",
        "",
        f"Generated: {meta['generated_at']}",
        "",
        "## Setup",
        "",
        f"- Task: {meta['task']}",
        f"- Corpus: {meta['corpus']['candidates']} candidates, {meta['corpus']['jobs']} jobs",
        f"- Labeled queries: {meta['corpus']['labeled_queries']}",
        f"- Top-K: {k}",
        f"- Skills mode: {meta['skills_mode']}",
        f"- Embedding model: `{meta['embedding_model']}`",
        "",
        "Production composite weights (full model):",
        "",
        "| Component | Weight |",
        "|-----------|--------|",
    ]
    for comp, weight in meta["composite_weights"].items():
        lines.append(f"| {comp.capitalize()} | {weight:.0%} |")

    lines.extend(
        [
            "",
            "## Summary (macro-averaged)",
            "",
            "| Variant | Category | P@K | R@K | MRR | nDCG@K | MAP | Latency (ms) |",
            "|---------|----------|-----|-----|-----|--------|-----|--------------|",
        ]
    )
    for row in report.summary:
        lines.append(
            f"| {row['variant']} | {row['category']} | "
            f"{row['precision_at_k']:.3f} | {row['recall_at_k']:.3f} | {row['mrr']:.3f} | "
            f"{row['ndcg_at_k']:.3f} | {row['map']:.3f} | {row['latency_ms']:.2f} |"
        )

    best = max(report.summary, key=lambda r: r["ndcg_at_k"])
    full = next(r for r in report.summary if r["variant_key"] == "full_composite")
    lines.extend(
        [
            "",
            "## Findings",
            "",
            f"- Best nDCG@{k}: **{best['variant']}** ({best['ndcg_at_k']:.3f})",
            f"- Full composite nDCG@{k}: {full['ndcg_at_k']:.3f}",
            f"- Full composite vs best delta: {full['ndcg_at_k'] - best['ndcg_at_k']:+.3f}",
            "",
            "## Table-ready long format",
            "",
            "See `ablation_table.csv` for columns: `variant`, `metric`, `top_k`, `score`, `latency_ms`.",
            "",
            "| Variant | Metric | top_k | Score | latency_ms |",
            "|---------|--------|-------|-------|------------|",
        ]
    )
    for row in report.table_rows:
        lines.append(
            f"| {row['variant']} | {row['metric']} | {row['top_k']} | "
            f"{row['score']:.4f} | {row['latency_ms']:.2f} |"
        )
    lines.append("")
    return "\n".join(lines)


def print_ablation_summary(report: AblationReport) -> None:
    k = report.meta["top_k"]
    print(f"\nAblation study: {report.meta['corpus']['labeled_queries']} queries, K={k}\n")
    header = f"{'Variant':<32} {'P@K':>6} {'R@K':>6} {'MRR':>6} {'nDCG':>6} {'MAP':>6} {'ms':>8}"
    print(header)
    print("-" * len(header))
    for row in report.summary:
        print(
            f"{row['variant']:<32} "
            f"{row['precision_at_k']:6.3f} "
            f"{row['recall_at_k']:6.3f} "
            f"{row['mrr']:6.3f} "
            f"{row['ndcg_at_k']:6.3f} "
            f"{row['map']:6.3f} "
            f"{row['latency_ms']:8.2f}"
        )
    print(f"\nBest nDCG@{k}: {report.meta['best_ndcg']}")
