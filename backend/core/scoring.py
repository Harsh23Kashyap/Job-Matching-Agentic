import numpy as np

from contracts.matching import ScoreBreakdown, ScoreComponentDetail
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.component_scores import (
    compensation_score,
    experience_score,
    remote_preference_score,
    title_similarity_score,
)
from core.similarity import compute_similarity
from core.skills import skills_score

COMPOSITE_WEIGHTS = {
    "semantic": 0.28,
    "skills": 0.27,
    "title": 0.10,
    "experience": 0.15,
    "compensation": 0.10,
    "remote": 0.10,
}

COMPOSITE_COMPONENT_SPECS: tuple[tuple[str, str, str], ...] = (
    ("semantic", "semantic_score", "Semantic fit"),
    ("skills", "skills_score", "Skills overlap"),
    ("title", "title_score", "Role title fit"),
    ("experience", "experience_score", "Experience"),
    ("compensation", "compensation_score", "Compensation"),
    ("remote", "remote_score", "Remote preference"),
)


def build_composite_components(breakdown: ScoreBreakdown) -> list[ScoreComponentDetail]:
    components: list[ScoreComponentDetail] = []
    for weight_key, score_attr, label in COMPOSITE_COMPONENT_SPECS:
        score = getattr(breakdown, score_attr, None)
        if score is None:
            continue
        weight = COMPOSITE_WEIGHTS[weight_key]
        components.append(
            ScoreComponentDetail(
                key=weight_key,
                label=label,
                weight=weight,
                score=float(score),
                contribution=weight * float(score),
            )
        )
    return components


def _safe_vec(values) -> np.ndarray:
    """Coerce an embedding to a finite float32 vector; non-finite entries (NaN/inf from a
    corrupted upstream embedding) are zeroed so they cannot score as a spurious perfect match."""
    vec = np.asarray(values, dtype=np.float32)
    if not np.all(np.isfinite(vec)):
        vec = np.nan_to_num(vec, nan=0.0, posinf=0.0, neginf=0.0)
    return vec


def compute_semantic(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    metric: str = "cosine",
) -> ScoreBreakdown:
    c_vec = _safe_vec(candidate.embedding)
    j_vec = _safe_vec(job.embedding)
    sem = compute_similarity(c_vec, j_vec, metric)
    return ScoreBreakdown(
        semantic_score=sem,
        skills_score=None,
        final_score=sem,
        strategy_used="semantic",
        metric_used=metric,
        skills_mode_used=None,
    )


def compute_multimodal_weighted(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    metric: str = "cosine",
    semantic_weight: float = 0.7,
    skills_mode: str = "jaccard",
    model_name: str = "all-MiniLM-L6-v2",
) -> ScoreBreakdown:
    if not 0.0 <= semantic_weight <= 1.0:
        raise ValueError("semantic_weight must be between 0 and 1")
    sem_result = compute_semantic(candidate, job, metric)
    skills = skills_score(
        candidate.skills,
        job.required_skills,
        skills_mode=skills_mode,
        model_name=model_name,
    )
    final = semantic_weight * sem_result.semantic_score + (1.0 - semantic_weight) * skills
    return ScoreBreakdown(
        semantic_score=sem_result.semantic_score,
        skills_score=skills,
        final_score=final,
        strategy_used="multimodal",
        metric_used=metric,
        skills_mode_used=skills_mode,
    )


def compute_composite(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    metric: str = "cosine",
    skills_mode: str = "jaccard",
    model_name: str = "all-MiniLM-L6-v2",
) -> ScoreBreakdown:
    sem_result = compute_semantic(candidate, job, metric)
    semantic = sem_result.semantic_score
    skills = skills_score(
        candidate.skills,
        job.required_skills,
        skills_mode=skills_mode,
        model_name=model_name,
    )
    title = title_similarity_score(candidate, job)
    exp = experience_score(candidate, job)
    comp = compensation_score(candidate, job)
    remote = remote_preference_score(candidate, job)

    final = (
        COMPOSITE_WEIGHTS["semantic"] * semantic
        + COMPOSITE_WEIGHTS["skills"] * skills
        + COMPOSITE_WEIGHTS["title"] * title
        + COMPOSITE_WEIGHTS["experience"] * exp
        + COMPOSITE_WEIGHTS["compensation"] * comp
        + COMPOSITE_WEIGHTS["remote"] * remote
    )
    final = max(0.0, min(1.0, final))

    breakdown = ScoreBreakdown(
        semantic_score=semantic,
        skills_score=skills,
        title_score=title,
        experience_score=exp,
        compensation_score=comp,
        location_score=remote,
        remote_score=remote,
        final_score=final,
        strategy_used="composite",
        metric_used=metric,
        skills_mode_used=skills_mode,
        fusion_mode_used="fixed",
    )
    return breakdown.model_copy(update={"score_components": build_composite_components(breakdown)})
