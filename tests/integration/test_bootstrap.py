def test_bootstrap_loads_corpus(system):
    assert len(system.candidate.list_profiles()) == 30
    assert len(system.employer.list_jobs()) == 15


def test_corpus_bootstrapped_event(system):
    events = [e for e in system.bus.recent_events if e.event_type.value == "system.corpus.bootstrapped"]
    assert events
    assert events[-1].payload["candidates_loaded"] == 30
    assert events[-1].payload["jobs_loaded"] == 15
