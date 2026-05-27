from contracts.matching import ScoreBreakdown
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.match_explanation import build_match_explanation


def _candidate(**overrides):
    base = dict(
        id="cv_01",
        name="Alex",
        skills=["Python", "FastAPI"],
        experience_years=6,
        remote_preference=True,
        preferred_salary=2_500_000,
        summary="Backend engineer",
        version=1,
        document_text_hash="h",
        embedding=[1.0, 0.0],
    )
    base.update(overrides)
    return CandidateSnapshot(**base)


def _job(**overrides):
    base = dict(
        id="job_01",
        title="Senior Backend Engineer",
        required_skills=["Python", "Docker", "PostgreSQL"],
        required_experience=5,
        remote_policy=True,
        budget_min=2_000_000,
        budget_max=3_000_000,
        description="Build APIs",
        version=1,
        document_text_hash="h",
        embedding=[1.0, 0.0],
    )
    base.update(overrides)
    return JobSnapshot(**base)


def _breakdown(**overrides):
    base = dict(
        semantic_score=0.82,
        skills_score=0.67,
        title_score=0.74,
        experience_score=1.0,
        compensation_score=0.95,
        remote_score=1.0,
        final_score=0.84,
        strategy_used="composite",
        metric_used="cosine",
        skills_mode_used="jaccard",
    )
    base.update(overrides)
    return ScoreBreakdown(**base)


def test_build_match_explanation_includes_skills_and_fits():
    candidate = _candidate()
    job = _job()
    breakdown = _breakdown()
    explanation = build_match_explanation(
        candidate,
        job,
        breakdown,
        matched_skills=["Python"],
        missing_skills=["Docker", "PostgreSQL"],
    )

    assert explanation.matched_skills == ["Python"]
    assert explanation.missing_skills == ["Docker", "PostgreSQL"]
    assert explanation.semantic.label == "Good fit"
    assert "semantic fit" in explanation.semantic.reason.lower()
    assert explanation.experience.label == "Strong fit"
    assert "6 years" in explanation.experience.reason
    assert explanation.compensation.label == "Strong fit"
    assert explanation.remote.label == "Strong fit"
    assert len(explanation.score_breakdown) == 6
    assert explanation.final_score == 0.84


def test_experience_gap_reason():
    candidate = _candidate(experience_years=2)
    job = _job(required_experience=5)
    breakdown = _breakdown(experience_score=0.4)
    explanation = build_match_explanation(
        candidate,
        job,
        breakdown,
        matched_skills=["Python"],
        missing_skills=["Docker"],
    )
    assert explanation.experience.label == "Weak fit"
    assert "gap" in explanation.experience.reason.lower()
