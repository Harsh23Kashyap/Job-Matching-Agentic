import logging
from collections import defaultdict
from collections.abc import Callable
from datetime import datetime, timezone

from bus.events import AgentEvent, EventType

logger = logging.getLogger(__name__)


class AgentEventBus:
    """In-process synchronous pub-sub."""

    def __init__(self) -> None:
        self._handlers: dict[EventType, list[Callable[[AgentEvent], None]]] = defaultdict(list)
        self.recent_events: list[AgentEvent] = []

    def subscribe(self, event_type: EventType, handler: Callable[[AgentEvent], None]) -> None:
        self._handlers[event_type].append(handler)

    def publish(self, event: AgentEvent) -> None:
        self.recent_events.append(event)
        if len(self.recent_events) > 50:
            self.recent_events = self.recent_events[-50:]
        for handler in self._handlers.get(event.event_type, []):
            try:
                handler(event)
            except Exception:
                logger.exception("Event handler failed for %s", event.event_type)

    def clear(self) -> None:
        self._handlers.clear()
        self.recent_events.clear()

    @staticmethod
    def make_event(event_type: EventType, publisher_id: str, payload: dict) -> AgentEvent:
        return AgentEvent(
            event_type=event_type,
            timestamp=datetime.now(timezone.utc),
            publisher_id=publisher_id,
            payload=payload,
        )
