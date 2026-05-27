# Handoff
> Written: 2026-05-27 | Branch: main | Dir: /Users/harshkashyap/Projects/JobMatcher-v1/Job-Matching-Agentic

## Goal

Deliver a thesis-ready JobMatch product with reliable portals, composite matching, improved document parsing, skill normalization, and employer/candidate **quality intelligence** — then commit and push the large uncommitted feature batch on `main`.

## Current state

- **Done (committed & pushed):**
  - Portal bug fixes, profile gates, employer job ownership — `9d1de25`
  - HLD/SDD v1.1 alignment — `b760b8b`
  - Prior research pipeline, composite scoring baseline, portal polish — older commits on `main`
- **Done (local, uncommitted):**
  - **API reliability:** `backend/gateway/errors.py`, `handlers.py`; consistent error envelopes; auth/store ownership hardening; route fixes in candidates, employers, matching, feedback, similar; `tests/integration/test_api_errors.py`
  - **Matching quality:** 6-signal composite (semantic 28%, skills 27%, title 10%, experience 15%, compensation 10%, remote 10%); `MatchDetailsDrawer` breakdown; `frontend/src/utils/matchScoring.js`
  - **Resume/JD parsing:** `document_parse.py`, `resume_structured_extract.py`, `job_structured_extract.py`, enhanced `resume_clean.py`; LLM merge; `ExtractedSectionsPanel`; integration tests
  - **Skill normalization:** `shared/skill_catalog.json`; expanded `skill_catalog.py`; `frontend/src/utils/skillCatalog.js`; dedupe on save via `hooks/parser.py`
  - **Employer job quality:** `backend/core/job_quality.py`, `POST /jobs/quality-check`, `JobQualityPanel` on `Jobs.jsx`; parse responses include `quality`
  - **Candidate profile quality:** `backend/core/profile_quality.py`, `POST /candidates/quality-check`, `ProfileQualityPanel` on `Onboarding.jsx` + `Profile.jsx`; upload includes `quality`; fixed missing `profileLoaded` state in Onboarding
- **In progress:** None actively coding — large diff sitting uncommitted (~37 modified + ~25 new files)
- **Blocked:** None for local demo

## Decisions made

| Decision | Why | Alternatives rejected |
|----------|-----|----------------------|
| Rule-based quality modules (job + profile) | Instant debounced UX, testable without LLM | LLM-only quality scoring (cost, latency) |
| `shared/skill_catalog.json` as synonym source | Single catalog for Python + Vite frontend | Duplicate maps in backend/frontend only |
| Parse pipeline: clean → rules → LLM merge | Works when LLM unavailable; rules fill gaps | LLM-only extraction |
| Quality on debounced `POST /*/quality-check` | Single source of truth; live form updates | Duplicate scoring logic in frontend only |
| Profile quality replaces `ProfileStrength` in edit flows | Richer guidance; keep `ProfileStrength` on read-only summary | Two overlapping panels in edit mode |
| Composite weights 28/27/10/15/10/10 | Better title/remote signals for match explain | Old 40/30/15/10/5 split |

## Open questions

- [ ] Hypothesis: Full `pytest ../tests -q` still passes with all changes — worth running before commit
- [ ] Unknown: Whether HLD/SDD should document new quality endpoints and composite weights — matters for thesis appendix alignment
- [ ] Hunch: Uncommitted API reliability changes may need a quick smoke test of employer/candidate auth edge cases — evidence: large route diff

## Blockers & dependencies

| What | Who/Where | Status |
|------|-----------|--------|
| Commit/push of feature batch | User/agent | not done |
| LLM keys for live parse | Local `.env` | optional for rule-only fallback |

None.

## Environment

- **Branch:** `main`
- **Uncommitted changes:** 37 modified files, ~25 untracked (quality modules, parsing, skill catalog, gateway errors, frontend panels, tests). ~1283 insertions / 408 deletions on tracked files.
- **Recent commits:**
  - `b760b8b` Align HLD and SDD v1.1 with implemented backend and frontend
  - `9d1de25` Fix portal profile/match flows and harden employer job ownership
  - `c1a451d` Polish portal theme, candidate profile flow, and employer jobs UX
- **Build status:** Frontend `npm run build` passing (last run this session)
- **Test status:** Targeted suites passing — profile quality (19), job quality (12), parsing (35), skill catalog (12); full suite not re-run this session
- **Active processes:** None known

## What worked

- Mirroring employer `JobQualityPanel` pattern for candidate `ProfileQualityPanel` (debounced API + parse snapshot on upload)
- Shared JSON skill catalog imported by Vite (`with { type: "json" }`) and Python `skill_catalog.py`
- Rule extract + LLM merge in `document_parse.py` with graceful `llm_status` fallbacks
- Gateway `errors.py` + global handlers for consistent API envelopes

## What didn't work

- Relying on case-sensitive skill overlap in tests after canonicalization — fixed by comparing `.lower()`
- `profileLoaded` referenced in Onboarding without `useState` — fixed when wiring profile quality
- Initial job quality test expected empty title on LLM-unavailable parse — updated for rule-based title inference

## Commands

```bash
# Backend tests (from backend/)
cd backend && pytest ../tests -q

# Targeted quality + parsing
pytest ../tests/unit/test_profile_quality.py ../tests/unit/test_job_quality.py \
  ../tests/integration/test_profile_quality_api.py ../tests/integration/test_job_quality_api.py \
  ../tests/integration/test_resume_upload.py ../tests/integration/test_job_parse.py -q

# Frontend
cd frontend && npm run build
node --test ../tests/unit/test_skills_input.mjs ../tests/unit/test_profile_normalize.mjs

# Dev servers
cd backend && uvicorn gateway.app:build_gateway --factory --reload --port 8001
cd frontend && npm run dev
```

## Key files

| File | Why It Matters |
|------|---------------|
| `backend/core/profile_quality.py` | Candidate completeness, summary/salary/parsing confidence, match suggestions |
| `backend/core/job_quality.py` | Employer JD quality score, missing fields, salary/skill warnings |
| `backend/core/document_parse.py` | Unified resume/JD parse; attaches `quality` on resume parse |
| `backend/core/resume_structured_extract.py` | Rule-based resume field extraction |
| `backend/core/job_structured_extract.py` | Rule-based JD field extraction |
| `shared/skill_catalog.json` | Synonym + display name catalog (backend + frontend) |
| `backend/gateway/errors.py` | Shared API error helpers and codes |
| `backend/core/scoring.py` | Composite weights and component breakdown |
| `frontend/src/components/ProfileQualityPanel.jsx` | Candidate quality UI |
| `frontend/src/components/JobQualityPanel.jsx` | Employer quality UI |
| `frontend/src/pages/candidate/Onboarding.jsx` | Upload → review with quality panel |
| `frontend/src/pages/candidate/Profile.jsx` | Re-upload + edit with quality panel |
| `frontend/src/pages/employer/Jobs.jsx` | JD import + form with job quality panel |
| `backend/gateway/routes/candidates.py` | `/upload-resume`, `/quality-check`, profile upsert |
| `backend/gateway/routes/employers.py` | `/parse-description`, `/quality-check`, job CRUD |

## External links

None.

## Memory snapshot

- `.claude/knowledge_graph.md` exists (v8 from earlier session) — **stale** relative to quality intelligence and skill catalog; refresh after commit if continuing docs work

## Persistent context

- Knowledge graph: `.claude/knowledge_graph.md`
- Design specs: `docs/design/HLD-multi-agent-system.md`, `docs/design/SDD-multi-agent-system.md` (v1.1; may not reflect latest composite weights or quality APIs)
- Scope doc: `docs/design/V1-V2-SCOPE.md`

## Next steps

1. Run full test suite — verify: `cd backend && pytest ../tests -q` exits 0
2. Commit uncommitted work in logical chunks (API hardening, matching, parsing, skills, quality) or one feature commit — verify: `git status` clean after push
3. Update HLD/SDD sections for composite weights, parse pipeline, `/quality-check` endpoints — verify: docs mention 6-signal breakdown and profile/job quality
4. Optional: show `ProfileQualityPanel` on read-only profile view (`CandidateProfileSummary`) — verify: quality visible without entering edit mode
5. Refresh `.claude/knowledge_graph.md` if continuing agent sessions — verify: new modules listed under `backend/core/`
