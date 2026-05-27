import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(system):
    from gateway.app import build_gateway

    app = build_gateway(system)
    with TestClient(app) as c:
        yield c


def test_openapi_loads(client):
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    assert "paths" in resp.json()


def test_agent_status_three_agents(client):
    resp = client.get("/agents/status")
    assert resp.status_code == 200
    data = resp.json()
    assert "candidates" in data
    assert "employer" in data
    assert "matchmaking" in data
    assert data["candidates"]["entity_count"] == 30
    assert data["employer"]["entity_count"] == 15


def test_list_candidates(client):
    resp = client.get("/candidates")
    assert resp.status_code == 200
    assert "Rahul Sharma" in resp.json()["names"]


def test_list_jobs(client):
    resp = client.get("/jobs")
    assert resp.status_code == 200
    assert "Machine Learning Engineer" in resp.json()["titles"]


def test_match_candidate_to_jobs(client):
    resp = client.post(
        "/match/candidate-to-jobs",
        json={"query_key": "Rahul Sharma", "top_k": 3},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["results"][0]["target_label"] == "Machine Learning Engineer"


def test_match_not_found(client):
    resp = client.post(
        "/match/candidate-to-jobs",
        json={"query_key": "Nobody Here", "top_k": 3},
    )
    assert resp.status_code == 404


def test_legacy_match_resume_alias(client):
    resp = client.post("/match-resume", json={"query_key": "Rahul Sharma", "top_k": 1})
    assert resp.status_code == 200


def test_system_config(client):
    resp = client.get("/system/config")
    assert resp.status_code == 200
    data = resp.json()
    assert data["vector_store"] == "chroma"
    assert data["read_only"] is False
    assert "read_only_note" in data
    assert "semantic" in data["strategies"]


def test_recent_agent_events(client):
    resp = client.get("/agents/events/recent")
    assert resp.status_code == 200
    assert "events" in resp.json()


def test_vector_store_switch_chroma(client):
    resp = client.post("/system/vector-store", json={"vector_store": "chroma"})
    assert resp.status_code == 200
    assert resp.json()["vector_store"] == "chroma"
    assert resp.json()["candidates_reindexed"] == 30


def test_job_match_contact_fields_optional(client):
    resp = client.post(
        "/match/job-to-candidates",
        json={"query_key": "Machine Learning Engineer", "top_k": 1},
    )
    assert resp.status_code == 200
    row = resp.json()["results"][0]
    assert "contact_email" in row
    assert "contact_phone" in row
    assert "candidate_experience_years" in row
