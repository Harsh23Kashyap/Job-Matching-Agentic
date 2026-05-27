## JAAMAS Manuscript Design Polish - 2026-05-17

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
**Outcome:** HLD drafted; SDD pending HLD approval; no code yet.
**Files affected:** `docs/design/HLD-multi-agent-system.md`, `.claude/knowledge_graph.md` (rewrite roadmap).
