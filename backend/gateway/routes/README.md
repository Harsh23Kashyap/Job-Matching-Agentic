# HTTP routes

FastAPI routers mounted by `gateway/app.py`.

## Route modules

| File | Prefix | Auth | Endpoints |
|------|--------|------|-----------|
| `candidates.py` | `/candidates` | candidate role for `/me` | List, get mine, **PUT upsert**, upload resume, saved jobs, applications, resume suggestions |
| `employers.py` | `/jobs` | employer role for `/mine` | List, mine, upload JD, **parse pasted JD**, update job, applications feed |
| `matching.py` | `/match` | varies | candidate-to-jobs, job-to-candidates, ensemble, daily-batch + legacy aliases |
| `feedback.py` | `/feedback` | portal | actions (save/apply/reject/…), `/me`, legacy pair feedback |
| `similar.py` | `/similar` | role-guarded | similar jobs, similar candidates |
| `agents.py` | `/agents` | · | status, events/recent |
| `system.py` | `/system` | admin-ish | config, vector-store switch, fairness |

Auth routes: `auth/routes.py` at `/auth/*`.

## Conventions

- 404 profile: `{"error": "...", "code": "NOT_FOUND"}`
- Candidate profile upsert: always `PUT /candidates/me` (create or update)
- Default match strategy in frontend: `composite`

Interactive docs: http://localhost:8001/docs
