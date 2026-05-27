from fastapi.testclient import TestClient


def test_recent_agent_events_after_bootstrap(system):
    from gateway.app import build_gateway

    app = build_gateway(system)
    with TestClient(app) as client:
        resp = client.get("/agents/events/recent")
        assert resp.status_code == 200
        body = resp.json()
        assert "events" in body
        assert len(body["events"]) >= 1
        types = {e["event_type"] for e in body["events"]}
        assert "system.corpus.bootstrapped" in types
        assert len(body["events"]) <= 50


def test_recent_events_after_match(system):
    from gateway.app import build_gateway

    app = build_gateway(system)
    with TestClient(app) as client:
        client.post(
            "/match/candidate-to-jobs",
            json={"query_key": "Rahul Sharma", "top_k": 2},
        )
        resp = client.get("/agents/events/recent")
        assert resp.status_code == 200
        types = {e["event_type"] for e in resp.json()["events"]}
        assert "match.requested" in types or "match.completed" in types
