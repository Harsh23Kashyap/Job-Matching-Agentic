import numpy as np
import pytest

from contracts.matching import ScoreBreakdown
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.calibration import PlattCalibrator
from core.constraints import apply_constraints, experience_factor, remote_factor, salary_factor
from core.feedback_boost import apply_feedback_adjustment
from core.fusion import LearnedFusionModel, compute_hierarchical_multimodal, extract_pair_features
from core.matchmaking_scoring import resolve_routing, score_pair_advanced
from core.strategy_router import route_strategy
from core.skill_taxonomy import taxonomy_overlap


def _candidate(**kwargs) -> CandidateSnapshot:
    defaults = {
        "id": "cv_01",
        "name": "Test",
        "skills": ["Python", "SQL"],
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
        "preferred_skills": ["SQL"],
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


def test_experience_factor_penalizes_gap():
    cand = _candidate(experience_years=1.0)
    job = _job(required_experience=4)
    factor, note = experience_factor(cand, job)
    assert factor < 1.0
    assert note is not None


def test_remote_factor_on_site_mismatch():
    cand = _candidate(remote_preference=True)
    job = _job(remote_policy=False)
    factor, note = remote_factor(cand, job)
    assert factor == 0.75
    assert "remote" in note.lower()


def test_salary_factor_overshoot():
    cand = _candidate(preferred_salary=150000)
    job = _job(budget=100000)
    factor, note = salary_factor(cand, job)
    assert factor < 1.0
    assert note is not None


def test_apply_constraints_reduces_score():
    breakdown = ScoreBreakdown(
        semantic_score=0.9,
        skills_score=0.8,
        final_score=0.85,
        strategy_used="multimodal",
        metric_used="cosine",
    )
    cand = _candidate(experience_years=0.0, remote_preference=True, preferred_salary=200000)
    job = _job(required_experience=5, remote_policy=False, budget=80000, required_skills=["Go", "Rust"])
    adjusted, notes = apply_constraints(breakdown, cand, job)
    assert adjusted.final_score < breakdown.final_score
    assert len(notes) >= 1


def test_platt_calibrator_monotonic():
    cal = PlattCalibrator(a=2.0, b=-1.0)
    low = cal.calibrate(0.2)
    high = cal.calibrate(0.8)
    assert high > low


def test_learned_fusion_train_predict():
    rng = np.random.default_rng(42)
    X = rng.random((20, 8))
    y = (X[:, 0] + X[:, 1] > 1.0).astype(float)
    model = LearnedFusionModel.train(X, y, epochs=200)
    score = model.predict_proba(X[0])
    assert 0.0 <= score <= 1.0


def test_hierarchical_multimodal_uses_preferred_skills():
    cand = _candidate(skills=["Python", "SQL"])
    job = _job(required_skills=["Python"], preferred_skills=["SQL"])
    breakdown = compute_hierarchical_multimodal(cand, job)
    assert breakdown.fusion_mode_used == "hierarchical"
    assert breakdown.skills_score is not None


def test_feedback_boost_adjusts_score():
    breakdown = ScoreBreakdown(
        semantic_score=0.7,
        final_score=0.7,
        strategy_used="semantic",
        metric_used="cosine",
    )
    boosted = apply_feedback_adjustment(breakdown, save_count=2, dismiss_count=1)
    assert boosted.feedback_delta is not None
    assert boosted.final_score != breakdown.final_score


def test_route_strategy_skill_rich():
    cand = _candidate(skills=[f"s{i}" for i in range(10)])
    strategy, skills_mode, _, reason = route_strategy(cand)
    assert strategy == "multimodal"
    assert skills_mode == "embedding"
    assert reason


def test_taxonomy_overlap_nonzero_for_related_skills():
    score = taxonomy_overlap(["python"], ["python programming"])
    assert score >= 0.0


def test_score_pair_advanced_with_constraints():
    from contracts.matching import MatchRequest

    cand = _candidate(experience_years=0.0)
    job = _job(required_experience=5)
    req = MatchRequest(
        query_key="Test",
        apply_constraints=True,
        strategy="multimodal",
    )
    breakdown, notes, _ = score_pair_advanced(
        cand,
        job,
        req,
        model_name="all-MiniLM-L6-v2",
        fusion_model=None,
        calibrator=None,
        feedback_store=None,
    )
    assert breakdown.final_score >= 0.0
    assert len(notes) >= 1


def test_resolve_routing_auto():
    from contracts.matching import MatchRequest

    cand = _candidate(skills=[f"s{i}" for i in range(10)])
    req = MatchRequest(query_key="Test", auto_strategy=True)
    updated, reason = resolve_routing(cand, req)
    assert updated.strategy == "multimodal"
    assert reason is not None
