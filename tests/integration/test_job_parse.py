from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(system):
    from gateway.app import build_gateway

    app = build_gateway(system)
    with TestClient(app) as c:
        yield c


def _register_employer(client, email="emp-jd@test.com"):
    return client.post(
        "/auth/register",
        json={"email": email, "password": "secret1", "role": "employer"},
    )


@patch("gateway.routes.employers.create_llm_parser")
def test_parse_job_description_text_success(mock_factory, client):
    from hooks.llm_parser import LlmParser

    mock_parser = LlmParser(client.app.state.container.settings)
    mock_parser.parse_job_from_text = lambda _text: {
        "title": "Data Engineer",
        "required_skills": ["Python", "SQL"],
        "required_experience": 4,
        "description": "Build data pipelines",
        "company": "Acme",
        "location": "Bengaluru",
        "remote_policy": True,
        "job_type": "Full-time",
        "link": None,
        "budget_currency": "INR",
        "budget_min": 1500000,
        "budget_max": 2200000,
        "budget": 2200000,
    }
    mock_factory.return_value = mock_parser

    _register_employer(client)
    jd = (
        "Data Engineer at Acme Labs in Bengaluru (Hybrid). "
        "4+ years with Python and SQL. Compensation 15–22 LPA INR. Full-time role."
    )
    resp = client.post("/jobs/parse-description", json={"text": jd})
    assert resp.status_code == 200
    data = resp.json()
    assert data["llm_status"] == "ok"
    assert data["extracted_fields"]["title"] == "Data Engineer"
    assert "Python" in data["extracted_fields"]["required_skills"]
    assert data["extracted_fields"]["budget_min"] == 1500000


@patch("gateway.routes.employers.create_llm_parser")
def test_parse_job_description_llm_unavailable(mock_factory, client):
    from hooks.llm_parser import LlmParser, LlmUnavailableError

    mock_parser = LlmParser(client.app.state.container.settings)
    mock_parser.parse_job_from_text = lambda _text: (_ for _ in ()).throw(LlmUnavailableError("off"))
    mock_factory.return_value = mock_parser

    _register_employer(client, "emp-jd-fail@test.com")
    jd = "Senior Backend Engineer role with Python, FastAPI, and 5 years experience in Bengaluru."
    resp = client.post("/jobs/parse-description", json={"text": jd})
    assert resp.status_code == 200
    data = resp.json()
    assert data["llm_status"] == "unavailable"
    assert data["extracted_fields"]["title"] == ""
    assert "message" in data


def test_parse_job_description_requires_auth(client):
    resp = client.post("/jobs/parse-description", json={"text": "x" * 50})
    assert resp.status_code == 401


def test_parse_job_description_text_too_short(client):
    _register_employer(client, "emp-jd-short@test.com")
    resp = client.post("/jobs/parse-description", json={"text": "too short"})
    assert resp.status_code == 400
