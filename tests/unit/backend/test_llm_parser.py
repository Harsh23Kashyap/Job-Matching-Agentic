import json
from unittest.mock import MagicMock, patch

import pytest

from config import Settings
from hooks.llm_parser import LlmParser, LlmUnavailableError


@pytest.fixture
def settings():
    return Settings(
        ollama_base_url="http://ollama.test",
        ollama_model="test-model",
        openai_api_key=None,
    )


@pytest.fixture
def parser(settings):
    return LlmParser(settings)


def test_parse_candidate_from_text_ollama(parser):
    payload = {
        "name": "Jane Doe",
        "skills": ["Python", "FastAPI"],
        "experience_years": 5,
        "preferred_salary": 120000,
        "remote_preference": True,
        "summary": "Backend engineer",
    }
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"message": {"content": json.dumps(payload)}}
    mock_resp.raise_for_status = MagicMock()

    with patch("hooks.llm_parser.httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.post.return_value = mock_resp
        result = parser.parse_candidate_from_text("Jane Doe resume text")

    assert result["name"] == "Jane Doe"
    assert "Python" in result["skills"]
    assert result["experience_years"] == 5
    assert result["remote_preference"] is True


def test_parse_retries_on_bad_json(parser):
    bad = MagicMock()
    bad.json.return_value = {"message": {"content": "not json"}}
    bad.raise_for_status = MagicMock()

    good = MagicMock()
    good.json.return_value = {
        "message": {
            "content": json.dumps(
                {
                    "name": "Retry User",
                    "skills": [],
                    "experience_years": 1,
                    "preferred_salary": None,
                    "remote_preference": False,
                    "summary": "",
                }
            )
        }
    }
    good.raise_for_status = MagicMock()

    with patch("hooks.llm_parser.httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.post.side_effect = [bad, good]
        result = parser.parse_candidate_from_text("resume")

    assert result["name"] == "Retry User"


def test_parse_job_from_text_ollama(parser):
    payload = {
        "title": "Backend Engineer",
        "required_skills": ["Python", "FastAPI"],
        "required_experience": 3,
        "description": "Build APIs",
        "company": "Acme",
        "location": "Remote",
        "remote_policy": True,
        "link": "https://example.com/jobs/1",
        "job_type": "Full-time",
        "budget_min": 1200000,
        "budget_max": 1800000,
        "budget_currency": "INR",
    }
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"message": {"content": json.dumps(payload)}}
    mock_resp.raise_for_status = MagicMock()

    with patch("hooks.llm_parser.httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.post.return_value = mock_resp
        result = parser.parse_job_from_text("Backend engineer job description")

    assert result["title"] == "Backend Engineer"
    assert "Python" in result["required_skills"]
    assert result["required_experience"] == 3
    assert result["remote_policy"] is True
    assert result["job_type"] == "Full-time"
    assert result["budget_min"] == 1200000
    assert result["budget_max"] == 1800000
    assert result["budget_currency"] == "INR"


def test_llm_unavailable(parser):
    with patch("hooks.llm_parser.httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.post.side_effect = OSError("connection refused")
        with pytest.raises(LlmUnavailableError):
            parser.parse_candidate_from_text("resume")
