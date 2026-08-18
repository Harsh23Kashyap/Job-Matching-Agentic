"""Checklist smoke tests for v1 portal features (items 1–11)."""
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(system):
    from gateway.app import build_gateway

    app = build_gateway(system)
    with TestClient(app) as c:
        yield c


def _register_candidate(client, email="reverify.candidate@test.com"):
    client.post(
        "/auth/register",
        json={"email": email, "password": "demo1234", "role": "candidate"},
    )


def _register_employer(client, email="reverify.employer@test.com"):
    client.post(
        "/auth/register",
        json={"email": email, "password": "demo1234", "role": "employer"},
    )


# 1. Composite ML scoring (semantic, skills, experience, compensation, location)
def test_composite_match_exposes_all_component_scores(client):
    resp = client.post(
        "/match/candidate-to-jobs",
        json={"query_key": "Rahul Sharma", "top_k": 3, "strategy": "composite"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["strategy_used"] == "composite"
    row = body["results"][0]
    for key in (
        "semantic_score",
        "skills_score",
        "experience_score",
        "compensation_score",
        "location_score",
    ):
        assert key in row
        assert row[key] is not None
    assert isinstance(row.get("matched_skills"), list)
    assert isinstance(row.get("missing_skills"), list)
    explanation = row.get("explanation")
    assert explanation is not None
    assert isinstance(explanation.get("matched_skills"), list)
    assert explanation.get("semantic", {}).get("reason")
    assert isinstance(explanation.get("score_breakdown"), list)
    assert len(explanation["score_breakdown"]) >= 5


# 2. Skill gap recommendations surface on match rows
def test_match_rows_include_skill_gaps(client):
    resp = client.post(
        "/match/job-to-candidates",
        json={"query_key": "Machine Learning Engineer", "top_k": 5, "strategy": "composite"},
    )
    assert resp.status_code == 200
    rows = resp.json()["results"]
    assert rows
    assert any(isinstance(r.get("missing_skills"), list) for r in rows)


# 3. LLM JD parser with unavailable fallback
@patch("gateway.routes.employers.create_llm_parser")
def test_jd_parser_llm_unavailable_fallback(mock_factory, client):
    from hooks.llm_parser import LlmParser, LlmUnavailableError

    mock_parser = LlmParser(client.app.state.container.settings)
    mock_parser.parse_job_from_text = lambda _text: (_ for _ in ()).throw(LlmUnavailableError("off"))
    mock_factory.return_value = mock_parser

    _register_employer(client, "reverify-jd@test.com")
    jd = "Senior Backend Engineer with Python, FastAPI, 5 years in Bengaluru. Full-time."
    resp = client.post("/jobs/parse-description", json={"text": jd})
    assert resp.status_code == 200
    data = resp.json()
    assert data["llm_status"] == "unavailable"
    assert "extracted_fields" in data
    assert "message" in data


# 5. Resume improvement suggestions for selected job
def test_resume_suggestions_for_linked_profile(client):
    _register_candidate(client, "reverify-coach@test.com")
    client.put(
        "/candidates/me",
        json={
            "name": "Rahul Sharma",
            "skills": ["Python"],
            "experience_years": 3,
            "summary": "Engineer",
        },
    )
    resp = client.post("/candidates/me/resume-suggestions", json={"job_id": "job_01"})
    assert resp.status_code == 200
    data = resp.json()
    assert "missing_skills" in data
    assert "suggested_summary" in data
    assert "ats_checklist" in data


# 6. Similar jobs and similar candidates
def test_similar_entities_endpoints(client):
    _register_candidate(client, "reverify-sim-c@test.com")
    jobs = client.get("/similar/jobs/job_01")
    assert jobs.status_code == 200
    assert jobs.json()["anchor_id"] == "job_01"
    assert len(jobs.json()["items"]) <= 3

    _register_employer(client, "reverify-sim-e@test.com")
    cands = client.get("/similar/candidates/cv_01")
    assert cands.status_code == 200
    assert cands.json()["anchor_id"] == "cv_01"
    assert len(cands.json()["items"]) <= 3


# 7. Save / apply / reject feedback persisted
def test_feedback_actions_round_trip(client):
    _register_candidate(client, "reverify-fb@test.com")
    client.put(
        "/candidates/me",
        json={"name": "FB User", "skills": ["Go"], "experience_years": 1, "summary": ""},
    )
    assert (
        client.post(
            "/feedback/actions",
            json={"target_id": "job_01", "action": "save", "target_label": "ML Engineer"},
        ).status_code
        == 200
    )
    listed = client.get("/feedback/me")
    assert listed.status_code == 200
    assert any(r["target_id"] == "job_01" and r["action"] == "save" for r in listed.json()["feedback"])


# 8. Employer job routes remain available (portal polish baseline)
def test_employer_job_routes_intact(client):
    _register_employer(client, "reverify-emp@test.com")
    assert client.get("/jobs/mine").status_code == 200
    created = client.post(
        "/jobs",
        json={
            "title": "Reverify Role",
            "required_skills": ["Python"],
            "required_experience": 2,
            "description": "Smoke test role",
        },
    )
    assert created.status_code == 201
    assert created.json()["title"] == "Reverify Role"


# 10. Resume CID cleanup and contact parsing
@patch("gateway.routes.candidates.create_llm_parser")
def test_resume_upload_cid_cleanup_and_contact(mock_factory, client):
    from hooks.llm_parser import LlmParser, LlmUnavailableError

    mock_parser = LlmParser(client.app.state.container.settings)
    mock_parser.parse_candidate_from_text = lambda _text: (_ for _ in ()).throw(LlmUnavailableError("off"))
    mock_factory.return_value = mock_parser

    _register_candidate(client, "reverify-resume@test.com")
    import io

    content = (
        b"Jordan Rivera (cid:131), (cid:239)\n"
        b"jordan@example.com | +91 9876543210\n"
        b"github.com/janedoe\n"
        b"https://leetcode.com/u/janedoe\n"
    )
    resp = client.post(
        "/candidates/upload-resume",
        files={"file": ("resume.txt", io.BytesIO(content), "text/plain")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "(cid:" not in data["cleaned_text"]
    fields = data["extracted_fields"]
    assert fields["name"] == "Jordan Rivera"
    assert fields["email"] == "jordan@example.com"
    assert any("github.com" in link for link in [fields.get("portfolio", ""), *fields.get("other_links", [])])


# 11. Profile upsert: GET /candidates/me and match refresh
def test_profile_upsert_then_search_jobs(client):
    _register_candidate(client, "reverify-flow@test.com")
    assert client.get("/candidates/me").status_code == 404

    saved = client.put(
        "/candidates/me",
        json={
            "name": "Flow User",
            "skills": ["Python", "FastAPI"],
            "experience_years": 2,
            "summary": "Backend",
        },
    )
    assert saved.status_code == 200
    profile_id = saved.json()["id"]

    me = client.get("/candidates/me")
    assert me.status_code == 200
    assert me.json()["id"] == profile_id

    updated = client.put(
        "/candidates/me",
        json={
            "name": "Flow User Updated",
            "skills": ["Python", "FastAPI", "React"],
            "experience_years": 3,
            "summary": "Full stack",
        },
    )
    assert updated.status_code == 200
    assert updated.json()["id"] == profile_id
    assert updated.json()["name"] == "Flow User Updated"

    match = client.post(
        "/match/candidate-to-jobs",
        json={"query_key": "Flow User Updated", "top_k": 3, "strategy": "composite"},
    )
    assert match.status_code == 200
    assert match.json()["results"]
