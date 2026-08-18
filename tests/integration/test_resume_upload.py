import io
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(system):
    from gateway.app import build_gateway

    app = build_gateway(system)
    with TestClient(app) as c:
        yield c


def _register_candidate(client, email="cand2@test.com"):
    return client.post(
        "/auth/register",
        json={"email": email, "password": "secret1", "role": "candidate"},
    )


@patch("gateway.routes.candidates.create_llm_parser")
def test_upload_llm_unavailable_returns_manual_fallback(mock_factory, client):
    from hooks.llm_parser import LlmParser, LlmUnavailableError

    mock_parser = LlmParser(client.app.state.container.settings)

    def fail(_text):
        raise LlmUnavailableError("LLM service unavailable")

    mock_parser.parse_candidate_from_text = fail
    mock_factory.return_value = mock_parser

    _register_candidate(client, "cand-llm-fail@test.com")
    content = b"Jordan Rivera\njordan@example.com\n+91 9876543210\nhttps://linkedin.com/in/jordan"
    resp = client.post(
        "/candidates/upload-resume",
        files={"file": ("resume.txt", io.BytesIO(content), "text/plain")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["llm_status"] == "unavailable"
    assert "raw_text_preview" in data
    assert "cleaned_text" in data
    assert "(cid:" not in data["cleaned_text"]
    assert data["extracted_fields"]["name"] == "Jordan Rivera"
    assert data["extracted_fields"]["email"] == "jordan@example.com"
    assert "linkedin.com/in/jordan" in data["extracted_fields"]["linkedin"]


@patch("gateway.routes.candidates.create_llm_parser")
def test_upload_strips_cid_noise_from_cleaned_text(mock_factory, client):
    from hooks.llm_parser import LlmParser, LlmUnavailableError

    mock_parser = LlmParser(client.app.state.container.settings)
    mock_parser.parse_candidate_from_text = lambda _text: (_ for _ in ()).throw(LlmUnavailableError("off"))
    mock_factory.return_value = mock_parser

    _register_candidate(client, "cand-cid@test.com")
    content = b"Jordan Rivera (cid:131)\nSkills \xc2\xa7 Python\njordan@example.com"
    resp = client.post(
        "/candidates/upload-resume",
        files={"file": ("resume.txt", io.BytesIO(content), "text/plain")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "(cid:" not in data["cleaned_text"]
    assert "\xc2\xa7" not in data["cleaned_text"]
    assert data["cleaned_text"].startswith("Jordan Rivera")
    assert "jordan@example.com" in data["cleaned_text"]
    assert data["extracted_fields"]["name"] == "Jordan Rivera"
    assert data["extracted_fields"]["email"] == "jordan@example.com"


@patch("gateway.routes.candidates.create_llm_parser")
def test_upload_resume_extracts_fields(mock_factory, client):
    from hooks.llm_parser import LlmParser

    mock_parser = LlmParser(client.app.state.container.settings)
    mock_parser.parse_candidate_from_text = lambda text: {
        "name": "Upload User",
        "skills": ["Java"],
        "experience_years": 3,
        "preferred_salary": None,
        "remote_preference": False,
        "summary": "Engineer",
    }
    mock_factory.return_value = mock_parser

    _register_candidate(client)
    content = b"Jane Doe\nSkills: Java, Spring\n3 years experience"
    resp = client.post(
        "/candidates/upload-resume",
        files={"file": ("resume.txt", io.BytesIO(content), "text/plain")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["extracted_fields"]["name"] == "Upload User"
    assert "Java" in data["extracted_fields"]["skills"]


def test_upload_requires_auth(client):
    resp = client.post(
        "/candidates/upload-resume",
        files={"file": ("resume.txt", io.BytesIO(b"hello"), "text/plain")},
    )
    assert resp.status_code == 401


def test_candidates_me_and_register(client):
    _register_candidate(client, "me@test.com")
    me = client.get("/candidates/me")
    assert me.status_code == 404

    reg = client.post(
        "/candidates",
        json={
            "name": "Me User",
            "skills": ["Go"],
            "experience_years": 2,
            "summary": "Dev",
        },
    )
    assert reg.status_code == 201

    me = client.get("/candidates/me")
    assert me.status_code == 200
    assert me.json()["name"] == "Me User"


def test_candidate_profile_upsert_on_post(client):
    _register_candidate(client, "upsert@test.com")
    first = client.post(
        "/candidates",
        json={
            "name": "Upsert User",
            "skills": ["Go"],
            "experience_years": 2,
            "summary": "Dev",
        },
    )
    assert first.status_code == 201
    profile_id = first.json()["id"]

    second = client.post(
        "/candidates",
        json={
            "name": "Upsert User Updated",
            "skills": ["Go", "Python"],
            "experience_years": 3,
            "summary": "Senior dev",
        },
    )
    assert second.status_code == 201
    assert second.json()["id"] == profile_id
    assert second.json()["name"] == "Upsert User Updated"
    assert "Python" in second.json()["skills"]


def test_candidate_profile_put_me(client):
    _register_candidate(client, "putme@test.com")
    client.post(
        "/candidates",
        json={
            "name": "Put User",
            "skills": ["Rust"],
            "experience_years": 1,
            "summary": "Dev",
        },
    )
    updated = client.put(
        "/candidates/me",
        json={
            "name": "Put User Updated",
            "skills": ["Rust", "Go"],
            "experience_years": 2,
            "summary": "Updated",
            "preferred_currency": "USD",
            "preferred_salary": 120000,
        },
    )
    assert updated.status_code == 200
    body = updated.json()
    assert body["name"] == "Put User Updated"
    assert body["preferred_currency"] == "USD"
    assert body["preferred_salary"] == 120000


def test_candidate_profile_put_me_creates_and_links(client):
    _register_candidate(client, "putcreate@test.com")
    me_before = client.get("/candidates/me")
    assert me_before.status_code == 404

    created = client.put(
        "/candidates/me",
        json={
            "name": "Create Via Put",
            "skills": ["Python"],
            "experience_years": 2,
            "summary": "New profile",
        },
    )
    assert created.status_code == 200
    profile_id = created.json()["id"]

    me_after = client.get("/candidates/me")
    assert me_after.status_code == 200
    assert me_after.json()["id"] == profile_id
    assert me_after.json()["name"] == "Create Via Put"


def test_employer_jobs_mine(client):
    client.post(
        "/auth/register",
        json={"email": "emp2@test.com", "password": "secret1", "role": "employer"},
    )
    mine = client.get("/jobs/mine")
    assert mine.status_code == 200
    assert mine.json() == []

    created = client.post(
        "/jobs",
        json={
            "title": "QA Engineer",
            "required_skills": ["Testing"],
            "required_experience": 2,
            "description": "Test apps",
        },
    )
    assert created.status_code == 201

    mine = client.get("/jobs/mine")
    assert len(mine.json()) == 1
    assert mine.json()[0]["title"] == "QA Engineer"
    job_id = mine.json()[0]["id"]
    assert mine.json()[0]["status"] == "open"
    assert mine.json()[0]["created_at"]

    updated = client.put(
        f"/jobs/mine/{job_id}",
        json={
            "title": "Senior QA Engineer",
            "required_skills": ["Testing", "Automation"],
            "required_experience": 3,
            "description": "Test apps deeply",
            "company": "Acme",
            "location": "Bengaluru",
            "remote_policy": True,
        },
    )
    assert updated.status_code == 200
    body = updated.json()
    assert body["title"] == "Senior QA Engineer"
    assert body["company"] == "Acme"
    assert body["created_at"]
    assert body["updated_at"]

    closed = client.patch(f"/jobs/mine/{job_id}/status", json={"status": "closed"})
    assert closed.status_code == 200
    assert closed.json()["status"] == "closed"
    assert closed.json()["accepts_applications"] is False


def test_employer_repost_same_job_id_still_lists_mine(client):
    client.post(
        "/auth/register",
        json={"email": "emp-dup@test.com", "password": "secret1", "role": "employer"},
    )
    payload = {
        "id": "platform-engineer-acme",
        "title": "Platform Engineer",
        "required_skills": ["Python"],
        "required_experience": 3,
        "description": "Build services",
    }
    first = client.post("/jobs", json=payload)
    assert first.status_code == 201
    assert first.json()["id"] == "platform-engineer-acme"

    second = client.post("/jobs", json={**payload, "description": "Build and operate services"})
    assert second.status_code == 201
    assert second.json()["id"] == "platform-engineer-acme"

    mine = client.get("/jobs/mine")
    assert mine.status_code == 200
    ids = [row["id"] for row in mine.json()]
    assert ids.count("platform-engineer-acme") == 1
    assert mine.json()[0]["description"] == "Build and operate services"


def test_employer_cannot_post_job_id_owned_by_another(client):
    client.post(
        "/auth/register",
        json={"email": "emp-owner@test.com", "password": "secret1", "role": "employer"},
    )
    created = client.post(
        "/jobs",
        json={
            "id": "shared-role-id",
            "title": "Shared Role",
            "required_skills": ["Python"],
            "required_experience": 2,
            "description": "Owned by first employer",
        },
    )
    assert created.status_code == 201

    client.post(
        "/auth/register",
        json={"email": "emp-intruder@test.com", "password": "secret1", "role": "employer"},
    )
    hijack = client.post(
        "/jobs",
        json={
            "id": "shared-role-id",
            "title": "Hijacked Role",
            "required_skills": ["Rust"],
            "required_experience": 1,
            "description": "Should be rejected",
        },
    )
    assert hijack.status_code == 403
    assert hijack.json()["detail"]["code"] == "JOB_NOT_OWNED"

    client.post(
        "/auth/login",
        json={"email": "emp-owner@test.com", "password": "secret1"},
    )
    job = client.get("/jobs/mine")
    assert job.json()[0]["title"] == "Shared Role"
