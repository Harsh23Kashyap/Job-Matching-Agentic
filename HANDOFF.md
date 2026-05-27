# Handoff
> Written: 2026-05-27 | Branch: main | Dir: /Users/harshkashyap/Projects/JobMatcher-v1/Job-Matching-Agentic

## Goal

Ship a **three-agent job matching product** (Candidate, Employer, Matchmaking) with role portals, explainable ML matching, benchmark parity, and **thesis-demo completeness**: polished candidate + employer UX, demo accounts, saved jobs/applications, employer job management, candidate matching for employers, and subtle animated backgrounds — all testable locally without external deps.

## Current state

- **Done (committed on `origin/main`, latest `517b099`):**
  - V1 + V1.1: three agents, auth, portals, LLM resume/JD upload, contact fields
  - V2 ML: lexical, cross-encoder, Qdrant switch, benchmarks, fusion/constraints/calibration/router/feedback, admin ML toggles
  - Activity: saved jobs, applications, employer applicant feed
  - Candidate profile UX: resume cleanup, compensation, skills chips, layout, match results with filters/drawer
  - **144 pytest + 12 node tests** at last commit; frontend build passing

- **Done (uncommitted — this session + prior agent work, not yet pushed):**
  - **`BackgroundPattern`** — reusable SVG backgrounds: `onboarding`, `profile`, `jobs`, `empty`, `employer-jobs`, `employer-candidates`, `employer-empty`; sage/sand/olive only; `prefers-reduced-motion` respected
  - **Candidate empty states** — ProfileNeeded, JobsReady, NoMatchingRoles + illustrations
  - **Navbar polish** — pill tabs, avatar-only user menu, mobile bottom nav, theme toggle
  - **Candidate QA** — profile update events, toasts, match error retry, `/feedback` vite proxy, profile loading shimmer
  - **Demo seed** — `backend/demo_seed.py` auto-seeds on startup (`SEED_DEMO=true` default): `demo.candidate@test.com`, `demo.employer@test.com`, `demo.admin@test.com` / `demo1234`; login page one-click buttons
  - **Employer job posting** — `JobPostingForm`, `BudgetRangeInput`, structured sections, budget range fields on backend
  - **Employer My Jobs** — rich role cards, search/filter/sort, Open/Closed/Draft badges, Edit + Close role, `PUT /jobs/mine/{id}`, `PATCH /jobs/mine/{id}/status`, `status`/`created_at`/`updated_at` on `JobProfile`
  - **Employer Candidates page** — title “Candidate matches”, summary cards (reviewed/strong/top/refreshed), role selector, rich candidate cards, match drawer, Save via `/feedback`, Contact mailto
  - **Match API enrichment** — `candidate_experience_years`, `candidate_preferred_salary`, `candidate_preferred_currency`, `candidate_remote_preference` on job→candidates results
  - **`scripts/smoke_employer_jobs.py`** — API smoke for list/update/close/reopen
  - **149 pytest + 12 node tests passing**; frontend build passing (verified 2026-05-27)

- **In progress:** None — all requested employer/candidate polish items from recent sessions appear complete
- **Blocked:** None for local thesis demo

## Decisions made

| Decision | Why | Alternatives rejected |
|----------|-----|----------------------|
| Activity store in same SQLite DB as auth | One file, no new infra | Separate DB or Postgres (deferred) |
| Profile upsert via `PUT /candidates/me` | Single save path; fixes “already linked” | Split POST create + PUT update only |
| Demo seed on startup (`SEED_DEMO=true`) | One-click thesis demo without manual corpus setup | Manual seed script only |
| Job status `open`/`closed`/`draft` on `JobProfile` | Employer list badges + close role UX | Soft-delete or archive table |
| Employer match Save → `POST /feedback` action `save` | Reuses existing feedback store | New employer-shortlist table |
| Client-side job/candidate filters | No backend filter API yet; instant UX | Server-side filter params (deferred) |
| Employer background variants separate from candidate `jobs` | Distinct visual language (job card → candidates vs role cards) | Reuse candidate `jobs` art on employer pages |
| Technical scores in `<details>` drawer only | Product-facing UX hides raw ML numbers | Show semantic/skills scores on cards |
| `git commit` with dual `-m` flags | HEREDOC in agent shell hung in this environment | Single HEREDOC commit (blocked ~90s+) |

## Open questions

- [ ] Hypothesis: Add `listed_at` / `remote_policy` to `MatchResult` for accurate “Recently added” and remote filter — worth backend pass when demo stabilizes
- [ ] Unknown: Whether LLM explainer should surface “template fallback” in UI when Ollama is offline
- [ ] Hunch: Full `paper_progression` with cross-encoder still needs refreshed `data/expected/` floats
- [ ] Paper §3 architecture diagram — waiting on supervisor approval
- [ ] Hypothesis: Employer “Save” should persist to a dedicated shortlist UI (not just feedback store) — deferred

## Blockers & dependencies

| What | Who/Where | Status |
|------|-----------|--------|
| Ollama for LLM explain + resume parse | Local dev | optional — template/manual fallback works |
| External job posting URLs for Apply | Job `link` field on corpus | sparse — in-app apply via API works |
| Commit + push uncommitted work | User | **not done** — large dirty tree on `main` |

## Environment

- **Branch:** `main` (last pushed commit `517b099`; **many uncommitted changes**)
- **Uncommitted changes:** ~36 modified + ~15 new files (see `git status --short`); includes all employer/candidate polish, demo seed, BackgroundPattern, tests
- **Recent commits:**
  - `517b099` Polish candidate profile UX and jobs results for thesis demo
  - `71c60b3` Add saved jobs, applications, fairness baseline, and ML defaults
  - `153a9d0` Add V2 ML pipeline, benchmarks, portal polish, and feedback loop
- **Build status:** passing (`npm run build`)
- **Test status:** **149 passed** pytest + **12 passed** node; 2 deprecation warnings
- **Active processes:** None known (start backend `:8001` + frontend `:5173` for manual QA)

## What worked

- Demo accounts + corpus linkage — employer sees 5 jobs, candidate linked to `cv_01` (Rahul Sharma)
- Employer jobs API smoke script — list/update/close/reopen in one command
- Browser QA flow — demo employer login → My Jobs filters → View candidates with `?job=` preselect
- `BackgroundPattern` + `PortalBackground.resolveVariant()` — page-level backgrounds without duplicating SVG in each page
- `EmployerJobList` + `EmployerJobCard` — filter/sort without backend changes
- `deriveEmployerWhyMatch()` — employer-facing copy (not “Matches your …”)
- `git -c core.fsmonitor=false commit -m "subject" -m "body"` — reliable when HEREDOC hangs

## What didn't work

- Long-running `git commit` with embedded HEREDOC in agent shell — hung; use `-m` twice or simple message
- Browser automation on narrow viewport — Edit/Close role buttons on My Jobs can sit behind mobile bottom nav; works on wider layouts
- Inline shell JSON for job list API smoke — job descriptions broke `json.loads`; use `scripts/smoke_employer_jobs.py` instead

## Commands

```bash
# Backend
cd backend && source .venv/bin/activate
uvicorn main:create_app --factory --reload --port 8001

# Frontend
cd frontend && npm run dev

# Tests
cd backend && source .venv/bin/activate && pytest ../tests -q
node --test tests/unit/test_skills_input.mjs tests/unit/test_match_format.mjs

# Build
cd frontend && npm run build

# Employer jobs API smoke
python3 scripts/smoke_employer_jobs.py

# Demo logins (password: demo1234)
# demo.candidate@test.com | demo.employer@test.com | demo.admin@test.com

# Train ML models
cd backend && python -m benchmarks.train_ml_models

# Fairness report
cd backend && python -c "from benchmarks.fairness_eval import run_fairness_eval; from config import Settings; import json; print(json.dumps(run_fairness_eval(Settings()), indent=2))"

# Benchmarks
python -m benchmarks.table11_fusion
python -m benchmarks.paper_progression --skip-cross-encoder

# Optional env
SEED_DEMO=true VECTOR_STORE=qdrant READ_ONLY=true
```

## Key files

| File | Why It Matters |
|------|---------------|
| `backend/demo_seed.py` | Auto-seeds demo users + links employer to 5 corpus jobs |
| `backend/gateway/routes/employers.py` | `GET/PUT/PATCH /jobs/mine`, job status + ownership |
| `backend/contracts/profiles.py` | `JobProfile` status, timestamps, budget fields |
| `backend/contracts/matching.py` | `MatchResult` + candidate profile fields for employer view |
| `backend/agents/matchmaking_agent.py` | Job→candidates ranking + contact + profile enrichment |
| `frontend/src/components/BackgroundPattern.jsx` | All page/panel/inline SVG background variants |
| `frontend/src/components/PortalBackground.jsx` | Route → variant mapping (candidate + employer) |
| `frontend/src/components/EmployerJobList.jsx` | My Jobs search/filter/sort + empty state |
| `frontend/src/components/EmployerJobCard.jsx` | Role card with badges and actions |
| `frontend/src/components/EmployerCandidateResults.jsx` | Candidate matches list, summary, drawer, filters |
| `frontend/src/components/JobPostingForm.jsx` | Structured employer posting form |
| `frontend/src/pages/employer/Jobs.jsx` | Two-column jobs list + post/edit form |
| `frontend/src/pages/employer/Matches.jsx` | Candidate matches page shell + refresh |
| `frontend/src/utils/jobFields.js` | Job form validation, payload, `jobFromApi` for edit |
| `frontend/src/utils/format.js` | Match formatting, employer why-match, compensation display |
| `frontend/src/constants/demoAccounts.js` | Login page demo button config |
| `scripts/smoke_employer_jobs.py` | Quick employer jobs API verification |
| `tests/integration/test_demo_seed.py` | Demo seed integration tests |
| `docs/demo/DEMO-CHECKLIST.md` | Pre-flight demo steps |

## External links

None.

## Memory snapshot

None directly relevant.

## Persistent context

- Knowledge graph: `.claude/knowledge_graph.md`
- Design specs: `docs/design/HLD-multi-agent-system.md`, `docs/design/SDD-multi-agent-system.md`, `docs/design/V1-V2-SCOPE.md`
- Demo: `docs/demo/DEMO-SCRIPT.md`, `docs/demo/DEMO-CHECKLIST.md`
- Paper inventory: `docs/research/PAPER-FEATURES-INVENTORY.md`

## Next steps

1. **Commit uncommitted work** — group logically (demo seed + auth, employer jobs API/UI, employer candidates polish, BackgroundPattern, candidate QA/navbar) — verify: `git status` clean after commit(s)
2. **Live demo dry-run** — demo.candidate → Jobs → Find matches; demo.employer → My Jobs → Candidates → Refresh matches — verify: `docs/demo/DEMO-CHECKLIST.md` + `scripts/smoke_employer_jobs.py`
3. **Mobile QA on employer My Jobs** — Edit/Close not blocked by bottom nav — verify: scroll or add bottom padding on action rows if needed
4. **Update DEMO-CHECKLIST / README** — 149 tests, demo accounts, employer flows — verify: doc counts match `pytest ../tests -q`
5. **Optional: push to remote** after commit — verify: `git log origin/main..HEAD`
