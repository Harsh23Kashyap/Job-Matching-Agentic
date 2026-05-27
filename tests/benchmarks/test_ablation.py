"""Tests for ablation study scoring and runner."""
from __future__ import annotations

import json

import pytest

from benchmarks.ablation import AblationStudy, build_ablation_strategies, write_ablation_report
from benchmarks.ablation_scoring import semantic_skills, semantic_skills_experience
from benchmarks.eval_data import cv_to_snapshot, job_to_snapshot
from config import Settings
from contracts.snapshots import CandidateSnapshot, JobSnapshot


@pytest.fixture
def pair():
    candidate = CandidateSnapshot(
        id="cv_01",
        name="Test",
        skills=["Python", "ML"],
        experience_years=3.0,
        remote_preference=True,
        preferred_salary=100000,
        summary="s",
        version=1,
        document_text_hash="h",
        embedding=[1.0, 0.0],
    )
    job = JobSnapshot(
        id="job_01",
        title="ML Engineer",
        required_skills=["Python", "TensorFlow"],
        preferred_skills=[],
        required_experience=2,
        remote_policy=True,
        budget=120000,
        description="d",
        version=1,
        document_text_hash="h2",
        embedding=[0.9, 0.1],
    )
    return candidate, job


def test_partial_composite_renormalizes(pair):
    candidate, job = pair
    ss = semantic_skills(candidate, job)
    assert ss.final_score > 0
    assert ss.fusion_mode_used == "renormalized_partial"
    sse = semantic_skills_experience(candidate, job)
    assert sse.experience_score is not None


def test_build_ablation_has_nine_variants():
    settings = Settings()
    resumes = json.loads((settings.data_dir / "cvs.json").read_text(encoding="utf-8"))
    jobs = json.loads((settings.data_dir / "jobs.json").read_text(encoding="utf-8"))
    job_snaps = [job_to_snapshot(j, settings.embedding_model) for j in jobs]
    strategies = build_ablation_strategies(job_snaps, model_name=settings.embedding_model)
    assert len(strategies) == 9


def test_ablation_run_and_outputs(tmp_path):
    study = AblationStudy(top_k=5)
    report = study.run()
    assert len(report.summary) == 9
    assert len(report.table_rows) == 45

    paths = write_ablation_report(report, tmp_path, prefix="test")
    md = paths["markdown"].read_text(encoding="utf-8")
    assert "Ablation Study" in md
    assert "Full composite" in md

    payload = json.loads(paths["report_json"].read_text(encoding="utf-8"))
    assert payload["meta"]["report_type"] == "ablation_study"
