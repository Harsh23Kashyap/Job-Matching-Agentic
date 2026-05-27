import pytest
from fastapi.testclient import TestClient

from demo_seed import DEMO_ADMIN_EMAIL, DEMO_CANDIDATE_EMAIL, DEMO_EMPLOYER_EMAIL, DEMO_PASSWORD


@pytest.fixture
def client(system):
    from gateway.app import build_gateway

    app = build_gateway(system)
    with TestClient(app) as c:
        yield c


def _login(client, email):
    response = client.post("/auth/login", json={"email": email, "password": DEMO_PASSWORD})
    assert response.status_code == 200


def test_system_config_includes_demo_mode(client):
    config = client.get("/system/config").json()
    assert config["demo_mode"] is True
    assert config["demo_accounts"] is not None
    assert config["demo_snapshot"]["candidates_in_corpus"] >= 30
    assert config["demo_snapshot"]["jobs_in_corpus"] >= 15


def test_demo_activity_seeded_on_startup(client):
    _login(client, DEMO_CANDIDATE_EMAIL)
    saved = client.get("/candidates/me/saved-jobs")
    assert saved.status_code == 200
    assert len(saved.json()["saved_jobs"]) >= 1

    applications = client.get("/candidates/me/applications")
    assert applications.status_code == 200
    assert len(applications.json()["applications"]) >= 1


def test_demo_reset_requires_admin(client):
    _login(client, DEMO_CANDIDATE_EMAIL)
    response = client.post("/system/demo/reset")
    assert response.status_code == 403


def test_demo_reset_restores_sample_data(client):
    _login(client, DEMO_ADMIN_EMAIL)

    first = client.post("/system/demo/reset")
    assert first.status_code == 200
    body = first.json()
    assert body["candidates_loaded"] >= 30
    assert body["jobs_loaded"] >= 15
    assert body["saved_jobs"] >= 1
    assert body["applications"] >= 1
    assert body["employer_shortlist"] >= 1

    _login(client, DEMO_CANDIDATE_EMAIL)
    profile = client.get("/candidates/me").json()
    assert profile["name"] == "Rahul Sharma"

    saved = client.get("/candidates/me/saved-jobs").json()
    assert len(saved["saved_jobs"]) >= 1

    _login(client, DEMO_EMPLOYER_EMAIL)
    jobs = client.get("/jobs/mine").json()
    assert len(jobs) >= 3
    assert any(job["title"] == "Machine Learning Engineer" for job in jobs)

    _login(client, DEMO_ADMIN_EMAIL)
    second = client.post("/system/demo/reset")
    assert second.status_code == 200
    assert second.json()["saved_jobs"] >= 1


def test_demo_reset_disabled_when_demo_mode_off(system):
    from config import Settings
    from gateway.app import build_gateway

    settings = system.settings.model_copy(update={"demo_mode": False})
    system.settings = settings
    app = build_gateway(system)
    with TestClient(app) as client:
        client.post("/auth/login", json={"email": DEMO_ADMIN_EMAIL, "password": DEMO_PASSWORD})
        response = client.post("/system/demo/reset")
        assert response.status_code == 403
