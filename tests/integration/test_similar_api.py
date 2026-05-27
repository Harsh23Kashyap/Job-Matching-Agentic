import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(system):
    from gateway.app import build_gateway

    app = build_gateway(system)
    with TestClient(app) as c:
        yield c


def _register_candidate(client, email="similar.candidate@test.com"):
    client.post("/auth/register", json={"email": email, "password": "demo1234", "role": "candidate"})
    client.post("/auth/login", json={"email": email, "password": "demo1234"})


def _register_employer(client, email="similar.employer@test.com"):
    client.post("/auth/register", json={"email": email, "password": "demo1234", "role": "employer"})
    client.post("/auth/login", json={"email": email, "password": "demo1234"})


def test_similar_jobs_for_candidate(client):
    _register_candidate(client)
    resp = client.get("/similar/jobs/job_01")
    assert resp.status_code == 200
    data = resp.json()
    assert data["anchor_id"] == "job_01"
    assert data["anchor_label"] == "Machine Learning Engineer"
    assert len(data["items"]) <= 3
    assert all(item["id"] != "job_01" for item in data["items"])


def test_similar_candidates_for_employer(client):
    _register_employer(client)
    resp = client.get("/similar/candidates/cv_01")
    assert resp.status_code == 200
    data = resp.json()
    assert data["anchor_id"] == "cv_01"
    assert data["anchor_label"] == "Rahul Sharma"
    assert len(data["items"]) <= 3
    assert all(item["id"] != "cv_01" for item in data["items"])


def test_similar_jobs_requires_candidate_role(client):
    _register_employer(client)
    resp = client.get("/similar/jobs/job_01")
    assert resp.status_code == 403


def test_similar_candidates_requires_employer_role(client):
    _register_candidate(client, "similar.candidate2@test.com")
    resp = client.get("/similar/candidates/cv_01")
    assert resp.status_code == 403


def test_similar_jobs_not_found(client):
    _register_candidate(client, "similar.candidate3@test.com")
    resp = client.get("/similar/jobs/missing_job")
    assert resp.status_code == 404
