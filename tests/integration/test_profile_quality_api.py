import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(system):
    from gateway.app import build_gateway

    app = build_gateway(system)
    with TestClient(app) as c:
        yield c


def _register_candidate(client, email="cand-quality@test.com"):
    return client.post(
        "/auth/register",
        json={"email": email, "password": "secret1", "role": "candidate"},
    )


def test_profile_quality_check_endpoint(client):
    _register_candidate(client)
    resp = client.post(
        "/candidates/quality-check",
        json={
            "name": "Jane Doe",
            "skills": ["Python"],
            "experience_years": 3,
            "summary": "Engineer",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "score" in data
    assert "parsing_confidence" in data
    assert "skill_suggestions" in data


def test_upload_resume_includes_quality(client):
    import io
    from unittest.mock import patch

    from hooks.llm_parser import LlmParser, LlmUnavailableError

    _register_candidate(client, "cand-quality-upload@test.com")

    with patch("gateway.routes.candidates.create_llm_parser") as mock_factory:
        mock_parser = LlmParser(client.app.state.container.settings)
        mock_parser.parse_candidate_from_text = lambda _text: (_ for _ in ()).throw(LlmUnavailableError("off"))
        mock_factory.return_value = mock_parser

        content = b"Harsh Kashyap\nharsh@example.com\nPython, FastAPI\n5 years experience"
        resp = client.post(
            "/candidates/upload-resume",
            files={"file": ("resume.txt", io.BytesIO(content), "text/plain")},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "quality" in data
    assert isinstance(data["quality"]["score"], int)
