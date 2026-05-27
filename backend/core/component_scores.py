"""Normalized 0–1 component scores for composite match ranking."""
from __future__ import annotations

from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.text_tokenizer import tokenize

_TITLE_STOPWORDS = frozenset(
    {
        "a",
        "an",
        "the",
        "and",
        "or",
        "of",
        "for",
        "to",
        "in",
        "at",
        "with",
        "senior",
        "junior",
        "lead",
        "staff",
        "principal",
        "associate",
        "level",
        "i",
        "ii",
        "iii",
        "iv",
        "v",
        "sr",
        "jr",
    }
)


def _meaningful_tokens(text: str) -> set[str]:
    return {token for token in tokenize(text) if token not in _TITLE_STOPWORDS and len(token) > 1}


def experience_score(candidate: CandidateSnapshot, job: JobSnapshot) -> float:
    gap = float(job.required_experience) - float(candidate.experience_years)
    if gap <= 0:
        return 1.0
    if gap <= 1:
        return 0.8
    if gap <= 2:
        return 0.6
    if gap <= 3:
        return 0.4
    return 0.2


def _job_budget_bounds(job: JobSnapshot) -> tuple[int | None, int | None]:
    budget_min = job.budget_min if job.budget_min is not None else job.budget
    budget_max = job.budget_max if job.budget_max is not None else job.budget
    return budget_min, budget_max


def compensation_score(candidate: CandidateSnapshot, job: JobSnapshot) -> float:
    expected = candidate.preferred_salary
    budget_min, budget_max = _job_budget_bounds(job)
    if expected is None or (budget_min is None and budget_max is None):
        return 1.0
    if budget_min is not None and budget_max is not None:
        if budget_min <= expected <= budget_max:
            return 1.0
        if expected < budget_min:
            return 0.95
        overshoot = (expected - budget_max) / max(budget_max, 1)
    elif budget_max is not None:
        if expected <= budget_max:
            return 1.0
        overshoot = (expected - budget_max) / max(budget_max, 1)
    elif budget_min is not None:
        if expected >= budget_min:
            return 1.0
        undershoot = (budget_min - expected) / max(budget_min, 1)
        if undershoot <= 0.1:
            return 0.9
        if undershoot <= 0.25:
            return 0.75
        return 0.6
    else:
        return 1.0

    if overshoot <= 0.05:
        return 0.92
    if overshoot <= 0.1:
        return 0.85
    if overshoot <= 0.25:
        return 0.65
    return 0.4


def remote_preference_score(candidate: CandidateSnapshot, job: JobSnapshot) -> float:
    if not candidate.remote_preference:
        return 1.0
    if job.remote_policy:
        return 1.0
    return 0.4


def location_score(candidate: CandidateSnapshot, job: JobSnapshot) -> float:
    """Backward-compatible alias for remote/work-setup alignment."""
    return remote_preference_score(candidate, job)


def title_similarity_score(candidate: CandidateSnapshot, job: JobSnapshot) -> float:
    """Overlap between job title tokens and candidate summary + skills."""
    title_tokens = _meaningful_tokens(job.title)
    if not title_tokens:
        return 1.0

    candidate_text = candidate.summary or ""
    if candidate.skills:
        candidate_text = f"{candidate_text} {' '.join(candidate.skills)}"
    candidate_tokens = _meaningful_tokens(candidate_text)
    if not candidate_tokens:
        return 0.35

    overlap = title_tokens & candidate_tokens
    if not overlap:
        return 0.15

    coverage = len(overlap) / len(title_tokens)
    jaccard = len(overlap) / len(title_tokens | candidate_tokens)
    return max(0.0, min(1.0, 0.6 * coverage + 0.4 * jaccard))
