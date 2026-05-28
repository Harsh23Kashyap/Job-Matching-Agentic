## JAAMAS portal screenshots (Figure 10) — 2026-05-28

**Decisions:**
- Purpose: prove prototype exists (back Figs 6–8, §4 frontend).
- Placement: §4 after frontend subsection; Figure 10 with three sub-panels.
- Set: (a) candidate matches+drawer, (b) employer matches+drawer, (c) composite breakdown crop.
- Capture via Playwright script against demo accounts; not usability study claims.

**Approach chosen:** Approach A — two-sided matches + breakdown detail panel.
**Outcome:** Implemented (screenshots + LaTeX + capture script).
**Files affected:** `figures/screenshots/*.png`, `figures/scripts/capture_portal_screenshots.mjs`, `manuscript/sections/section-4-implementation.tex`, `manuscript/jaamas-macros.tex`, `figures/README.md`.


**Decisions:**
- Keep the active manuscript visually Springer/JAAMAS-safe: no colored headings, figure borders, shaded rows, or layout packages.
- Improve design through captions, table notes, column structure, figure sizing macros, and clearer heading wording.

**Approach chosen:** Compliant editorial polish inside the existing `sn-jnl` manuscript.
**Outcome:** Implemented.
**Files affected:** `docs/submission/jaamas/manuscript/jaamas-macros.tex`, `sections/section-3.tex`, `sections/section-4.tex`, `sections/section-5.tex`, `sections/section-7.tex`.

## JAAMAS PDF layout (reviewer-safe) — 2026-05-17

**Decisions:**
- No section `\hrule` dividers, no underlined headings, no LaTeX figure `\fcolorbox` (Springer audit).
- Improve PDF via sn-jnl-only running head + footer hairline + section spacing.
- Figure borders only in draw.io export, not TeX wrappers.

**Approach chosen:** Approach A — typography rhythm in `jaamas-style.tex`.
**Outcome:** Implemented (`2026-05-17-layout-v2` build marker).
**Files affected:** `jaamas-style.tex`, `main.tex`.

## Multi-agent architecture rewrite — 2026-05-27

**Decisions:**
- Greenfield code rewrite (not paper-only reframe).
- Three agents: Candidate, Employer, Matchmaking + UI layer.
- Hybrid agentic: structured agents v1; LLM hooks v2 (parse, explain, refine).
- Event-driven monolith (in-process bus, not microservices).
- Preserve eval corpus + benchmarks only; rewrite rest.

**Approach chosen:** Event-driven monolith with agent state ownership and pub-sub events.
**Outcome:** HLD drafted; SDD drafted; V1-V2 scope doc added; no code yet.
**Files affected:** `docs/design/HLD-multi-agent-system.md`, `docs/design/SDD-multi-agent-system.md`, `docs/design/V1-V2-SCOPE.md`, local knowledge graph (rewrite roadmap).

## Role portals + auth (v1.1) — 2026-05-27

**Decisions:**
- Real product: 3 logged-in portals (Candidate, Employer, Admin) — not v2 defer.
- Three route-based portals (`/candidate`, `/employer`, `/admin`) with shared match components.
- Candidate flow: upload resume → LLM extract → edit profile → search jobs.
- LLM CV parser in v1.1 (Ollama/OpenAI); heuristics-only rejected.
- Auth: email/password, HTTP-only cookie session, SQLite user store.
- Admin keeps current Match Console unchanged.

**Approach chosen:** Three route portals + FastAPI auth + LlmParser resume pipeline.
**Outcome:** Spec saved; implementation pending.
**Files affected:** `docs/design/v1.1-role-portals-auth.md`.

## Role portals + auth (v1.1) — implementation — 2026-05-27

**Outcome:** Implemented — auth, 3 portals, LLM resume upload, 59 tests.
**Files affected:** `backend/auth/`, `backend/hooks/llm_parser.py`, `backend/core/resume_text.py`, `frontend/src/pages/`, `frontend/src/layouts/`, `frontend/src/context/`.

## Demo-ready sprint — 2026-05-27

**Decisions:**
- Next sprint optimizes for supervisor demo, not v2 benchmarks or new product features yet.
- Scripted 15-min path (not Playwright E2E): DEMO-SCRIPT + DEMO-CHECKLIST + demo accounts.
- Admin console remains research baseline; candidate/employer portals are the product story.

**Approach chosen:** Scripted demo path with manual smoke verification.
**Outcome:** Demo docs written; smoke passed (69 tests, Rahul→ML rank 1, demo accounts work).
**Files affected:** `docs/demo/DEMO-SCRIPT.md`, `docs/demo/DEMO-CHECKLIST.md`, `HANDOFF.md`, `README.md`.
