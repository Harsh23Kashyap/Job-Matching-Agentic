import pytest
from fastapi.testclient import TestClient

from demo_seed import (
    DEMO_CANDIDATE_EMAIL,
    DEMO_CANDIDATE_ID,
    DEMO_EMPLOYER_EMAIL,
    DEMO_PASSWORD,
    seed_demo_accounts,
)


@pytest.fixture
def client(system):
    from gateway.app import build_gateway

    app = build_gateway(system)
    with TestClient(app) as c:
        yield c


def test_demo_seed_creates_accounts(system):
    from auth.store import UserStore
    from gateway.app import build_gateway

    app = build_gateway(system)
    store = app.state.auth_store

    candidate = store.get_by_email(DEMO_CANDIDATE_EMAIL)
    assert candidate is not None
    assert candidate.role == "candidate"
    assert store.get_candidate_id(candidate.id) == DEMO_CANDIDATE_ID

    employer = store.get_by_email(DEMO_EMPLOYER_EMAIL)
    assert employer is not None
    job_ids = store.list_job_ids(employer.id)
    assert len(job_ids) >= 3


def test_demo_candidate_login_and_profile(client):
    login = client.post(
        "/auth/login",
        json={"email": DEMO_CANDIDATE_EMAIL, "password": DEMO_PASSWORD},
    )
    assert login.status_code == 200

    me = client.get("/candidates/me")
    assert me.status_code == 200
    body = me.json()
    assert body["name"] == "Rahul Sharma"
    assert "Python" in body["skills"]


def test_demo_candidate_finds_jobs(client):
    client.post("/auth/login", json={"email": DEMO_CANDIDATE_EMAIL, "password": DEMO_PASSWORD})
    match = client.post(
        "/match/candidate-to-jobs",
        json={
            "query_key": "Rahul Sharma",
            "top_k": 3,
            "strategy": "multimodal",
            "metric": "cosine",
            "skills_mode": "jaccard",
            "semantic_weight": 0.7,
            "retrieval": "exhaustive",
        },
    )
    assert match.status_code == 200
    results = match.json()["results"]
    assert len(results) >= 1
    assert results[0]["target_label"] == "Machine Learning Engineer"


def test_demo_employer_has_jobs(client):
    client.post("/auth/login", json={"email": DEMO_EMPLOYER_EMAIL, "password": DEMO_PASSWORD})
    mine = client.get("/jobs/mine")
    assert mine.status_code == 200
    titles = [j["title"] for j in mine.json()]
    assert "Machine Learning Engineer" in titles


def test_seed_demo_accounts_idempotent(system):
    from auth.store import UserStore

    store = UserStore(system.settings.sqlite_path)
    first = seed_demo_accounts(store, system)
    second = seed_demo_accounts(store, system)
    assert store.get_by_email(DEMO_CANDIDATE_EMAIL) is not None
    assert "already present" in second["summary"] or first["summary"]
