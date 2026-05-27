# Unit tests

Fast, isolated tests · no live server required (except where noted).

## Python (`test_*.py`)

| Area | Examples |
|------|----------|
| Agents | `test_candidate_agent.py`, `test_employer_agent.py`, `test_matchmaking_agent.py` |
| Scoring | `test_scoring.py`, `test_component_scores.py`, `test_skill_overlap.py` |
| Resume | `test_resume_clean.py`, `test_contact_extract.py`, `test_resume_text.py` |
| Stores | `test_chroma_store.py`, `test_qdrant_store.py`, `test_feedback_store.py` |
| ML v2 | `test_ml_features.py`, `test_lexical.py`, `test_fairness.py` |
| Bus | `test_event_bus.py`, `test_rrf.py` |

Run: `pytest tests/unit -q`

## Node (`test_*.mjs`)

Frontend utility tests · run from repo root:

```bash
node --test tests/unit/test_profile_fields.mjs
node --test tests/unit/test_match_format.mjs
node --test tests/unit/test_feedback_state.mjs
node --test tests/unit/test_skills_input.mjs
node --test tests/unit/test_portal_background.mjs
```

Or all: `node --test tests/unit/test_*.mjs`
