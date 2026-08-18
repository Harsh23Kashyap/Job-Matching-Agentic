"""Phase 24 — scientific-claim regression guards (audit §9).

Encodes the paper's core invariants as executable tests so a future edit that breaks them fails CI.
Deliberately uses dummy embeddings + the rule-based channels so these run fast and never load a model
(no hang under machine load). Run: cd backend && PYTHONPATH=. .venv/bin/python -m pytest ../tests/unit/backend/test_scientific_claims.py -q
"""
from __future__ import annotations
import math

import pytest

from core.scoring import COMPOSITE_WEIGHTS, compute_composite
from core.skills import skills_score, graded_coverage_skills
from contracts.snapshots import CandidateSnapshot, JobSnapshot

DIM = 384


def _cand(skills, exp=5.0, remote=True, salary=100000):
    return CandidateSnapshot(id="c1", name="X", skills=list(skills), experience_years=exp,
                             remote_preference=remote, preferred_salary=salary, summary="s",
                             version=1, document_text_hash="", embedding=[0.1] * DIM)


def _job(req, exp=3, remote=True, budget=120000, title="Software Engineer"):
    return JobSnapshot(id="j1", title=title, required_skills=list(req), preferred_skills=[],
                       required_experience=exp, remote_policy=remote, budget=budget, description="d",
                       version=1, document_text_hash="", embedding=[0.1] * DIM)


def test_weight_sum_equals_one():
    assert abs(sum(COMPOSITE_WEIGHTS.values()) - 1.0) < 1e-12, COMPOSITE_WEIGHTS


def test_decomposition_reconciles_to_final_or_clamped():
    b = compute_composite(_cand(["Python", "AWS"]), _job(["Python"]))
    contrib = sum(c.contribution for c in (b.score_components or []))
    raw = sum(COMPOSITE_WEIGHTS[k] * getattr(b, f"{k}_score") for k in COMPOSITE_WEIGHTS)
    # displayed decomposition must equal final_score, UNLESS the [0,1] clamp changed the raw sum
    clamped = abs(raw - b.final_score) > 1e-9
    assert clamped or abs(contrib - b.final_score) < 1e-9, (contrib, b.final_score, raw)


def test_final_score_in_unit_interval():
    b = compute_composite(_cand(["Python"]), _job(["Python"]))
    assert 0.0 <= b.final_score <= 1.0


def test_skill_addition_increases_or_holds_skill_channel():
    # candidate gains a skill the job requires -> skills overlap must not decrease
    base = skills_score(["Python"], ["Python", "AWS"], skills_mode="jaccard", model_name="all-MiniLM-L6-v2")
    added = skills_score(["Python", "AWS"], ["Python", "AWS"], skills_mode="jaccard", model_name="all-MiniLM-L6-v2")
    assert added >= base and added > 0.0


def test_missing_salary_and_remote_do_not_crash():
    b = compute_composite(_cand(["Python"], salary=None), _job(["Python"], budget=None))
    assert 0.0 <= b.final_score <= 1.0


def test_skills_channel_zero_when_no_overlap():
    assert skills_score(["Cobol"], ["Python"], skills_mode="jaccard", model_name="all-MiniLM-L6-v2") == 0.0


def test_calibration_is_monotonic_if_model_present():
    from pathlib import Path
    import json
    repo = Path(__file__).resolve().parents[3]
    calib = repo / "data" / "models" / "calibration.json"
    if not calib.exists() or not calib.read_text().strip():
        pytest.skip("no calibration model on disk")
    from core.calibration import PlattCalibrator
    cal = PlattCalibrator.load(calib)
    lo, hi = cal.calibrate(0.1), cal.calibrate(0.9)
    # fitted a>0 -> monotonic non-decreasing; probabilities in [0,1]
    assert 0.0 <= lo <= 1.0 and 0.0 <= hi <= 1.0
    assert hi >= lo, (lo, hi)


def test_entity_overlap_leakage_checker():
    def overlap(a, b):
        return sorted(set(a) & set(b))
    assert overlap(["cv_01", "cv_02"], ["cv_03"]) == []
    assert overlap(["cv_01", "cv_02"], ["cv_02"]) == ["cv_02"]


def test_graded_channel_never_gives_related_full_credit():
    """EXP-043 invariant: a merely-related skill (same taxonomy group, different canonical) must
    score STRICTLY BELOW an exact match, and the graded coverage stays in [0,1]."""
    exact = graded_coverage_skills(["Python"], ["Python"])            # exact -> 1.0
    related = graded_coverage_skills(["Java"], ["Python"])            # same 'programming' group -> 0.5
    unrelated = graded_coverage_skills(["Figma"], ["Python"])         # different group -> 0.0
    assert exact == 1.0
    assert 0.0 < related < exact, (related, exact)
    assert unrelated == 0.0
    assert 0.0 <= related <= 1.0


def test_graded_channel_monotone_in_exact_coverage():
    """Adding a skill that exactly covers a required skill must not decrease graded coverage."""
    base = graded_coverage_skills(["Python"], ["Python", "Kubernetes"])
    added = graded_coverage_skills(["Python", "Kubernetes"], ["Python", "Kubernetes"])
    assert added >= base and added == 1.0, (base, added)


def test_graded_mode_routes_through_skills_score():
    """skills_mode='graded' must dispatch to the graded coverage scorer (not Jaccard)."""
    via_mode = skills_score(["Java"], ["Python"], skills_mode="graded", model_name="all-MiniLM-L6-v2")
    direct = graded_coverage_skills(["Java"], ["Python"])
    assert via_mode == direct == 0.5


def test_nonfinite_embedding_does_not_score_perfect():
    """EXP-033 regression: a corrupted (NaN/inf) embedding must NOT yield a spurious perfect
    semantic match; core.scoring._safe_vec zeroes non-finite entries -> semantic contributes 0."""
    nan_cand = _cand(["Python"])
    nan_cand = nan_cand.model_copy(update={"embedding": [float("nan")] * DIM})
    b = compute_composite(nan_cand, _job(["Python"]))
    assert math.isfinite(b.final_score) and 0.0 <= b.final_score <= 1.0
    # semantic channel must be exactly 0 for a non-finite embedding (not 1.0)
    assert b.semantic_score == 0.0, b.semantic_score
