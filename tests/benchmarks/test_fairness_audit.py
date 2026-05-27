"""Tests for synthetic fairness audit framework."""
from __future__ import annotations

import json

import pytest

from benchmarks.fairness_audit import (
    FairnessAudit,
    audit_profile_pair,
    explanation_drift,
    write_fairness_audit_report,
)
from benchmarks.fairness_profiles import load_audit_profiles, merge_variant_cv
from config import Settings
from contracts.snapshots import CandidateSnapshot, JobSnapshot


def test_explanation_drift_identical():
    d = explanation_drift(["a", "b"], ["a", "b"])
    assert d["drift_score"] == 0.0
    assert d["unchanged"] is True


def test_explanation_drift_partial():
    d = explanation_drift(["a", "b"], ["b", "c"])
    assert 0.0 < d["drift_score"] < 1.0


def test_merge_variant_only_changes_demographics():
    core = {
        "skills": ["Python"],
        "experience_years": 3,
        "remote_preference": True,
        "preferred_salary": 100000,
        "summary": "Engineer.",
    }
    a = merge_variant_cv(core, {"suffix": "a", "name": "Alice Test"}, pair_id="p1")
    b = merge_variant_cv(core, {"suffix": "b", "name": "Bob Test"}, pair_id="p1")
    assert a["skills"] == b["skills"]
    assert a["experience_years"] == b["experience_years"]
    assert a["name"] != b["name"]


def test_audit_pair_rank_stable_with_identical_snapshots():
    cand = CandidateSnapshot(
        id="c1",
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
        id="j1",
        title="Eng",
        required_skills=["Python"],
        required_experience=2,
        remote_policy=True,
        budget=120000,
        description="d",
        version=1,
        document_text_hash="h2",
        embedding=[0.9, 0.1],
    )
    pair_meta = {"pair_id": "t", "category": "test", "field_changed": "name"}
    summary, _, flagged = audit_profile_pair(
        pair_meta, cand, cand, [job], top_k=1, score_delta_threshold=0.5
    )
    assert summary["top_1_stable"] is True
    assert summary["max_score_delta"] == 0.0
    assert not flagged


def test_load_synthetic_profiles():
    settings = Settings()
    path = settings.data_dir / "fairness_audit_profiles.json"
    payload = load_audit_profiles(path)
    assert payload["meta"]["synthetic"] is True
    assert len(payload["pairs"]) >= 8


def test_fairness_audit_run_and_write(tmp_path):
    audit = FairnessAudit(top_k=5)
    report = audit.run()
    assert report.meta["synthetic_only"] is True
    assert len(report.pair_summaries) == report.meta["pairs"]
    assert "rank_stability" in report.meta["metrics_reported"]

    paths = write_fairness_audit_report(report, tmp_path, prefix="test")
    payload = json.loads(paths["json"].read_text(encoding="utf-8"))
    assert payload["meta"]["report_type"] == "fairness_bias_audit"
    md = paths["markdown"].read_text(encoding="utf-8")
    assert "Synthetic Controlled Profiles" in md
