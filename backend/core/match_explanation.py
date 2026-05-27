"""Structured explainability payload for candidate–job matches."""
from __future__ import annotations

from contracts.matching import FitSignal, MatchExplanation, ScoreBreakdown, ScoreComponentDetail
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.scoring import build_composite_components


def _fit_label(score: float | None) -> str:
    if score is None:
        return "Not scored"
    if score >= 0.85:
        return "Strong fit"
    if score >= 0.65:
        return "Good fit"
    if score >= 0.45:
        return "Moderate fit"
    return "Weak fit"


def _semantic_reason(score: float) -> str:
    pct = f"{score:.0%}"
    if score >= 0.75:
        return f"Resume and job description align closely ({pct} semantic fit)"
    if score >= 0.55:
        return f"Profile context partially matches the role ({pct} semantic fit)"
    return f"Limited profile-to-role text alignment ({pct} semantic fit)"


def _experience_reason(candidate: CandidateSnapshot, job: JobSnapshot, score: float) -> str:
    cand = candidate.experience_years
    required = job.required_experience
    if score >= 0.95:
        return f"{cand:g} years experience meets the {required}+ year requirement"
    if score >= 0.75:
        gap = max(0.0, float(required) - cand)
        if gap <= 0:
            return f"{cand:g} years experience meets the {required}+ year requirement"
        return f"{cand:g} years experience — about {gap:g} year(s) below the {required}+ year ask"
    if score >= 0.55:
        gap = max(0.0, float(required) - cand)
        return f"Role targets ~{required} years; you have {cand:g} ({gap:g} year gap)"
    gap = max(0.0, float(required) - cand)
    return f"Experience gap: role asks ~{required} years, you have {cand:g} ({gap:g} year shortfall)"


def _format_amount(amount: int, currency: str) -> str:
    if currency == "USD":
        if amount >= 1_000_000:
            return f"${amount / 1_000_000:.1f}M"
        if amount >= 1_000:
            return f"${amount / 1_000:.0f}K"
        return f"${amount:,}"
    if amount >= 10_000_000:
        return f"₹{amount / 10_000_000:.1f}Cr"
    if amount >= 100_000:
        return f"₹{amount / 100_000:.1f}L"
    return f"₹{amount:,}"


def _compensation_reason(candidate: CandidateSnapshot, job: JobSnapshot, score: float) -> str:
    expected = candidate.preferred_salary
    budget_min = job.budget_min if job.budget_min is not None else job.budget
    budget_max = job.budget_max if job.budget_max is not None else job.budget
    currency = "INR"

    if expected is None and budget_min is None and budget_max is None:
        return "No salary expectation or budget listed — compensation not penalized"
    if expected is None:
        if budget_min is not None and budget_max is not None:
            return f"Role budget {_format_amount(budget_min, currency)}–{_format_amount(budget_max, currency)}; add your expectation to filter pay mismatches"
        return "Add expected compensation to filter roles outside your range"
    if budget_min is None and budget_max is None:
        return f"Expected {_format_amount(expected, currency)}; role budget not specified"

    if score >= 0.95:
        if budget_min is not None and budget_max is not None:
            return f"Expected {_format_amount(expected, currency)} fits budget {_format_amount(budget_min, currency)}–{_format_amount(budget_max, currency)}"
        if budget_max is not None:
            return f"Expected {_format_amount(expected, currency)} is within the posted budget"
        return "Compensation expectations align with the role budget"

    if score >= 0.75:
        return f"Expected {_format_amount(expected, currency)} is close to the role budget band"

    if expected > (budget_max or budget_min or expected):
        cap = budget_max or budget_min
        return f"Expected {_format_amount(expected, currency)} exceeds posted budget (~{_format_amount(cap, currency)})"
    floor = budget_min or budget_max
    return f"Expected {_format_amount(expected, currency)} may sit below the role budget (~{_format_amount(floor, currency)})"


def _remote_reason(candidate: CandidateSnapshot, job: JobSnapshot, score: float) -> str:
    if not candidate.remote_preference:
        return "On-site preference — remote policy has limited impact"
    if job.remote_policy:
        return "Remote-friendly role matches your remote preference"
    if score <= 0.5:
        return "You prefer remote work; this role may require on-site presence"
    return "Remote preference partially aligns with role setup"


def _fit_signal(score: float | None, reason: str) -> FitSignal:
    return FitSignal(score=score, label=_fit_label(score), reason=reason)


def _resolve_score_breakdown(breakdown: ScoreBreakdown) -> list[ScoreComponentDetail]:
    if breakdown.score_components:
        return breakdown.score_components
    if breakdown.strategy_used == "composite":
        return build_composite_components(breakdown)
    return []


def build_match_explanation(
    candidate: CandidateSnapshot,
    job: JobSnapshot,
    breakdown: ScoreBreakdown,
    *,
    matched_skills: list[str],
    missing_skills: list[str],
) -> MatchExplanation:
    remote_score = breakdown.remote_score if breakdown.remote_score is not None else breakdown.location_score
    semantic = breakdown.semantic_score
    experience = breakdown.experience_score
    compensation = breakdown.compensation_score

    return MatchExplanation(
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        semantic=_fit_signal(semantic, _semantic_reason(semantic)),
        experience=_fit_signal(
            experience,
            _experience_reason(candidate, job, experience) if experience is not None else "Experience not scored for this strategy",
        ),
        compensation=_fit_signal(
            compensation,
            _compensation_reason(candidate, job, compensation) if compensation is not None else "Compensation not scored for this strategy",
        ),
        remote=_fit_signal(
            remote_score,
            _remote_reason(candidate, job, remote_score) if remote_score is not None else "Remote fit not scored for this strategy",
        ),
        score_breakdown=_resolve_score_breakdown(breakdown),
        final_score=breakdown.final_score,
    )
