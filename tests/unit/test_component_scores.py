import pytest

from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.component_scores import compensation_score, experience_score, location_score


def _candidate(**kwargs) -> CandidateSnapshot:
    defaults = {
        "id": "cv_01",
        "name": "Test",
        "skills": ["Python"],
        "experience_years": 3.0,
        "remote_preference": False,
        "preferred_salary": None,
        "summary": "Engineer",
        "version": 1,
        "document_text_hash": "h",
        "embedding": [1.0, 0.0],
    }
    defaults.update(kwargs)
    return CandidateSnapshot(**defaults)


def _job(**kwargs) -> JobSnapshot:
    defaults = {
        "id": "job_01",
        "title": "Role",
        "required_skills": ["Python"],
        "required_experience": 2,
        "remote_policy": True,
        "budget": 100000,
        "description": "desc",
        "version": 1,
        "document_text_hash": "h",
        "embedding": [1.0, 0.0],
    }
    defaults.update(kwargs)
    return JobSnapshot(**defaults)


def test_experience_score_meets_requirement():
    assert experience_score(_candidate(experience_years=4), _job(required_experience=3)) == 1.0


def test_experience_score_large_gap():
    assert experience_score(_candidate(experience_years=1), _job(required_experience=6)) == 0.2


def test_compensation_score_within_range():
    cand = _candidate(preferred_salary=95000)
    job = _job(budget_min=90000, budget_max=110000)
    assert compensation_score(cand, job) == 1.0


def test_compensation_score_missing_data_is_neutral():
    assert compensation_score(_candidate(preferred_salary=None), _job(budget=None)) == 1.0


def test_location_score_remote_mismatch():
    assert location_score(_candidate(remote_preference=True), _job(remote_policy=False)) == 0.4


def test_location_score_remote_match():
    assert location_score(_candidate(remote_preference=True), _job(remote_policy=True)) == 1.0
