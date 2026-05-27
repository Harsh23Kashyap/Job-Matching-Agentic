# Handoff
> Written: 2026-05-27 | Branch: main | Dir: /Users/harshkashyap/Projects/JobMatcher-v1/Job-Matching-Agentic

## Goal

Ship a **thesis-ready JobMatch product** (candidate / employer / admin portals, composite matching, demo seed) with **polished UX and reliable core flows**, plus an **offline research evaluation pipeline** and report-backed manuscript. This session completed **copy humanization**, **functional bug fixes** (profile/matches/jobs), **QA hardening** (stale profile, job ownership), and **knowledge graph v8** — all still **uncommitted** on top of `c1a451d`.

## Current state

- **Done:**
  - V1/V1.1 product: three agents, auth, portals, LLM resume/JD parse, composite scoring, drawer breakdown, demo seed, feedback
  - Offline research stack (`backend/benchmarks/`, `run_research_pipeline.py`) · committed `1bef648`
  - Portal theme: `tokens.css`, `polish.css`, `auth.css`, dark mode, `data-portal` on `<html>`
  - **Copy humanization** across auth, candidate, employer UI (empty states, errors, buttons, helpers)
  - **Clean-slop** pass on docs/benchmarks (emoji status → yes/no, section banners, module docstrings)
  - **Functional fixes:** profile-already-exists → edit not block; matches after save (`searchAfterSave` auto-search); employer job persist (`link_job_if_unowned` + optimistic list merge); refresh loading states; empty states vs real backend (filter-empty, all-closed roles)
  - **QA fixes:** `PROFILE_STALE_MARKER` + restore UI; `POST /jobs` 403 `JOB_NOT_OWNED`; employer `load()` no longer wipes list on failure; employer matches `jobsLoading` skeleton
  - **Tests added:** `test_employer_repost_same_job_id_still_lists_mine`, `test_employer_cannot_post_job_id_owned_by_another`, stale profile flow, `test_profile_fields.mjs` stale marker
  - **Knowledge graph v8** refreshed (`.claude/knowledge_graph.md`)
  - **Build + targeted tests passing** (see Environment)
- **In progress:** **137 modified files, ~1.9k insertions** — not committed or pushed
- **Blocked:** None for local demo

## Decisions made

| Decision | Why | Alternatives rejected |
|----------|-----|----------------------|
| `hasCandidateProfile` / `isCandidateProfileReady` / `isProfileStale` split | Distinguish no link, incomplete, stale, ready for gates | Single boolean `hasProfile` |
| `fetchMyProfileOrNull` returns `PROFILE_STALE_MARKER` on `PROFILE_NOT_FOUND` | Auth link kept after restart; PUT recreates profile | Treat all 404 as null (misleading empty state) |
| `link_job_if_unowned` on `POST /jobs` | Repost same job id without ownership insert failure | Always `link_job` (IntegrityError on duplicate) |
| `get_job_owner` + 403 before `register()` | Prevent cross-tenant job corpus overwrite | Silent skip link only |
| Matches header CTA hidden until results exist | Avoid duplicate Find jobs + nav overlap clicks | Two CTAs always visible |
| `EmployerAllClosedEmpty` vs `EmployerNoJobsEmpty` | Reflect jobs exist but all closed | Single empty when `openJobs.length === 0` |
| Employer `load()` toast on error, keep prior `jobs` | Failed refetch must not wipe list after successful post | `catch(() => setJobs([]))` |
| Semantic tokens without Tailwind | Shadcn-style theming in plain CSS | Hardcoded colors only |
| Always `PUT /candidates/me` upsert | Save works when profile already exists | POST-only create |
| Single research pipeline CLI | Reproducible paper artifacts | Scattered scripts only |

## Open questions

- [ ] Hypothesis: 100×50 corpus widens bootstrap CIs but confirms composite lead — run `--data-dir data/research`
- [ ] Unknown: Cross-encoder permanently disabled or needs tuning — nDCG Δ −0.108 on demo
- [ ] Hunch: `AdminConsole.jsx` wrong `ResultsPanel` props — admin match UI may be empty
- [ ] Unknown: `demo.admin@test.com` 401 in some automated smoke runs
- [ ] Should uncommitted work split into commits (product fixes / copy / research docs) or one thesis commit?
- [ ] Paper §3 architecture diagram — supervisor approval pending
- [ ] Playwright E2E for register → profile → match — optional hardening

## Blockers & dependencies

| What | Who/Where | Status |
|------|-----------|--------|
| Git commit + push of session work | User | **not done** · 137 files modified |
| Ollama for LLM parse/explain | Local dev | optional · template fallback works |
| 100×50 research eval run | Dev | corpus in `data/research/`; pipeline not run at scale |

## Environment

- **Branch:** `main` @ `c1a451d` (last pushed commit)
- **Uncommitted changes:** 137 files · +1872 / −1124 lines · spans frontend portals, `backend/auth/store.py`, `gateway/routes/candidates.py`, `gateway/routes/employers.py`, benchmarks/docs, tests, `.claude/knowledge_graph.md`, `HANDOFF.md`
- **Recent commits:**
  - `c1a451d` Polish portal theme, candidate profile flow, and employer jobs UX
  - `1bef648` Add offline research pipeline, evaluation suite, and paper draft
  - `bfa27e1` Add composite scoring, portal polish, and candidate flow fixes for thesis demo
- **Build status:** passing (`npm run build` · 2026-05-27)
- **Test status:** `pytest ../tests/integration/test_candidate_profile_flow.py ../tests/integration/test_resume_upload.py -q` · 15 passed; `node --test tests/unit/test_profile_fields.mjs` · 5 passed; full `pytest ../tests -q` not re-run this session
- **Active processes:** backend `:8001` and frontend `:5173` running (verified HTTP 200)

## What worked

- Demo candidate flow in browser: login → Jobs → Find jobs → 10 matches; profile summary; dark mode toggle
- API smoke: register → PUT profile → match returns results
- `PROFILE_STALE_MARKER` + Profile/Matches restore UI aligned with backend `PROFILE_NOT_FOUND`
- Integration test for cross-employer job id rejection (403)
- `npm run build` after large JSX/CSS changes
- `/knowledge update` v8 — stale profile + ownership entries documented
- `git commit -m "single line"` in agent shell (HEREDOC hangs)

## What didn't work

- HEREDOC `git commit` in agent shell · hung; use single `-m` line
- Browser automation after heavy HMR · empty `#root` until hard refresh (`Cmd+Shift+R`)
- Hero "Find jobs" button click intercepted by fixed nav when duplicate CTA at scroll 0 — mitigated by hiding header CTA until results exist
- Cross-encoder reranking · nDCG degrades; not production default
- `@jobmatch.test` email in register smoke · pydantic rejects reserved TLD
- Importing `PROFILE_STALE_MARKER` from `client.js` in node unit tests · breaks on `import.meta.env`; use inline marker in tests

## Commands

```bash
# Frontend
cd frontend && npm run dev
cd frontend && npm run build

# Frontend unit tests
node --test tests/unit/test_profile_fields.mjs
node --test tests/unit/test_profile_normalize.mjs

# Backend
cd backend && source .venv/bin/activate
uvicorn main:create_app --factory --reload --port 8001

# Integration tests (profile + employer jobs)
cd backend && pytest ../tests/integration/test_candidate_profile_flow.py ../tests/integration/test_resume_upload.py -q

# Full suite (before commit)
cd backend && pytest ../tests -q
node --test tests/unit/test_*.mjs

# Research pipeline
python backend/scripts/run_research_pipeline.py --skip-cross-encoder --run-id research_run_smoke_test

# Demo logins (password: demo1234)
# demo.candidate@test.com | demo.employer@test.com | demo.admin@test.com
```

## Key files

| File | Why It Matters |
|------|---------------|
| `frontend/src/api/client.js` | `fetchMyProfileOrNull`, `PROFILE_STALE_MARKER`, `DEFAULT_CANDIDATE_MATCH` |
| `frontend/src/utils/profileFields.js` | `hasCandidateProfile`, `isProfileStale`, `isCandidateProfileReady`, payloads |
| `frontend/src/pages/candidate/Matches.jsx` | Profile gates, auto-search, match refresh |
| `frontend/src/pages/candidate/Profile.jsx` | View/edit/stale/incomplete profile flows |
| `frontend/src/pages/candidate/Onboarding.jsx` | Upload → save → navigate with `searchAfterSave` |
| `frontend/src/components/EmptyState.jsx` | `ProfileStaleEmpty`, `EmployerAllClosedEmpty`, `filteredOut` no-results |
| `frontend/src/pages/employer/Jobs.jsx` | Post/edit jobs, optimistic merge, safe reload |
| `frontend/src/pages/employer/Matches.jsx` | `jobsLoading`, open vs closed empty states |
| `backend/auth/store.py` | `get_job_owner`, `link_job_if_unowned` |
| `backend/gateway/routes/candidates.py` | GET `/me` `PROFILE_NOT_FOUND`, PUT upsert |
| `backend/gateway/routes/employers.py` | `register_job` ownership guard |
| `tests/integration/test_resume_upload.py` | Employer jobs mine, repost, cross-owner tests |
| `tests/integration/test_candidate_profile_flow.py` | Upsert, stale profile, match after save |
| `frontend/src/theme/tokens.css` | Semantic CSS variables + dark mode |
| `.claude/knowledge_graph.md` | v8 codebase map · start here for architecture |
| `docs/demo/DEMO-CHECKLIST.md` | Manual demo script |
| `docs/research/RESEARCH-PAPER.md` | Manuscript draft (report-backed) |

## External links

None.

## Memory snapshot

None directly relevant.

## Persistent context

- Knowledge graph: `.claude/knowledge_graph.md` (v8 · portal QA, stale profile, job ownership)
- Design specs: `docs/design/HLD-multi-agent-system.md`, `SDD-multi-agent-system.md`, `V1-V2-SCOPE.md`
- Research: `docs/research/RESEARCH-PAPER.md`, `docs/research/evaluation/`
- Demo: `docs/demo/DEMO-SCRIPT.md`, `docs/demo/DEMO-CHECKLIST.md`
- Theme QA: `frontend/THEME-QA.md`

## Next steps

1. **Hard refresh dev app** after HMR — open http://localhost:5173/login · verify: React renders (not empty `#root`)
2. **Manual demo dry-run** — `docs/demo/DEMO-CHECKLIST.md`: candidate onboarding save → auto-match; employer post role; stale profile restore (optional: delete in-memory profile, GET 404, re-save) · verify: correct empty states and toasts
3. **Full pytest** — `cd backend && pytest ../tests -q` · verify: all green before commit
4. **Commit session work** — stage product fixes + tests first, optionally split docs/research · verify: `git status` clean; suggest message: `Fix portal profile/match flows, stale recovery, and employer job ownership`
5. **Employer browser pass** — demo employer → Candidates → Find candidates · verify: loading skeleton, match results, refresh spinner
6. **Research at scale** (optional) — `python backend/scripts/run_research_pipeline.py --data-dir data/research --run-id research_run_100x50` · verify: 100×50 in `dataset_validation.json`
7. **Fix admin console** (if demo needs it) — `AdminConsole.jsx` `ResultsPanel` props · verify: admin match tab shows results
