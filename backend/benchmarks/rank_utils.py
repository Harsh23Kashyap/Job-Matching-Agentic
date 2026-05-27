"""Ranking helpers for exhaustive benchmark evaluation."""
from __future__ import annotations

from collections import defaultdict
from typing import Callable

from contracts.matching import ScoreBreakdown
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.scoring import compute_multimodal_weighted, compute_semantic


def rank_exhaustive(
    candidate: CandidateSnapshot,
    jobs: list[JobSnapshot],
    score_fn: Callable[[CandidateSnapshot, JobSnapshot], ScoreBreakdown],
) -> list[tuple[str, float]]:
    scored = []
    for job in jobs:
        breakdown = score_fn(candidate, job)
        scored.append((job.id, breakdown.final_score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


def semantic_score(candidate: CandidateSnapshot, job: JobSnapshot, metric: str = "cosine") -> ScoreBreakdown:
    return compute_semantic(candidate, job, metric)


def multimodal_score(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    *,
    metric: str = "cosine",
    semantic_weight: float = 0.7,
    skills_mode: str = "jaccard",
    model_name: str = "all-MiniLM-L6-v2",
) -> ScoreBreakdown:
    return compute_multimodal_weighted(
        candidate,
        job,
        metric=metric,
        semantic_weight=semantic_weight,
        skills_mode=skills_mode,
        model_name=model_name,
    )


def rrf_fuse_lists(lists: list[list[tuple[str, float]]], k: int = 60) -> list[tuple[str, float]]:
    scores: dict[str, float] = defaultdict(float)
    for ranked in lists:
        for rank, (doc_id, _) in enumerate(ranked, start=1):
            scores[doc_id] += 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
