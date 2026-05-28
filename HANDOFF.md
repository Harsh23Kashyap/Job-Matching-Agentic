# Handoff
> Written: 2026-05-28 15:45 | Branch: main @ `14eaad0` (pushed) | Dir: /Users/harshkashyap/Projects/JobMatcher-v1/Job-Matching-Agentic

## Goal

Ship a **thesis-ready multi-agent JobMatch platform** and a **JAAMAS submission package**: nine architecture/evaluation figures, eight portal screenshots (Figure 10), Springer-safe LaTeX manuscript with real authors, and an Overleaf upload zip.

## Current state

- **Done (committed & pushed @ `14eaad0`):**
  - **JAAMAS manuscript** — authors Harsh Kashyap + Taranumpreet Kaur Wasu (Thapar Institute); supervisor Dr Parteek Bhatia (WSU) in acknowledgments; `main.pdf` ~41 pages
  - **Figures 1–9** — Fig 1 draw.io HLD; Figs 2–9 Mermaid + crop/border pipeline; LaTeX `\JFigFramed` borders on diagram PDFs
  - **Figure 10** — 8 stacked portal screenshots (onboarding, profile, matches, breakdown, employer jobs/matches, admin console + match run); Playwright capture script
  - **Layout fixes** — tables use `[h!]` in-flow placement; screenshots vertical stack in §4
  - **Overleaf zip** — `docs/submission/jaamas/build/jaamas-overleaf-upload.zip` (54 files, all PNGs + PDFs)
  - **Profile bugfix** — `hasExtractedSections(null)` crash on `/candidate/profile` fixed in `extractedSections.js`
  - **Zip script** — includes `figures/screenshots/*.png`; ignores `node_modules`
- **Done (committed @ `03dc791`):** responsive layout, admin console rebuild, Qdrant fix, live jobs API (`a4005e0`), test reorg
- **In progress:** None
- **Blocked:** Springer submission still needs corresponding-author email; ~29 manuscript `\todo`s (12 citation gaps in §2); `REAL_JOBS_BASE_URL` not in repo

## Decisions made

| Decision | Why | Alternatives rejected |
|----------|-----|----------------------|
| Fig 1 canonical source = draw.io | Matches reference Agentic-Job-Matching style; pageframe `#94a3b8` | Mermaid-only Fig 1 |
| Figure 10 = 8 vertical panels | Covers all three portals + ingestion; user requested more screenshots | 3-panel side-by-side (too cramped) |
| `\JFigShot` for screenshots, `\JFigFramed` for PDFs | Avoid double borders in compiled PDF | LaTeX frame on PNGs only |
| Tables `[h!]` not `float [H]` | sn-jnl wraps `table` in `threeparttable`; `[H]` breaks compile | `[!t]` float-to-top (overlapped prose) |
| Admin screenshot = semantic match run | Admin console has no composite strategy dropdown | Fake composite label in caption |
| Exclude LaTeX aux + Playwright node_modules from git | Build artifacts and heavy deps | Commit everything |

## Open questions

- [ ] Unknown: Corresponding-author email for Springer — not in repo
- [ ] Hypothesis: Professor accepts citation TODOs as draft — prior QA marked citations **FAIL**
- [ ] Unknown: Redraw Figs 2–9 in draw.io reference style — Fig 1 done, rest still Mermaid
- [ ] Unknown: Add admin UI button for `POST /real-jobs/sync` — API ready, no frontend control
- [ ] Hunch: Figure 10 may span 3+ PDF pages — acceptable for prototype proof; could split to Figure 11 if reviewer complains

## Blockers & dependencies

| What | Who/Where | Status |
|------|-----------|--------|
| Corresponding-author `\email{}` | User | open |
| ~29 `\todo`s (12 citations §2) | User/literature | open |
| `REAL_JOBS_BASE_URL` | Deployment env | not in repo |
| Springer upload | User | zip ready |

None blocking localhost demo or Overleaf compile.

## Environment

- **Branch:** `main` @ `14eaad0` (synced with `origin/main`)
- **Uncommitted changes:** None (HANDOFF timestamp line only if amended)
- **Recent commits (on remote):**
  - `14eaad0` Complete JAAMAS submission package with figures, screenshots, and docs sync
  - `03dc791` Add responsive layout system and sync frontend unit tests
  - `edd7a7c` Polish portal UX, rebuild admin console, fix Qdrant store
  - `a4005e0` Add live jobs API, reorganize tests, sync manuscript
- **Build status:** `main.pdf` compiles (pdfLaTeX); frontend `npm run build` passed 2026-05-28
- **Test status:** 310 passed at last full run; not re-run after profile null-guard fix
- **Active processes:** Dev stack was on `:5173` + `:8001` for screenshot capture

## What worked

- `bash archive/dev-scripts/make_overleaf_zip.sh` after fixing screenshot glob (`compgen -G`)
- `node capture_portal_screenshots.mjs` with demo accounts — 8 PNGs + auto border pass
- `crop_figures.py --borders-only --border-screenshots-only` for `#94a3b8` frames
- Fig 1 via `export_fig1_drawio.sh` + `gen_fig1_drawio.py`
- Stacked `\JFigShot` panels at 0.92\linewidth — readable in PDF
- Null-safe `hasExtractedSections(extractedRaw ?? {})` — unblocks profile page

## What didn't work

- `float` package `[H]` on `JTable` — breaks sn-jnl `threeparttable` wrapper
- Side-by-side 3 minipage screenshots — overlap and illegible on Springer column
- Profile capture before null-guard — white screen from `hasExtractedSections(null)`
- Committing `figures/scripts/node_modules/` — added `package.json` + `.gitignore` instead

## Commands

```bash
# Dev stack (screenshot capture prereq)
cd backend && source .venv/bin/activate && uvicorn main:create_app --factory --reload --port 8001
cd frontend && npm run dev

# Capture Figure 10 screenshots
cd docs/submission/jaamas/figures/scripts && npm install && npx playwright install chromium
node capture_portal_screenshots.mjs

# Regenerate figures
cd docs/submission/jaamas/figures
bash export_fig1_drawio.sh
bash export_all_mermaid.sh
bash apply_figure_borders.sh

# Manuscript + Overleaf zip
cd docs/submission/jaamas/manuscript && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
bash archive/dev-scripts/make_overleaf_zip.sh

# Tests
bash scripts/run_tests.sh

# Manuscript TODO audit
rg '\\todo' docs/submission/jaamas/manuscript
```

## Key files

| File | Why It Matters |
|------|---------------|
| `docs/submission/jaamas/manuscript/main.tex` | Authors, abstract, `\maketitle` |
| `docs/submission/jaamas/manuscript/sections/section-4-implementation.tex` | Figure 10 (8 screenshots) |
| `docs/submission/jaamas/manuscript/jaamas-macros.tex` | `\JFigFramed`, `\JFigShot` |
| `docs/submission/jaamas/manuscript/jaamas-style.tex` | `JTable [h!]`, figure placement |
| `docs/submission/jaamas/figures/scripts/capture_portal_screenshots.mjs` | Playwright capture all portals |
| `docs/submission/jaamas/figures/crop_figures.py` | Crop, square pad, border PNG/PDF |
| `archive/dev-scripts/make_overleaf_zip.sh` | Overleaf upload package |
| `docs/submission/jaamas/build/jaamas-overleaf-upload.zip` | Upload artifact |
| `frontend/src/utils/extractedSections.js` | Profile page null-safe guard |
| `docs/submission/jaamas/figures/DIAGRAM-DESIGNS.md` | Figure design spec |

## External links

None.

## Memory snapshot

- Authors: Harsh Kashyap, Taranumpreet Kaur Wasu (Thapar); supervisor Dr Parteek Bhatia (WSU)
- Demo accounts: `demo.candidate@test.com`, `demo.employer@test.com`, `demo.admin@test.com` / `demo1234`
- Professor QA (2026-05-27): citations marked FAIL among ~29 todos

## Persistent context

- Knowledge graph: `.claude/knowledge_graph.md` (v15 JAAMAS entries)
- Brainstorm: `.claude/brainstorm-history.md` (Figure 10 decisions)
- JAAMAS build: `docs/submission/jaamas/build_all.sh`
- Design: `docs/design/HLD-multi-agent-system.md`

## Next steps

1. **Add corresponding-author email** in `main.tex` — verify: `\email{...}` renders on title page
2. **Resolve §2 citation TODOs** — verify: `rg '\\todo' manuscript` count drops
3. **Optional: redraw Figs 2–9 in draw.io** — verify: match Fig 1 pageframe style
4. **Run full test suite** after push — verify: `bash scripts/run_tests.sh` → 310+ pass
5. **Set `REAL_JOBS_BASE_URL` and smoke sync** — verify: `POST /real-jobs/sync` → 200
6. **Springer upload** — verify: Overleaf compiles zip to same ~41-page PDF
