"""Normalized 0–1 component scores for composite match ranking."""
from __future__ import annotations

from contracts.snapshots import CandidateSnapshot, JobSnapshot


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


def location_score(candidate: CandidateSnapshot, job: JobSnapshot) -> float:
    if not candidate.remote_preference:
        return 1.0
    if job.remote_policy:
        return 1.0
    return 0.4
