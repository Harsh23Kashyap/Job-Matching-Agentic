# Contracts

Shared Pydantic models and DTOs used across agents, gateway routes, and tests.

## Files

| File | Models |
|------|--------|
| `profiles.py` | `CandidateProfile`, `JobProfile` · entity schemas |
| `snapshots.py` | `CandidateSnapshot`, `JobSnapshot` · match-time read models with embeddings |
| `matching.py` | `MatchRequest`, `MatchResponse`, `MatchResult`, `ScoreBreakdown`, ensemble/batch DTOs |
| `agent_status.py` | `AgentStatus` · health payload for `/agents/status` |
| `interfaces.py` | Protocol/type hints for stores and parsers |

## Design rule

Agents expose **snapshots** to the matchmaker; raw profiles stay in agent state. Snapshots include precomputed embeddings for scoring.
