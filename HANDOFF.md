# Handoff
> Written: 2026-05-27 | Branch: main | v1.1 implemented

## Goal

Multi-agent job matching with **three role portals** (Candidate, Employer, Admin), session auth, and LLM resume onboarding.

## Current state

- **V1:** Full backend (3 agents, Chroma, FastAPI), Match Console UI, 41 tests — **done**
- **V1.1:** Auth + portals + LLM resume extraction — **done**
- **Tests:** 59 passing (`pytest ../tests -v` from `backend/`)

## V1.1 deliverables

| Area | What shipped |
|------|----------------|
| Auth | SQLite users, bcrypt, HTTP-only cookie sessions, `/auth/*` |
| Candidate portal | Resume upload → Ollama LLM extract → profile → job match |
| Employer portal | Create jobs, list owned jobs, candidate match |
| Admin portal | Original Match Console at `/admin/console` |
| API | `POST /candidates/upload-resume`, `GET /candidates/me`, `GET /jobs/mine` |

## Run

```bash
# Backend
cd backend && source .venv/bin/activate
uvicorn main:create_app --factory --reload --port 8001

# Frontend
cd frontend && npm run dev

# Ollama (for resume extraction)
ollama pull llama3.2
```

Open http://localhost:5173 → `/register` to create an account.

## Key docs

- [docs/design/v1.1-role-portals-auth.md](docs/design/v1.1-role-portals-auth.md) — v1.1 spec (implemented)
- [docs/design/V1-V2-SCOPE.md](docs/design/V1-V2-SCOPE.md) — v1 / v1.1 / v2 split
- [README.md](README.md) — setup and smoke checklist

## Next (v2)

- LLM JD parser, LLM explainer, OAuth/production auth
- Qdrant, Redis bus, benchmark regression gate
- Agent event log panel
