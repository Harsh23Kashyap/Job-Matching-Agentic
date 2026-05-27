# Handoff
> Written: 2026-05-28 | Branch: main @ `a4005e0` (pushed) | Dir: /Users/harshkashyap/Projects/JobMatcher-v1/Job-Matching-Agentic

## Goal

Deliver a thesis-ready **multi-agent JobMatch platform** with polished candidate/employer/admin portals and a **JAAMAS submission manuscript**. Platform work spans live jobs API (committed), portal UX polish (local), admin console rebuild (local), and manuscript cleanup (citations, author metadata, `\todo`s).

## Current state

- **Done (committed & pushed @ `a4005e0`):**
  - Live jobs API (`real_jobs_sync`, `RealJobsService`, `/real-jobs/*`, snapshot boot, daily-batch pre-sync)
  - Test reorganization (`tests/unit/backend/`, `tests/unit/frontend/`, `scripts/run_tests.sh`)
  - Manuscript sync with latest platform narrative
- **Done (local, not committed — ~72 files):**
  - **Portal UI polish (v14)** — `frontend/src/theme/page-shell.css`; unified **1120px** shell; deduped hero stats/refresh on employer + candidate match pages; compact summary cards; scroll-safe bottom padding (96px)
  - **Applicants page** — flat feed (`Applications.jsx`): search, role filter, sort, interactive rows (name | role | match | date | status + View)
  - **Match drawer** — 400px width, `100dvh`, 96px bottom padding; overlay `rgba(20,20,20,0.42)`
  - **My jobs post-role panel** — `post-role-panel` scroll-safe; sticky footer via `form-footer-inner`
  - **Employer job cards** — compact 5-col meta grid; title + status + remote on one line
  - **Candidate onboarding/profile** — accordion sections, sticky footer, helper panel, quality score, resume upload zone
  - **Admin console rebuild** — `AdminConsole`, `AgentStatusPanel`, `AdminMatchResults`, fairness/flow panels, admin CSS
  - **Dark mode polish** — match cards, stat cards, drawer scrim, error page, profile helper hierarchy
  - **Error page UX** — centered card, token-based illustration colors, dark-mode contrast
  - **Qdrant store fix** — local changes in `qdrant_store.py` + test update
  - **Knowledge graph v14** — refreshed UI entries + JSON export (local)
- **In progress:** None active
- **Blocked:** Springer upload (author placeholders); professor resubmission (~29 `\todo`s, 12 citation gaps in §2); `REAL_JOBS_BASE_URL` not in repo

## Decisions made

| Decision | Why | Alternatives rejected |
|----------|-----|----------------------|
| Single stats/refresh inside results card | User reported duplicate hero + inner stats and double refresh buttons | Keep hero stats for at-a-glance |
| Flat applicant list (not grouped by role) | Saves vertical space; role shown as column | Group headers per job title |
| `page-shell.css` as shared layout layer | One max-width/padding source for all portal pages | Per-page inline styles |
| Hero on employer matches = role dropdown only | Refresh belongs in card toolbar with filters | Hero toolbar with refresh + dropdown |
| Match drawer 400px (not 440px) | User feedback: too wide on desktop | Full-width mobile sheet |
| `Link` rows for applicants | Clickable affordance + keyboard nav | `<div>` + separate View button only |
| `post-role-panel` internal scroll | Sticky footer was clipping lower form fields | Fixed bottom sheet (deferred) |
| Admin console component split | Readable panels vs monolithic AdminConsole | Single 800-line file |
| Knowledge graph v14 separate from product commit | User has not requested git commit for UI polish | Single mega-commit |

## Open questions

- [ ] Unknown: Production `REAL_JOBS_BASE_URL` — not in repo
- [ ] Unknown: Whether live jobs provider requires auth headers
- [ ] Hypothesis: Professor accepts 12 citation TODOs as draft — prior QA marked **FAIL** on citations
- [ ] Unknown: Add admin UI button for `POST /real-jobs/sync` — API ready, no frontend yet
- [ ] Hunch: Mobile post-role panel may still need bottom-sheet pattern on very small viewports — desktop scroll fix done, not fully QA'd on phone
- [ ] Unknown: Split UI polish into one commit vs candidate/employer/admin commits — user preference

## Blockers & dependencies

| What | Who/Where | Status |
|------|-----------|--------|
| Author placeholders in `main.tex` | User | open |
| ~29 `\todo`s (12 citations in §2) | User/literature | open |
| `REAL_JOBS_BASE_URL` for live sync | Deployment env | not in repo |
| Professor resubmission | User | waiting on todo cleanup |
| Springer upload | User | not started |

None blocking localhost demo.

## Environment

- **Branch:** `main` @ `a4005e0` (synced with `origin/main`)
- **Uncommitted changes:** ~72 files — portal UI polish, admin console, onboarding/profile, dark mode, Qdrant fix, knowledge graph v14
- **Untracked (new files):** `page-shell.css`, `candidate-onboarding.css`, `dark-admin.css`, admin components (`AdminFairnessPanel`, `AdminMatchResults`, etc.), profile components (`ProfileFormFooter`, `ProfileHelperPanel`, `ResumeUploadZone`, etc.), admin utils/hooks
- **Recent commits:**
  - `a4005e0` Add live jobs API, reorganize tests, sync manuscript
  - `9db6abc` Rewrite JAAMAS manuscript §2–§7 + artifacts
  - `010dadf` Knowledge graph for JAAMAS/explainability
- **Build status:** Frontend `npm run build` **passes** (2026-05-28)
- **Test status:** **310 passed** at last full run (`bash scripts/run_tests.sh`); not re-run after latest UI-only changes
- **Active processes:** None

## What worked

- `page-shell.css` as single source for 1120px container, scroll padding, form footer alignment
- Removing hero `stats` + `inlineAction` refresh on match pages — immediate dedupe win
- Flat applicant rows with `Link` + hover states — fills empty dark-mode page
- Drawer `padding-bottom: 96px` on `.match-drawer` — fixes bottom cutoff
- `post-role-panel` max-height + overflow on employer Jobs form panel
- Admin console split into focused panels + `useAgentStatus` hook
- Knowledge graph refresh via `/knowledge update` — v14 documents UI layer
- Frontend build stays green through CSS-heavy changes

## What didn't work

- HEREDOC / `--trailer` git commits hang in Cursor shell — use plain `git commit -m "..."`
- Do not commit LaTeX `.aux/.log/.bbl/.blg/.out`
- Negative-margin sticky footers clipped form content — replaced with `form-footer-inner` + panel scroll
- Grouping applicants by role wasted vertical space — flat list preferred
- Cross-encoder rerank: worse nDCG on demo corpus — do not oversell in paper

## Commands

```bash
# Full test suite
bash scripts/run_tests.sh

# Backend only
cd backend && source .venv/bin/activate && pytest ../tests -q

# Frontend build
cd frontend && npm run build

# Dev servers
cd backend && uvicorn main:create_app --factory --reload --port 8001
cd frontend && npm run dev

# Live jobs sync (requires REAL_JOBS_* in backend/.env)
curl -s http://localhost:8001/real-jobs/status | jq
curl -s -X POST http://localhost:8001/real-jobs/sync -H 'Content-Type: application/json' -d '{"reindex":true}' | jq

# Manuscript compile
bash docs/submission/jaamas/build_all.sh
rg '\\todo' docs/submission/jaamas/manuscript

# Knowledge graph staleness check
python3 -c "
import re; from pathlib import Path; from datetime import datetime
t=Path('.claude/knowledge_graph.md').read_text()
for m in re.finditer(r'^### ([^\n]+)\n\*\*Language:\*\* [^|]+\| \*\*Importance:\*\* [^|]+\| \*\*Indexed:\*\* (\d{4}-\d{2}-\d{2})', t, re.M):
 p,idx=Path(m.group(1)),m.group(2)
 if p.exists() and datetime.fromtimestamp(p.stat().st_mtime).date()>datetime.strptime(idx,'%Y-%m-%d').date(): print(p)
"
```

## Key files

| File | Why It Matters |
|------|---------------|
| `frontend/src/theme/page-shell.css` | Shared 1120px shell, scroll padding, form footer, post-role panel |
| `frontend/src/layouts/PortalShell.jsx` | Unified shell routes; `UNIFIED_SHELL_PREFIXES` |
| `frontend/src/pages/employer/Matches.jsx` | Hero = role dropdown only; stats/refresh in card |
| `frontend/src/pages/candidate/Matches.jsx` | Hero deduped; refresh only in `CandidateJobResults` toolbar |
| `frontend/src/components/EmployerCandidateResults.jsx` | Inner MatchSummaryCards + MatchResultsFilters |
| `frontend/src/components/CandidateJobResults.jsx` | Same pattern for candidate jobs |
| `frontend/src/pages/employer/Applications.jsx` | Flat applicant feed with search/filter |
| `frontend/src/pages/employer/Jobs.jsx` | My jobs + `post-role-panel` scroll-safe form |
| `frontend/src/components/MatchDetailsDrawer.jsx` | Side drawer; 400px / 100dvh / bottom pad |
| `frontend/src/App.css` | Imports theme layers; drawer, applicant-row, match card styles |
| `frontend/src/pages/admin/AdminConsole.jsx` | Rebuilt admin layout |
| `frontend/src/theme/dark-mode.css` | Dark contrast for cards, drawer, applicants |
| `backend/core/real_jobs_sync.py` | Live jobs fetch + snapshot (committed) |
| `backend/services/real_jobs_service.py` | Sync orchestration (committed) |
| `docs/submission/jaamas/manuscript/sections/section-2-literature-review.tex` | 12 citation TODOs |
| `.claude/knowledge_graph.md` | Codebase map v14 (local, uncommitted) |

## External links

None.

## Memory snapshot

- `.claude/knowledge_graph.md` **v14** — portal UI polish, page-shell, applicants feed, match dedupe (local)
- Professor QA (2026-05-27): 10 PASS / 4 PARTIAL / 1 FAIL (citations)
- Code review (2026-05-27): localhost-only until auth/PII hardening
- 14 graph entries still stale: Profile, Onboarding, MatchExplainability, README, etc.

## Persistent context

- Knowledge graph: `.claude/knowledge_graph.md`, `.claude/knowledge_graph.json`
- Live jobs contract: `docs/design/external-live-jobs-api-HANDOFF.md`
- JAAMAS build: `docs/submission/jaamas/build_all.sh`
- Design: `docs/design/HLD-multi-agent-system.md`, `docs/design/SDD-multi-agent-system.md`

## Next steps

1. **Manual QA portal polish** — verify: `/employer/matches` (no duplicate stats/refresh), `/employer/applications` (flat rows, dark mode), `/employer/jobs` (scroll form to bottom), open match drawer (bottom not clipped)
2. **Commit UI polish + admin + onboarding** — verify: `git status` clean except LaTeX aux; `npm run build` passes
3. **Run full test suite after commit** — verify: `bash scripts/run_tests.sh` → 310+ pass
4. **Refresh remaining stale knowledge entries** — verify: `/knowledge refresh frontend/src/pages/candidate/`
5. **Set `REAL_JOBS_BASE_URL`** and smoke-test sync — verify: `POST /real-jobs/sync` → 200
6. **Resolve ~29 `\todo`s** (12 citations in §2) — verify: `rg '\\todo' docs/submission/jaamas/manuscript` minimal
7. **Fill author block + CRediT** — verify: no `First Author` / `example.edu`
8. **Optional: admin UI for live jobs sync** — verify: button calls `/real-jobs/sync`
