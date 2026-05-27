# Job-Matching-Agentic

Multi-agent job matching system — Candidate Agent, Employer Agent, and Matchmaking Agent.

| Document | Path |
|----------|------|
| High-Level Design (HLD) | [docs/design/HLD-multi-agent-system.md](docs/design/HLD-multi-agent-system.md) |
| Software Design Document (SDD) | [docs/design/SDD-multi-agent-system.md](docs/design/SDD-multi-agent-system.md) |
| V1 vs V2 scope | [docs/design/V1-V2-SCOPE.md](docs/design/V1-V2-SCOPE.md) |

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

## API overview

| Route | Description |
|-------|-------------|
| `GET /agents/status` | Candidate, Employer, Matchmaking agent health |
| `GET /candidates`, `GET /jobs` | List names / titles |
| `POST /match/candidate-to-jobs` | Resume → jobs (default semantic cosine) |
| `POST /match/job-to-candidates` | Job → candidates |
| `POST /match/ensemble` | RRF over multiple strategy/metric combos |
| `POST /match/daily-batch` | ANN daily recommendations JSON artifact |
| `GET /system/config` | Supported strategies, metrics, skills modes |

Legacy aliases: `/match-resume`, `/match-job`, `/match-resume-ensemble`, `/agent/run-daily-recommendations`.

## Manual smoke checklist

1. Start backend and frontend (see Setup).
2. Agent panel shows 3 agents with 30 candidates and 15 jobs.
3. Select **Rahul Sharma**, run semantic cosine match → **Machine Learning Engineer** rank 1.
4. Toggle **skills mode** to soft embedding and re-run — scores change.
5. Run **Daily batch** — file written under `data/daily_recommendations_YYYY-MM-DD.json`.

## Smoke test

```bash
cd backend && source .venv/bin/activate
pytest ../tests -v
```

Expected: Rahul Sharma → Machine Learning Engineer rank 1 on integration smoke test.
