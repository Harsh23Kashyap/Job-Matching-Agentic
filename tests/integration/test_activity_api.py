import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(system):
    from gateway.app import build_gateway

    app = build_gateway(system)
    with TestClient(app) as c:
        yield c


def _register_candidate(client, email="activity.candidate@test.com"):
    client.post("/auth/register", json={"email": email, "password": "demo1234", "role": "candidate"})
    client.post("/auth/login", json={"email": email, "password": "demo1234"})
    client.post(
        "/candidates",
        json={
            "name": "Activity Test",
            "skills": ["Python"],
            "experience_years": 2,
            "summary": "test",
        },
    )


def _register_employer(client, email="activity.employer@test.com"):
    client.post("/auth/register", json={"email": email, "password": "demo1234", "role": "employer"})
    client.post("/auth/login", json={"email": email, "password": "demo1234"})
    client.post(
        "/jobs",
        json={
            "title": "Activity Test Role",
            "required_skills": ["Python"],
            "required_experience": 1,
            "description": "test job",
        },
    )


def test_saved_jobs_and_dismiss(client):
    _register_candidate(client)
    resp = client.put(
        "/candidates/me/saved-jobs",
        json={"job_id": "job_01", "job_title": "Machine Learning Engineer", "saved": True},
    )
    assert resp.status_code == 200
    listed = client.get("/candidates/me/saved-jobs")
    assert listed.status_code == 200
    assert len(listed.json()["saved_jobs"]) == 1

    resp = client.put(
        "/candidates/me/saved-jobs",
        json={"job_id": "job_01", "job_title": "Machine Learning Engineer", "saved": False},
    )
    assert resp.status_code == 200
    listed = client.get("/candidates/me/saved-jobs")
    assert listed.json()["saved_jobs"] == []


def test_application_flow(client):
    _register_candidate(client, "apply.candidate@test.com")
    resp = client.post(
        "/candidates/me/applications",
        json={"job_id": "job_01", "job_title": "Machine Learning Engineer", "match_score": 0.91},
    )
    assert resp.status_code == 201
    apps = client.get("/candidates/me/applications")
    assert apps.json()["applications"][0]["job_id"] == "job_01"


def test_employer_sees_applications(client):
    _register_employer(client, "apps.employer@test.com")
    jobs = client.get("/jobs/mine")
    job_id = jobs.json()[0]["id"]

    client.post("/auth/logout")
    _register_candidate(client, "apps.candidate@test.com")
    client.post(
        "/candidates/me/applications",
        json={"job_id": job_id, "job_title": "Activity Test Role", "match_score": 0.75},
    )

    client.post("/auth/logout")
    client.post("/auth/login", json={"email": "apps.employer@test.com", "password": "demo1234"})
    resp = client.get("/jobs/mine/applications")
    assert resp.status_code == 200
    assert len(resp.json()["applications"]) >= 1


def test_fairness_endpoint(client):
    resp = client.get("/system/fairness")
    assert resp.status_code == 200
    data = resp.json()
    assert data["queries_evaluated"] == 30
    assert "experience_disparate_impact" in data
