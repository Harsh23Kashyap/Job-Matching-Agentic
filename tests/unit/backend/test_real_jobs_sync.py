import json
from unittest.mock import patch

import pytest

from core.real_jobs_sync import (
    RealJobsConfig,
    fetch_all_jobs,
    normalize_external_job,
    write_snapshot,
    load_snapshot,
)


def test_normalize_external_job_aliases():
    raw = {
        "job_id": "abc",
        "job_title": "ML Engineer",
        "company_name": "Acme",
        "url": "https://example.com/apply",
        "job_description": "Build models",
        "skills": "Python, TensorFlow",
        "experience_years": 2,
        "salary_min": 130000,
        "remote": "remote",
        "location": "Remote",
        "created_at": "2026-05-15T10:00:00Z",
        "source": "aiforjob",
    }
    job = normalize_external_job(raw, fallback_idx=1)
    assert job["id"] == "abc"
    assert job["title"] == "ML Engineer"
    assert job["company"] == "Acme"
    assert job["link"] == "https://example.com/apply"
    assert job["required_skills"] == ["Python", "TensorFlow"]
    assert job["required_experience"] == 2
    assert job["budget"] == 130000
    assert job["remote_policy"] is True
    assert job["posted_at"] == "2026-05-15T10:00:00Z"
    assert job["source"] == "aiforjob"


def test_normalize_external_job_fallback_id():
    job = normalize_external_job({}, fallback_idx=3)
    assert job["id"] == "ext_3"
    assert job["title"] == "Untitled Role"


def test_fetch_all_jobs_paginates(monkeypatch):
    pages = [
        {"total": 3, "jobs": [{"id": "1", "title": "A"}, {"id": "2", "title": "B"}]},
        {"total": 3, "jobs": [{"id": "3", "title": "C"}]},
    ]

    def fake_request(url: str, timeout_sec: int):
        assert timeout_sec == 30
        if "skip=0" in url:
            return pages[0]
        if "skip=2" in url:
            return pages[1]
        raise AssertionError(f"unexpected url {url}")

    monkeypatch.setattr("core.real_jobs_sync._request_json", fake_request)
    config = RealJobsConfig(
        base_url="https://api.example.com",
        jobs_path="/jobs",
        limit=2,
        timeout_sec=30,
        enabled=True,
        output_path="/tmp/jobs_live.json",
    )
    snapshot = fetch_all_jobs(config)
    assert snapshot["raw_count"] == 3
    assert snapshot["deduped_count"] == 3
    assert len(snapshot["jobs"]) == 3


def test_fetch_all_jobs_dedupes_by_id(monkeypatch):
    monkeypatch.setattr(
        "core.real_jobs_sync._request_json",
        lambda url, timeout_sec: {"total": 2, "jobs": [{"id": "1", "title": "A"}, {"id": "1", "title": "A dup"}]},
    )
    config = RealJobsConfig(
        base_url="https://api.example.com",
        jobs_path="/jobs",
        limit=50,
        timeout_sec=30,
        enabled=True,
        output_path="/tmp/jobs_live.json",
    )
    snapshot = fetch_all_jobs(config)
    assert snapshot["deduped_count"] == 1


def test_fetch_all_jobs_missing_base_url():
    config = RealJobsConfig(
        base_url="",
        jobs_path="/jobs",
        limit=50,
        timeout_sec=30,
        enabled=False,
        output_path="/tmp/jobs_live.json",
    )
    with pytest.raises(ValueError, match="REAL_JOBS_BASE_URL"):
        fetch_all_jobs(config)


def test_snapshot_roundtrip(tmp_path):
    path = tmp_path / "jobs_live.json"
    payload = {
        "fetched_at_utc": "2026-05-27T00:00:00+00:00",
        "jobs": [{"id": "1", "title": "Engineer", "required_skills": []}],
    }
    write_snapshot(payload, str(path))
    loaded = load_snapshot(str(path))
    assert loaded["jobs"][0]["id"] == "1"
