# Frontend unit tests

Node built-in test runner for `frontend/src/utils/*` helpers. Imports use repo-root paths.

| File | Covers |
|------|--------|
| `test_profile_fields.mjs` | Profile readiness, stale marker, payload mapping |
| `test_profile_normalize.mjs` | Field cleaning and normalization |
| `test_match_format.mjs` | Score bands, labels, currency formatting |
| `test_match_scoring.mjs` | Client-side score helpers |
| `test_match_filters.mjs` | Filter/sort logic for match result panels |
| `test_match_explainability.mjs` | Explanation resolver |
| `test_feedback_state.mjs` | Feedback map builders |
| `test_skills_input.mjs` | Skill chip input parsing |
| `test_portal_background.mjs` | Portal background styling helpers |

Run from repo root:

```bash
node --test tests/unit/frontend/test_*.mjs
```

Single file:

```bash
node --test tests/unit/frontend/test_profile_fields.mjs
```
