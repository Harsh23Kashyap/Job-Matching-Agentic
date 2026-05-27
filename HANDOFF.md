# Handoff
> Written: 2026-05-28 | Branch: main @ `9db6abc` (pushed) | Dir: /Users/harshkashyap/Projects/JobMatcher-v1/Job-Matching-Agentic

## Goal

Deliver a thesis-ready **multi-agent JobMatch platform** and a **JAAMAS submission manuscript** reframed as an accessible multi-agent recruitment paper. Manuscript §2–§7 rewrite is **committed and pushed**. Remaining work: commit product features (live jobs API, test reorg, error UX), resolve manuscript `\todo`s and citations, fill author metadata, optional API hardening before professor resubmission.

## Current state

- **Done (committed & pushed @ `9db6abc`):**
  - JAAMAS manuscript §1–§7 rewrite, Algorithm 1, Fig1–5 PDFs, knowledge graph v12 snapshot in that commit
- **Done (local, not committed):**
  - **External live jobs API** — `core/real_jobs_sync.py`, `services/real_jobs_service.py`, `GET/POST /real-jobs/*`, snapshot boot, daily-batch pre-sync, CLI `sync_real_jobs_once.py`, 8 new tests
  - **Test reorganization** — `tests/unit/backend/` (33 py), `tests/unit/frontend/` (9 mjs), `scripts/run_tests.sh`, READMEs
  - **Error page UX** — full-screen centered layout, broken-route SVG, animated background, 502 copy update
  - **PortalShell fix** — replaced `NavLink` with `Link` + manual active state (fixes `isActive` DOM warning)
  - **Docs** — `docs/design/external-live-jobs-api-HANDOFF.md` (full contract from legacy repo)
- **In progress:** None
- **Blocked:** Springer upload (author placeholders); professor resubmission (~29 `\todo`s, 12 citation gaps in §2)

## Decisions made

| Decision | Why | Alternatives rejected |
|----------|-----|----------------------|
| Port live jobs to multi-agent rewrite (Employer Agent) | Handoff contract from `Agentic-Job-Matching`; employer owns job corpus | Keep legacy monolith `app.py` sync only |
| `RealJobsService` on `SystemContainer` | Orchestrates replace_corpus + reindex without bloating matchmaker | Global module state like legacy `app.py` |
| Snapshot boot without `REAL_JOBS_ENABLE` | Survive restarts from last good fetch (legacy behavior) | Require enable flag for boot |
| Test split `unit/backend` + `unit/frontend` | Mixed .py/.mjs in flat `unit/` was confusing | Domain subfolders under integration (deferred) |
| `Link` instead of `NavLink` for portal nav | React 19 + RR7 leaked `isActive` to DOM | Styled transient props / custom wrapper |
| Matching routes still unauthenticated | Admin console + existing tests | Auth-gate all `/match/*` (needs test rewrite) |
| Manuscript committed before product features | User requested push of paper work first | Single mega-commit |

## Open questions

- [ ] Unknown: Production `REAL_JOBS_BASE_URL` (likely aiforjob.ai provider) — not in repo
- [ ] Unknown: Whether provider requires auth headers — legacy client sends none
- [ ] Hypothesis: Professor accepts 12 citation TODOs as draft — QA marked **FAIL** on citations
- [ ] Unknown: Add admin UI button for `POST /real-jobs/sync` — API ready, no frontend yet
- [ ] Hunch: Security review gaps matter if demo is network-exposed — open admin register, PII on match routes

## Blockers & dependencies

| What | Who/Where | Status |
|------|-----------|--------|
| Author placeholders in `main.tex` | User | open |
| 12 §2 citation TODOs + ~29 total `\todo`s | User/literature | open |
| `REAL_JOBS_BASE_URL` for live sync | Deployment env | not in repo |
| Professor resubmission | User | waiting on todo cleanup |
| Springer upload | User | not started |

None blocking localhost demo or manuscript compile.

## Environment

- **Branch:** `main` @ `9db6abc` (pushed)
- **Uncommitted changes:** ~63 files — live jobs API, test reorg, error pages, PortalShell, READMEs, `.gitignore`, `backend/.env.example`
- **Untracked:** `backend/services/`, `backend/core/real_jobs_sync.py`, `backend/gateway/routes/real_jobs.py`, test files, `scripts/run_tests.sh`, LaTeX aux in manuscript/
- **Recent commits:**
  - `9db6abc` Rewrite JAAMAS manuscript §2–§7 + artifacts
  - `010dadf` Knowledge graph for JAAMAS/explainability
  - `3631bcb` Portal docs, build pipeline
- **Build status:** Frontend `npm run build` passes; manuscript was 33 pp. at last compile
- **Test status:** **310 passed** (`pytest ../tests -q`, 2026-05-28); node utils via `run_tests.sh`
- **Active processes:** None

## What worked

- Porting `real_jobs_sync` from legacy repo with `EmployerAgent.replace_corpus()` + rich Chroma metadata
- `scripts/run_tests.sh` as single entry point (pytest + node)
- Error page: `.error-page` flex center + `ErrorBackground` matches dashboard ornament language
- `Link` + `linkIsActive()` eliminates React `isActive` warning cleanly
- Simple `git commit -m "..."` (avoid HEREDOC/trailer hangs in Cursor shell)

## What didn't work

- HEREDOC / `--trailer` git commits hang in Cursor shell — use plain `-m`
- Do not commit LaTeX `.aux/.log/.bbl/.blg/.out`
- CSP `contentScript.bundle.js` console error is a **browser extension**, not app code
- `/review` security findings still open — tests assert unauthenticated match/admin behavior
- Cross-encoder rerank: worse nDCG on demo corpus — do not oversell

## Commands

```bash
# Full test suite
bash scripts/run_tests.sh

# Backend only
cd backend && source .venv/bin/activate && pytest ../tests -q

# Frontend utils only
node --test tests/unit/frontend/test_*.mjs

# Dev servers
cd backend && uvicorn main:create_app --factory --reload --port 8001
cd frontend && npm run dev

# Live jobs sync (requires REAL_JOBS_* in backend/.env)
curl -s http://localhost:8001/real-jobs/status | jq
curl -s -X POST http://localhost:8001/real-jobs/sync -H 'Content-Type: application/json' -d '{"reindex":true}' | jq
python backend/scripts/sync_real_jobs_once.py

# Manuscript compile
cd docs/submission/jaamas/manuscript && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
bash docs/submission/jaamas/build_all.sh

# Count manuscript TODOs
rg '\\todo' docs/submission/jaamas/manuscript
```

## Key files

| File | Why It Matters |
|------|---------------|
| `backend/core/real_jobs_sync.py` | Upstream fetch, normalize, pagination, snapshot I/O |
| `backend/services/real_jobs_service.py` | Sync orchestration, boot from snapshot, reindex |
| `backend/gateway/routes/real_jobs.py` | `GET/POST /real-jobs/*` proxy API |
| `backend/agents/employer_agent.py` | `replace_corpus()` for live job feed |
| `docs/design/external-live-jobs-api-HANDOFF.md` | Full 6-contract spec (ported from legacy) |
| `scripts/run_tests.sh` | Unified pytest + node runner |
| `frontend/src/pages/errors/ErrorPage.jsx` | Redesigned error UX |
| `frontend/src/layouts/PortalShell.jsx` | Portal nav (Link-based active state) |
| `docs/submission/jaamas/manuscript/sections/section-2-literature-review.tex` | 12 citation TODOs |
| `docs/submission/jaamas/manuscript/references.bib` | Only 7 entries — needs expansion |
| `backend/gateway/routes/matching.py` | Unauthenticated match + daily-batch pre-sync |
| `.claude/knowledge_graph.md` | Codebase map (v13 local refresh pending commit) |

## External links

None.

## Memory snapshot

- `.claude/knowledge_graph.md` v13 — live jobs, test layout, error pages (local)
- Professor QA (2026-05-27): 10 PASS / 4 PARTIAL / 1 FAIL (citations)
- Code review (2026-05-27): localhost-only until auth/PII hardening
- Legacy live-jobs handoff source: `/Users/harshkashyap/Projects/JobMatcher-v1/Agentic-Job-Matching/HANDOFF.md`

## Persistent context

- Knowledge graph: `.claude/knowledge_graph.md`, `.claude/knowledge_graph.json`
- Live jobs contract: `docs/design/external-live-jobs-api-HANDOFF.md`
- JAAMAS build: `docs/submission/jaamas/build_all.sh`
- Design: `docs/design/HLD-multi-agent-system.md`, `docs/design/SDD-multi-agent-system.md`

## Next steps

1. **Commit product work** (live jobs, tests, error UX, PortalShell) — verify: `git status` clean except aux/LaTeX
2. **Set `REAL_JOBS_BASE_URL`** in deployment `.env` and smoke-test sync — verify: `POST /real-jobs/sync` → 200 + `jobs_live.json`
3. **Fix §1 “matchmaking engine” → “Matchmaking agent”** — verify: `rg 'matchmaking engine' docs/submission/jaamas/manuscript` → 0
4. **Resolve ~29 `\todo`s** (12 citations in §2) — verify: `rg '\\todo' docs/submission/jaamas/manuscript` minimal
5. **Fill author block + CRediT** — verify: no `First Author` / `example.edu`
6. **Optional: admin UI for live jobs sync** — verify: button calls `/real-jobs/sync` then refreshes `/jobs/full`
7. **Optional API hardening** if network demo required — verify: match routes require auth; admin register gated
8. **Re-run `build_all.sh`** + sync portal PDFs with §6 numbers — verify: cover letter matches abstract
9. **Commit knowledge graph v13** after product commit — verify: graph documents `core/real_jobs_sync.py` path
