import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(system):
    from gateway.app import build_gateway

    app = build_gateway(system)
    with TestClient(app) as test_client:
        yield test_client


def test_get_real_jobs_status(client: TestClient):
    resp = client.get("/real-jobs/status")
    assert resp.status_code == 200
    body = resp.json()
    assert "enabled" in body
    assert "state" in body
    assert body["state"]["source"] in {"local_seed", "snapshot", "external_api"}
    assert "job_count" in body["state"]


def test_real_jobs_sync_disabled(client: TestClient):
    resp = client.post("/real-jobs/sync", json={"reindex": False})
    assert resp.status_code == 400
    assert "disabled" in resp.json()["detail"].lower()
