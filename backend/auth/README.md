# Auth

Email/password authentication with HTTP-only session cookies and role-based access.

## Files

| File | Purpose |
|------|---------|
| `store.py` | SQLite `UserStore` · users, candidate/job ownership links |
| `routes.py` | `POST /auth/register`, `/login`, `/logout`, `GET /auth/me` |
| `deps.py` | FastAPI dependencies: `require_role`, `get_optional_user` |
| `passwords.py` | bcrypt hash and verify |

## Roles

`candidate`, `employer`, `admin` · enforced on portal routes via `require_role()`.

## Ownership

| Table | Links |
|-------|-------|
| `candidate_ownership` | One candidate profile per candidate user |
| `job_ownership` | One employer user per job posting |

`link_candidate()` is idempotent · same ID no-ops; PUT `/candidates/me` upsert keeps the link stable across restarts.

## Session

Cookie name: `jm_session`. Secret: `SESSION_SECRET` in `.env` (change in production).
