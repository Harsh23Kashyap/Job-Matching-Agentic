"""Ablation scoring variants — offline research only; production uses compute_composite."""
from __future__ import annotations

from typing import Callable

from contracts.matching import ScoreBreakdown
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.component_scores import compensation_score, experience_score, location_score
from core.scoring import COMPOSITE_WEIGHTS, compute_composite, compute_semantic
from core.skills import skills_score


def _clamp(score: float) -> float:
    return max(0.0, min(1.0, score))


def _single_component_breakdown(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    *,
    key: str,
    value: float,
    metric: str = "cosine",
    skills_mode: str = "jaccard",
) -> ScoreBreakdown:
    kwargs = {
        "semantic_score": value if key == "semantic" else 0.0,
        "skills_score": value if key == "skills" else None,
        "experience_score": value if key == "experience" else None,
        "compensation_score": value if key == "compensation" else None,
        "location_score": value if key == "location" else None,
        "final_score": value,
        "strategy_used": f"{key}_only",
        "metric_used": metric if key == "semantic" else "n/a",
        "skills_mode_used": skills_mode if key == "skills" else None,
    }
    return ScoreBreakdown(**kwargs)


def semantic_only(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    metric: str = "cosine",
    skills_mode: str = "jaccard",
    model_name: str = "all-MiniLM-L6-v2",
) -> ScoreBreakdown:
    del skills_mode, model_name
    return compute_semantic(candidate, job, metric)


def skills_only(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    metric: str = "cosine",
    skills_mode: str = "jaccard",
    model_name: str = "all-MiniLM-L6-v2",
) -> ScoreBreakdown:
    del metric
    val = skills_score(candidate.skills, job.required_skills, skills_mode, model_name)
    return _single_component_breakdown(candidate, job, key="skills", value=val, skills_mode=skills_mode)


def experience_only(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    metric: str = "cosine",
    skills_mode: str = "jaccard",
    model_name: str = "all-MiniLM-L6-v2",
) -> ScoreBreakdown:
    del metric, skills_mode, model_name
    val = experience_score(candidate, job)
    return _single_component_breakdown(candidate, job, key="experience", value=val)


def compensation_only(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    metric: str = "cosine",
    skills_mode: str = "jaccard",
    model_name: str = "all-MiniLM-L6-v2",
) -> ScoreBreakdown:
    del metric, skills_mode, model_name
    val = compensation_score(candidate, job)
    return _single_component_breakdown(candidate, job, key="compensation", value=val)


def location_only(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    metric: str = "cosine",
    skills_mode: str = "jaccard",
    model_name: str = "all-MiniLM-L6-v2",
) -> ScoreBreakdown:
    del metric, skills_mode, model_name
    val = location_score(candidate, job)
    return _single_component_breakdown(candidate, job, key="location", value=val)


def _partial_composite(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    components: list[str],
    *,
    metric: str = "cosine",
    skills_mode: str = "jaccard",
    model_name: str = "all-MiniLM-L6-v2",
) -> ScoreBreakdown:
    getters: dict[str, Callable[[CandidateSnapshot, JobSnapshot], float]] = {
        "semantic": lambda c, j: compute_semantic(c, j, metric).semantic_score,
        "skills": lambda c, j: skills_score(c.skills, j.required_skills, skills_mode, model_name),
        "experience": experience_score,
        "compensation": compensation_score,
        "location": location_score,
    }
    raw_weights = {k: COMPOSITE_WEIGHTS[k] for k in components}
    total = sum(raw_weights.values())
    values = {k: getters[k](candidate, job) for k in components}
    final = sum(raw_weights[k] / total * values[k] for k in components)
    label = "+".join(components)
    return ScoreBreakdown(
        semantic_score=values.get("semantic"),
        skills_score=values.get("skills"),
        experience_score=values.get("experience"),
        compensation_score=values.get("compensation"),
        location_score=values.get("location"),
        final_score=_clamp(final),
        strategy_used=f"ablation_{label}",
        metric_used=metric,
        skills_mode_used=skills_mode if "skills" in components else None,
        fusion_mode_used="renormalized_partial",
    )


def semantic_skills(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    metric: str = "cosine",
    skills_mode: str = "jaccard",
    model_name: str = "all-MiniLM-L6-v2",
) -> ScoreBreakdown:
    return _partial_composite(
        candidate, job, ["semantic", "skills"], metric=metric, skills_mode=skills_mode, model_name=model_name
    )


def semantic_skills_experience(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    metric: str = "cosine",
    skills_mode: str = "jaccard",
    model_name: str = "all-MiniLM-L6-v2",
) -> ScoreBreakdown:
    return _partial_composite(
        candidate,
        job,
        ["semantic", "skills", "experience"],
        metric=metric,
        skills_mode=skills_mode,
        model_name=model_name,
    )


def full_composite(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    metric: str = "cosine",
    skills_mode: str = "jaccard",
    model_name: str = "all-MiniLM-L6-v2",
) -> ScoreBreakdown:
    return compute_composite(candidate, job, metric=metric, skills_mode=skills_mode, model_name=model_name)
