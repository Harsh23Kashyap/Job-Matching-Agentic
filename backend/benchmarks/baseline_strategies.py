"""Lexical and symbolic baselines for offline research comparison only."""
from __future__ import annotations

from typing import Callable

from contracts.matching import ScoreBreakdown
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.lexical import LexicalRanker
from core.skills import raw_skill_overlap

from benchmarks.rank_utils import rank_exhaustive
from benchmarks.strategies import BenchmarkStrategy


def _exact_skill_overlap_score(candidate: CandidateSnapshot, job: JobSnapshot) -> ScoreBreakdown:
    """Exact normalized token overlap: |intersection| / |required_skills|."""
    overlap = raw_skill_overlap(candidate.skills, job.required_skills)
    required = len(job.required_skills)
    score = len(overlap) / required if required else 0.0
    return ScoreBreakdown(
        semantic_score=0.0,
        skills_score=score,
        final_score=score,
        strategy_used="exact_skill_overlap",
        metric_used="n/a",
        skills_mode_used="exact",
    )


def build_lexical_baselines(
    jobs: list[dict],
    resumes_by_id: dict[str, dict],
    job_snaps: list[JobSnapshot],
    *,
    model_name: str,
) -> list[BenchmarkStrategy]:
    """
    BM25, TF-IDF cosine, and exact skill overlap · no embedding model calls.
    Uses the same document templates as dense retrieval (via LexicalRanker).
    """
    del model_name  # lexical paths do not embed; kept for a uniform builder signature
    ranker = LexicalRanker(jobs)
    corpus_size = len(jobs)

    def resume_rank(method: str) -> Callable[[CandidateSnapshot], list[tuple[str, float]]]:
        def rank(snap: CandidateSnapshot) -> list[tuple[str, float]]:
            resume = resumes_by_id[snap.id]
            return ranker.rank_jobs(resume, method, top_k=corpus_size)

        return rank

    def exhaustive(score_fn: Callable[[CandidateSnapshot, JobSnapshot], ScoreBreakdown]):
        return lambda snap: rank_exhaustive(snap, job_snaps, score_fn)

    return [
        BenchmarkStrategy(
            key="bm25",
            label="BM25 (lexical)",
            description="BM25 over resume/job document templates (same text as dense retrieval).",
            rank_fn=resume_rank("bm25"),
            contributes_to_rrf=False,
        ),
        BenchmarkStrategy(
            key="tfidf_cosine",
            label="TF-IDF cosine (lexical)",
            description="TF-IDF weighted cosine similarity on tokenized document templates.",
            rank_fn=resume_rank("tfidf"),
            contributes_to_rrf=False,
        ),
        BenchmarkStrategy(
            key="exact_skill_overlap",
            label="Exact skill overlap",
            description="Fraction of required job skills matched exactly (normalized string equality).",
            rank_fn=exhaustive(_exact_skill_overlap_score),
            contributes_to_rrf=False,
        ),
    ]


def build_all_strategies(
    jobs: list[dict],
    resumes_by_id: dict[str, dict],
    job_snaps: list[JobSnapshot],
    *,
    model_name: str,
    semantic_weight: float = 0.7,
    rrf_k: int = 60,
    include_lexical_baselines: bool = True,
) -> list[BenchmarkStrategy]:
    """Lexical baselines first, then embedding-based strategies (offline benchmark only)."""
    from benchmarks.strategies import build_strategies

    strategies: list[BenchmarkStrategy] = []
    if include_lexical_baselines:
        strategies.extend(build_lexical_baselines(jobs, resumes_by_id, job_snaps, model_name=model_name))
    strategies.extend(
        build_strategies(
            job_snaps,
            model_name=model_name,
            semantic_weight=semantic_weight,
            rrf_k=rrf_k,
        )
    )
    return strategies
