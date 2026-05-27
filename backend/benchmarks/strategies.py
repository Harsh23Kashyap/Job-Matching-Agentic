"""Benchmark-only retrieval strategies — isolated from production match routing."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from contracts.matching import ScoreBreakdown
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.scoring import compute_multimodal_weighted
from core.skills import skills_score

from benchmarks.rank_utils import rank_exhaustive, rrf_fuse_lists, semantic_score


@dataclass(frozen=True)
class BenchmarkStrategy:
    """One exhaustive ranking method for offline evaluation."""

    key: str
    label: str
    description: str
    rank_fn: Callable[[CandidateSnapshot], list[tuple[str, float]]]
    contributes_to_rrf: bool = True


def _skills_only_score(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    *,
    skills_mode: str,
    model_name: str,
) -> ScoreBreakdown:
    score = skills_score(candidate.skills, job.required_skills, skills_mode, model_name)
    return ScoreBreakdown(
        semantic_score=0.0,
        skills_score=score,
        final_score=score,
        strategy_used=f"skills_{skills_mode}",
        metric_used="n/a",
        skills_mode_used=skills_mode,
    )


def build_strategies(
    job_snaps: list[JobSnapshot],
    *,
    model_name: str,
    semantic_weight: float = 0.7,
    rrf_k: int = 60,
) -> list[BenchmarkStrategy]:
    """Register research strategies requested for JobMatch benchmark suite."""

    def exhaustive(score_fn: Callable[[CandidateSnapshot, JobSnapshot], ScoreBreakdown]):
        return lambda snap: rank_exhaustive(snap, job_snaps, score_fn)

    base: list[BenchmarkStrategy] = [
        BenchmarkStrategy(
            key="semantic_cosine",
            label="Semantic cosine",
            description="Bi-encoder cosine similarity on document embeddings.",
            rank_fn=exhaustive(lambda c, j: semantic_score(c, j, "cosine")),
        ),
        BenchmarkStrategy(
            key="semantic_euclidean",
            label="Semantic euclidean-derived",
            description="1 / (1 + L2 distance) on document embeddings.",
            rank_fn=exhaustive(lambda c, j: semantic_score(c, j, "euclidean")),
        ),
        BenchmarkStrategy(
            key="skills_jaccard",
            label="Skills Jaccard",
            description="Jaccard overlap on canonicalized required skills (skills-only signal).",
            rank_fn=exhaustive(
                lambda c, j: _skills_only_score(c, j, skills_mode="jaccard", model_name=model_name)
            ),
        ),
        BenchmarkStrategy(
            key="soft_skill_embed",
            label="Soft skill embedding",
            description="Mean max cosine between required job skills and resume skill embeddings.",
            rank_fn=exhaustive(
                lambda c, j: _skills_only_score(c, j, skills_mode="embedding", model_name=model_name)
            ),
        ),
        BenchmarkStrategy(
            key="multimodal_weighted",
            label="Multimodal weighted blend",
            description=f"Weighted blend: semantic_weight={semantic_weight}, skills_mode=jaccard.",
            rank_fn=exhaustive(
                lambda c, j: compute_multimodal_weighted(
                    c,
                    j,
                    metric="cosine",
                    semantic_weight=semantic_weight,
                    skills_mode="jaccard",
                    model_name=model_name,
                )
            ),
        ),
    ]

    def rrf_rank(snap: CandidateSnapshot) -> list[tuple[str, float]]:
        lists = [strategy.rank_fn(snap) for strategy in base if strategy.contributes_to_rrf]
        return rrf_fuse_lists(lists, k=rrf_k)

    ensemble = BenchmarkStrategy(
        key="rrf_ensemble",
        label="RRF ensemble",
        description=f"Reciprocal rank fusion (k={rrf_k}) over the five base rankers above.",
        rank_fn=rrf_rank,
        contributes_to_rrf=False,
    )
    return base + [ensemble]
