from bus.event_bus import AgentEventBus
from bus.events import EventType


def test_publish_calls_subscriber():
    bus = AgentEventBus()
    seen = []

    def handler(event):
        seen.append(event.event_type)

    bus.subscribe(EventType.MATCH_COMPLETED, handler)
    event = bus.make_event(EventType.MATCH_COMPLETED, "test", {"ok": True})
    bus.publish(event)
    assert seen == [EventType.MATCH_COMPLETED]


def test_handler_exception_does_not_break_other_handlers():
    bus = AgentEventBus()
    seen = []

    def bad_handler(_event):
        raise RuntimeError("boom")

    def good_handler(event):
        seen.append(event.payload["id"])

    bus.subscribe(EventType.MATCH_REQUESTED, bad_handler)
    bus.subscribe(EventType.MATCH_REQUESTED, good_handler)
    bus.publish(bus.make_event(EventType.MATCH_REQUESTED, "x", {"id": 1}))
    assert seen == [1]


def test_recent_events_ring_buffer():
    bus = AgentEventBus()
    for i in range(55):
        bus.publish(bus.make_event(EventType.MATCH_REQUESTED, "x", {"i": i}))
    assert len(bus.recent_events) == 50
    assert bus.recent_events[0].payload["i"] == 5


def test_clear_removes_handlers_and_events():
    bus = AgentEventBus()
    bus.subscribe(EventType.MATCH_COMPLETED, lambda _e: None)
    bus.publish(bus.make_event(EventType.MATCH_COMPLETED, "x", {}))
    bus.clear()
    assert not bus.recent_events
    assert not bus._handlers
