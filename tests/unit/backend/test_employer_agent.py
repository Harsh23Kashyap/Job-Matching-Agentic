from bus.events import EventType
from bus.event_bus import AgentEventBus
from hooks.parser import JsonParser
from stores.factory import create_store


def test_register_job_publishes_event(settings):
    from agents.employer_agent import EmployerAgent

    bus = AgentEventBus()
    store = create_store(settings, "test_jobs")
    agent = EmployerAgent(bus=bus, store=store, parser=JsonParser(), settings=settings)
    events = []
    bus.subscribe(EventType.JOB_PROFILE_UPDATED, lambda e: events.append(e))

    raw = {
        "id": "job_test",
        "title": "Test Role",
        "required_skills": ["Python"],
        "required_experience": 1,
        "description": "Test job",
    }
    agent.register(raw)
    assert len(events) == 1
    assert agent.list_titles() == ["Test Role"]


def test_snapshot_fields(settings):
    from agents.employer_agent import EmployerAgent

    bus = AgentEventBus()
    agent = EmployerAgent(
        bus=bus,
        store=create_store(settings, "test_jobs2"),
        parser=JsonParser(),
        settings=settings,
    )
    agent.register(
        {
            "id": "job_y",
            "title": "Backend Engineer",
            "required_skills": ["Java"],
            "required_experience": 3,
            "description": "Backend",
        }
    )
    job = agent.get_by_title("Backend Engineer")
    snap = agent.snapshot(job.id)
    assert snap.required_skills == ["Java"]
