"""Explainability evaluation runner — offline research only."""
from __future__ import annotations

import csv
import json
import statistics
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from config import Settings
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.scoring import compute_composite
from hooks.explainer import RuleExplainer
from hooks.grounded_explainer import GroundedLlmExplainer

from benchmarks.eval_data import cv_to_snapshot, job_to_snapshot
from benchmarks.explainability_checks import (
    ExplanationAudit,
    audit_explanation,
    consistency_between_profiles,
)
from benchmarks.fairness_profiles import build_pair_snapshots, load_audit_profiles
from benchmarks.rank_utils import rank_exhaustive


INSTANCE_CSV_FIELDS = [
    "candidate_id",
    "job_id",
    "explain_mode",
    "rank",
    "faithfulness_score",
    "specificity_score",
    "mentions_matched_or_missing_skill",
    "no_hallucinated_skills",
    "component_claims_valid",
    "has_specific_skill_reference",
    "flagged",
    "violations",
    "hallucinated_skills",
    "matched_skills",
    "missing_skills",
    "bullets",
]

CONSISTENCY_CSV_FIELDS = [
    "pair_id",
    "category",
    "job_id",
    "explain_mode",
    "jaccard_similarity",
    "drift_score",
    "same_matched_skills",
    "consistent",
    "flagged",
]


@dataclass
class ExplainabilityReport:
    meta: dict[str, Any]
    instances: list[dict[str, Any]]
    consistency: list[dict[str, Any]]
    summary: dict[str, Any]


def _build_skill_vocabulary(resumes: list[dict], jobs: list[dict]) -> list[str]:
    skills: set[str] = set()
    for cv in resumes:
        skills.update(cv.get("skills", []))
    for job in jobs:
        skills.update(job.get("required_skills", []))
        skills.update(job.get("preferred_skills", []))
    return sorted(skills, key=lambda s: len(s), reverse=True)


def _explainer_fn(mode: str, settings: Settings) -> Callable[..., list[str]]:
    if mode == "rules":
        explainer = RuleExplainer()
        return explainer.explain
    if mode == "template":
        grounded = GroundedLlmExplainer(settings)
        return grounded._template_explain
    raise ValueError(f"Unknown explain mode: {mode}")


class ExplainabilityEval:
    """Evaluate rule/template explanations on eval corpus + synthetic similar pairs."""

    def __init__(
        self,
        *,
        settings: Settings | None = None,
        data_dir: Path | None = None,
        profiles_path: Path | None = None,
        top_k: int = 5,
        explain_modes: list[str] | None = None,
        consistency_min_jaccard: float = 0.5,
    ) -> None:
        self.settings = settings or Settings()
        self.data_dir = Path(data_dir or self.settings.data_dir)
        self.profiles_path = Path(profiles_path or self.data_dir / "fairness_audit_profiles.json")
        self.top_k = top_k
        self.explain_modes = explain_modes or ["rules", "template"]
        self.consistency_min_jaccard = consistency_min_jaccard

    def run(self) -> ExplainabilityReport:
        resumes = json.loads((self.data_dir / "cvs.json").read_text(encoding="utf-8"))
        jobs_raw = json.loads((self.data_dir / "jobs.json").read_text(encoding="utf-8"))
        model_name = self.settings.embedding_model
        vocabulary = _build_skill_vocabulary(resumes, jobs_raw)

        job_snaps = [job_to_snapshot(j, model_name) for j in jobs_raw]
        cv_snaps = {r["id"]: cv_to_snapshot(r, model_name) for r in resumes}
        job_by_id = {j.id: j for j in job_snaps}

        instances: list[dict[str, Any]] = []
        consistency_rows: list[dict[str, Any]] = []

        score_fn = lambda c, j: compute_composite(c, j, model_name=model_name)

        for mode in self.explain_modes:
            explain = _explainer_fn(mode, self.settings)

            for cv in resumes:
                qid = cv["id"]
                if qid not in cv_snaps:
                    continue
                cand = cv_snaps[qid]
                ranked = rank_exhaustive(cand, job_snaps, score_fn)
                for rank, (job_id, _) in enumerate(ranked[: self.top_k], start=1):
                    job = job_by_id[job_id]
                    breakdown = score_fn(cand, job)
                    bullets = explain(cand, job, breakdown)
                    audit = audit_explanation(
                        candidate=cand,
                        job=job,
                        breakdown=breakdown,
                        bullets=bullets,
                        explain_mode=mode,
                        vocabulary=vocabulary,
                    )
                    instances.append(_audit_to_row(audit, rank=rank))

        if self.profiles_path.is_file():
            payload = load_audit_profiles(self.profiles_path)
            for pair in payload["pairs"]:
                pair_meta, snap_a, snap_b = build_pair_snapshots(pair, model_name)
                for mode in self.explain_modes:
                    explain = _explainer_fn(mode, self.settings)
                    ranked_a = rank_exhaustive(snap_a, job_snaps, score_fn)
                    if not ranked_a:
                        continue
                    top_job_id = ranked_a[0][0]
                    job = job_by_id[top_job_id]
                    bd_a = score_fn(snap_a, job)
                    bd_b = score_fn(snap_b, job)
                    audit_a = audit_explanation(
                        candidate=snap_a,
                        job=job,
                        breakdown=bd_a,
                        bullets=explain(snap_a, job, bd_a),
                        explain_mode=mode,
                        vocabulary=vocabulary,
                    )
                    audit_b = audit_explanation(
                        candidate=snap_b,
                        job=job,
                        breakdown=bd_b,
                        bullets=explain(snap_b, job, bd_b),
                        explain_mode=mode,
                        vocabulary=vocabulary,
                    )
                    cons = consistency_between_profiles(
                        audit_a, audit_b, min_jaccard=self.consistency_min_jaccard
                    )
                    flagged = not cons["consistent"]
                    consistency_rows.append(
                        {
                            "pair_id": pair_meta["pair_id"],
                            "category": pair_meta["category"],
                            "field_changed": pair_meta["field_changed"],
                            "job_id": top_job_id,
                            "explain_mode": mode,
                            **cons,
                            "flagged": flagged,
                        }
                    )

        summary = _aggregate_summary(instances, consistency_rows)
        meta = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "report_type": "explainability_evaluation",
            "offline_only": True,
            "candidates": len(resumes),
            "jobs": len(jobs_raw),
            "top_k": self.top_k,
            "explain_modes": self.explain_modes,
            "strategy": "composite",
            "embedding_model": model_name,
            "instances_evaluated": len(instances),
            "consistency_pairs": len(consistency_rows),
            "automated_checks": [
                "mentions_matched_or_missing_skill",
                "no_hallucinated_skills",
                "component_claims_valid",
                "has_specific_skill_reference",
            ],
            "dimensions": [
                "faithfulness",
                "consistency",
                "specificity",
                "hallucination",
            ],
            **summary,
        }
        return ExplainabilityReport(
            meta=meta,
            instances=instances,
            consistency=consistency_rows,
            summary=summary,
        )


def _audit_to_row(audit: ExplanationAudit, *, rank: int) -> dict[str, Any]:
    return {
        "candidate_id": audit.candidate_id,
        "job_id": audit.job_id,
        "explain_mode": audit.explain_mode,
        "rank": rank,
        "faithfulness_score": audit.faithfulness_score,
        "specificity_score": audit.specificity_score,
        "mentions_matched_or_missing_skill": audit.checks["mentions_matched_or_missing_skill"],
        "no_hallucinated_skills": audit.checks["no_hallucinated_skills"],
        "component_claims_valid": audit.checks["component_claims_valid"],
        "has_specific_skill_reference": audit.checks["has_specific_skill_reference"],
        "flagged": audit.flagged,
        "violations": audit.violations,
        "hallucinated_skills": audit.hallucinated_skills,
        "matched_skills": audit.matched_skills,
        "missing_skills": audit.missing_skills,
        "mentioned_skills": audit.mentioned_skills,
        "component_alignment": audit.component_alignment,
        "bullets": audit.bullets,
    }


def _aggregate_summary(
    instances: list[dict[str, Any]],
    consistency: list[dict[str, Any]],
) -> dict[str, Any]:
    if not instances:
        return {}

    by_mode: dict[str, list[dict[str, Any]]] = {}
    for row in instances:
        by_mode.setdefault(row["explain_mode"], []).append(row)

    mode_stats: dict[str, Any] = {}
    for mode, rows in by_mode.items():
        mode_stats[mode] = {
            "count": len(rows),
            "flagged": sum(1 for r in rows if r["flagged"]),
            "flagged_rate": round(sum(1 for r in rows if r["flagged"]) / len(rows), 4),
            "avg_faithfulness": round(statistics.mean(r["faithfulness_score"] for r in rows), 4),
            "avg_specificity": round(statistics.mean(r["specificity_score"] for r in rows), 4),
            "pass_mentions_skill": round(
                sum(1 for r in rows if r["mentions_matched_or_missing_skill"]) / len(rows), 4
            ),
            "pass_no_hallucination": round(
                sum(1 for r in rows if r["no_hallucinated_skills"]) / len(rows), 4
            ),
            "pass_component_alignment": round(
                sum(1 for r in rows if r["component_claims_valid"]) / len(rows), 4
            ),
        }

    cons_by_mode: dict[str, Any] = {}
    if consistency:
        for mode in {r["explain_mode"] for r in consistency}:
            rows = [r for r in consistency if r["explain_mode"] == mode]
            cons_by_mode[mode] = {
                "pairs": len(rows),
                "consistent": sum(1 for r in rows if r["consistent"]),
                "consistent_rate": round(sum(1 for r in rows if r["consistent"]) / len(rows), 4),
                "avg_jaccard": round(statistics.mean(r["jaccard_similarity"] for r in rows), 4),
            }

    flagged_instances = [r for r in instances if r["flagged"]]

    return {
        "by_mode": mode_stats,
        "consistency_by_mode": cons_by_mode,
        "total_flagged_instances": len(flagged_instances),
        "hallucination_count": sum(1 for r in instances if not r["no_hallucinated_skills"]),
    }


def write_explainability_report(
    report: ExplainabilityReport,
    out_dir: Path,
    *,
    prefix: str = "explainability",
) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "json": out_dir / f"{prefix}_report.json",
        "markdown": out_dir / f"{prefix}_summary.md",
        "instances_csv": out_dir / f"{prefix}_instances.csv",
        "flagged_csv": out_dir / f"{prefix}_flagged.csv",
        "consistency_csv": out_dir / f"{prefix}_consistency.csv",
    }

    flagged = [r for r in report.instances if r["flagged"]]

    paths["json"].write_text(
        json.dumps(
            {
                "meta": report.meta,
                "summary": report.summary,
                "flagged_instances": flagged,
                "consistency": report.consistency,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    with paths["instances_csv"].open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=INSTANCE_CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in report.instances:
            out = dict(row)
            out["violations"] = "|".join(row.get("violations", []))
            out["hallucinated_skills"] = "|".join(row.get("hallucinated_skills", []))
            out["matched_skills"] = "|".join(row.get("matched_skills", []))
            out["missing_skills"] = "|".join(row.get("missing_skills", []))
            out["bullets"] = " || ".join(row.get("bullets", []))
            writer.writerow(out)

    with paths["flagged_csv"].open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=INSTANCE_CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in flagged:
            out = dict(row)
            out["violations"] = "|".join(row.get("violations", []))
            out["hallucinated_skills"] = "|".join(row.get("hallucinated_skills", []))
            out["matched_skills"] = "|".join(row.get("matched_skills", []))
            out["missing_skills"] = "|".join(row.get("missing_skills", []))
            out["bullets"] = " || ".join(row.get("bullets", []))
            writer.writerow(out)

    with paths["consistency_csv"].open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=CONSISTENCY_CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in report.consistency:
            writer.writerow({k: row.get(k) for k in CONSISTENCY_CSV_FIELDS})

    paths["markdown"].write_text(render_explainability_markdown(report), encoding="utf-8")
    return paths


def render_explainability_markdown(report: ExplainabilityReport) -> str:
    meta = report.meta
    lines = [
        "# Explainability Evaluation — Match Explanations",
        "",
        f"Generated: {meta['generated_at']}",
        "",
        "> Offline research only. Evaluates rule-based and template-grounded explainers.",
        "",
        "## Setup",
        "",
        f"- Instances: {meta['instances_evaluated']} ({meta['candidates']} candidates × top-{meta['top_k']} jobs × {len(meta['explain_modes'])} modes)",
        f"- Scoring: `{meta['strategy']}`",
        f"- Explain modes: {', '.join(meta['explain_modes'])}",
        f"- Consistency pairs (synthetic): {meta['consistency_pairs']}",
        "",
        "## Automated checks",
        "",
        "1. Must mention at least one matched or missing skill",
        "2. Must not mention skills absent from both candidate and job",
        "3. Textual claims must align with score components",
        "4. Specificity: concrete skill references vs generic-only bullets",
        "",
        "## Results by explainer mode",
        "",
        "| Mode | Flagged | Avg faithfulness | Avg specificity | Pass skill mention | Pass no hallucination | Pass component align |",
        "|------|---------|------------------|-----------------|--------------------|-----------------------|----------------------|",
    ]
    for mode, stats in meta.get("by_mode", {}).items():
        lines.append(
            f"| {mode} | {stats['flagged']}/{stats['count']} ({stats['flagged_rate']:.0%}) | "
            f"{stats['avg_faithfulness']:.3f} | {stats['avg_specificity']:.3f} | "
            f"{stats['pass_mentions_skill']:.0%} | {stats['pass_no_hallucination']:.0%} | "
            f"{stats['pass_component_alignment']:.0%} |"
        )

    lines.extend(["", "## Consistency (synthetic similar profiles)", ""])
    for mode, stats in meta.get("consistency_by_mode", {}).items():
        lines.append(
            f"- **{mode}:** {stats['consistent']}/{stats['pairs']} pairs consistent "
            f"(avg Jaccard={stats['avg_jaccard']:.3f})"
        )

    flagged = [r for r in report.instances if r["flagged"]][:15]
    lines.extend(["", "## Sample flagged instances", ""])
    if flagged:
        for row in flagged:
            v = ", ".join(row.get("violations", []))
            lines.append(
                f"- `{row['candidate_id']}` × `{row['job_id']}` ({row['explain_mode']}, rank {row['rank']}): "
                f"{v}"
            )
    else:
        lines.append("- None flagged.")

    lines.append("")
    return "\n".join(lines)


def print_explainability_summary(report: ExplainabilityReport) -> None:
    print(f"\nExplainability eval — {report.meta['instances_evaluated']} instances\n")
    for mode, stats in report.meta.get("by_mode", {}).items():
        print(
            f"  [{mode}] flagged={stats['flagged']}/{stats['count']} "
            f"faithfulness={stats['avg_faithfulness']:.3f} "
            f"specificity={stats['avg_specificity']:.3f} "
            f"skill_mention={stats['pass_mentions_skill']:.0%} "
            f"no_halluc={stats['pass_no_hallucination']:.0%}"
        )
    print(f"\nTotal flagged: {report.meta.get('total_flagged_instances', 0)}")
