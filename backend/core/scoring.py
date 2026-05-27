import numpy as np

from contracts.matching import ScoreBreakdown
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.component_scores import compensation_score, experience_score, location_score
from core.similarity import compute_similarity
from core.skills import skills_score

COMPOSITE_WEIGHTS = {
    "semantic": 0.40,
    "skills": 0.30,
    "experience": 0.15,
    "compensation": 0.10,
    "location": 0.05,
}


def compute_semantic(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    metric: str = "cosine",
) -> ScoreBreakdown:
    c_vec = np.asarray(candidate.embedding, dtype=np.float32)
    j_vec = np.asarray(job.embedding, dtype=np.float32)
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
    exp = experience_score(candidate, job)
    comp = compensation_score(candidate, job)
    loc = location_score(candidate, job)

    final = (
        COMPOSITE_WEIGHTS["semantic"] * semantic
        + COMPOSITE_WEIGHTS["skills"] * skills
        + COMPOSITE_WEIGHTS["experience"] * exp
        + COMPOSITE_WEIGHTS["compensation"] * comp
        + COMPOSITE_WEIGHTS["location"] * loc
    )
    final = max(0.0, min(1.0, final))

    return ScoreBreakdown(
        semantic_score=semantic,
        skills_score=skills,
        experience_score=exp,
        compensation_score=comp,
        location_score=loc,
        final_score=final,
        strategy_used="composite",
        metric_used=metric,
        skills_mode_used=skills_mode,
        fusion_mode_used="fixed",
    )
