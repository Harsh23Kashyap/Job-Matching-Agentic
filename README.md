# Job-Matching-Agentic

Multi-agent job matching system — Candidate Agent, Employer Agent, and Matchmaking Agent.

| Document | Path |
|----------|------|
| High-Level Design (HLD) | [docs/design/HLD-multi-agent-system.md](docs/design/HLD-multi-agent-system.md) |
| Software Design Document (SDD) | [docs/design/SDD-multi-agent-system.md](docs/design/SDD-multi-agent-system.md) |
| V1 vs V2 scope | [docs/design/V1-V2-SCOPE.md](docs/design/V1-V2-SCOPE.md) |
| V1.1 role portals + auth | [docs/design/v1.1-role-portals-auth.md](docs/design/v1.1-role-portals-auth.md) |

## Setup

```bash
# Backend (Python 3.11+ recommended)
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements-min.txt

# From repo root — run API (factory app)
cd backend && source .venv/bin/activate
uvicorn main:create_app --factory --reload --port 8001

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 (frontend) and http://localhost:8001/docs (API).

### LLM resume extraction (candidate onboarding)

Candidate resume upload uses **Ollama** by default. Start Ollama locally and pull a model:

```bash
ollama pull llama3.2
ollama serve   # if not already running
```

Optional: set `OPENAI_API_KEY` in `backend/.env` to use an OpenAI-compatible API instead of Ollama.

## Portals (v1.1)

| Role | Routes | Purpose |
|------|--------|---------|
| **Candidate** | `/candidate/onboarding`, `/profile`, `/matches` | Upload resume → AI extract → find jobs |
| **Employer** | `/employer/jobs`, `/matches` | Create jobs → find candidates |
| **Admin** | `/admin/console` | Full Match Console (eval, ensemble, daily batch) |

Register at `/register` and pick a role. Sign in at `/login`.

## API overview

| Route | Description |
|-------|-------------|
| `POST /auth/register`, `/auth/login`, `/auth/logout`, `GET /auth/me` | Session auth (HTTP-only cookie) |
| `GET /agents/status` | Candidate, Employer, Matchmaking agent health |
| `GET /candidates`, `GET /jobs` | List names / titles |
| `GET /candidates/me`, `GET /jobs/mine` | Owned profile / jobs (authenticated) |
| `POST /candidates/upload-resume` | PDF/DOCX/TXT → LLM field extraction (candidate) |
| `POST /match/candidate-to-jobs` | Resume → jobs (default semantic cosine) |
| `POST /match/job-to-candidates` | Job → candidates |
| `POST /match/ensemble` | RRF over multiple strategy/metric combos |
| `POST /match/daily-batch` | ANN daily recommendations JSON artifact |
| `GET /system/config` | Supported strategies, metrics, skills modes |

Legacy aliases: `/match-resume`, `/match-job`, `/match-resume-ensemble`, `/agent/run-daily-recommendations`.

## Manual smoke checklist

1. Start backend and frontend (see Setup).
2. Register as **admin** → `/admin/console` shows 3 agents with 30 candidates and 15 jobs.
3. Select **Rahul Sharma**, run semantic cosine match → **Machine Learning Engineer** rank 1.
4. Register as **candidate** → upload resume on onboarding → save profile → find jobs.
5. Register as **employer** → create a job → find matching candidates.

## Tests

```bash
cd backend && source .venv/bin/activate
pytest ../tests -v
```

Expected: **59 tests** pass, including Rahul Sharma → Machine Learning Engineer rank 1 smoke test.
