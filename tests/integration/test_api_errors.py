import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(system):
    from gateway.app import build_gateway

    app = build_gateway(system)
    with TestClient(app) as c:
        yield c


def _register_candidate(client, email="api-err@test.com"):
    return client.post(
        "/auth/register",
        json={"email": email, "password": "secret1", "role": "candidate"},
    )


def _register_employer(client, email="api-emp@test.com"):
    return client.post(
        "/auth/register",
        json={"email": email, "password": "secret1", "role": "employer"},
    )


def test_profile_save_requires_name(client):
    _register_candidate(client, "noname@test.com")
    resp = client.put("/candidates/me", json={"skills": ["Go"], "experience_years": 1})
    assert resp.status_code == 422
    assert resp.json()["detail"]["code"] == "VALIDATION"
    assert "name" in resp.json()["detail"]["error"]


def test_job_create_requires_title(client):
    _register_employer(client, "notitle@test.com")
    resp = client.post("/jobs", json={"required_skills": ["Python"], "required_experience": 2})
    assert resp.status_code == 422
    assert resp.json()["detail"]["code"] == "VALIDATION"


def test_match_unknown_candidate_returns_clean_error(client):
    resp = client.post(
        "/match/candidate-to-jobs",
        json={"query_key": "Nobody Here", "top_k": 5, "strategy": "composite"},
    )
    assert resp.status_code == 404
    body = resp.json()["detail"]
    assert body["code"] == "NOT_FOUND"
    assert "Nobody Here" in body["error"]


def test_match_unknown_job_returns_clean_error(client):
    resp = client.post(
        "/match/job-to-candidates",
        json={"query_key": "Missing Role Title", "top_k": 5, "strategy": "composite"},
    )
    assert resp.status_code == 404
    body = resp.json()["detail"]
    assert body["code"] == "NOT_FOUND"
    assert "Missing Role Title" in body["error"]


def test_application_uses_profile_not_found_when_stale(client):
    _register_candidate(client, "app-stale@test.com")
    created = client.put(
        "/candidates/me",
        json={"name": "App Stale", "skills": ["Go"], "experience_years": 1, "summary": "Dev"},
    )
    profile_id = created.json()["id"]
    candidate_agent = client.app.state.container.candidate
    del candidate_agent.state.profiles[profile_id]

    resp = client.post(
        "/candidates/me/applications",
        json={"job_id": "job_01", "job_title": "Engineer"},
    )
    assert resp.status_code == 404
    assert resp.json()["detail"]["code"] == "PROFILE_NOT_FOUND"


def test_save_job_validates_job_exists(client):
    _register_candidate(client, "save-job@test.com")
    client.put(
        "/candidates/me",
        json={"name": "Save Job User", "skills": ["Go"], "experience_years": 1, "summary": "Dev"},
    )
    resp = client.put(
        "/candidates/me/saved-jobs",
        json={"job_id": "missing-job-id", "job_title": "Ghost", "saved": True},
    )
    assert resp.status_code == 404
    assert resp.json()["detail"]["code"] == "NOT_FOUND"


def test_upload_resume_rejects_short_text(client):
    _register_candidate(client, "short-resume@test.com")
    resp = client.post(
        "/candidates/upload-resume",
        files={"file": ("resume.txt", b"too short", "text/plain")},
    )
    assert resp.status_code == 422
    assert resp.json()["detail"]["code"] == "VALIDATION"


def test_validation_error_envelope_for_bad_register_body(client):
    resp = client.post("/auth/register", json={"email": "not-an-email", "password": "x", "role": "candidate"})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail["code"] == "VALIDATION"
    assert "email" in detail["error"] or "password" in detail["error"]
