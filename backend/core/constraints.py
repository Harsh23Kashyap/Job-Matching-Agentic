"""Constraint-aware adjustments for hiring feasibility."""
from __future__ import annotations

from contracts.matching import ScoreBreakdown
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.skills import skill_overlap_details


def experience_factor(candidate: CandidateSnapshot, job: JobSnapshot) -> tuple[float, str | None]:
    gap = job.required_experience - candidate.experience_years
    if gap <= 0:
        return 1.0, None
    if gap <= 1:
        return 0.92, f"Experience gap: {gap:.1f} years below requirement"
    if gap <= 2:
        return 0.82, f"Experience gap: {gap:.1f} years below requirement"
    return 0.65, f"Experience gap: {gap:.1f} years below requirement"


def remote_factor(candidate: CandidateSnapshot, job: JobSnapshot) -> tuple[float, str | None]:
    if not candidate.remote_preference:
        return 1.0, None
    if job.remote_policy:
        return 1.0, None
    return 0.75, "Candidate prefers remote; role is on-site"


def salary_factor(candidate: CandidateSnapshot, job: JobSnapshot) -> tuple[float, str | None]:
    if candidate.preferred_salary is None or job.budget is None:
        return 1.0, None
    if candidate.preferred_salary <= job.budget:
        return 1.0, None
    overshoot = (candidate.preferred_salary - job.budget) / max(job.budget, 1)
    if overshoot <= 0.1:
        return 0.95, "Salary expectation slightly above budget"
    if overshoot <= 0.25:
        return 0.85, "Salary expectation above budget"
    return 0.7, "Salary expectation well above budget"


def must_have_coverage(candidate: CandidateSnapshot, job: JobSnapshot) -> tuple[float, list[str]]:
    matched, missing = skill_overlap_details(candidate.skills, job.required_skills)
    if not job.required_skills:
        return 1.0, missing
    return len(matched) / len(job.required_skills), missing


def apply_constraints(
    breakdown: ScoreBreakdown,
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    *,
    min_must_have_ratio: float = 0.34,
) -> tuple[ScoreBreakdown, list[str]]:
    notes: list[str] = []
    factor = 1.0

    exp_f, exp_note = experience_factor(candidate, job)
    factor *= exp_f
    if exp_note:
        notes.append(exp_note)

    rem_f, rem_note = remote_factor(candidate, job)
    factor *= rem_f
    if rem_note:
        notes.append(rem_note)

    sal_f, sal_note = salary_factor(candidate, job)
    factor *= sal_f
    if sal_note:
        notes.append(sal_note)

    coverage, missing = must_have_coverage(candidate, job)
    if job.required_skills and coverage < min_must_have_ratio:
        factor *= 0.5 + 0.5 * coverage
        notes.append(f"Missing must-have skills: {', '.join(missing[:4])}")

    adjusted = max(0.0, min(1.0, breakdown.final_score * factor))
    return breakdown.model_copy(
        update={"final_score": adjusted, "constraint_factor": factor}
    ), notes
