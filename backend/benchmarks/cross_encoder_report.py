"""Offline report: bi-encoder vs two-stage cross-encoder reranking."""
from __future__ import annotations

import csv
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import Settings

from benchmarks.eval_data import load_eval_labels
from benchmarks.metrics import eval_rankings
from contracts.matching import MatchRequest


TABLE_FIELDS = [
    "method",
    "metric",
    "top_k",
    "score",
    "bi_encoder_ms",
    "cross_encoder_ms",
    "total_ms",
    "rank_changes_top_k",
    "queries_unchanged_top_k",
]

METRIC_KEYS = [
    ("precision_at_k", "Precision@K"),
    ("recall_at_k", "Recall@K"),
    ("mrr", "MRR"),
    ("ndcg_at_k", "nDCG@K"),
    ("map", "MAP"),
]


@dataclass
class CrossEncoderReport:
    meta: dict[str, Any]
    rows: list[dict[str, Any]]
    ranking_changes: list[dict[str, Any]]


def _run_mode(
    container,
    eval_map: dict,
    *,
    top_k: int,
    strategy: str,
    use_cross_encoder: bool,
) -> tuple[dict[str, list[tuple[str, float]]], dict[str, float], list[dict]]:
    ranked: dict[str, list[tuple[str, float]]] = {}
    bi_ms: list[float] = []
    ce_ms: list[float] = []
    rank_changes: list[dict] = []

    for qid in eval_map:
        profile = container.candidate.get_by_id(qid)
        if profile is None:
            continue
        request = MatchRequest(
            query_key=profile.name,
            top_k=top_k,
            strategy=strategy,
            use_cross_encoder=use_cross_encoder,
        )
        t0 = time.perf_counter()
        response = container.matchmaker.match_candidate_to_jobs(request)
        total = (time.perf_counter() - t0) * 1000.0
        ranked[qid] = [(r.target_id, r.final_score or r.similarity) for r in response.results]
        if response.rerank:
            bi_ms.append(response.rerank.bi_encoder_ms)
            ce_ms.append(response.rerank.cross_encoder_ms)
            if response.rerank.ranking_changes:
                for change in response.rerank.ranking_changes:
                    rank_changes.append(
                        {
                            "query_id": qid,
                            "target_id": change.target_id,
                            "target_label": change.target_label,
                            "rank_before": change.rank_before,
                            "rank_after": change.rank_after,
                            "moved": change.moved,
                        }
                    )
        else:
            bi_ms.append(total)
            ce_ms.append(0.0)

    timing = {
        "avg_bi_encoder_ms": sum(bi_ms) / max(len(bi_ms), 1),
        "avg_cross_encoder_ms": sum(ce_ms) / max(len(ce_ms), 1),
        "avg_total_ms": sum(b + c for b, c in zip(bi_ms, ce_ms)) / max(len(bi_ms), 1),
    }
    return ranked, timing, rank_changes


def run_report(
    *,
    settings: Settings | None = None,
    top_k: int = 5,
    strategy: str = "composite",
) -> CrossEncoderReport:
    from bootstrap import create_system

    settings = settings or Settings()
    settings = settings.model_copy(update={"enable_cross_encoder_rerank": True})
    container = create_system(settings)
    eval_map = load_eval_labels(settings.data_dir / "eval_pairs.json")

    baseline_ranked, baseline_timing, _ = _run_mode(
        container, eval_map, top_k=top_k, strategy=strategy, use_cross_encoder=False
    )
    rerank_ranked, rerank_timing, rank_changes = _run_mode(
        container, eval_map, top_k=top_k, strategy=strategy, use_cross_encoder=True
    )

    _, baseline_agg = eval_rankings(eval_map, baseline_ranked, top_k)
    _, rerank_agg = eval_rankings(eval_map, rerank_ranked, top_k)

    rows: list[dict[str, Any]] = []
    for field, label in METRIC_KEYS:
        rows.append(
            {
                "method": "Bi-encoder only",
                "metric": label,
                "top_k": top_k,
                "score": round(baseline_agg[f"avg_{field}"], 6),
                "bi_encoder_ms": round(baseline_timing["avg_bi_encoder_ms"], 3),
                "cross_encoder_ms": 0.0,
                "total_ms": round(baseline_timing["avg_bi_encoder_ms"], 3),
                "rank_changes_top_k": 0,
                "queries_unchanged_top_k": len(eval_map),
            }
        )
        delta = rerank_agg[f"avg_{field}"] - baseline_agg[f"avg_{field}"]
        unchanged = sum(
            1
            for qid in eval_map
            if qid in baseline_ranked
            and qid in rerank_ranked
            and [d for d, _ in baseline_ranked[qid][:top_k]]
            == [d for d, _ in rerank_ranked[qid][:top_k]]
        )
        rows.append(
            {
                "method": "Bi-encoder + cross-encoder",
                "metric": label,
                "top_k": top_k,
                "score": round(rerank_agg[f"avg_{field}"], 6),
                "bi_encoder_ms": round(rerank_timing["avg_bi_encoder_ms"], 3),
                "cross_encoder_ms": round(rerank_timing["avg_cross_encoder_ms"], 3),
                "total_ms": round(rerank_timing["avg_total_ms"], 3),
                "rank_changes_top_k": len(eval_map) - unchanged,
                "queries_unchanged_top_k": unchanged,
            }
        )
        rows.append(
            {
                "method": "Delta (CE - bi-encoder)",
                "metric": label,
                "top_k": top_k,
                "score": round(delta, 6),
                "bi_encoder_ms": round(
                    rerank_timing["avg_bi_encoder_ms"] - baseline_timing["avg_bi_encoder_ms"], 3
                ),
                "cross_encoder_ms": round(rerank_timing["avg_cross_encoder_ms"], 3),
                "total_ms": round(rerank_timing["avg_total_ms"] - baseline_timing["avg_bi_encoder_ms"], 3),
                "rank_changes_top_k": len(eval_map) - unchanged,
                "queries_unchanged_top_k": unchanged,
            }
        )

    meta = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "report_type": "cross_encoder_two_stage",
        "strategy": strategy,
        "top_k": top_k,
        "rerank_pool": settings.cross_encoder_rerank_pool,
        "queries": len(eval_map),
        "quality_summary": {
            "ndcg_baseline": baseline_agg["avg_ndcg_at_k"],
            "ndcg_with_ce": rerank_agg["avg_ndcg_at_k"],
            "ndcg_delta": rerank_agg["avg_ndcg_at_k"] - baseline_agg["avg_ndcg_at_k"],
            "mrr_delta": rerank_agg["avg_mrr"] - baseline_agg["avg_mrr"],
        },
        "latency_summary": {
            "baseline_avg_ms": baseline_timing["avg_bi_encoder_ms"],
            "with_ce_avg_ms": rerank_timing["avg_total_ms"],
            "cross_encoder_overhead_ms": rerank_timing["avg_cross_encoder_ms"],
        },
    }
    return CrossEncoderReport(meta=meta, rows=rows, ranking_changes=rank_changes)


def write_report(report: CrossEncoderReport, out_dir: Path, *, prefix: str = "cross_encoder") -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "table_csv": out_dir / f"{prefix}_table.csv",
        "report_json": out_dir / f"{prefix}_report.json",
        "rank_changes_json": out_dir / f"{prefix}_rank_changes.json",
    }
    with paths["table_csv"].open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=TABLE_FIELDS)
        writer.writeheader()
        writer.writerows(report.rows)
    paths["report_json"].write_text(
        json.dumps({"meta": report.meta, "rows": report.rows}, indent=2),
        encoding="utf-8",
    )
    paths["rank_changes_json"].write_text(
        json.dumps({"meta": report.meta, "changes": report.ranking_changes}, indent=2),
        encoding="utf-8",
    )
    return paths


def print_report(report: CrossEncoderReport) -> None:
    print("\nCross-encoder two-stage report\n")
    print(f"{'Method':<28} {'Metric':<12} {'top_k':>5} {'Score':>8} {'bi_ms':>8} {'ce_ms':>8} {'total_ms':>9}")
    print("-" * 86)
    for row in report.rows:
        print(
            f"{row['method']:<28} {row['metric']:<12} {row['top_k']:5d} "
            f"{row['score']:8.4f} {row['bi_encoder_ms']:8.2f} {row['cross_encoder_ms']:8.2f} "
            f"{row['total_ms']:9.2f}"
        )
    q = report.meta["quality_summary"]
    lat = report.meta["latency_summary"]
    print(
        f"\nQuality: nDCG {q['ndcg_baseline']:.3f} → {q['ndcg_with_ce']:.3f} "
        f"(Δ {q['ndcg_delta']:+.3f})"
    )
    print(
        f"Latency: {lat['baseline_avg_ms']:.1f}ms → {lat['with_ce_avg_ms']:.1f}ms "
        f"(+{lat['cross_encoder_overhead_ms']:.1f}ms CE overhead)"
    )
    print(f"Rank changes logged: {len(report.ranking_changes)}")
