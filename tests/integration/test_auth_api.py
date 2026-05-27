import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(system):
    from gateway.app import build_gateway

    app = build_gateway(system)
    with TestClient(app) as c:
        yield c


def _register(client, email, password, role):
    return client.post(
        "/auth/register",
        json={"email": email, "password": password, "role": role},
    )


def test_register_candidate(client):
    resp = _register(client, "cand@test.com", "secret1", "candidate")
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "cand@test.com"
    assert data["role"] == "candidate"
    assert "id" in data


def test_register_employer(client):
    resp = _register(client, "emp@test.com", "secret1", "employer")
    assert resp.status_code == 201
    assert resp.json()["role"] == "employer"


def test_register_admin(client):
    resp = _register(client, "admin@test.com", "secret1", "admin")
    assert resp.status_code == 201
    assert resp.json()["role"] == "admin"


def test_register_duplicate_email_409(client):
    _register(client, "dup@test.com", "secret1", "candidate")
    resp = _register(client, "dup@test.com", "secret2", "employer")
    assert resp.status_code == 409


def test_login_and_me(client):
    _register(client, "login@test.com", "secret1", "candidate")
    client.post("/auth/logout")
    login = client.post("/auth/login", json={"email": "login@test.com", "password": "secret1"})
    assert login.status_code == 200
    me = client.get("/auth/me")
    assert me.status_code == 200
    assert me.json()["email"] == "login@test.com"


def test_login_invalid_credentials(client):
    _register(client, "bad@test.com", "secret1", "candidate")
    client.post("/auth/logout")
    resp = client.post("/auth/login", json={"email": "bad@test.com", "password": "wrong"})
    assert resp.status_code == 401


def test_me_unauthenticated(client):
    resp = client.get("/auth/me")
    assert resp.status_code == 401


def test_logout_clears_session(client):
    _register(client, "out@test.com", "secret1", "candidate")
    client.post("/auth/logout")
    resp = client.get("/auth/me")
    assert resp.status_code == 401
