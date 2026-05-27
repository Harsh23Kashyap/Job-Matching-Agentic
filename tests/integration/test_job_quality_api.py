from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(system):
    from gateway.app import build_gateway

    app = build_gateway(system)
    with TestClient(app) as c:
        yield c


def _register_employer(client, email="emp-quality@test.com"):
    return client.post(
        "/auth/register",
        json={"email": email, "password": "secret1", "role": "employer"},
    )


def test_job_quality_check_endpoint(client):
    _register_employer(client)
    resp = client.post(
        "/jobs/quality-check",
        json={
            "title": "Backend Engineer",
            "required_skills": ["Python"],
            "description": "Build APIs",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "score" in data
    assert "missing_fields" in data
    assert "skill_suggestions" in data


@patch("gateway.routes.employers.create_llm_parser")
def test_parse_description_includes_quality(mock_factory, client):
    from hooks.llm_parser import LlmParser

    mock_parser = LlmParser(client.app.state.container.settings)
    mock_parser.parse_job_from_text = lambda _text: {
        "title": "Data Engineer",
        "required_skills": ["Python", "SQL"],
        "required_experience": 4,
        "description": "Build data pipelines and own batch jobs.",
        "company": "Acme",
        "location": "Bengaluru",
        "remote_policy": True,
        "job_type": "Full-time",
        "link": None,
        "budget_currency": "INR",
        "budget_min": 1500000,
        "budget_max": 2200000,
        "budget": 2200000,
        "education_requirements": [],
        "responsibilities": [],
    }
    mock_factory.return_value = mock_parser

    _register_employer(client, "emp-quality-parse@test.com")
    jd = "Data Engineer at Acme Labs in Bengaluru. Python and SQL. 4+ years. 15-22 LPA."
    resp = client.post("/jobs/parse-description", json={"text": jd})
    assert resp.status_code == 200
    data = resp.json()
    assert "quality" in data
    assert isinstance(data["quality"]["score"], int)
