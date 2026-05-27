import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(system):
    from gateway.app import build_gateway

    app = build_gateway(system)
    with TestClient(app) as c:
        yield c


def _register(client, email="flow@test.com"):
    client.post(
        "/auth/register",
        json={"email": email, "password": "secret1", "role": "candidate"},
    )


def _profile_body(name="Flow User", skills=None):
    return {
        "name": name,
        "skills": skills or ["Python"],
        "experience_years": 2,
        "summary": "Backend engineer",
    }


def test_put_me_upserts_empty_id_and_get_me_returns_profile(client):
    _register(client, "empty-id@test.com")
    assert client.get("/candidates/me").status_code == 404

    created = client.put("/candidates/me", json={**_profile_body(), "id": ""})
    assert created.status_code == 200
    profile_id = created.json()["id"]
    assert profile_id
    assert created.json()["name"] == "Flow User"

    me = client.get("/candidates/me")
    assert me.status_code == 200
    assert me.json()["id"] == profile_id

    updated = client.put(
        "/candidates/me",
        json={
            **_profile_body(name="Flow User Updated"),
            "skills": ["Python", "FastAPI"],
            "experience_years": 3,
        },
    )
    assert updated.status_code == 200
    assert updated.json()["id"] == profile_id
    assert updated.json()["name"] == "Flow User Updated"
    assert "FastAPI" in updated.json()["skills"]


def test_post_candidates_upserts_for_logged_in_candidate(client):
    _register(client, "post-upsert@test.com")
    first = client.post("/candidates", json=_profile_body(name="Post User"))
    assert first.status_code == 201
    profile_id = first.json()["id"]

    second = client.post(
        "/candidates",
        json={
            **_profile_body(name="Post User Updated"),
            "skills": ["Go", "Python"],
            "id": "some-other-id",
        },
    )
    assert second.status_code == 201
    assert second.json()["id"] == profile_id
    assert second.json()["name"] == "Post User Updated"
    assert "Go" in second.json()["skills"]

    me = client.get("/candidates/me")
    assert me.status_code == 200
    assert me.json()["id"] == profile_id


def test_stale_in_memory_profile_is_recreated_on_put(client):
    _register(client, "stale-link@test.com")
    created = client.put("/candidates/me", json=_profile_body(name="Stale User"))
    assert created.status_code == 200
    profile_id = created.json()["id"]

    candidate_agent = client.app.state.container.candidate
    del candidate_agent.state.profiles[profile_id]
    candidate_agent.state.name_index.pop("Stale User", None)

    missing = client.get("/candidates/me")
    assert missing.status_code == 404
    assert missing.json()["detail"]["code"] == "PROFILE_NOT_FOUND"

    recreated = client.put(
        "/candidates/me",
        json={**_profile_body(name="Stale User"), "skills": ["Rust"]},
    )
    assert recreated.status_code == 200
    assert recreated.json()["id"] == profile_id
    assert "Rust" in recreated.json()["skills"]

    me = client.get("/candidates/me")
    assert me.status_code == 200
    assert me.json()["name"] == "Stale User"


def test_match_works_after_profile_upsert_without_reupload(client):
    _register(client, "match-flow@test.com")
    client.put("/candidates/me", json=_profile_body(name="Rahul Sharma", skills=["Python", "ML"]))

    match = client.post(
        "/match/candidate-to-jobs",
        json={
            "query_key": "Rahul Sharma",
            "top_k": 5,
            "strategy": "composite",
        },
    )
    assert match.status_code == 200
    body = match.json()
    assert body["results"]
    assert body["query_label"]

    refresh = client.post(
        "/match/candidate-to-jobs",
        json={
            "query_key": "Rahul Sharma",
            "top_k": 5,
            "strategy": "composite",
        },
    )
    assert refresh.status_code == 200
    assert refresh.json()["results"]
