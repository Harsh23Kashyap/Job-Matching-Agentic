from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(system):
    from gateway.app import build_gateway

    app = build_gateway(system)
    with TestClient(app) as c:
        yield c


def _register_candidate(client, email="coach.candidate@test.com"):
    client.post("/auth/register", json={"email": email, "password": "demo1234", "role": "candidate"})
    client.post("/auth/login", json={"email": email, "password": "demo1234"})
    client.post(
        "/candidates",
        json={
            "name": "Coach Test",
            "skills": ["Python", "Machine Learning"],
            "experience_years": 3,
            "summary": "ML engineer with Python experience building models.",
        },
    )


@patch("gateway.routes.candidates.create_llm_parser")
def test_resume_suggestions_rule_based_when_llm_unavailable(mock_factory, client):
    from hooks.llm_parser import LlmParser, LlmUnavailableError

    mock_parser = LlmParser(client.app.state.container.settings)
    mock_parser.suggest_resume_for_job = lambda *_args: (_ for _ in ()).throw(LlmUnavailableError("off"))
    mock_factory.return_value = mock_parser

    _register_candidate(client)
    resp = client.post("/candidates/me/resume-suggestions", json={"job_id": "job_01"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["job_title"] == "Machine Learning Engineer"
    assert data["llm_status"] == "rule_based"
    assert "TensorFlow" in data["missing_skills"]
    assert data["suggested_summary"]
    assert len(data["ats_checklist"]) >= 4
    assert "Suggestions only" in data["disclaimer"]


@patch("gateway.routes.candidates.create_llm_parser")
def test_resume_suggestions_llm_enriched(mock_factory, client):
    from hooks.llm_parser import LlmParser

    mock_parser = LlmParser(client.app.state.container.settings)
    mock_parser.suggest_resume_for_job = lambda _c, _j: {
        "missing_keywords": ["TensorFlow"],
        "weak_skills": ["Machine Learning"],
        "missing_skills": ["TensorFlow"],
        "suggested_summary": "Tailored ML engineer summary.",
        "bullet_improvements": [
            {
                "original": "Built models in Python.",
                "suggested": "Built TensorFlow models in Python.",
                "reason": "Add TensorFlow.",
            }
        ],
        "ats_checklist": [{"item": "Keywords", "status": "warn", "tip": "Add TensorFlow."}],
    }
    mock_factory.return_value = mock_parser

    _register_candidate(client, "coach.candidate2@test.com")
    resp = client.post("/candidates/me/resume-suggestions", json={"job_id": "job_01"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["llm_status"] == "ok"
    assert data["suggested_summary"] == "Tailored ML engineer summary."
    assert data["bullet_improvements"][0]["suggested"].startswith("Built TensorFlow")


def test_resume_suggestions_requires_auth(client):
    resp = client.post("/candidates/me/resume-suggestions", json={"job_id": "job_01"})
    assert resp.status_code == 401


def test_resume_suggestions_unknown_job(client):
    _register_candidate(client, "coach.candidate3@test.com")
    resp = client.post("/candidates/me/resume-suggestions", json={"job_id": "missing_job"})
    assert resp.status_code == 404
