# Handoff
> Written: 2026-05-27 16:25 | Branch: main | Dir: /Users/harshkashyap/Projects/JobMatcher-v1/Job-Matching-Agentic

## Goal

Build and demonstrate a **three-agent job matching system** (Candidate, Employer, Matchmaking) with core ML matching, a research eval console, and **v1.1 product portals** (Candidate / Employer / Admin) including session auth, LLM-assisted resume onboarding, and **calm hiring-workspace UX** (not debug dashboards). Long-term: white-paper manuscript aligned with implemented architecture (code first).

## Current state

- **Done:**
  - **V1** — Full backend (3 agents, in-process event bus, Chroma, FastAPI gateway), admin Match Console UI, eval corpus (30 CVs / 15 jobs / 47 pairs)
  - **V1.1 (`75c7d4b`)** — SQLite auth, role portals (React Router), LLM resume upload, ownership APIs, auth/upload tests
  - **Product UX Polish (`5cbb2fb`, pushed)** — Warm editorial design system, shared form components, stepper onboarding, profile strength + toast, card-based candidate/employer match results, UserMenu nav, branded error pages, LLM graceful fallback, `backend/.env.example`, `experience_years` as float (0–50)
  - Design docs: HLD, SDD, V1-V2-SCOPE, v1.1 spec, PAPER-FEATURES-INVENTORY
- **In progress:**
  - None — UX polish plan todos all completed
- **Blocked:**
  - None for local demo once backend on 8001 and frontend dev server running

## Decisions made

| Decision | Why | Alternatives rejected |
|----------|-----|----------------------|
| Event-driven monolith (3 agent classes + in-process bus) | Credible MAS story without microservice ops | Microservices day one |
| Split results UI by audience | Admin keeps technical `ResultsPanel`; candidate/employer get card UI with % scores | Single shared results table |
| Frontend-only INR formatting | API stores integer salary; UI formats Indian grouping | Store formatted strings in API |
| `experience_years` as float | Supports 0.5-year steps in profile forms | Keep int-only |
| Client-side match filters v1 | No new API; filter/sort existing `response.results` | Server-side filter params |
| LLM upload returns 200 on unavailable | Don't block onboarding when Ollama/OpenAI down | 503 hard fail |
| OpenAI when key set, else Ollama | User provided OpenAI key; Ollama optional fallback | Heuristics-only |
| `load_dotenv(..., override=True)` | Stale shell `OPENAI_API_KEY` was overriding `.env` | Trust shell env first |
| API port **8001** | Port 8000 conflict on user's machine | Keep 8000 |
| UI: warm neutral + sage accent | User rejected blue "AI startup" aesthetic | LinkedIn blue theme |
| Secrets in `backend/.env` only | Never commit API keys | Key in repo |

## Open questions

- [ ] **Hypothesis:** OpenAI key was pasted in chat — rotate in OpenAI dashboard before any prod use
- [ ] **Unknown:** Manual E2E smoke after push (register → onboarding → find jobs → employer post job → find candidates) — not run in CI
- [ ] **Paper timing:** Update §3 multi-agent diagram after supervisor approves demo
- [ ] **V2 priority:** Benchmark Table 9 parity vs LLM JD parser vs Qdrant — not decided

## Blockers & dependencies

| What | Who/Where | Status |
|------|-----------|--------|
| OpenAI for resume extract | `backend/.env` `OPENAI_API_KEY` | Configured locally (gitignored) |
| Ollama fallback | Local `ollama serve` + `llama3.2` | Optional if OpenAI key set |
| Backend v1.1 on port 8001 | Developer restart uvicorn | Required for auth + upload |
| Legacy benchmark parity (Table 9) | V2 scope | Not started |

## Environment

- **Branch:** main (tracking `origin/main`)
- **Uncommitted changes:** `HANDOFF.md` only (this update)
- **Recent commits:**
  - `5cbb2fb` Polish candidate/employer UX with product-facing match results and shared form system
  - `75c7d4b` Add v1.1 auth, role portals, LLM resume parsing, and research feature inventory
  - `fb678ae` Polish frontend UI and default API port to 8001
- **Build status:** passing (`npm run build` in `frontend/`)
- **Test status:** **60 passed** (`pytest ../tests -v` from `backend/`)
- **Active processes:** `npm run dev` in `frontend/` (may need restart if showing stale Vite parse error — `npm run build` is clean)

## What worked

- Phased v1 → v1.1 → UX polish without breaking integration tests
- Shared `ProfileForm` + field components reused in Onboarding and Profile
- `CandidateJobResults` / `EmployerCandidateResults` with summary cards, filters, humanized copy
- Vite proxy `/auth` → 8001 + `withCredentials: true` for session cookies
- `load_dotenv(override=True)` fixed stale shell env overriding `.env`
- Plain `git commit -m "..."` (simple `-m` flag) — succeeds reliably
- Push to `origin/main` succeeded (`75c7d4b..5cbb2fb`)

## What didn't work

- **Stale backend on 8001** — Old process served v1.0.0 without `/auth/*`; registration 404
- **git commit with HEREDOC** — Hung indefinitely in this session; use plain `-m` instead
- **Shell `OPENAI_API_KEY` overriding `.env`** — Fixed via `override=True` in `config.py`
- **503 on resume upload without Ollama** — Fixed to graceful fallback
- **Blue LinkedIn theme** — User rejected; replaced with sage/warm neutrals
- **Python 3.14 venv** — Use **Python 3.11**

## Commands

```bash
cd /Users/harshkashyap/Projects/JobMatcher-v1/Job-Matching-Agentic

# Backend setup (first time)
cd backend && python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements-min.txt

# Secrets (first time — never commit .env)
cp backend/.env.example backend/.env
# Edit backend/.env: set OPENAI_API_KEY, SESSION_SECRET

# Backend (must show 1.1.0)
cd backend && source .venv/bin/activate
uvicorn main:create_app --factory --reload --port 8001

# Verify auth + version
curl -s http://localhost:8001/openapi.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['info']['version'])"

# Frontend
cd frontend && npm install && npm run dev
# http://localhost:5173/login

# Tests
cd backend && source .venv/bin/activate && pytest ../tests -v

# Production build check
cd frontend && npm run build
```

## Key files

| File | Why It Matters |
|------|---------------|
| `frontend/src/App.css` | Canonical design tokens, form system, match cards, nav, admin table polish |
| `frontend/src/utils/format.js` | INR, match %, tiers, humanized strategy/why_ranked |
| `frontend/src/utils/validation.js` | Profile validation + strength scoring |
| `frontend/src/components/ProfileForm.jsx` | Shared profile fields (Onboarding + Profile) |
| `frontend/src/components/CandidateJobResults.jsx` | Product match UI for candidates |
| `frontend/src/components/EmployerCandidateResults.jsx` | Product match UI for employers |
| `frontend/src/layouts/PortalShell.jsx` | 72px nav + UserMenu dropdown |
| `frontend/src/pages/candidate/Onboarding.jsx` | Stepper + resume preview + ProfileForm |
| `frontend/src/pages/candidate/Matches.jsx` | Empty states + Find jobs flow |
| `frontend/src/components/ResultsPanel.jsx` | **Admin only** — technical eval table |
| `backend/contracts/profiles.py` | `experience_years: float` (0–50) |
| `backend/config.py` | Settings + `load_dotenv(override=True)` |
| `backend/hooks/llm_parser.py` | OpenAI (if key) else Ollama resume parsing |
| `backend/.env.example` | Safe secrets template (committed) |
| `docs/research/PAPER-FEATURES-INVENTORY.md` | Paper feature checklist |
| `docs/design/V1-V2-SCOPE.md` | v1 / v1.1 shipped vs v2 deferred |

## External links

- Repo: https://github.com/Harsh23Kashyap/Job-Matching-Agentic
- Latest push: `5cbb2fb` on `main`
- Legacy eval source: https://github.com/Taranum01/Agentic-Job-Matching

## Memory snapshot

- **UI direction:** Warm off-white `#F7F3EC`, sage accent `#52635A`, DM Sans — no bright blue
- **Smoke test:** Rahul Sharma → Machine Learning Engineer rank 1 (semantic cosine)
- **Paper framing:** Khan *Brave New Words* Part VIII — see `.claude/knowledge_graph.md`

## Persistent context

- Knowledge graph: `.claude/knowledge_graph.md`
- Design specs: `docs/design/HLD-multi-agent-system.md`, `SDD-multi-agent-system.md`, `V1-V2-SCOPE.md`, `v1.1-role-portals-auth.md`
- Paper inventory: `docs/research/PAPER-FEATURES-INVENTORY.md`

## Next steps

1. **Manual E2E smoke** — register candidate → onboarding (upload resume) → save profile → Find jobs → expand match details — verify: % scores not raw decimals, admin console still shows technical table
2. **Restart dev servers if stale** — Ctrl+C Vite, rerun `npm run dev`; restart uvicorn on 8001 — verify: no JSX parse error, `/auth/register` returns 201
3. **Rotate OpenAI key** — key was pasted in chat; regenerate and update `backend/.env` — verify: resume upload extracts fields
4. **Employer flow smoke** — register employer → create job card → Find candidates — verify: card UI with match % badges
5. **Paper §3 diagram** — three-agent + event bus matching HLD labels — verify: Candidate/Employer/Matchmaking naming
