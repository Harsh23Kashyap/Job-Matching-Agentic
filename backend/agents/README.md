# Agents

Three domain agents with clear ownership boundaries. The Matchmaking Agent reads snapshots only — it never writes to vector stores.

## Files

| File | Agent | Owns |
|------|-------|------|
| `candidate_agent.py` | Candidate | CV profiles, `candidates_collection` embeddings |
| `employer_agent.py` | Employer | Job postings, `jobs_collection` embeddings |
| `matchmaking_agent.py` | Matchmaking | Scoring, ranking, explanations, match sessions |
| `base.py` | — | Shared `BaseAgent` helpers |

## Events published

- `CandidateProfileUpdated` — candidate register/update
- `JobProfileUpdated` — job register/update
- `CorpusBootstrapped` — startup load from `data/cvs.json` + `data/jobs.json`
- `MatchCompleted` — after a match run

## Key flows

1. **Register profile** — agent validates → embeds → upserts vector store → publishes update event
2. **Match request** — matchmaker reads snapshots from both agents → scores all pairs → ranks top-K

See [../README.md](../README.md) and [../../docs/design/HLD-multi-agent-system.md](../../docs/design/HLD-multi-agent-system.md).
