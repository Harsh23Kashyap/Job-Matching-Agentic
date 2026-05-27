"""Tests for dataset validation."""
from __future__ import annotations

import json
from pathlib import Path

from benchmarks.dataset_validation import validate_eval_corpus, write_validation_report
from config import Settings


def test_validate_demo_corpus_passes():
    settings = Settings()
    report = validate_eval_corpus(data_dir=settings.data_dir)
    assert report.valid is True
    assert report.stats["candidates"] == 30
    assert report.stats["jobs"] == 15
    assert report.stats["labeled_queries"] == 30
    assert not any(i.level == "error" for i in report.issues)


def test_validate_detects_unknown_query(tmp_path):
    settings = Settings()
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    cvs = [{"id": "cv_1", "skills": ["Python"], "experience_years": 2}]
    jobs = [{"id": "job_1", "required_skills": ["Python"], "required_experience": 1}]
    labels = {"labels": [{"query_id": "cv_missing", "doc_id": "job_1", "relevance": 2}]}
    (data_dir / "cvs.json").write_text(json.dumps(cvs), encoding="utf-8")
    (data_dir / "jobs.json").write_text(json.dumps(jobs), encoding="utf-8")
    (data_dir / "eval_pairs.json").write_text(json.dumps(labels), encoding="utf-8")

    report = validate_eval_corpus(data_dir=data_dir)
    assert report.valid is False
    assert any(i.code == "unknown_query_id" for i in report.issues)


def test_write_validation_report(tmp_path):
    settings = Settings()
    report = validate_eval_corpus(data_dir=settings.data_dir)
    paths = write_validation_report(report, tmp_path)
    assert paths["json"].is_file()
    assert paths["markdown"].is_file()
    payload = json.loads(paths["json"].read_text(encoding="utf-8"))
    assert "valid" in payload
    assert "stats" in payload
