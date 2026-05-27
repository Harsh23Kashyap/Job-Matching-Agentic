from bus.events import EventType
from bus.event_bus import AgentEventBus
from hooks.parser import JsonParser
from stores.factory import create_store


def test_register_bumps_version_and_publishes(settings):
    from agents.candidate_agent import CandidateAgent

    bus = AgentEventBus()
    store = create_store(settings, "test_candidates")
    agent = CandidateAgent(bus=bus, store=store, parser=JsonParser(), settings=settings)
    events = []
    bus.subscribe(EventType.CANDIDATE_PROFILE_UPDATED, lambda e: events.append(e))

    raw = {
        "id": "cv_test",
        "name": "Test User",
        "skills": ["Python"],
        "experience_years": 1,
        "summary": "Test",
    }
    p1 = agent.register(raw)
    p2 = agent.register(raw)
    assert p1.version == 1
    assert p2.version == 2
    assert agent.state.store_version == 2
    assert len(events) == 2


def test_get_by_name(settings):
    from agents.candidate_agent import CandidateAgent

    bus = AgentEventBus()
    agent = CandidateAgent(
        bus=bus,
        store=create_store(settings, "test_candidates2"),
        parser=JsonParser(),
        settings=settings,
    )
    agent.register(
        {
            "id": "cv_x",
            "name": "Alice",
            "skills": ["Go"],
            "experience_years": 2,
            "summary": "Go dev",
        }
    )
    assert agent.get_by_name("Alice") is not None
    assert agent.get_by_name("Missing") is None
