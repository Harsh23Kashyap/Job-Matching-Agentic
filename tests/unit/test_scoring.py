import numpy as np
import pytest

from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.document_text import job_document_text, resume_document_text
from core.scoring import compute_multimodal_weighted, compute_semantic
from core.skills import jaccard_skills, soft_overlap


def _candidate(**kwargs):
    defaults = dict(
        id="cv_01",
        name="Rahul Sharma",
        skills=["Python", "Machine Learning", "AWS"],
        experience_years=3,
        remote_preference=True,
        summary="Machine learning engineer with Python experience.",
        version=1,
        document_text_hash="h1",
        embedding=[1.0, 0.0, 0.0],
    )
    defaults.update(kwargs)
    return CandidateSnapshot(**defaults)


def _job(**kwargs):
    defaults = dict(
        id="job_01",
        title="Machine Learning Engineer",
        required_skills=["Python", "Machine Learning", "TensorFlow"],
        required_experience=2,
        remote_policy=True,
        description="Looking for ML engineer.",
        version=1,
        document_text_hash="h2",
        embedding=[0.9, 0.1, 0.0],
    )
    defaults.update(kwargs)
    return JobSnapshot(**defaults)


def test_semantic_cosine_perfect_match():
    cand = _candidate(embedding=[1.0, 0.0])
    job = _job(embedding=[1.0, 0.0])
    result = compute_semantic(cand, job, metric="cosine")
    assert result.final_score == pytest.approx(1.0, abs=1e-5)


def test_semantic_euclidean_derived():
    cand = _candidate(embedding=[0.0, 0.0])
    job = _job(embedding=[3.0, 4.0])
    result = compute_semantic(cand, job, metric="euclidean")
    assert result.final_score == pytest.approx(1 / 6, abs=1e-5)


def test_multimodal_jaccard_blend():
    cand = _candidate()
    job = _job()
    result = compute_multimodal_weighted(
        cand, job, metric="cosine", semantic_weight=0.7, skills_mode="jaccard"
    )
    expected_jaccard = jaccard_skills(cand.skills, job.required_skills)
    expected = 0.7 * result.semantic_score + 0.3 * expected_jaccard
    assert result.skills_score == pytest.approx(expected_jaccard)
    assert result.final_score == pytest.approx(expected, abs=1e-5)


def test_multimodal_embedding_mode():
    cand = _candidate(skills=["Python", "Machine Learning"])
    job = _job(required_skills=["Python", "Machine Learning"])
    result = compute_multimodal_weighted(
        cand, job, metric="cosine", semantic_weight=0.5, skills_mode="embedding"
    )
    assert result.skills_score == pytest.approx(1.0, abs=0.05)


def test_invalid_semantic_weight_raises():
    cand = _candidate()
    job = _job()
    with pytest.raises(ValueError):
        compute_multimodal_weighted(cand, job, semantic_weight=1.5)


def test_document_text_field_order_resume():
    text = resume_document_text(
        {
            "name": "A",
            "email": "a@test.com",
            "experience_years": 1,
            "remote_preference": True,
            "skills": ["Python"],
            "summary": "s",
        }
    )
    lines = text.split("\n")
    assert lines[0] == "resume profile"
    assert lines[1].startswith("name:")
    assert any(line.startswith("email:") for line in lines)
    assert any(line.startswith("experience_years:") for line in lines)
    assert any(line.startswith("work_mode:") for line in lines)
    assert any(line.startswith("skills:") for line in lines)
    assert any(line.startswith("summary:") for line in lines)


def test_document_text_field_order_job():
    text = job_document_text(
        {
            "title": "Dev",
            "required_experience": 2,
            "remote_policy": False,
            "required_skills": ["Java"],
            "description": "d",
        }
    )
    lines = text.split("\n")
    assert lines[0] == "job description"
    assert lines[1].startswith("title:")
    assert "required_skills:" in text


def test_soft_overlap_perfect_skill_match():
    score = soft_overlap(["Python"], ["Python"], model_name="all-MiniLM-L6-v2")
    assert score == pytest.approx(1.0, abs=0.05)


def test_composite_weights_sum_to_one():
    from core.scoring import COMPOSITE_WEIGHTS

    assert sum(COMPOSITE_WEIGHTS.values()) == pytest.approx(1.0)


def test_composite_perfect_alignment():
    from core.scoring import compute_composite

    cand = _candidate(
        skills=["Python", "Machine Learning"],
        experience_years=5,
        preferred_salary=100000,
        remote_preference=True,
        embedding=[1.0, 0.0],
    )
    job = _job(
        required_skills=["Python", "Machine Learning"],
        required_experience=3,
        remote_policy=True,
        budget_min=90000,
        budget_max=110000,
        embedding=[1.0, 0.0],
    )
    result = compute_composite(cand, job, metric="cosine", skills_mode="jaccard")
    assert result.semantic_score == pytest.approx(1.0, abs=1e-5)
    assert result.skills_score == pytest.approx(1.0, abs=1e-5)
    assert result.experience_score == pytest.approx(1.0)
    assert result.compensation_score == pytest.approx(1.0)
    assert result.location_score == pytest.approx(1.0)
    assert result.final_score == pytest.approx(1.0, abs=1e-5)
    assert result.strategy_used == "composite"


def test_composite_semantic_only_strategy_unchanged():
    cand = _candidate(embedding=[1.0, 0.0])
    job = _job(embedding=[1.0, 0.0])
    semantic = compute_semantic(cand, job, metric="cosine")
    assert semantic.final_score == pytest.approx(1.0, abs=1e-5)
    assert semantic.skills_score is None
    assert semantic.experience_score is None


def test_composite_penalizes_experience_gap():
    from core.scoring import compute_composite

    cand = _candidate(experience_years=1)
    job = _job(required_experience=5)
    result = compute_composite(cand, job)
    assert result.experience_score == pytest.approx(0.2)
    assert result.final_score < result.semantic_score


def test_composite_compensation_overshoot():
    from core.scoring import compute_composite

    cand = _candidate(preferred_salary=150000)
    job = _job(budget_min=80000, budget_max=100000)
    result = compute_composite(cand, job)
    assert result.compensation_score == pytest.approx(0.4)
    assert result.final_score < 1.0
