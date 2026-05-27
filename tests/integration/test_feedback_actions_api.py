import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(system):
    from gateway.app import build_gateway

    app = build_gateway(system)
    with TestClient(app) as c:
        yield c


def _register_candidate(client, email="fb.candidate@test.com"):
    client.post("/auth/register", json={"email": email, "password": "demo1234", "role": "candidate"})
    client.post("/auth/login", json={"email": email, "password": "demo1234"})
    client.post(
        "/candidates",
        json={
            "name": "Feedback Candidate",
            "skills": ["Python"],
            "experience_years": 2,
            "summary": "test profile",
        },
    )


def _register_employer(client, email="fb.employer@test.com"):
    client.post("/auth/register", json={"email": email, "password": "demo1234", "role": "employer"})
    client.post("/auth/login", json={"email": email, "password": "demo1234"})


def test_candidate_feedback_actions(client):
    _register_candidate(client)
    save = client.post(
        "/feedback/actions",
        json={"target_id": "job_01", "action": "save", "target_label": "Machine Learning Engineer"},
    )
    assert save.status_code == 200

    dismiss = client.post(
        "/feedback/actions",
        json={"target_id": "job_02", "action": "not_interested", "target_label": "Frontend Developer"},
    )
    assert dismiss.status_code == 200

    apply = client.post(
        "/feedback/actions",
        json={
            "target_id": "job_03",
            "action": "apply",
            "target_label": "Backend Engineer",
            "match_score": 0.72,
        },
    )
    assert apply.status_code == 200

    listed = client.get("/feedback/me")
    assert listed.status_code == 200
    by_target = {row["target_id"]: row["action"] for row in listed.json()["feedback"]}
    assert by_target["job_01"] == "save"
    assert by_target["job_02"] == "not_interested"
    assert by_target["job_03"] == "apply"

    saved_jobs = client.get("/candidates/me/saved-jobs")
    assert any(row["job_id"] == "job_01" for row in saved_jobs.json()["saved_jobs"])


def test_employer_feedback_actions(client):
    _register_employer(client)
    save = client.post(
        "/feedback/actions",
        json={
            "target_id": "cv_01",
            "action": "save",
            "context_id": "job_01",
            "target_label": "Rahul Sharma",
        },
    )
    assert save.status_code == 200

    reject = client.post(
        "/feedback/actions",
        json={
            "target_id": "cv_02",
            "action": "reject",
            "context_id": "job_01",
            "target_label": "Priya Mehta",
        },
    )
    assert reject.status_code == 200

    contact = client.post(
        "/feedback/actions",
        json={
            "target_id": "cv_03",
            "action": "contact",
            "context_id": "job_01",
            "target_label": "Arjun Verma",
        },
    )
    assert contact.status_code == 200

    listed = client.get("/feedback/me", params={"context_id": "job_01"})
    assert listed.status_code == 200
    by_target = {row["target_id"]: row["action"] for row in listed.json()["feedback"]}
    assert by_target["cv_01"] == "save"
    assert by_target["cv_02"] == "reject"
    assert by_target["cv_03"] == "contact"


def test_feedback_actions_require_auth(client):
    resp = client.post("/feedback/actions", json={"target_id": "job_01", "action": "save"})
    assert resp.status_code == 401
