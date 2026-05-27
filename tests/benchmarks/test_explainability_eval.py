"""Tests for explainability evaluation checks."""
from __future__ import annotations

import json

from benchmarks.explainability_checks import (
    audit_explanation,
    consistency_between_profiles,
    mentions_matched_or_missing,
)
from benchmarks.explainability_eval import ExplainabilityEval, write_explainability_report
from contracts.matching import ScoreBreakdown
from contracts.snapshots import CandidateSnapshot, JobSnapshot


def test_mentions_matched_skill():
    assert mentions_matched_or_missing(
        ["Matching skills: Python"], ["Python"], ["TensorFlow"]
    )


def test_hallucination_detected():
    candidate = CandidateSnapshot(
        id="cv_test",
        name="Test",
        skills=["Python", "ML"],
        experience_years=3.0,
        remote_preference=True,
        preferred_salary=100000,
        summary="ML engineer.",
        version=1,
        document_text_hash="h",
        embedding=[1.0, 0.0],
    )
    job = JobSnapshot(
        id="job_test",
        title="ML Engineer",
        required_skills=["Python", "TensorFlow"],
        required_experience=2,
        remote_policy=True,
        budget=120000,
        description="d",
        version=1,
        document_text_hash="h2",
        embedding=[0.9, 0.1],
    )
    breakdown = ScoreBreakdown(
        semantic_score=0.72,
        skills_score=0.5,
        final_score=0.75,
        strategy_used="composite",
        metric_used="cosine",
    )
    audit = audit_explanation(
        candidate=candidate,
        job=job,
        breakdown=breakdown,
        bullets=["Matching skills: Python, Kubernetes"],
        explain_mode="rules",
        vocabulary=["Python", "Kubernetes", "TensorFlow", "ML"],
    )
    assert not audit.checks["no_hallucinated_skills"]
    assert audit.flagged


def test_component_claim_invalid():
    candidate = CandidateSnapshot(
        id="cv_test",
        name="Test",
        skills=["Python"],
        experience_years=3.0,
        remote_preference=True,
        preferred_salary=100000,
        summary="s",
        version=1,
        document_text_hash="h",
        embedding=[1.0, 0.0],
    )
    job = JobSnapshot(
        id="job_test",
        title="ML Engineer",
        required_skills=["Python"],
        required_experience=2,
        remote_policy=True,
        budget=120000,
        description="d",
        version=1,
        document_text_hash="h2",
        embedding=[0.9, 0.1],
    )
    bd = ScoreBreakdown(
        semantic_score=0.3,
        skills_score=0.2,
        final_score=0.25,
        strategy_used="composite",
        metric_used="cosine",
    )
    audit = audit_explanation(
        candidate=candidate,
        job=job,
        breakdown=bd,
        bullets=["High semantic similarity"],
        explain_mode="rules",
        vocabulary=["Python"],
    )
    assert not audit.checks["component_claims_valid"]


def test_explainability_eval_run_and_write(tmp_path):
    eval_ = ExplainabilityEval(top_k=3, explain_modes=["rules"])
    report = eval_.run()
    assert report.meta["instances_evaluated"] > 0

    paths = write_explainability_report(report, tmp_path, prefix="test")
    payload = json.loads(paths["json"].read_text(encoding="utf-8"))
    assert payload["meta"]["report_type"] == "explainability_evaluation"
