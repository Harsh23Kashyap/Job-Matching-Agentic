import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(system):
    from gateway.app import build_gateway

    app = build_gateway(system)
    with TestClient(app) as c:
        yield c


def test_record_feedback(client):
    resp = client.post(
        "/feedback",
        json={"candidate_id": "cv_01", "job_id": "job_01", "action": "save"},
    )
    assert resp.status_code == 200
    assert resp.json()["ok"] is True


def test_feedback_counts(client):
    client.post(
        "/feedback",
        json={"candidate_id": "cv_01", "job_id": "job_02", "action": "save"},
    )
    client.post(
        "/feedback",
        json={"candidate_id": "cv_01", "job_id": "job_02", "action": "apply"},
    )
    resp = client.get("/feedback/counts", params={"candidate_id": "cv_01", "job_id": "job_02"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["save_count"] == 1
    assert data["apply_count"] == 1


def test_match_with_constraints(client):
    resp = client.post(
        "/match/candidate-to-jobs",
        json={
            "query_key": "Rahul Sharma",
            "top_k": 3,
            "apply_constraints": True,
            "strategy": "multimodal",
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["results"]


def test_match_auto_strategy(client):
    resp = client.post(
        "/match/candidate-to-jobs",
        json={
            "query_key": "Rahul Sharma",
            "top_k": 3,
            "auto_strategy": True,
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("routing_reason")


def test_system_config_ml_features(client):
    resp = client.get("/system/config")
    assert resp.status_code == 200
    data = resp.json()
    assert "fusion_modes" in data
    assert "ml_features" in data
