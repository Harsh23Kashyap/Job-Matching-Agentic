# Handoff
> Written: 2026-05-27 | Branch: main | Dir: /Users/harshkashyap/Projects/JobMatcher-v1/Job-Matching-Agentic

## Goal

Ship a **three-agent job matching product** (Candidate, Employer, Matchmaking) with role portals, explainable ML matching, benchmark parity, and **thesis-demo completeness**: learned fusion pipeline in the candidate UX, backend saved jobs/applications, employer applicant feed, fairness baseline, and grounded LLM explanations.

## Current state

- **Done (committed — `153a9d0`):**
  - V1 + V1.1: three agents, auth, portals, LLM resume/JD upload, contact fields
  - V2 ML: lexical, cross-encoder, Qdrant switch, benchmarks, fusion/constraints/calibration/router/feedback, admin ML toggles
  - UI polish across candidate/employer/admin portals
  - 105 tests at commit time; API **2.0.0**

- **Done (local — uncommitted on `main`):**
  - **Backend saved jobs & applications** (`stores/candidate_activity_store.py`)
    - `GET/PUT /candidates/me/saved-jobs` — save → feedback `save`, unsave → feedback `dismiss`
    - `GET/POST /candidates/me/applications` — apply entity + feedback `apply`
    - `GET /jobs/mine/applications` — employer applicant feed
  - **Fairness baseline** (`core/fairness.py`, `benchmarks/fairness_eval.py`, `GET /system/fairness`)
    - Experience + remote-preference proxy groups, disparate impact ratios on 30-CV corpus
  - **Grounded LLM explainer** — Ollama/OpenAI call with structured facts; template fallback (`hooks/grounded_explainer.py`)
  - **Candidate ML defaults** — `DEFAULT_CANDIDATE_MATCH` in `client.js`: learned fusion, constraints, auto-strategy, calibration, feedback boost, `explain_mode=llm`
  - **Employer ML defaults** — `DEFAULT_EMPLOYER_MATCH` (learned fusion + constraints + calibration)
  - **Frontend pages:** `/candidate/saved`, `/employer/applications`; admin fairness summary strip
  - **Docs:** `PAPER-FEATURES-INVENTORY.md`, `DEMO-CHECKLIST.md` updated (116 tests, API 2.0.0)
  - **116 tests passing**; frontend build passing

- **In progress:** None
- **Blocked:** None for local demo; latest activity/fairness work **not committed or pushed**

## Decisions made

| Decision | Why | Alternatives rejected |
|----------|-----|----------------------|
| Activity store in same SQLite DB as auth | One file, no new infra; ownership via existing candidate/job links | Separate DB or Postgres (deferred) |
| Save/unsave via PUT with `saved` boolean | Single endpoint; unsave auto-records dismiss feedback | Separate DELETE + manual dismiss call from UI |
| Fairness uses experience + remote proxies | Actionable on synthetic corpus without demographic inference | Name-based gender proxy (ethically risky for paper) |
| LLM explainer: facts JSON in, bullets JSON out | Grounded; falls back to templates if LLM down | Raw LLM prose from profiles (hallucination risk) |
| Candidate default = full ML pipeline | Thesis demo shows best system, not bare semantic | Keep semantic default (under-sells V2 work) |
| Applications idempotent per candidate+job pair | Prevents duplicate apply rows; UI shows "Applied" | Allow multiple apply records |

## Open questions

- [ ] Hypothesis: Commit + push activity/fairness batch before supervisor demo — avoids stale remote vs local
- [ ] Unknown: Whether LLM explainer should be default when Ollama is offline (currently falls back silently to templates)
- [ ] Hunch: Full `paper_progression` with cross-encoder still needs refreshed `data/expected/` floats
- [ ] Paper §3 architecture diagram — waiting on supervisor approval

## Blockers & dependencies

| What | Who/Where | Status |
|------|-----------|--------|
| Commit + push latest work | User | waiting (not requested) |
| Ollama for LLM explain + resume parse | Local dev | optional — template/manual fallback works |

## Environment

- **Branch:** main (tracking `origin/main`)
- **Uncommitted changes:** 18 modified + 7 untracked files (~433 insertions). Activity store, fairness, Saved/Applications pages, tests.
- **Recent commits:**
  - `153a9d0` Add V2 ML pipeline, benchmarks, portal polish, and feedback loop
  - `53a4906` Add demo script and checklist for supervisor walkthrough
  - `c31b233` Add match explainability, profile contact fields, and jobs UX polish
- **Build status:** passing (`npm run build`)
- **Test status:** **116 passed** (`pytest ../tests -v` from `backend/`)
- **Active processes:** None known

## What worked

- `CandidateActivityStore` on shared SQLite — saved jobs, applications, employer feed in one store
- Wiring save/unsave to feedback dismiss in the PUT handler — single UI action, no extra dismiss call
- `DEFAULT_CANDIDATE_MATCH` constant — one place for thesis-demo ML config
- `GET /system/fairness` reuses loaded fusion/calibration models from matchmaker
- Integration tests with register → login → apply → employer view flow

## What didn't work

- None this session. Prior: concurrent `git commit` processes can hang — kill stuck shells and retry with `git -c core.fsmonitor=false commit`.

## Commands

```bash
# Backend
cd backend && source .venv/bin/activate
uvicorn main:create_app --factory --reload --port 8001

# Frontend
cd frontend && npm run dev

# Tests
cd backend && pytest ../tests -v

# Train ML models
cd backend && python -m benchmarks.train_ml_models

# Fairness report (CLI equivalent of GET /system/fairness)
cd backend && python -c "from benchmarks.fairness_eval import run_fairness_eval; from config import Settings; import json; print(json.dumps(run_fairness_eval(Settings()), indent=2))"

# Benchmarks
python -m benchmarks.table11_fusion
python -m benchmarks.paper_progression --skip-cross-encoder

# Optional env
VECTOR_STORE=qdrant READ_ONLY=true
```

## Key files

| File | Why It Matters |
|------|---------------|
| `backend/stores/candidate_activity_store.py` | Saved jobs + applications SQLite schema |
| `backend/gateway/routes/candidates.py` | `/me/saved-jobs`, `/me/applications` |
| `backend/gateway/routes/employers.py` | `/mine/applications` |
| `backend/core/fairness.py` | Proxy-group fairness metrics |
| `backend/benchmarks/fairness_eval.py` | Corpus-wide fairness driver |
| `backend/hooks/grounded_explainer.py` | LLM-grounded `why_ranked` with fallback |
| `frontend/src/api/client.js` | `DEFAULT_CANDIDATE_MATCH`, activity API helpers |
| `frontend/src/pages/candidate/Saved.jsx` | Saved + applied list |
| `frontend/src/pages/employer/Applications.jsx` | Employer applicant feed |
| `frontend/src/components/CandidateJobResults.jsx` | Backend save/apply/dismiss wiring |
| `tests/integration/test_activity_api.py` | End-to-end activity flow tests |
| `docs/research/PAPER-FEATURES-INVENTORY.md` | Updated feature claims for paper |
| `docs/demo/DEMO-CHECKLIST.md` | Pre-flight (116 tests, API 2.0.0) |

## External links

None.

## Memory snapshot

None directly relevant.

## Persistent context

- Knowledge graph: `.claude/knowledge_graph.md`
- Design specs: `docs/design/HLD-multi-agent-system.md`, `docs/design/SDD-multi-agent-system.md`, `docs/design/V1-V2-SCOPE.md`
- Demo: `docs/demo/DEMO-SCRIPT.md`, `docs/demo/DEMO-CHECKLIST.md`
- Paper inventory: `docs/research/PAPER-FEATURES-INVENTORY.md`

## Still deferred

- OAuth / Postgres / production auth
- Real external job sync, Redis/NATS bus, microservices
- Online retraining from feedback, full ESCO ontology, LLM strategy selection
- Bootstrap significance CI as merge gate, legacy Table 9 exact float parity
- CI/CD pipeline (explicitly out of scope)
- Application status workflow (reviewing/rejected), employer actions on applicants
- Email notifications, admin corpus editor

## Next steps

1. **Commit + push activity/fairness batch** — verify: `git status` clean; remote has Saved/Applications routes
2. **Live demo flow** — candidate Find jobs → Save → Apply → Saved tab; employer Applicants tab; admin fairness strip — verify: `docs/demo/DEMO-CHECKLIST.md`
3. **Optional: run full `paper_progression`** and refresh `data/expected/` — verify: regression test passes
4. **§3 architecture diagram** for paper — verify: supervisor approval then add to `docs/design/`
5. **Employer applicant actions** (shortlist/reject status) if product demo needs pipeline UX — verify: status column on `/employer/applications`
