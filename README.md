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

### Environment variables (secrets)

```bash
cd backend
cp .env.example .env   # first time only — .env is gitignored
# Edit .env and set OPENAI_API_KEY locally. Never commit .env.
```

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | Resume AI extraction (uses OpenAI instead of Ollama when set) |
| `SESSION_SECRET` | Signs auth cookies — **must** change in production |
| `VECTOR_STORE` | `chroma` (default) or `qdrant` |
| `READ_ONLY` | `true` blocks mutating API except auth login/register |
| `OLLAMA_BASE_URL` / `OLLAMA_MODEL` | Local LLM fallback when no OpenAI key |

**Production:** set secrets in your host’s environment / secret manager (Render, Railway, Fly, AWS, etc.). Use `backend/.env.example` as documentation only — do not deploy a `.env` file with real keys.

### LLM resume extraction (candidate onboarding)

Candidate resume upload uses **Ollama** by default. Start Ollama locally and pull a model:

```bash
ollama pull llama3.2
ollama serve   # if not already running
```

Optional: set `OPENAI_API_KEY` in `backend/.env` (see `backend/.env.example`) to use OpenAI instead of Ollama.

## Portals (v1.1 + v2)

| Role | Routes | Purpose |
|------|--------|---------|
| **Candidate** | `/candidate/onboarding`, `/profile`, `/matches` | Upload resume → AI extract → find jobs; save roles; re-upload from profile |
| **Employer** | `/employer/jobs`, `/matches` | Create/upload JD → find candidates; view contact in match drawer |
| **Admin** | `/admin/console` | Match Console, agent events, Chroma/Qdrant switch, ensemble weights |

Register at `/register` and pick a role. Sign in at `/login`.

### Demo accounts (auto-seeded on startup)

| Role | Email | Password |
|------|-------|----------|
| **Candidate** (profile ready) | `demo.candidate@test.com` | `demo1234` |
| **Employer** (5 sample jobs) | `demo.employer@test.com` | `demo1234` |
| **Admin** | `demo.admin@test.com` | `demo1234` |

The candidate demo links to **Rahul Sharma** in the bootstrapped corpus — open **Jobs → Find matches** for instant results. Disable seeding with `SEED_DEMO=false` in `backend/.env`.

## Quick demo (15 min)

Follow the scripted walkthrough for supervisors and stakeholders:

- **[Demo script](docs/demo/DEMO-SCRIPT.md)** — candidate → employer → admin narrative
- **[Pre-flight checklist](docs/demo/DEMO-CHECKLIST.md)** — servers, corpus smoke, demo accounts

## API overview

| Route | Description |
|-------|-------------|
| `POST /auth/register`, `/auth/login`, `/auth/logout`, `GET /auth/me` | Session auth (HTTP-only cookie) |
| `GET /agents/status` | Candidate, Employer, Matchmaking agent health |
| `GET /agents/events/recent` | Last 50 bus events (admin strip) |
| `GET /candidates`, `GET /jobs` | List names / titles |
| `GET /candidates/me`, `GET /jobs/mine` | Owned profile / jobs (authenticated) |
| `POST /candidates/upload-resume` | PDF/DOCX/TXT → LLM field extraction (candidate) |
| `POST /jobs/upload-description` | PDF/DOCX/TXT → LLM JD extraction (employer) |
| `POST /match/candidate-to-jobs` | Resume → jobs (`use_cross_encoder` optional) |
| `POST /match/job-to-candidates` | Job → candidates (includes contact fields when set) |
| `POST /match/ensemble` | RRF over multiple strategy/metric combos |
| `POST /match/daily-batch` | ANN daily recommendations JSON artifact |
| `GET /system/config` | Supported strategies, metrics, vector store, read-only flag |
| `POST /system/vector-store` | Switch Chroma ↔ Qdrant and reindex |

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

Expected: **88 tests** pass, including Rahul Sharma → Machine Learning Engineer rank 1 smoke test and Table 9 regression gate.

### Benchmarks (v2)

From `backend/` with venv active:

```bash
python -m benchmarks.smoke_eval
python -m benchmarks.paper_progression --skip-cross-encoder
python -m benchmarks.phase11 --stores chroma
```

Outputs land in `backend/benchmark_outputs/`.
