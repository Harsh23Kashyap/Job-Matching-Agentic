# Handoff
> Written: 2026-05-27 | Branch: main | Dir: /Users/harshkashyap/Projects/JobMatcher-v1/Job-Matching-Agentic

## Goal

Build and demonstrate a **three-agent job matching system** (Candidate, Employer, Matchmaking) with core ML matching, a research eval console, and **v1.1 product portals** (Candidate / Employer / Admin) including session auth, LLM-assisted resume onboarding, explainable match UI, and calm hiring-workspace UX.

## Current state

- **Done:**
  - **V1** — Full backend (3 agents, in-process event bus, Chroma, FastAPI gateway), admin Match Console UI, eval corpus (30 CVs / 15 jobs / 47 pairs)
  - **V1.1** — SQLite auth, role portals (React Router), LLM resume upload, ownership APIs, PUT `/candidates/me` upsert
  - **Product UX (`5cbb2fb`)** — Warm editorial design system, shared form components, stepper onboarding, card-based match results
  - **Match explainability + contact (`c31b233`)** — `matched_skills` / `missing_skills` on API, MatchDetailsDrawer, profile contact fields (email, phone, LinkedIn, portfolio, other links) with resume extraction, jobs page polish
  - **Demo docs** — `docs/demo/DEMO-SCRIPT.md`, `docs/demo/DEMO-CHECKLIST.md`
  - Design docs: HLD, SDD, V1-V2-SCOPE, v1.1 spec, PAPER-FEATURES-INVENTORY
- **In progress:** None
- **Blocked:** None for local demo once backend on 8001 and frontend dev server running

## Decisions made

| Decision | Why | Alternatives rejected |
|----------|-----|----------------------|
| Event-driven monolith (3 agent classes + in-process bus) | Credible MAS story without microservice ops | Microservices day one |
| Split results UI by audience | Admin keeps technical `ResultsPanel`; candidate/employer get card UI with % scores | Single shared results table |
| Skill gap on API (`matched_skills`, `missing_skills`) | Powers drawer without parsing `why_ranked` strings | Frontend-only gap inference |
| Contact extract before resume clean | PDF clean step breaks `@` in emails | Extract after clean only |
| Client-side match filters v1 | No new API; filter/sort existing `response.results` | Server-side filter params |
| LLM upload returns 200 on unavailable | Don't block onboarding when Ollama/OpenAI down | 503 hard fail |
| API port **8001** | Port 8000 conflict on user's machine | Keep 8000 |
| UI: warm neutral + sage accent | User rejected blue "AI startup" aesthetic | LinkedIn blue theme |

## Open questions

- [ ] **Security:** OpenAI key may have been pasted in chat — rotate before any prod use
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

- **Branch:** main
- **Latest commit:** `c31b233` — match explainability, contact fields, jobs UX polish
- **Build status:** passing (`npm run build` in `frontend/`)
- **Test status:** **69 passed** (`pytest ../tests -v` from `backend/`)

## Commands

```bash
cd /Users/harshkashyap/Projects/JobMatcher-v1/Job-Matching-Agentic

# Backend
cd backend && source .venv/bin/activate
uvicorn main:create_app --factory --reload --port 8001

# Frontend
cd frontend && npm run dev
# http://localhost:5173/login

# Tests
cd backend && pytest ../tests -v

# Demo
# See docs/demo/DEMO-SCRIPT.md and docs/demo/DEMO-CHECKLIST.md
```

## Key files

| File | Why It Matters |
|------|---------------|
| `docs/demo/DEMO-SCRIPT.md` | 15-min supervisor walkthrough |
| `docs/demo/DEMO-CHECKLIST.md` | Pre-demo verification |
| `frontend/src/components/MatchDetailsDrawer.jsx` | Matched/missing skills + score explanation |
| `frontend/src/components/CandidateJobResults.jsx` | Product jobs UI |
| `frontend/src/components/ProfileForm.jsx` | Contact & links + skills |
| `backend/core/contact_extract.py` | Regex contact extraction from resume |
| `backend/contracts/matching.py` | `MatchResult.matched_skills`, `missing_skills` |
| `docs/design/V1-V2-SCOPE.md` | v1 / v1.1 shipped vs v2 deferred |

## Next steps

1. **Run live demo** using `docs/demo/DEMO-SCRIPT.md` — candidate → employer → admin
2. **Push to remote** if not already synced (`git push origin main`)
3. **Rotate OpenAI key** if it was ever exposed in chat
4. **Supervisor feedback** → paper §3 diagram update or v1.1 fast-follow (agent events API)
5. **Product follow-ups (post-demo):** saved jobs, apply stub, re-upload resume from Profile, employer sees candidate contact

## External links

- Repo: https://github.com/Harsh23Kashyap/Job-Matching-Agentic
