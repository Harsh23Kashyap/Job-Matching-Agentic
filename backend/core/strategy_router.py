"""Agent-triggered strategy selection from candidate profile features."""
from __future__ import annotations

from contracts.snapshots import CandidateSnapshot


def route_strategy(
    candidate: CandidateSnapshot,
    *,
    default_strategy: str = "semantic",
    default_skills_mode: str = "jaccard",
    default_semantic_weight: float = 0.7,
) -> tuple[str, str, float, str]:
    """Return (strategy, skills_mode, semantic_weight, reason)."""
    n_skills = len(candidate.skills)
    summary_len = len(candidate.summary.split())

    if n_skills >= 8:
        return (
            "multimodal",
            "embedding",
            0.65,
            "Skill-rich profile → multimodal soft-embed",
        )
    if n_skills >= 4:
        return (
            "multimodal",
            "jaccard",
            default_semantic_weight,
            "Moderate skills → multimodal Jaccard",
        )
    if summary_len >= 40:
        return (
            "semantic",
            default_skills_mode,
            default_semantic_weight,
            "Sparse skills, rich summary → semantic cosine",
        )
    if n_skills <= 2:
        return (
            "semantic",
            default_skills_mode,
            default_semantic_weight,
            "Very sparse profile → semantic fallback",
        )
    return default_strategy, default_skills_mode, default_semantic_weight, "Default strategy"
