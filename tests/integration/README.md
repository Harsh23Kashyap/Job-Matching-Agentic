# Integration tests

HTTP-level tests using FastAPI `TestClient` — full request/response cycles.

## Key suites

| File | Covers |
|------|--------|
| `test_feature_reverification.py` | End-to-end feature checklist (composite, JD, feedback, CID, upsert) |
| `test_candidate_profile_flow.py` | PUT `/candidates/me` create/update, ownership |
| `test_auth_api.py` | Register, login, session cookie, role guard |
| `test_match_flow.py` | Match endpoints, score breakdown fields |
| `test_api_gateway.py` | Route wiring, system config |
| `test_resume_upload.py` | Upload + CID cleanup + contact extract |
| `test_job_parse.py` | JD paste parse endpoint |
| `test_feedback_actions_api.py` | Portal feedback persistence |
| `test_similar_api.py` | Similar jobs/candidates |
| `test_demo_seed.py` | Demo account seeding |
| `test_bootstrap.py` | Corpus load counts |

Run: `pytest tests/integration -q`

## Live smoke (optional)

Requires backend running on `:8001`:

```bash
python3 scripts/smoke_employer_jobs.py
```
