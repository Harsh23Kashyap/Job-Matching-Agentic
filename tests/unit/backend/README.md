# Backend unit tests

Fast, isolated Python tests — no live server required (except where noted).

| Area | Examples |
|------|----------|
| Agents | `test_candidate_agent.py`, `test_employer_agent.py`, `test_matchmaking_agent.py` |
| Scoring | `test_scoring.py`, `test_component_scores.py`, `test_skill_overlap.py` |
| Resume / JD | `test_resume_clean.py`, `test_contact_extract.py`, `test_job_structured_extract.py` |
| Stores | `test_chroma_store.py`, `test_qdrant_store.py`, `test_feedback_store.py` |
| ML / eval helpers | `test_ml_features.py`, `test_lexical.py`, `test_fairness.py`, `test_benchmark_metrics.py` |
| Bus / fusion | `test_event_bus.py`, `test_rrf.py` |

Run from repo root:

```bash
cd backend && source .venv/bin/activate
pytest ../tests/unit/backend -q
```
