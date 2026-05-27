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
    content = b"Harsh Kashyap\nharsh@example.com\n+91 9876543210\nhttps://linkedin.com/in/harsh"
    resp = client.post(
        "/candidates/upload-resume",
        files={"file": ("resume.txt", io.BytesIO(content), "text/plain")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["llm_status"] == "unavailable"
    assert "raw_text_preview" in data
    assert data["extracted_fields"]["name"] == ""
    assert data["extracted_fields"]["email"] == "harsh@example.com"
    assert "linkedin.com/in/harsh" in data["extracted_fields"]["linkedin"]


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
