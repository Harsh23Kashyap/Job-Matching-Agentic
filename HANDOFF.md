# Handoff
> Written: 2026-05-27 | Branch: main | Dir: /Users/harshkashyap/Projects/JobMatcher-v1/Job-Matching-Agentic

## Goal

Deliver a **thesis-ready JobMatch system**: three-agent product (candidate / employer / admin portals) with composite matching and polished UX, **plus** a complete **offline research evaluation pipeline** and report-backed manuscript (`docs/research/RESEARCH-PAPER.md`). Current session focus was **portal UI polish** (theme, auth, candidate onboarding/profile, employer jobs) on top of the committed research stack.

## Current state

- **Done:**
  - V1/V1.1 product: three agents, auth, portals, LLM resume/JD parse, composite scoring, drawer breakdown, demo seed, feedback
  - **Offline research stack** (`backend/benchmarks/`, `backend/scripts/run_research_pipeline.py`) — smoke run `backend/reports/research_run_smoke_test/`; committed at `1bef648`
  - **Theme system:** `frontend/src/theme/tokens.css`, `polish.css`, `auth.css`; semantic CSS variables; dark mode; `PortalShell` syncs `data-portal` on `<html>`
  - **Auth polish:** split layout, `AuthIllustrations.jsx`, `AuthLayout.jsx`, Login/Register copy
  - **Candidate onboarding:** CID cleanup (`profileNormalize.js`, `resumeClean.cleanFieldText`), contact normalization, skills chips, compensation currency labels, validation + scroll-to-error, reliable PUT upsert when profile exists; backend `_sanitize_profile_payload` strips CID on contact fields
  - **Candidate profile:** view vs edit modes; `CandidateProfileSummary`; strong empty state; `fetchMyProfileOrNull` + `isCandidateProfileReady`
  - **Employer jobs:** two-column sticky layout; `JdImportPanel`, `RemotePolicyField`, `FormFeedback`; Open/Closed/All filters; `ActivePostingsEmpty`; skills required on submit; `employer-jobs` background variant
  - **Visual QA checklist:** `frontend/THEME-QA.md`
- **In progress:** **Uncommitted UI polish** (~24 modified files, ~10 new frontend files) — not committed or pushed
- **Blocked:** None for local demo

## Decisions made

| Decision | Why | Alternatives rejected |
|----------|-----|----------------------|
| Semantic tokens in `tokens.css` + legacy aliases | Shadcn-style theming without Tailwind; gradual migration | Hardcoded colors only in `App.css` |
| `auth.css` imported after `App.css` in `App.jsx` | Vite fails on trailing `@import` in CSS bundles | `@import` at end of `App.css` |
| Profile page: summary view + edit toggle | Enterprise readability; form only when editing | Always-on full form |
| Onboarding: always `PUT /candidates/me` upsert | Save works when profile already exists | POST-only create |
| Employer jobs: separate `jdError` vs `formError` | JD extraction failures don’t block form save feedback | Single error string |
| `portalBackground.js` → `employer-jobs` on `/employer/jobs` | SVG ornaments match empty-state illustrations | `base` (dot grid only) |
| Require ≥1 skill on job post (`validateJobFields`) | Better matching; enterprise form completeness | Optional skills |
| Single pipeline `run_research_pipeline.py` | Reproducible paper artifacts | Scattered scripts only |
| Cross-encoder optional in pipeline | Hurts nDCG on demo corpus (+141 ms/query) | Always-on CE |
| Paper numbers only from `backend/reports/` | No hallucinated results | Inline estimates |

## Open questions

- [ ] Hypothesis: 100×50 corpus will widen bootstrap CIs but confirm composite lead — run pipeline with `--data-dir data/research`
- [ ] Unknown: Cross-encoder permanently disabled or needs domain tuning — nDCG Δ = −0.108 on demo
- [ ] Hunch: `AdminConsole.jsx` wrong `ResultsPanel` props — admin match UI may be empty
- [ ] Unknown: `demo.admin@test.com` 401 in some automated smoke runs
- [ ] Should UI polish ship in one commit or split (theme / candidate / employer)?
- [ ] Paper §3 architecture diagram — supervisor approval pending

## Blockers & dependencies

| What | Who/Where | Status |
|------|-----------|--------|
| Git commit + push of UI polish | User | **not done** — uncommitted frontend + `candidates.py` |
| Ollama for LLM parse/explain | Local dev | optional — template fallback works |
| 100×50 research eval run | Dev | corpus in `data/research/`; pipeline not run at scale |

## Environment

- **Branch:** `main`
- **Uncommitted changes:** 24 modified + untracked: `frontend/src/theme/`, `profileNormalize.js`, `CandidateProfileSummary.jsx`, `FormFeedback.jsx`, `JdImportPanel.jsx`, `RemotePolicyField.jsx`, `THEME-QA.md`, `test_profile_normalize.mjs`, `backend/gateway/routes/candidates.py`, plus pages/components listed in `git status`
- **Recent commits:**
  - `1bef648` Add offline research pipeline, evaluation suite, and paper draft
  - `bfa27e1` Add composite scoring, portal polish, and candidate flow fixes for thesis demo
  - `0185fa8` Polish employer portal, demo seed, and shared portal UX for thesis demo
- **Build status:** passing (`npm run build` — verified 2026-05-27)
- **Test status:** `node --test tests/unit/test_profile_normalize.mjs tests/unit/test_profile_fields.mjs` — 8 passed; `tests/benchmarks/` 38 passed (prior session); full `pytest ../tests -q` not re-run this session
- **Active processes:** None assumed; demo: backend `:8001`, frontend `:5173`

## What worked

- `npm run build` after large CSS/JSX changes — no errors
- `profileNormalize.js` + unit tests for CID strip, URL normalize, merge behavior
- `fetchMyProfileOrNull` + PUT upsert for existing candidate profiles
- `CompensationInput` currency labels reused on candidate + employer forms
- `EmptyStatePanel` + `ProfileNeededEmpty` / `EmployerRolesEmpty` pattern for zero states
- `python backend/scripts/run_research_pipeline.py --skip-cross-encoder` — ~12s, all stages OK
- `git commit -m "single line"` — reliable in agent shell (HEREDOC hangs)

## What didn't work

- HEREDOC `git commit` in agent shell — hung; use single `-m` line
- Cross-encoder reranking — nDCG degrades (−0.108); not production default
- Browser automation on demo login — stale refs; use API smoke or manual demo
- `@jobmatch.test` email in register smoke — pydantic rejects reserved TLD
- `@import` at bottom of `App.css` for theme files — Vite build failure; import in `App.jsx` instead

## Commands

```bash
# Frontend
cd frontend && npm run dev
cd frontend && npm run build

# Frontend unit tests (profile)
node --test tests/unit/test_profile_normalize.mjs tests/unit/test_profile_fields.mjs

# Backend
cd backend && source .venv/bin/activate
uvicorn main:create_app --factory --reload --port 8001

# Full test suite (before commit)
cd backend && pytest ../tests -q
node --test tests/unit/test_*.mjs

# Research pipeline
python backend/scripts/run_research_pipeline.py --skip-cross-encoder --run-id research_run_smoke_test
bash scripts/run_research_suite.sh

# Demo logins (password: demo1234)
# demo.candidate@test.com | demo.employer@test.com | demo.admin@test.com
```

## Key files

| File | Why It Matters |
|------|---------------|
| `frontend/src/theme/tokens.css` | Semantic CSS variables + dark mode |
| `frontend/src/theme/polish.css` | Page rhythm, panels, employer jobs, profile summary, JD import |
| `frontend/src/theme/auth.css` | Auth split layout + form cards |
| `frontend/src/App.jsx` | Imports theme CSS (order matters) |
| `frontend/src/utils/profileNormalize.js` | CID cleanup, contact normalize, merge extracted fields |
| `frontend/src/utils/resumeClean.js` | `cleanFieldText`, resume preview |
| `frontend/src/utils/validation.js` | Profile + richer field errors |
| `frontend/src/pages/candidate/Onboarding.jsx` | Upload → review → save flow |
| `frontend/src/pages/candidate/Profile.jsx` | Summary vs edit modes |
| `frontend/src/components/CandidateProfileSummary.jsx` | Profile read-only card |
| `frontend/src/pages/employer/Jobs.jsx` | Two-column jobs + posting form |
| `frontend/src/components/JdImportPanel.jsx` | JD paste/upload block |
| `frontend/src/components/RemotePolicyField.jsx` | Remote toggle cards |
| `frontend/src/components/JobPostingForm.jsx` | Employer role form sections |
| `frontend/src/components/FormFeedback.jsx` | Inline form error/info banners |
| `frontend/src/utils/portalBackground.js` | Route → background SVG variant |
| `backend/gateway/routes/candidates.py` | `_sanitize_profile_payload` CID strip |
| `frontend/THEME-QA.md` | Light/dark visual checklist |
| `backend/scripts/run_research_pipeline.py` | Offline eval single entry |
| `docs/research/RESEARCH-PAPER.md` | Manuscript draft (report-backed) |

## External links

None.

## Memory snapshot

None directly relevant.

## Persistent context

- Knowledge graph: `.claude/knowledge_graph.md`
- Design specs: `docs/design/HLD-multi-agent-system.md`, `docs/design/SDD-multi-agent-system.md`, `docs/design/V1-V2-SCOPE.md`
- Research: `docs/research/RESEARCH-PAPER.md`, `docs/research/evaluation/`
- Demo: `docs/demo/DEMO-SCRIPT.md`, `docs/demo/DEMO-CHECKLIST.md`
- Theme QA: `frontend/THEME-QA.md`

## Next steps

1. **Manual UI pass** — run `frontend/THEME-QA.md` on `/login`, `/candidate/onboarding`, `/candidate/profile`, `/employer/jobs` in light + dark — verify: no low-contrast helper text, green focus rings
2. **Commit UI polish** — stage `frontend/src/theme/`, new components, page changes, `candidates.py`, `test_profile_normalize.mjs` — verify: `git status` clean; message e.g. `Polish portal theme, candidate profile flow, and employer jobs UX`
3. **Full pytest** — `cd backend && pytest ../tests -q` — verify: no regressions
4. **Thesis demo dry-run** — `docs/demo/DEMO-CHECKLIST.md`: onboarding CID resume, profile edit, employer JD extract + post — verify: toasts and empty states behave as expected
5. **Research at scale** (optional) — `python backend/scripts/run_research_pipeline.py --data-dir data/research --eval-path data/research/eval_pairs.json --run-id research_run_100x50` — verify: `dataset_validation.json` shows 100×50
6. **Fix admin console** (if demo needs it) — inspect `AdminConsole.jsx` `ResultsPanel` props — verify: admin match tab shows results
