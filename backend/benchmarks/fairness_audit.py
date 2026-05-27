"""Offline fairness & bias audit using synthetic controlled profile pairs."""
from __future__ import annotations

import csv
import json
import statistics
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from config import Settings
from contracts.matching import ScoreBreakdown
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.explain import build_why_ranked
from core.scoring import compute_composite

from benchmarks.eval_data import job_to_snapshot
from benchmarks.fairness_profiles import build_pair_snapshots, load_audit_profiles


DEFAULT_SCORE_DELTA_THRESHOLD = 0.01
DEFAULT_TOP_K = 5

PAIR_CSV_FIELDS = [
    "pair_id",
    "category",
    "field_changed",
    "top_k",
    "top_1_stable",
    "top_k_overlap",
    "max_rank_change",
    "mean_rank_change",
    "mean_score_delta",
    "max_score_delta",
    "top1_explanation_drift",
    "flagged",
    "flag_reasons",
]

FLAGGED_CSV_FIELDS = [
    "pair_id",
    "category",
    "field_changed",
    "job_id",
    "rank_a",
    "rank_b",
    "rank_change",
    "score_a",
    "score_b",
    "score_delta",
    "explanation_drift",
    "flag_reasons",
]


@dataclass
class FairnessAuditReport:
    meta: dict[str, Any]
    pair_summaries: list[dict[str, Any]]
    per_job: list[dict[str, Any]]
    flagged_cases: list[dict[str, Any]]


def explanation_drift(explanations_a: list[str], explanations_b: list[str]) -> dict[str, Any]:
    set_a = set(explanations_a)
    set_b = set(explanations_b)
    union = set_a | set_b
    if not union:
        return {
            "jaccard_similarity": 1.0,
            "drift_score": 0.0,
            "added": [],
            "removed": [],
            "unchanged": True,
        }
    inter = set_a & set_b
    jaccard = len(inter) / len(union)
    return {
        "jaccard_similarity": round(jaccard, 6),
        "drift_score": round(1.0 - jaccard, 6),
        "added": sorted(set_b - set_a),
        "removed": sorted(set_a - set_b),
        "unchanged": set_a == set_b,
    }


def _rank_map(ranked: list[tuple[str, float]]) -> dict[str, int]:
    return {job_id: rank for rank, (job_id, _) in enumerate(ranked, start=1)}


def _score_map(ranked: list[tuple[str, float]]) -> dict[str, float]:
    return {job_id: score for job_id, score in ranked}


def compare_rankings(
    ranked_a: list[tuple[str, float]],
    ranked_b: list[tuple[str, float]],
    *,
    top_k: int,
) -> dict[str, Any]:
    rank_a = _rank_map(ranked_a)
    rank_b = _rank_map(ranked_b)
    score_a = _score_map(ranked_a)
    score_b = _score_map(ranked_b)

    all_jobs = sorted(set(rank_a) | set(rank_b))
    rank_changes = {jid: abs(rank_a[jid] - rank_b[jid]) for jid in all_jobs}

    top_a = [jid for jid, _ in ranked_a[:top_k]]
    top_b = [jid for jid, _ in ranked_b[:top_k]]
    overlap = len(set(top_a) & set(top_b))

    return {
        "top_1_stable": top_a[0] == top_b[0] if top_a and top_b else True,
        "top_k_overlap": overlap / top_k if top_k else 1.0,
        "top_k_overlap_count": overlap,
        "max_rank_change": max(rank_changes.values()) if rank_changes else 0,
        "mean_rank_change": statistics.mean(rank_changes.values()) if rank_changes else 0.0,
        "rank_changes": rank_changes,
        "top_a": top_a,
        "top_b": top_b,
        "score_a": score_a,
        "score_b": score_b,
    }


def audit_profile_pair(
    pair_meta: dict[str, Any],
    snap_a: CandidateSnapshot,
    snap_b: CandidateSnapshot,
    jobs: list[JobSnapshot],
    *,
    top_k: int = DEFAULT_TOP_K,
    score_fn: Callable[[CandidateSnapshot, JobSnapshot], ScoreBreakdown] | None = None,
    score_delta_threshold: float = DEFAULT_SCORE_DELTA_THRESHOLD,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    score_fn = score_fn or (lambda c, j: compute_composite(c, j))

    ranked_a = sorted(
        [(job.id, score_fn(snap_a, job).final_score) for job in jobs],
        key=lambda x: x[1],
        reverse=True,
    )
    ranked_b = sorted(
        [(job.id, score_fn(snap_b, job).final_score) for job in jobs],
        key=lambda x: x[1],
        reverse=True,
    )
    stability = compare_rankings(ranked_a, ranked_b, top_k=top_k)

    per_job: list[dict[str, Any]] = []
    flagged_map: dict[str, dict[str, Any]] = {}
    score_deltas: list[float] = []

    top_job_set = set(stability["top_a"]) | set(stability["top_b"])

    rank_map_a = _rank_map(ranked_a)
    rank_map_b = _rank_map(ranked_b)

    for job in jobs:
        jid = job.id
        breakdown_a = score_fn(snap_a, job)
        breakdown_b = score_fn(snap_b, job)
        expl_a = build_why_ranked(snap_a, job, breakdown_a)
        expl_b = build_why_ranked(snap_b, job, breakdown_b)
        drift = explanation_drift(expl_a, expl_b)
        delta = abs(breakdown_a.final_score - breakdown_b.final_score)
        score_deltas.append(delta)

        rank_change = stability["rank_changes"][jid]
        row = {
            "pair_id": pair_meta["pair_id"],
            "category": pair_meta["category"],
            "field_changed": pair_meta["field_changed"],
            "job_id": jid,
            "rank_a": rank_map_a[jid],
            "rank_b": rank_map_b[jid],
            "rank_change": rank_change,
            "score_a": round(breakdown_a.final_score, 6),
            "score_b": round(breakdown_b.final_score, 6),
            "score_delta": round(delta, 6),
            "explanation_a": expl_a,
            "explanation_b": expl_b,
            "explanation_drift": drift["drift_score"],
            "explanation_jaccard": drift["jaccard_similarity"],
            "explanations_unchanged": drift["unchanged"],
        }
        per_job.append(row)

        reasons: list[str] = []
        if jid in top_job_set and rank_change > 0:
            reasons.append("rank_change_in_top_k_union")
        if jid in top_job_set and delta > score_delta_threshold:
            reasons.append(f"score_delta>{score_delta_threshold}")
        if jid in top_job_set and drift["drift_score"] > 0:
            reasons.append("explanation_drift")

        if reasons:
            existing = flagged_map.get(jid)
            if existing:
                existing["flag_reasons"] = sorted(set(existing["flag_reasons"]) | set(reasons))
            else:
                flagged_map[jid] = {**row, "flag_reasons": reasons}

    if not stability["top_1_stable"] and stability["top_a"]:
        top1 = stability["top_a"][0]
        top1_row = next(r for r in per_job if r["job_id"] == top1)
        existing = flagged_map.get(top1)
        if existing:
            existing["flag_reasons"] = sorted(set(existing["flag_reasons"]) | {"top_1_changed"})
        else:
            flagged_map[top1] = {**top1_row, "flag_reasons": ["top_1_changed"]}

    flagged = list(flagged_map.values())
    top1_id = stability["top_a"][0] if stability["top_a"] else None
    top1_drift = 0.0
    if top1_id:
        top1_row = next(r for r in per_job if r["job_id"] == top1_id)
        top1_drift = top1_row["explanation_drift"]

    pair_summary = {
        "pair_id": pair_meta["pair_id"],
        "category": pair_meta["category"],
        "field_changed": pair_meta["field_changed"],
        "description": pair_meta.get("description", ""),
        "variant_a_id": snap_a.id,
        "variant_b_id": snap_b.id,
        "variant_a_name": snap_a.name,
        "variant_b_name": snap_b.name,
        "top_k": top_k,
        "top_1_stable": stability["top_1_stable"],
        "top_k_overlap": round(stability["top_k_overlap"], 4),
        "top_k_overlap_count": stability["top_k_overlap_count"],
        "top_a": stability["top_a"],
        "top_b": stability["top_b"],
        "max_rank_change": stability["max_rank_change"],
        "mean_rank_change": round(stability["mean_rank_change"], 4),
        "mean_score_delta": round(statistics.mean(score_deltas), 6),
        "max_score_delta": round(max(score_deltas), 6),
        "top1_explanation_drift": top1_drift,
        "flagged": bool(flagged) or not stability["top_1_stable"],
        "flag_count": len({f["job_id"] for f in flagged}),
        "flag_reasons": sorted({reason for f in flagged for reason in f["flag_reasons"]}),
    }
    return pair_summary, per_job, flagged


class FairnessAudit:
    """Audit ranking stability under synthetic demographic counterfactuals."""

    def __init__(
        self,
        *,
        settings: Settings | None = None,
        profiles_path: Path | None = None,
        jobs_path: Path | None = None,
        top_k: int = DEFAULT_TOP_K,
        score_delta_threshold: float = DEFAULT_SCORE_DELTA_THRESHOLD,
        strategy: str = "composite",
    ) -> None:
        self.settings = settings or Settings()
        self.profiles_path = Path(profiles_path or self.settings.data_dir / "fairness_audit_profiles.json")
        self.jobs_path = Path(jobs_path or self.settings.jobs_path)
        self.top_k = top_k
        self.score_delta_threshold = score_delta_threshold
        self.strategy = strategy

    def _score_fn(self):
        if self.strategy == "composite":
            return lambda c, j: compute_composite(
                c, j, model_name=self.settings.embedding_model
            )
        raise ValueError(f"Unsupported audit strategy: {self.strategy}")

    def run(self) -> FairnessAuditReport:
        payload = load_audit_profiles(self.profiles_path)
        jobs_raw = json.loads(self.jobs_path.read_text(encoding="utf-8"))
        model_name = self.settings.embedding_model
        job_snaps = [job_to_snapshot(j, model_name) for j in jobs_raw]

        pair_summaries: list[dict[str, Any]] = []
        per_job_all: list[dict[str, Any]] = []
        flagged_all: list[dict[str, Any]] = []

        score_fn = self._score_fn()
        for pair in payload["pairs"]:
            pair_meta, snap_a, snap_b = build_pair_snapshots(pair, model_name)
            summary, per_job, flagged = audit_profile_pair(
                pair_meta,
                snap_a,
                snap_b,
                job_snaps,
                top_k=self.top_k,
                score_fn=score_fn,
                score_delta_threshold=self.score_delta_threshold,
            )
            pair_summaries.append(summary)
            per_job_all.extend(per_job)
            flagged_all.extend(flagged)

        n_flagged_pairs = sum(1 for s in pair_summaries if s["flagged"])
        meta = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "report_type": "fairness_bias_audit",
            "synthetic_only": True,
            "warning": payload["meta"]["warning"],
            "profiles_path": str(self.profiles_path),
            "jobs": len(job_snaps),
            "pairs": len(pair_summaries),
            "top_k": self.top_k,
            "strategy": self.strategy,
            "score_delta_threshold": self.score_delta_threshold,
            "embedding_model": model_name,
            "flagged_pairs": n_flagged_pairs,
            "flagged_pair_rate": round(n_flagged_pairs / max(len(pair_summaries), 1), 4),
            "metrics_reported": [
                "rank_stability",
                "score_delta",
                "explanation_drift",
                "flagged_cases",
            ],
        }
        return FairnessAuditReport(
            meta=meta,
            pair_summaries=pair_summaries,
            per_job=per_job_all,
            flagged_cases=flagged_all,
        )


def write_fairness_audit_report(
    report: FairnessAuditReport,
    out_dir: Path,
    *,
    prefix: str = "fairness_audit",
) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "json": out_dir / f"{prefix}_report.json",
        "markdown": out_dir / f"{prefix}_summary.md",
        "pairs_csv": out_dir / f"{prefix}_pairs.csv",
        "flagged_csv": out_dir / f"{prefix}_flagged.csv",
    }

    paths["json"].write_text(
        json.dumps(
            {
                "meta": report.meta,
                "pair_summaries": report.pair_summaries,
                "flagged_cases": [
                    {k: v for k, v in row.items() if k not in ("explanation_a", "explanation_b")}
                    for row in report.flagged_cases
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    with paths["pairs_csv"].open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=PAIR_CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in report.pair_summaries:
            out = dict(row)
            out["flag_reasons"] = "|".join(row.get("flag_reasons", []))
            writer.writerow(out)

    with paths["flagged_csv"].open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FLAGGED_CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in report.flagged_cases:
            writer.writerow(
                {
                    "pair_id": row["pair_id"],
                    "category": row["category"],
                    "field_changed": row["field_changed"],
                    "job_id": row["job_id"],
                    "rank_a": row["rank_a"],
                    "rank_b": row["rank_b"],
                    "rank_change": row["rank_change"],
                    "score_a": row["score_a"],
                    "score_b": row["score_b"],
                    "score_delta": row["score_delta"],
                    "explanation_drift": row["explanation_drift"],
                    "flag_reasons": "|".join(row.get("flag_reasons", [])),
                }
            )

    paths["markdown"].write_text(render_fairness_audit_markdown(report), encoding="utf-8")
    return paths


def render_fairness_audit_markdown(report: FairnessAuditReport) -> str:
    meta = report.meta
    k = meta["top_k"]
    lines = [
        "# Fairness & Bias Audit: Synthetic Controlled Profiles",
        "",
        f"Generated: {meta['generated_at']}",
        "",
        "> **Offline research only.** {warning}".format(warning=meta["warning"]),
        "",
        "## Setup",
        "",
        f"- Synthetic profile pairs: **{meta['pairs']}**",
        f"- Jobs scored per variant: **{meta['jobs']}**",
        f"- Scoring strategy: `{meta['strategy']}` (production composite weights)",
        f"- Top-K: {k}",
        f"- Score-delta flag threshold: {meta['score_delta_threshold']}",
        f"- Flagged pairs: **{meta['flagged_pairs']}** / {meta['pairs']} "
        f"({meta['flagged_pair_rate']:.0%})",
        "",
        "## Pair summary",
        "",
        "| Pair | Category | Field changed | Top-1 stable | Top-K overlap | Max rank Δ | Max score Δ | Exp drift (top-1) | Flagged |",
        "|------|----------|---------------|--------------|---------------|------------|-------------|-------------------|---------|",
    ]
    for row in report.pair_summaries:
        flag = "yes" if row["flagged"] else "no"
        lines.append(
            f"| {row['pair_id']} | {row['category']} | {row['field_changed']} | "
            f"{'yes' if row['top_1_stable'] else '**no**'} | "
            f"{row['top_k_overlap_count']}/{k} | {row['max_rank_change']} | "
            f"{row['max_score_delta']:.4f} | {row['top1_explanation_drift']:.3f} | {flag} |"
        )

    lines.extend(["", "## Flagged cases", ""])
    if report.flagged_cases:
        seen: set[tuple[str, str]] = set()
        for row in report.flagged_cases:
            key = (row["pair_id"], row["job_id"])
            if key in seen:
                continue
            seen.add(key)
            reasons = ", ".join(row.get("flag_reasons", []))
            lines.append(
                f"- **{row['pair_id']}** / `{row['job_id']}`: rank {row['rank_a']}→{row['rank_b']}, "
                f"Δscore={row['score_delta']:.4f}, expl drift={row['explanation_drift']:.2f}: {reasons}"
            )
    else:
        lines.append("- No cases flagged under current thresholds.")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Demographic-like fields **should not** change rankings when qualifications are identical.",
            "- Non-zero semantic drift is expected when names appear in document text (embedding path).",
            "- Flagged cases warrant manual review, not automatic bias findings.",
            "",
        ]
    )
    return "\n".join(lines)


def print_fairness_audit_summary(report: FairnessAuditReport) -> None:
    print(
        f"\nFairness audit: {report.meta['pairs']} synthetic pairs, "
        f"{report.meta['jobs']} jobs, K={report.meta['top_k']}\n"
    )
    print(f"{'Pair':<22} {'Category':<22} {'Top-1':>6} {'Ovlp':>5} {'MaxRk':>6} {'MaxSc':>7} {'Flag':>5}")
    print("-" * 78)
    for row in report.pair_summaries:
        print(
            f"{row['pair_id']:<22} "
            f"{row['category']:<22} "
            f"{'OK' if row['top_1_stable'] else 'CHG':>6} "
            f"{row['top_k_overlap_count']}/{report.meta['top_k']:>3} "
            f"{row['max_rank_change']:>6} "
            f"{row['max_score_delta']:>7.4f} "
            f"{'yes' if row['flagged'] else 'no':>5}"
        )
    print(
        f"\nFlagged pairs: {report.meta['flagged_pairs']}/{report.meta['pairs']} "
        f"({report.meta['flagged_pair_rate']:.0%})"
    )
