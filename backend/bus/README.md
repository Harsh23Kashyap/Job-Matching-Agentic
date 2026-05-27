# Event bus

In-process pub-sub for agent communication (event-driven monolith — no Redis or external broker in v1).

## Files

| File | Purpose |
|------|---------|
| `event_bus.py` | `AgentEventBus` — subscribe, publish, recent events ring buffer |
| `events.py` | `EventType` enum and `AgentEvent` dataclass |

## Event types

| Event | Publisher | Typical subscriber |
|-------|-----------|-------------------|
| `CandidateProfileUpdated` | Candidate Agent | Matchmaking Agent (cache invalidation) |
| `JobProfileUpdated` | Employer Agent | Matchmaking Agent |
| `CorpusBootstrapped` | System bootstrap | Admin event strip |
| `MatchCompleted` | Matchmaking Agent | Admin event strip |

## Admin visibility

`GET /agents/events/recent` returns the last 50 bus events for debugging.
