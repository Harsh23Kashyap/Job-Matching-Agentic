# Codebase Knowledge Graph
> Last updated: 2026-05-28 (v15 · JAAMAS figures, Figure 10 screenshots, authors, Overleaf zip) | Entries: 500+ | Modules: 16

---

## Team handoff · read this first

**Project:** Job-Matching-Agentic · greenfield **multi-agent rewrite** of the job matching system. Three agents (Candidate, Employer, Matchmaking), role portals, composite explainable matching, thesis-demo ready.

**Authors:** Harsh Kashyap, Taranumpreet Kaur Wasu (Thapar Institute of Engineering and Technology). Supervisor: Dr Parteek Kumar (Washington State University).

**Repository:** https://github.com/Harsh23Kashyap/Job-Matching-Agentic  
**Branch:** `main` · **Local uncommitted (2026-05-28):** JAAMAS manuscript (authors, Figs 1–10, 8 portal screenshots, Overleaf zip), figure borders, table layout, profile null-guard · **Recent pushed commit:** `03dc791` responsive layout + frontend tests

**Handoff:** [HANDOFF.md](../HANDOFF.md) · **Overleaf zip:** `docs/submission/jaamas/build/jaamas-overleaf-upload.zip`

**Legacy note:** Entries under [Module: backend (legacy monolith)](#module-backend-legacy-monolith) describe the **pre-rewrite** `app.py` monolith. Current runtime uses `main.py` → `bootstrap.py` → `gateway/app.py`. See [Module: rewrite (current)](#module-rewrite-current) and [Module: research evaluation](#module-research-evaluation).

### Current architecture (rewrite)

| Agent | Owns | Does not own |
|-------|------|--------------|
| **Candidate Agent** | CV profiles, embeddings (`candidates_collection`), profile events | Jobs, match scores |
| **Employer Agent** | Job postings, embeddings (`jobs_collection`), job events | Candidates, rankings |
| **Matchmaking Agent** | Scoring, ranking, explanations, match sessions | Vector writes, raw profiles |

**Event bus:** in-process pub-sub (`AgentEventBus`). Events: `CandidateProfileUpdated`, `JobProfileUpdated`, `CorpusBootstrapped`, `MatchCompleted`.

**Default product scoring:** `composite` · semantic 28%, skills 27%, title 10%, experience 15%, compensation 10%, remote 10%. UI bands: Strong ≥80, Good ≥65, Moderate ≥50, Low <50.

### Thesis-demo features (shipped)

- **Six-signal composite** + `MatchDetailsDrawer` breakdown with contribution points (`score_components`)
- **Match explainability** · `core/match_explanation.py` → structured `explanation` on every `MatchResult` (matched/missing skills, experience/compensation/remote fit, semantic reason, score breakdown); compact UI via `MatchExplainability.jsx`
- **Search & filters** · role search, skill chips, remote, salary/budget, experience, match score range, sort (best/newest/compensation); `matchFilters.js`, `MatchResultsFilters.jsx` on both result panels
- **Demo data mode** · `demo_reset.py`, `seed_demo_activity()` pre-seeds saved jobs/applications/employer shortlist; `POST /system/demo/reset` (admin); reset button in `SystemConfigPanel.jsx`; `DEMO_MODE` config flag
- **Frontend layout polish (v14)** · unified `1120px` page shell (`page-shell.css`); employer/candidate match pages dedupe hero stats/refresh; flat applicant feed with search/filter; match drawer `400px`/`100dvh`; post-role panel scroll-safe
- **External live jobs** · `core/real_jobs_sync.py` + `RealJobsService`; `GET/POST /real-jobs/*`; snapshot `data/jobs_live.json`; `EmployerAgent.replace_corpus()`; daily-batch pre-sync when `REAL_JOBS_ENABLE=true`
- **Frontend state management** · profile/job cross-page events (`profileEvents.js`); stale-while-revalidate refresh; row-action guards; optimistic employer job close; `searchAfterSave` + `?job=` auto-match navigation
- **Resume/JD parsing pipeline:** clean → rule extract → LLM merge (`document_parse.py`, structured extract modules)
- **Skill normalization:** `shared/skill_catalog.json` · canonical dedupe on save and in UI (`skillCatalog.js`)
- **Employer job quality** · `POST /jobs/quality-check`, `JobQualityPanel` on paste/upload/edit
- **Candidate profile quality** · `POST /candidates/quality-check`, `ProfileQualityPanel` on onboarding/profile edit
- Resume upload with CID cleanup; profile upsert via `PUT /candidates/me`; stale link recovery
- Employer `POST /jobs` ownership guard (`get_job_owner` · 403 `JOB_NOT_OWNED`)
- Gateway error envelopes (`gateway/errors.py`, `handlers.py`) · consistent `{detail: {error, code}}`
- Candidate profile gates: `hasCandidateProfile` / `isCandidateProfileReady` / `isProfileStale`
- Employer JD paste + file upload; resume coach; similar jobs/candidates; feedback in SQLite
- **310 pytest + node tests** passing (product; 2026-05-28)
- Offline research pipeline · 9 stages → `backend/reports/research_run_<timestamp>/`

### Run locally

```bash
# Backend :8001
cd backend && source .venv/bin/activate
uvicorn main:create_app --factory --reload --port 8001

# Frontend :5173
cd frontend && npm run dev
```

**Demo accounts:** `demo.candidate@test.com`, `demo.employer@test.com`, `demo.admin@test.com` / `demo1234`

**Demo reset (local):** Admin Console → System → **Reset demo data**, or `POST /system/demo/reset` (requires `DEMO_MODE=true`, admin session, not read-only). Reloads 30 CVs + 15 jobs, re-links accounts, re-seeds saved/applied/shortlist activity.

### Key flows (v10)

| Flow | Path |
|------|------|
| Demo startup | `gateway/app.py` → `seed_demo_accounts` → `seed_demo_activity` (saved jobs, 1 application, employer shortlist) |
| Demo reset | Admin → `POST /system/demo/reset` → `reload_corpus` → `clear_demo_sqlite` → re-seed |
| Match explainability | `matchmaking_agent` → `build_match_explanation` → `MatchResult.explanation` → `MatchExplainability` compact/full |
| Client filters | `MatchResultsFilters` → `filterAndSortMatchRows` (no extra API calls) |
| Cross-page sync | `notifyProfileUpdated` / `notifyJobsUpdated` → Matches/Saved/employer pages invalidate or silent refetch |
| Auto-search | Onboarding/Profile first save → `navigate(..., { searchAfterSave: true })` → Matches auto-runs once |
| Employer deep link | `/employer/matches?job=job_01` → auto-match after role resolves |
| Applicant feed | `Applications.jsx` → flat rows · search/role/sort · link to matches |
| Shared page shell | `PortalShell` → `page-container` 1120px · `page-shell.css` tokens |

### Key docs

| Doc | Path |
|-----|------|
| Handoff | `HANDOFF.md` |
| JAAMAS figures | `docs/submission/jaamas/figures/README.md` |
| Overleaf zip | `docs/submission/jaamas/build/jaamas-overleaf-upload.zip` |
| HLD | `docs/design/HLD-multi-agent-system.md` |
| SDD | `docs/design/SDD-multi-agent-system.md` |
| Demo script | `docs/demo/DEMO-SCRIPT.md` |

### JAAMAS submission (2026-05-28)

| Item | Detail |
|------|--------|
| Manuscript PDF | `docs/submission/jaamas/manuscript/main.pdf` (~41 pp) |
| Authors | Harsh Kashyap, Taranumpreet Kaur Wasu (Thapar) |
| Figures 1–9 | PDF in `docs/submission/jaamas/figures/`; Fig 1 draw.io, 2–9 Mermaid |
| Figure 10 | 8 PNG screenshots in `figures/screenshots/` (all portals) |
| Capture | `figures/scripts/capture_portal_screenshots.mjs` (Playwright) |
| Borders | `\JFigFramed` (LaTeX PDFs); `\JFigShot` + `crop_figures.py` (PNG) |
| Zip | `archive/dev-scripts/make_overleaf_zip.sh` → 54 files |

---

### Benchmark & research evaluation

Corpus (demo): 30 CVs, 15 jobs, 47 graded pairs (scale 0–2). **Primary driver:** `python backend/scripts/run_research_pipeline.py` → timestamped run folder with validation, baselines, composite, ablation, significance, fairness, explainability, paper tables.

| Result (K=5, demo corpus) | Source report |
|---------------------------|---------------|
| Production composite nDCG@5 **0.942** | `composite_eval_report.json` |
| Best comparison baseline multimodal **0.924** | `comparison_summary.json` |
| Full composite vs semantic-only p=**0.019** (nDCG) | `significance_ablation_comparisons.csv` |
| Cross-encoder nDCG Δ **−0.108**, +141 ms/query | `cross_encoder_report.json` |
| Fairness flagged **6/10** synthetic pairs | `fairness_audit_report.json` |

Legacy drivers still present: `paper_progression`, `phase11`, `research_sweep`. Large-scale corpus at `data/research/` (100×50) generated but not yet pipeline-evaluated.

```bash
python backend/scripts/run_research_pipeline.py
python backend/scripts/run_research_pipeline.py --skip-cross-encoder --run-id my_run
bash scripts/run_research_suite.sh   # export → docs/research/evaluation/
```

---

## Paper rewrite roadmap · STATUS (user directive, 2026-05-27)

> **Committed:** `cfae2c2` + `3631bcb` (manuscript v1, portal, build). **Local session (2026-05-27):** full §2–§7 rewrite, professor QA pass, security code review — **not yet committed**.

**Completion checklist**

| Item | Status |
|------|--------|
| 7-section structure (§1–§7) | Done · committed + locally refined |
| Introduction story arc (no subsections, no tech opening) | Done · §1 (contrib bullet still says “matchmaking engine” — fix pending) |
| Multi-agent architecture §3 | Done · Fig1 multi-agent, §3.4 communication, Algorithm 1 |
| §4 Implementation (consolidated technical detail) | Done · local rewrite |
| §5 Quality Metrics (formulas only, no results) | Done · local rewrite; equations only in §5 |
| §6 Results (narrative + interpreted tables) | Done · local rewrite; `tab-method-comparison` moved here from §5 |
| §7 Conclusion + Future Scope (decision-support framing) | Done · local rewrite; 8 future-scope items |
| §2 Literature Review (6 themed subsections) | Done · local rewrite; **12 citation `\todo`s**, 7 bib entries |
| Portal cover letter + information sheet | Done · may need sync with §6 numbers |
| Build pipeline + Overleaf zip | Done · `build_all.sh`; re-run after commit |
| Abstract reframed (multi-agent) | Done · `main.tex` |
| Fig1 export fix (no `--crop`) | Done · local PDF re-export |
| Professor QA (14 criteria) | Done · 10 PASS / 4 PARTIAL / 1 FAIL (citations) |
| Author/affiliation placeholders | Open |
| Resolve ~29 `\todo` markers | Open · body + tables + declarations |
| Portal-weight composite ablation (28/27/10/15/10/10) | Open · `tab-ablation.tex` uses research weights |
| Explainability / fairness / phase11 result tables | Open |
| Optional Sal Khan bib entry | Open |

> **Original directive (archived intent).** Target: **white paper / internet-style** narrative for a general audience. Core reframe: a **multi-agentic recruitment system** where candidate-side and employer-side agents collaborate via shared representations and a matchmaking agent, not keyword search alone.

### 1. Reframe completely

- Lead with **why the problem matters**, recruitment pain points, time/cost of filtering, impact · not implementation.
- Defer technical terms (keyword search, embeddings, vector stores) until later sections.
- Current draft = technical report; target = accessible white paper with results that land for general readers.

### 2. Introduction (no subsections)

Single flowing narrative · **no 1.1, 1.2, etc.** Story arc:

1. Job seeker struggles today
2. Recruitment system problems
3. Time/cost of interviewing and filtering
4. Vision from **Sal Khan book chapter** (dual agents: candidate/client + employer)
5. Need for **agent collaboration**
6. Proposed solution: **multi-agentic job-matching system**
7. Contributions (see below)
8. Paper organization

Do **not** open with keyword/semantic search, embeddings, or vector stores.

### 2b. Sal Khan · *Brave New Words*, Part VIII (narrative anchor)

**Source:** Sal Khan, *Brave New Words* · Part VIII split into (1) future of K‑12 assessments, (2) AI of college admissions. User provided detailed walkthrough 2026-05-27.

**Khan's core thesis (Part VIII):** AI can move hiring/admissions-style gatekeeping from **narrow one-shot snapshots** (exams, test scores, keyword filters) toward **continuous, holistic, mastery-informed evaluation** · if designed with **transparency and equity**.

**Themes to echo in our intro (adapted from admissions → job matching):**

| Khan idea (Part VIII) | Job-matching parallel |
|----------------------|------------------------|
| One-shot high-stakes tests miss what people know | Resume keyword filters + single ATS score miss fit and growth |
| Continuous, low-stakes assessment embedded in learning | Ongoing profile updates, skill evidence over time (candidate agent state) |
| Mastery-based, granular progress records | Structured candidate/job profiles + versioned agent state, not one PDF dump |
| Holistic admissions beyond blunt test scores | Multimodal match (semantic + skills), graded relevance labels |
| AI triages volume; humans judge nuance | Matchmaker agent ranks; recruiter/human final decision (human-in-the-loop) |
| Richer signals: improvement curves, persistence, context | `why_ranked` explanations; future LLM hooks for narrative traits |
| Expanded opportunity for under-resourced candidates | Semantic/soft-skill overlap vs pure keyword gatekeeping |

**Dual-agent vision (maps to our architecture):**
- **Candidate-side representative** · owns CV/profile, advocates seeker interests (Candidate Agent)
- **Employer-side representative** · owns JD/requirements (Employer Agent)
- **Neutral broker** · holistic matching, not either party's keyword box (Matchmaking Agent)

**Guardrails Khan implies · bake into paper §1/§7 and system design:**
1. **Human-in-the-loop** · AI supports decisions; does not auto-hire/reject
2. **Transparency & auditability** · explain scores, show agent stages, publish eval protocol
3. **Bias monitoring** · test rankings across demographic proxies; report limits (small synthetic corpus)
4. **Clear rules for AI assistance** · disclose LLM use on parsing/explanation when v2 added

**Intro paragraph bridge (draft angle):** Khan argues admissions should see students as **growth curves and context**, not scores alone · the same shift applies when employers reduce millions of applicants to keyword search. A **multi-agent system** gives each side a dedicated representative and a shared matchmaker, moving from one-shot filtering toward **continuous, explainable alignment**.

**Do not overclaim:** We are not implementing Khan's full K‑12 continuous assessment stack; we **instantiate the admissions half of his vision** in the recruitment domain with measurable IR metrics.

### 3. Contributions (reworked)

1. **Candidate/client-side agent** · processes resumes/CVs
2. **Employer-side agent** · processes job descriptions
3. **Matchmaking agent** · semantic matching and ranking (intro bullet still says “engine” — pending fix)
4. **Multi-agent communication flow** · agents share relevant states/data
5. **UI/application layer** · end-to-end demonstrator
6. **Evaluation** · quality metrics showing improvement over baselines

### 4. Section 3 · multi-agent architecture diagram (block diagram first)

Not presentation/application/backend layers. Must show:

| Agent | Components |
|-------|------------|
| **Candidate Agent** | CV input → parsing → embedding → candidate vector store → profile/state |
| **Employer Agent** | JD input → parsing → embedding → job vector store → profile/state |
| **Matchmaking Agent** | reads both stores → semantic search → similarity score → ranked matches |
| **UI/Application Layer** | results, interaction, full workflow demo |

### 5. Agent communication (core framing)

Document explicitly: which agents exist; data ownership; state each agent maintains; communication protocol; shared data; vector store update flow; how matchmaking agent consumes both sides.

**Code mapping note (for rewrite):** today `ingestion.py` + `embedding.py` + `stores/*` map to both agents; `similarity_engine.py` + `app.py` match routes map to matchmaking; `real_jobs_sync.py` + daily batch map to employer-side refresh; reframe in prose, do not invent agents that do not exist unless implementing.

### 6. Matching algorithm (add/clean)

Formal algorithm block covering: inputs (resumes, JDs) → preprocessing/parsing → embedding → vector storage → semantic similarity → ranking → output (matched candidates/jobs). Align with existing `document_text.py` → `embedding.py` → `similarity_engine.py` pipeline.

### 7. New paper structure

| § | Title | Content |
|---|-------|---------|
| 1 | Introduction | Story intro (above) |
| 2 | Literature Review | Refine later · recruitment systems, AI agents in hiring, semantic search, gaps |
| 3 | Architecture of the Multi-Agent System | 3.1 Candidate Agent, 3.2 Employer Agent, 3.3 Matchmaking Agent, 3.4 Agent Communication & State Sharing, 3.5 Overall Workflow |
| 4 | Implementation | libraries, APIs, data structures, parameters, backend/UI details |
| 5 | Quality Metrics | formulas, P/R/nDCG, similarity, ranking criteria |
| 6 | Results and Discussion | tables, graphs, benchmarks, interpretation |
| 7 | Conclusion and Future Scope | |

**Move out of intro/architecture:** APIs, frameworks, parameters → §4. Formulas and metric definitions → §5.

### 8. Literature review (deferred refinement)

Connect prior work to: recruitment systems; AI agents in hiring; semantic search/embeddings; limitations; gap this work fills. Current §2 flagged as weak · revisit after structure lock.

### 9. Preserved from current system (do not lose in rewrite)

- Table 9/10 numbers and dual eval protocols (`paper_progression`, `phase11`)
- Soft embed @ w=0.7 as best exhaustive result (nDCG 0.969)
- Honest bootstrap CI (not significant)
- Paper↔code gaps to resolve or reframe: LLM rerank described but not built; API lacks `skills_mode`; RRF list mismatch; match routes exhaustive not ANN-first

### 10. Edit cascade when rewrite lands

**Landed 2026-05-27.** Renamed `section-*-*.tex` (7 files), abstract/keywords in `main.tex`, portal PDFs, `build_all.sh`, supplementary SI. Still open: author block, `\todo` cleanup, Fig1/Fig4 re-export, sync cover letter if § titles change again.

---

## JAAMAS Manuscript · Complete Architecture Reference

> **Active manuscript (v2, May 2026):** Seven-section multi-agent restructure. **Compiled ~33 pages (local).** Legacy 9-section / 31-page map retained below for table-number and benchmark cross-reference only.

### Paper identity (current)

| Field | Value |
|-------|-------|
| Title | JobMatch: An Agentic Multi-Role Platform for Explainable Job--Candidate Matching |
| Journal | Journal of Autonomous Agents and Multi-Agent Systems (JAAMAS) |
| Type | Original research article |
| Compiled PDF | `docs/submission/jaamas/manuscript/main.pdf` (~33 pp. local) · copy: `build/jaamas-manuscript.pdf` |
| LaTeX entry | `docs/submission/jaamas/manuscript/main.tex` |
| Engine | **pdfLaTeX** + BibTeX (`sn-mathphys-num.bst`) |
| Class | `sn-jnl.cls` · `\documentclass[pdflatex,sn-mathphys-num]{sn-jnl}` |
| Git commits | `cfae2c2` (source v1), `3631bcb` (portal/build) · **local §2–§7 rewrite uncommitted** |

### Manuscript directory tree (current)

```
docs/submission/jaamas/
├── manuscript/
│   ├── main.tex
│   ├── jaamas-style.tex, jaamas-macros.tex
│   ├── references.bib (7 entries)
│   ├── sn-jnl.cls, sn-mathphys-num.bst, vendored *.sty
│   ├── sections/
│   │   ├── section-1-introduction.tex
│   │   ├── section-2-literature-review.tex
│   │   ├── section-3-architecture.tex
│   │   ├── section-4-implementation.tex
│   │   ├── section-5-quality-metrics.tex
│   │   ├── section-6-results-discussion.tex
│   │   ├── section-7-conclusion-future.tex
│   │   └── declarations.tex
│   ├── algorithms/ alg-multi-agent-matching.tex (Algorithm 1 · 15 steps)
│   └── tables/ tab-*.tex (10 tables from benchmark artifacts)
├── figures/ Fig1.pdf … Fig5.pdf + source/*.drawio, *.mmd
├── supplementary/ supplementary-information.{tex,pdf}
├── portal/ cover-letter + information-sheet (md/tex/pdf)
├── build/ jaamas-manuscript.pdf, jaamas-overleaf-upload.zip
├── build_all.sh
└── figures/README.md
```

### How compilation works (current)

```
main.tex
  ├── \input{jaamas-macros} + jaamas-style
  ├── abstract + keywords (inline)
  ├── \input{sections/section-1-introduction} … section-7-conclusion-future
  ├── \input{sections/declarations}
  └── \bibliography{references}
```

**Build:** `bash docs/submission/jaamas/build_all.sh` → manuscript PDF, portal PDFs, supplementary SI, Overleaf zip via `archive/dev-scripts/make_overleaf_zip.sh`.

**Figure generation:** `python scripts/generate_jaamas_figures.py` → draw.io sources in `figures/source/` · export PDF **without `--crop`** (crop produced ~47 pt tall PDFs).

### PDF document map (current · ~33 pages local)

| § | Source file | Title / content (v12 local) |
|---|-------------|------------------------------|
| 1 | `section-1-introduction.tex` | Introduction — story arc, Sal Khan, 6 contributions, no subsections |
| 2 | `section-2-literature-review.tex` | Literature Review — 6 themes + gaps + positioning; **12 citation TODOs** |
| 3 | `section-3-architecture.tex` | Multi-agent architecture — 3 agents, §3.4 state sharing, Algorithm 1, Figs 1–3 |
| 4 | `section-4-implementation.tex` | Implementation — gateway, agents, stores, portals, params, reproducibility, Fig 4 |
| 5 | `section-5-quality-metrics.tex` | Quality Metrics — matching scores + P/R/nDCG/MRR/MAP formulas only, Fig 5 |
| 6 | `section-6-results-discussion.tex` | Results — narrative interpretation; 8 tables; human-audience structure |
| 7 | `section-7-conclusion-future.tex` | Conclusion + Future Scope — decision-support; 8 future items |

**Key committed metrics (K=5, demo corpus):** soft-embed nDCG@5 **0.969**, learned fusion **0.968**, composite ablation **0.942** (research weights 40/30/15/10/5), TF–IDF **0.905**, BM25 **0.901**, P@5 ~**0.31** at best configs, cross-encoder ΔnDCG **−0.108** @ ~141.7 ms/query.

### Professor QA summary (2026-05-27)

| Criterion | Result |
|-----------|--------|
| Less like technical report | PARTIAL — §4–§5 still dense |
| Intro no subsections / story-first | PASS |
| §3 multi-agent + Fig1 + Algorithm 1 | PASS (Fig1 after brief intro para) |
| Formulas in §5, implementation in §4 | PASS |
| §6 readable + interpreted | PASS |
| Literature review strength | PARTIAL content / **FAIL citations** (7 bib, 12 TODOs) |
| Consistent multi-agent framing | PARTIAL — “matchmaking engine” in §1 contrib |

### Security review summary (2026-05-27 · `/review` · no fixes applied)

| Severity | Issue |
|----------|-------|
| Critical | Open `admin` self-registration (`/auth/register`); unauthenticated `/match/*` exposes candidate PII (email/phone) |
| Critical | Unauthenticated `GET /candidates/full`, `/candidates/{name}`, `/jobs/full` |
| High | Unauthenticated `POST /system/vector-store`, `POST /match/daily-batch` (path traversal on `output_path`) |
| High | Unauthenticated corpus pollution via `POST /candidates`, `POST /jobs` |
| Medium | Demo passwords in `GET /system/config`; default `session_secret=dev-change-me` |
| Tests | `test_register_admin`, `test_match_*` assert insecure behavior — auth hardening needs test rewrites |

**Deployment rule:** localhost/demo only until auth + PII redaction land. Documented intentionally in §4 for admin console access.

---

### [LEGACY] Pre-restructure manuscript reference (9 sections · 31 pages)

> The following documents the **old** draft (`section-1.tex` … `section-9.tex`). Use only for historical table/figure numbering and migration notes.

### Paper identity (legacy)

| Field | Value |
|-------|-------|
| Title | Agentic Job Matching: A Semantic Retrieval System for Resume-to-Job Alignment |
| Compiled PDF | `Agentic Job Matching.pdf` (31 pages) · **removed** |
| Build marker | `2026-05-17-page-rhythm-v7` |
| Engine | pdfLaTeX + `sn-mathphys.bst` |

### Manuscript directory tree

```
docs/submission/jaamas/
├── manuscript/                    ← PRIMARY LaTeX source
│   ├── main.tex                   ← compile this (not preamble alone)
│   ├── jaamas-style.tex           ← tables, floats, page rhythm
│   ├── jaamas-macros.tex          ← \modelname, \pAt, \figcap, \onres
│   ├── author-emails.tex          ← affiliation + contact list
│   ├── acknowledgments.tex
│   ├── declarations.tex           ← Springer Declarations block
│   ├── references.bib             ← 7 BibTeX entries
│   ├── sn-jnl.cls, sn-mathphys.bst
│   ├── sections/
│   │   ├── section-1.tex … section-9.tex
│   │   └── appendix-recommendations.tex
│   └── Agentic Job Matching.pdf   ← compiled output (local)
├── figures/                       ← Fig1.pdf … Fig10.pdf (referenced from §3)
├── supplementary/                 ← SI PDF + CSV/JSON for replication
│   ├── si-main.tex, si-appendix.tex
│   ├── paper_progression_summary.json
│   ├── paper_bootstrap_significance.json
│   └── phase11_*.csv
├── portal/                        ← cover letter + information sheet (separate build)
├── build/jaamas-overleaf-upload.zip
├── OVERLEAF.md                      ← compile troubleshooting
└── archive/dev-scripts/           ← build.sh, make_overleaf_zip.sh, polish scripts
```

### How compilation works

```
main.tex
  ├── \input{jaamas-style}      % packages, JTable/JFigure/JSchemaTable envs
  ├── \input{jaamas-macros}     % metric macros, figure refs
  ├── \input{author-emails}     % \AffilInstitution, email list
  ├── \maketitle + abstract + keywords (inline in main.tex)
  ├── \input{sections/section-1} … section-9
  ├── \appendix
  │     └── \input{sections/appendix-recommendations}
  ├── \backmatter
  │     ├── Supplementary information (inline paragraph)
  │     ├── \input{acknowledgments}
  │     └── \input{declarations}
  └── \bibliography{references}
```

**Build chain:** `pdflatex main → bibtex main → pdflatex main → pdflatex main`

**Overleaf settings:** Compiler pdfLaTeX; Bibliography BibTeX; Main document `manuscript/main.tex`. Delete any `output.pdf` in project or Overleaf will not emit PDF.

**Separate builds (do not confuse):**
| Build | Entry | Engine | Output |
|-------|-------|--------|--------|
| JAAMAS submission | `manuscript/main.tex` | pdfLaTeX + sn-jnl | Submission PDF |
| Technical report | `docs/latex/main.tex` | XeLaTeX | `docs/report/Agentic Job Matching.pdf` |
| Preprint (coloured) | `archive/preprint/main-preprint.tex` | XeLaTeX | Internal only |
| Supplementary SI | `supplementary/si-main.tex` | pdfLaTeX article | Online Resources 1–3 |
| Portal | `portal/cover-letter.tex`, `information-sheet.tex` | via build scripts | Portal PDFs |

**Regeneration path (legacy):** `archive/dev-scripts/prepare_manuscript.py` once copied content from `docs/latex/body.tex`. **Current practice:** edit `sections/*.tex` directly; do not run `build_from_md.py` into manuscript folder.

### LaTeX infrastructure (custom environments)

| Macro / env | File | Purpose |
|-------------|------|---------|
| `JSchemaTable` | jaamas-style.tex | Non-floating schema tables (entity fields, encoding templates) · full `\textwidth` |
| `JTable` | jaamas-style.tex | Float table `[!t]`, top-aligned, booktabs |
| `JFigure` | jaamas-style.tex | Float figure `[!t]` with `\JFig{../figures/FigN.pdf}` |
| `\figcap{n}{text}` | jaamas-macros.tex | Caption text only · class adds “Fig. n” |
| `\figref{fig:N}` | jaamas-macros.tex | “Fig.~\ref{…}” |
| `\topic{…}` / `\topicblock{…}` | jaamas-macros.tex | Inline topic labels (Methodology §4) |
| `\modelname` | jaamas-macros.tex | `\texttt{all-MiniLM-L6-v2}` |
| `\pAt{K}`, `\rAt{K}`, `\ndcgAt{K}` | jaamas-macros.tex | Metric notation |
| `\onres{n}` | jaamas-macros.tex | “Online Resource n” |
| `\JBackmatterRule` | jaamas-style.tex | Thin rule before back matter |

**Page rhythm fixes (v7):** `\raggedbottom`, tighter `\titlespacing`, no `\FloatBarrier` before every section, float pages top-aligned, `\parskip` 0.2em · fixes uneven vertical centering on Overleaf.

### PDF document map (31 pages)

| PDF pages | LaTeX source | Section title | Role |
|-----------|--------------|---------------|------|
| 1 | main.tex | Title, abstract, keywords | Headline metrics: soft embed nDCG 0.969, bootstrap CI, ANN 0.913 |
| 2–3 | section-1.tex | §1 Introduction | Problem, motivation, contributions, **JAAMAS agentic framing** (`sec:agentic`) |
| 3–6 | section-2.tex | §2 Literature Review | DPR, SBERT, HNSW, RRF, nDCG, cross-encoder, LLM rerank, soft skills gap |
| 6–12 | section-3.tex | §3 System Architecture | **Figs 1–7** · layered architecture narrative |
| 12–17 | section-4.tex | §4 Methodology | **Algebra** · entities, templates, formulas, stores (implementation-independent) |
| 17–20 | section-5.tex | §5 Architectural realization | FastAPI, **Table 6** (14 endpoints), **Table 7**, frontend, sync, daily batch |
| 20–23 | section-6.tex | §6 Evaluation Framework | Labels, metrics formulas, 40-config sweep, dual drivers |
| 23–27 | section-7.tex | §7 Results and Discussion | **Tables 8–11**, ablation, tradeoffs, cross-encoder |
| 27–28 | section-8.tex | §8 Conclusion | Limits + practitioner/agent community takeaways |
| 28–29 | section-9.tex | §9 Future Work | LLM agent orchestration, preferences, scale, dataset, taxonomy |
| 29 | appendix-recommendations.tex | Appendix A Recommendation Summary | 5 production bullets |
| 29–30 | main.tex + declarations | Supplementary info, Acknowledgments, Declarations | GitHub, data/code availability |
| 30–31 | references.bib | References | 7 citations |

### Section-by-section content (what each file owns)

#### §1 Introduction · `sections/section-1.tex` (`\label{sec:1}`)

| Subsection | Label | Content |
|------------|-------|---------|
| (opening) | · | Hiring mismatch; lexical vs semantic failure modes |
| Problem Statement | · | Lexical alignment + structured fit |
| Motivation | · | Bi-encoder + ANN; Jaccard blend; RRF |
| Our contributions | · | 6-item bullet list → maps to entire system |
| Agentic workflows and JAAMAS relevance | `sec:agentic` | Daily recs, live sync, ensemble as **agent patterns**; modular failure diagnosis |

**Code mapping:** `app.py` batch endpoints, `real_jobs_sync.py`, ensemble routes.  
**Forward refs:** Table `tab:progression-k5`, `tab:results-k5`; Sections `sec:6`, `sec:7`.

#### §2 Literature Review · `sections/section-2.tex` (`\label{sec:2}`)

| Subsection | Key citations | Ties to implementation |
|------------|---------------|------------------------|
| Semantic Search with Dense Embeddings | karpukhin2020dpr, reimers2019sbert | `matching/embedding.py`, all-MiniLM-L6-v2 |
| ANN Retrieval | malkov2018hnsw | `stores/chroma`, `stores/qdrant` |
| Hybrid Scoring and Rank Fusion | cormack2009rrf | `similarity_engine.py`, `app.rrf_aggregate` |
| IR Evaluation | · | `benchmarks/metrics.py` |
| LLM-based Reranking | nogueira2019bert, sun2023chatgptsearch | `cross_encoder_rerank.py`, Ollama LLM path |
| Soft Skill Matching | · | `matching/soft_skills.py` · paper’s main novelty argument |

#### §3 System Architecture · `sections/section-3.tex` (`\label{sec:3}`)

**Narrative arc:** presentation → orchestration → scoring → persistence → optional rerank/benchmark.

| Subsection | Figure | PDF file | Describes |
|------------|--------|----------|-----------|
| High-level modules | Fig. 1 | `figures/Fig1.pdf` | Module graph + info flow |
| Presentation layer | Fig. 2 | `Fig2.pdf` | React SPA, localStorage, HTTP boundary |
| Application layer | Fig. 3 | `Fig3.pdf` | FastAPI surfaces |
| Matching core | Fig. 4 | `Fig4.pdf` | Embedder, semantic + Jaccard + soft branch |
| Data plane | Fig. 5 | `Fig5.pdf` | Ingestion, Chroma/Qdrant, live jobs |
| Optional rerank + offline eval | Fig. 6 | `Fig6.pdf` | Ollama + benchmark module |
| Full module diagram | Fig. 7 | `Fig7.pdf` | End-to-end with legend + numbered walkthrough |

**Figure labels:** `fig:1` … `fig:7`.  
**Supplementary:** Online Resources 1–3 (`supplementary/si-appendix.tex`) · ingestion, query, offline eval **flow diagrams** (not in main PDF body).

#### §4 Methodology · `sections/section-4.tex` (`\label{sec:4}`)

**Critical for architecture migration:** This section is written as **re-implementable algebra**, not file paths.

| Subsection | Tables | Key formulas / specs |
|------------|--------|----------------------|
| Data Representation | `tab:1` resume fields, `tab:2` job fields, `tab:3` eval pair | Pydantic schemas in `schemas.py` |
| Embedding Strategy | `tab:resume-template`, `tab:job-template` | **`document_text.py`** line order is normative |
| Similarity Metrics | · | Cosine, Euclidean-derived |
| Matching Strategies | · | Semantic; Multimodal \(s = \alpha s_{sem} + (1-\alpha) J\); RRF \(k=60\) |
| Soft skill + LLM rerank | · | \(s_{soft}\) formula; LLM blend \(\alpha_r=0.4\), score map \((z-1)/4\) |
| Vector Store Design | · | Chroma vs Qdrant HNSW params |

**Default hyperparameters cited in paper:** multimodal \(\alpha=0.7\); RRF \(k=60\); four-list ensemble (semantic×cosine, semantic×Euclidean, multimodal×cosine, multimodal×Euclidean).

#### §5 Architectural realization · `sections/section-5.tex` (`\label{sec:5}`)

| Subsection | Tables | Code anchor |
|------------|--------|-------------|
| Backend orchestration | `tab:api-endpoints` (Table 6 in PDF) | `backend/app.py` · all 14 routes |
| | `tab:optional-components` (Table 7) | soft_skills, LLM rerank, Ollama gateway |
| Frontend | · | `frontend/src/App.jsx` · **see paper vs UI gaps** |
| Real-time job integration | · | `real_jobs_sync.py`, `data/jobs_live.json` |
| Daily recommendation batch | · | ANN pool default **120**, dated JSON output |

**Startup sequence (paper):** factory → load JSON → optional live snapshot → ingestion/reindex.

#### §6 Evaluation Framework · `sections/section-6.tex` (`\label{sec:6}`)

| Subsection | Content |
|------------|---------|
| Ground Truth Labels | 30 resumes, 15 jobs, 47 pairs; rel 0/1/2; `eval_pairs.json` |
| Metrics | P@K, R@K, nDCG@K formulas; latency = ANN search only |
| Parameter Sweep Methodology | **40 configurations** · stores × metrics × weights × HNSW |
| Experimental design notes | Lexical baselines, pool size, paper_progression driver |

**Dual evaluation protocols (central to all claims):**

| Protocol | Driver | Retrieval | Purpose in paper |
|----------|--------|-----------|------------------|
| **Exhaustive progression** | `benchmarks.paper_progression` | Score all 15 jobs per query | Table 9 (`tab:progression-k5`) · method ladder, bootstrap |
| **ANN store sweep** | `benchmarks.phase11` | Pool size **10**, then rerank | Table 10 (`tab:results-k5`) · latency, backend parity |

#### §7 Results and Discussion · `sections/section-7.tex` (`\label{sec:7}`)

| PDF Table | LaTeX label | Source file | Content |
|-----------|-------------|-------------|---------|
| Table 8 | `tab:strategy-qual` | section-7.tex | Qualitative strategy behaviors |
| Table 9 | `tab:progression-k5` | section-7.tex | **BM25 → soft embed** numeric ladder |
| Table 10 | `tab:results-k5` | section-7.tex | Chroma/Qdrant ANN excerpt + latency |
| Table 11 | `tab:vector-stores` | section-7.tex | Store characteristics |

| Subsection | Label | Notes |
|------------|-------|-------|
| Matching Strategy Comparison | · | Tables 8–10 |
| Ablation reading | `sec:ablation` | How to read Table 10 rows |
| Vector Store Comparison | · | Table 11 |
| Tradeoffs | · | Pool size, Jaccard vs soft, RRF vs learned, in-memory limits |
| Optional stages | · | Cross-encoder 0.939; LLM not tabulated |

#### §8 Conclusion · `sections/section-8.tex` (`\label{sec:8}`)

Restates headline numbers, limits (small n, inflated lexical R@5, no LLM metrics), practitioner decomposition (representation / retrieval / fusion), agents contribution (tool-using workflows).

#### §9 Future Work · `sections/section-9.tex` (`\label{sec:9}`)

| Subsection | Migration relevance |
|------------|---------------------|
| Agentic Orchestration | LLM picks strategy · **opposite of current explicit controls** |
| Candidate Preference Modeling | Interaction feedback embeddings |
| Scalability | ANN-first serving, decoupled ingestion, cron agent, GPU LLM |
| Evaluation Dataset Expansion | Crowd, clickthrough, synthetic labels |
| Skill Taxonomy Integration | ESCO/O*NET vs current soft embed |

#### Appendix · `sections/appendix-recommendations.tex` (`\label{sec:appendix-recommendations}`)

Five operational recommendations · **preserve as checklist** when redesigning architecture.

### Complete label / cross-reference index

**Sections:** `sec:1` … `sec:9`, `sec:agentic`, `sec:ablation`, `sec:appendix-recommendations`

**Figures:** `fig:1` … `fig:7`

**Tables:** `tab:1`, `tab:2`, `tab:3`, `tab:resume-template`, `tab:job-template`, `tab:api-endpoints`, `tab:optional-components`, `tab:strategy-qual`, `tab:progression-k5`, `tab:results-k5`, `tab:vector-stores`

**Typical citation flow:** §1 cites Tables 9–10 by forward ref → §4 defines entities → §5 maps to HTTP → §6 defines protocols → §7 fills tables → §8 summarizes → Appendix operationalizes §7.

### Bibliography (`references.bib` · 7 entries)

| Key | Topic |
|-----|-------|
| karpukhin2020dpr | Dense passage retrieval |
| reimers2019sbert | Sentence-BERT |
| malkov2018hnsw | HNSW ANN |
| cormack2009rrf | Reciprocal rank fusion |
| nogueira2019bert | Cross-encoder reranking |
| sun2023chatgptsearch | LLM reranking / agent framing |
| wang2020minilm | MiniLM (encoder lineage) |

### Supplementary materials package

| Artifact | Role |
|----------|------|
| `supplementary/si-main.tex` | Standalone SI document |
| `si-appendix.tex` | Online Resources 1–3 diagrams |
| `paper_progression_summary.json` | Table 9 numbers (source of truth) |
| `paper_bootstrap_significance.json` | Bootstrap CI for soft vs semantic |
| `phase11_summary.csv`, `phase11_per_query.csv` | Table 10 full 40-config sweep |
| `lexical_summary.csv` | Lexical baseline rows |
| `eval_pairs_README.md` | Labeling protocol notes |

Main PDF back matter points readers to these files; they ship with submission zip.

### Portal documents (not part of manuscript PDF)

| File | Pages | Audience |
|------|-------|----------|
| `portal/cover-letter.pdf` | 1 | Editor · JAAMAS fit, headline metrics, no prior publication |
| `portal/information-sheet.pdf` | 3 | Springer mandatory Q&A · claims, evidence tables, related work list |

Sources: `cover-letter.tex/.md`, `information-sheet.tex/.md`. Keep emails in sync with `author-emails.tex`.

### Paper claims ↔ code traceability matrix

| Paper claim | Evidence location | Regenerate command |
|-------------|-------------------|-------------------|
| Soft embed nDCG@5 0.969 | Table 9 / `paper_progression_summary.json` | `python -m benchmarks.paper_progression` |
| Semantic nDCG@5 0.911 | same | same |
| Bootstrap CI [−0.013, +0.146] | `paper_bootstrap_significance.json` | same |
| ANN Jaccard nDCG 0.913 vs semantic 0.884 | Table 10 / `phase11_summary.csv` | `python -m benchmarks.phase11` |
| Qdrant 0.38 ms vs Chroma 0.81 ms | Table 10 | same |
| 14 HTTP endpoints | Table 6 / `tests/test_api.py` | pytest |
| Encoding templates | Tables resume/job template | `matching/document_text.py` |
| RRF k=60 | §4 formula | `app.rrf_aggregate`, `research_sweep.rrf_fuse` |

### Architecture migration · what to preserve vs revisit

**Preserve (evaluation contract):**
- Graded labels in `eval_pairs.json` and rel 0/1/2 semantics
- Dual protocols: exhaustive progression + ANN phase11
- Table 9/10 numbers or explicitly re-run and update all TeX + portal + README
- Encoding template **line order** if comparing to published baseline
- Bootstrap reporting for any headline soft-embed claim

**Likely to change (paper already flags as future work):**
- In-memory full-corpus scoring → ANN-first serving (§9.3)
- Manual strategy selection → LLM agent orchestration (§9.1)
- Monolithic FastAPI process state → decoupled ingestion/serving
- Single React `App.jsx` → new frontend architecture
- String skills → taxonomy (§9.5)

**Update cascade if architecture changes:** `sections/section-3.tex`, `section-5.tex`, figures Fig1–7, `README.md`, `portal/information-sheet`, supplementary JSON/CSV, then recompile PDF + Overleaf zip.

### Narrative structure (argument the paper makes)

```
Problem: lexical mismatch + narrative match without skills
    ↓
Approach: structured text → bi-encoder → ANN index → semantic | multimodal | RRF
    ↓
Agentic layer: HTTP/batch workflows (daily recs, sync, ensemble) without per-step manual ops
    ↓
Evidence: graded n=30 benchmark, two protocols, honest limits (bootstrap n.s., small corpus)
    ↓
Contribution to JAAMAS: tool-using, traceable stages · not autonomous LLM policy selection (yet)
```

---

## Manuscript deep-dive (paragraph-level)

### Front matter (`main.tex` lines 28–46)

**Title (short):** Agentic Job Matching  
**Full title:** Agentic Job Matching: A Semantic Retrieval System for Resume-to-Job Alignment

**Authors:** Harsh Kashyap* (corresponding), Taranumpreet Kaur Wasu · affiliation block from `\AffilInstitution` + bullet email list.

**Abstract (3 paragraphs):**
1. Problem framing · lexical failure; semantic alone misses structured constraints unless stages measured separately.
2. System summary · `\modelname`, Chroma/Qdrant, semantic / multimodal Jaccard / RRF, batch + HTTP workflows.
3. Numbers · 30 queries, 47 pairs, K=5; soft embed nDCG 0.969, R@5 1.000 vs semantic 0.911/0.900; bootstrap CI; ANN sweep 0.913 vs 0.884; Qdrant latency half of Chroma.

**Keywords:** resume–job matching, semantic retrieval, vector databases, software agents, reciprocal rank fusion, reproducible evaluation

---

### §1 Introduction · `section-1.tex` (42 lines, PDF pp. 2–3)

| Block | Lines | Content summary |
|-------|-------|-----------------|
| Opening | 4–4 | Hiring mismatch; lexical search; whole-doc similarity misses skills |
| §1.1 Problem Statement | 7–11 | Lexical alignment obstacle; structured fit obstacle; objective = semantic + skill overlap |
| §1.2 Motivation | 14–18 | Bi-encoder + ANN; Jaccard blend; RRF when multiple runs exist |
| §1.3 Our contributions | 21–34 | 6 bullets: pipeline, strategies, stores, refinements (soft/cross/LLM), app layer (14 endpoints), evaluation |
| §1.4 Agentic + JAAMAS | 36–41 | Daily recs, live sync, ensemble as agent patterns; cite `sun2023chatgptsearch`; failure traceability |

**Key forward references:** `tab:progression-k5`, `tab:results-k5`, `sec:6`, `sec:7`, `sec:agentic`

---

### §2 Literature Review · `section-2.tex` (69 lines, PDF pp. 3–6)

| §2.x | Topic | Citations | Implementation hook |
|------|-------|-----------|---------------------|
| 2.1 | Dense embeddings / DPR / SBERT | karpukhin2020dpr, reimers2019sbert, wang2020minilm | `embedding.py`, 384-d MiniLM |
| 2.2 | ANN / HNSW / Chroma / Qdrant | malkov2018hnsw | `stores/vector_store.py`, `qdrant_vector_store.py` |
| 2.3 | Hybrid scoring + RRF | cormack2009rrf | `similarity_engine.py`, `app.rrf_aggregate` |
| 2.4 | P@K, R@K, nDCG@K | · | `benchmarks/metrics.py` |
| 2.5 | Cross-encoder + LLM rerank | nogueira2019bert, sun2023chatgptsearch | `cross_encoder_rerank.py`; **LLM path described in paper only** |
| 2.6 | Soft skill gap in prior work | · | Motivates `soft_skills.py`; diagnosis of expected vs observed rankings |

**Literature stack narrative:** embed → ANN retrieve → hybrid score → evaluate → optional rerank.

---

### §3 System Architecture · `section-3.tex` (120 lines, PDF pp. 6–12)

**Opening thesis:** Four layers · presentation, orchestration, scoring, persistence · connected by HTTP, vector abstraction, shared encoder.

| §3.x | Layer | Figure | What the figure shows |
|------|-------|--------|----------------------|
| 3.1 | High-level modules | Fig. 1 (`fig:1`) | Client → API → scoring → storage; dashed = optional rerank / offline |
| 3.2 | Presentation | Fig. 2 (`fig:2`) | React SPA, local persistence, HTTP boundary |
| 3.3 | Application | Fig. 3 (`fig:3`) | FastAPI route groups: match, ensemble, catalog, sync, batch |
| 3.4 | Matching core | Fig. 4 (`fig:4`) | Shared embedder; semantic channel; Jaccard; dashed soft-skill branch |
| 3.5 | Data plane | Fig. 5 (`fig:5`) | JSON corpora, ingestion, Chroma/Qdrant factory, live job sync |
| 3.6 | Optional paths | Fig. 6 (`fig:6`) | Ollama LLM rerank + offline benchmark outputs |
| 3.7 | Consolidated | Fig. 7 (`fig:7`) | Full end-to-end with numbered walkthrough |

**Fig. 7 walkthrough (paper steps 1–6):**
1. User selects direction, strategy, metric, skill mode, rerank flag → client POST.
2. Handler queries vector store (step 5) for ANN pool or uses in-memory full scan (current `app.py` match endpoints score **all** jobs).
3. Scoring core (step 3): semantic-only OR multimodal (Jaccard default; soft branch if selected).
4. Optional LLM rerank (step 4) blends model score · **not wired in current `app.py`**.
5. Ensemble: multiple full scoring passes → RRF in handler (step 2).
6. Offline benchmark (step 6): same indexes + labels, no HTTP.

**Supplementary figures (not in main body):**
| OR | File | Content |
|----|------|---------|
| Online Resource 1 | `Fig8.pdf` | Ingestion: validate → template → embed → upsert |
| Online Resource 2 | `Fig9.pdf` | Query: embed → ANN pool → score → optional RRF → optional LLM |
| Online Resource 3 | `Fig10.pdf` | Offline eval loop per configuration |

Figure assets: symlinks from `docs/submission/jaamas/figures/FigN.pdf` → `docs/latex/figures/figNN.pdf`. Regenerate: `bash archive/dev-scripts/export_figures.sh`.

---

### §4 Methodology · `section-4.tex` (222 lines, PDF pp. 12–17)

#### §4.1 Data representation

**Resume fields (`tab:1`):** id, name, skills[], experience_years, preferred_salary, remote_preference, summary  
**Job fields (`tab:2`):** id, title, required_skills[], required_experience, budget, remote_policy, description + optional company, location, job_type, link  
**Eval pair (`tab:3`):** query_id, doc_id, relevance ∈ {0,1,2} (−1 excluded)

**Pydantic models:** `backend/schemas.py` · Resume, Job (note: optional job fields may exist in JSON beyond strict schema).

#### §4.2 Embedding strategy

**Model:** `all-MiniLM-L6-v2` · 384-d, CPU-friendly, sentence-transformers.

**Resume encoding template (normative · matches `document_text.py` default):**
```
resume profile
name: {name}
experience_years: {years}
work_mode: remote|onsite
skills: {sorted, deduplicated, lowercased, catalog-normalized}
summary: {text}
```

**Job encoding template:**
```
job description
title: {title}
company: {company}
location: {location}
job_type: {job_type}
required_experience_years: {years}
work_mode: remote|onsite
required_skills: {sorted skill list}
description: {text}
apply_link: {url}
```

**Rich template variant** (`BENCHMARK_RICH_TEMPLATES=1`): longer natural-language headers; tested in progression as separate row (nDCG 0.922).

**Skill normalization:** `skill_catalog.py` · 40+ alias entries (react.js→react, k8s→kubernetes, ml→machine learning, etc.) before Jaccard/soft overlap.

#### §4.3 Similarity metrics

| Metric | Formula | Code |
|--------|---------|------|
| Cosine | \(s_{\cos} = \frac{a^\top b}{\|a\|_2 \|b\|_2}\) | `semantic_similarity.py` |
| Euclidean-derived | \(s_{\text{euc}} = 1/(1+\|a-b\|_2)\) | same |

#### §4.4 Matching strategies

| Strategy | Formula | Default params |
|----------|---------|----------------|
| Semantic | `final = s_sem` | metric=cosine |
| Multimodal (Jaccard) | `final = α·s_sem + (1−α)·J(A,B)` | α=0.7 |
| Multimodal (soft) | `final = α·s_sem + (1−α)·s_soft` | α=0.7, skills_mode=embedding |
| RRF | `s_RRF(d) = Σ w_i / (k + rank_i(d))` | k=60, w_i=1.0 default |

**Soft overlap formula (paper §4.4.1):**
\[
s_{\text{soft}}(R,J) = \frac{1}{|J|}\sum_{j\in J}\max_{r\in R}\cos(e(r),e(j))
\]
Implementation: `soft_skills.py` · per-skill embedding cache, mean of max cosines.

**LLM rerank formula (paper):** `s_final = α_r·s_ret + (1−α_r)·s_llm`, α_r=0.4, z∈{1..5} → `(z-1)/4`. **No Ollama/LLM module in current backend tree.**

#### §4.5 Vector store design

| Backend | Persist path | Key config |
|---------|--------------|------------|
| Chroma | `backend/chroma_db/` | `CHROMA_SPACE` cosine/l2 at collection create |
| Qdrant | `backend/qdrant_db/` | UUID5 ids; `QDRANT_HNSW_EF`, `_M`, `_EF_CONSTRUCT`, collection suffix |

---

### §5 Architectural realization · `section-5.tex` (108 lines, PDF pp. 17–20)

#### Startup sequence (paper)
1. `get_vector_store()` → Chroma default  
2. Load + validate `cvs.json`, `jobs.json`  
3. Optional `jobs_live.json` snapshot replaces static jobs  
4. `ingest_data()` embed + upsert all entities  

#### Table 6 · 14 HTTP endpoints (full API spec)

| # | Method | Path | Request body | Response | Scoring behavior |
|---|--------|------|--------------|----------|------------------|
| 1 | POST | `/match-resume` | `{name, top_k, strategy, metric}` | ranked jobs[] | **Exhaustive:** scores every job in memory |
| 2 | POST | `/match-job` | `{title, top_k, strategy, metric}` | ranked resumes[] | Exhaustive all resumes |
| 3 | POST | `/match-resume-ensemble` | `{name, top_k, searches[]}` | RRF fused jobs[] | One exhaustive run per search config |
| 4 | POST | `/match-job-ensemble` | `{title, top_k, searches[]}` | RRF fused resumes[] | Same |
| 5 | POST | `/candidate/daily-recommendations` | `{name, top_k, strategy, metric, candidate_pool=120}` | `{results[], why_ranked[]}` | ANN pool then score |
| 6 | POST | `/agent/run-daily-recommendations` | `{top_k, strategy, metric, sync_before_run, candidate_pool, max_users}` | `{output_file, users_processed}` | Batch all resumes → JSON file |
| 7 | GET | `/resumes` | · | name[] | |
| 8 | GET | `/resumes/full` | · | Resume[] | |
| 9 | GET | `/jobs` | · | title[] | |
| 10 | GET | `/jobs/full` | · | Job[] | |
| 11 | GET | `/real-jobs/status` | · | sync config + state | |
| 12 | POST | `/real-jobs/sync` | `{reindex=true}` | sync stats | Fetch external API, optional reindex |
| 13 | GET | `/system-config` | · | stores, strategies, metrics | |
| 14 | POST | `/system-config/vector-store` | `{vector_store}` | switch + reindex | |

**Request model defaults (`app.py`):** strategy=`semantic`, metric=`cosine`, top_k=5, candidate_pool=120, RRF k=60.

**Response fields (match):** job_title/candidate_name, semantic_score, skills_score, similarity, metric_used, strategy_used, vector_store_used, rank.

**Explainability (`_build_why_ranked`):** skill overlap bullets; title/summary token overlap; semantic band (≥0.65 high, ≥0.5 moderate); multimodal blend note.

#### §5.2 Frontend (paper claims vs code)

| Paper feature | Frontend (`App.jsx`) | Backend |
|---------------|---------------------|---------|
| Dual-mode match | yes mode toggle | yes |
| Strategy/metric dropdowns | yes from `/system-config` | yes |
| Ensemble (4 configs) | yes all strategy×metric combos selected by default; weight=1 | yes |
| Skills mode Jaccard/soft | no not exposed | yes via `compute_multimodal(..., skills_mode)` but **API uses default jaccard only** |
| LLM rerank toggle | no | no not implemented |
| Live sync + daily agent | yes buttons | yes |
| Score normalization UI | yes maps scores to [0,1] if clustered low | · |

#### §5.3 Real-time jobs
- `real_jobs_sync.py`: paginated HTTP, dedupe by id, `data/jobs_live.json`
- Env: `REAL_JOBS_ENABLE`, `REAL_JOBS_BASE_URL`, `REAL_JOBS_PATH`, limit, timeout

#### §5.4 Daily batch
- ANN pool default **120** → score → top-K → `why_ranked`
- Output: `data/daily_recommendations_YYYY-MM-DD.json`

---

### §6 Evaluation · `section-6.tex` (97 lines, PDF pp. 20–23)

#### Ground truth statistics (measured from `data/eval_pairs.json`)

| Stat | Value |
|------|-------|
| Resumes (queries) | 30 |
| Jobs (corpus) | 15 |
| Labeled pairs | 47 |
| Relevance 2 (strong) | 21 |
| Relevance 1 (partial) | 26 |
| Relevant docs per query | min 1, max 2, mean **1.57** |
| Unjudged (rel −1) | excluded |

**Implication:** R@5 often high on small corpus because each query has at most ~2 relevant jobs out of 15; exhaustive scoring inflates lexical R@5 to ~0.983.

#### Metric definitions (paper = code)

- **P@K:** fraction of top-K slots with rel ≥ 1  
- **R@K:** fraction of all rel≥1 docs retrieved in top-K  
- **nDCG@K:** graded DCG with \( (2^{rel}-1)/\log_2(i+1) \), normalized by IDCG  
- **Latency:** ANN `search_jobs` wall time only (phase11); not HTTP, not cross-encoder, not LLM

#### Dual protocols

| Protocol | Driver | Retrieval | Skills mode in sweep | Output files |
|----------|--------|-----------|---------------------|--------------|
| **Progression** | `benchmarks.paper_progression` | All 15 jobs scored | jaccard + embedding explicit | `paper_progression_summary.json`, per-query CSV, bootstrap JSON, failure cases |
| **Phase11 ANN** | `benchmarks.phase11` | pool=10 ANN then rerank | **Jaccard only** (default `compute_multimodal`) | `phase11_summary.csv`, per-query CSV |

#### Phase11 · exact 40-configuration grid (from shipped `phase11_summary.csv`)

**Per store (20 configs each):**

| Component | Count | Values |
|-----------|-------|--------|
| Chroma distance spaces | 2 | cosine, l2 |
| Qdrant hnsw_ef (when store=qdrant) | 2 | 64, 128 (with default m/efc combos in suffix) |
| Strategies | 2 | semantic, multimodal |
| Metrics | 2 | cosine, euclidean |
| Multimodal α weights | 4 | 0.8, 0.7, 0.6, 0.5 |

**Formula:** 2 stores × (4 semantic configs + 16 multimodal configs) = **40 rows**  
- Semantic: 2 spaces × 2 metrics = 4 per store  
- Multimodal: 2 spaces × 2 metrics × 4 weights = 16 per store  

**Run params in CSV:** top_k=5, candidate_pool=10, repeats=3, queries=30.

**Table 10 excerpt rows** (paper): Chroma semantic cosine; Chroma multimodal w=0.7; Chroma multimodal w=0.5; Qdrant semantic ef=64; Qdrant multimodal w=0.7 ef=64.

#### Paper progression · method ladder (exact driver order)

| Order | Method name in JSON | Scoring function |
|-------|---------------------|------------------|
| 1 | TF-IDF (lexical) | `LexicalRanker.rank_jobs(..., tfidf)` full corpus |
| 2 | BM25 (lexical) | same, bm25 |
| 3 | Semantic cosine | `rank_exhaustive` + `compute_semantic(cosine)` |
| 4 | Multimodal Jaccard w=0.7 | `compute_multimodal_weighted(..., jaccard)` |
| 5 | Multimodal soft embed w=0.7 | `compute_multimodal_weighted(..., embedding)` |
| 6 | RRF ensemble (4 lists) | see RRF table below |
| 7 | Semantic cosine (rich templates) | env `BENCHMARK_RICH_TEMPLATES=1` |
| 8 | Soft embed + cross-encoder (pool=10) | soft shortlist → `rerank_jobs` blend α=0.4 |
| (opt) | Semantic cosine (BGE-small) | env `EMBEDDING_MODEL=BAAI/bge-small-en-v1.5` |

**Bootstrap:** 5000 resamples, seed=42; soft embed vs semantic cosine on per-query nDCG@5.

---

### §7 Results · `section-7.tex` (119 lines, PDF pp. 23–27)

#### Table 8 (`tab:strategy-qual`) · qualitative only

#### Table 9 (`tab:progression-k5`) · headline numbers

| Method | P@5 | R@5 | nDCG@5 |
|--------|-----|-----|--------|
| BM25 | 0.307 | 0.983 | 0.901 |
| TF-IDF | 0.307 | 0.983 | 0.905 |
| Semantic cosine | 0.280 | 0.900 | 0.911 |
| Multimodal Jaccard w=0.7 | 0.293 | 0.950 | 0.933 |
| **Multimodal soft embed w=0.7** | **0.313** | **1.000** | **0.969** |
| RRF ensemble (four lists) | 0.293 | 0.950 | 0.935 |
| Soft embed + cross-encoder | 0.307 | 0.983 | 0.939 |

#### Table 10 (`tab:results-k5`) · ANN excerpt + latency

| Configuration | P@5 | R@5 | nDCG@5 | Latency ms |
|---------------|-----|-----|--------|------------|
| Chroma, semantic, cosine | 0.267 | 0.867 | 0.884 | 0.81 |
| Chroma, multimodal, w=0.7 | 0.280 | 0.917 | 0.913 | 0.67 |
| Chroma, multimodal, w=0.5 | 0.280 | 0.917 | 0.913 | 0.66 |
| Qdrant, semantic, ef=64 | 0.267 | 0.867 | 0.884 | 0.38 |
| Qdrant, multimodal, w=0.7 | 0.280 | 0.917 | 0.913 | 0.43 |

#### Table 11 (`tab:vector-stores`) · Chroma vs Qdrant prose comparison

#### §7.2 Ablation (`sec:ablation`) · how to read Table 10 rows

#### §7.4 Tradeoffs · pool size, Jaccard vs soft, RRF vs learned, in-memory limits

#### §7.5 Cross-encoder · nDCG 0.939; LLM not tabulated

---

### §8 Conclusion · `section-8.tex` (11 lines, PDF p. 27–28)

Restates numbers + limits + practitioner decomposition + agents contribution + ethics deferral.

---

### §9 Future Work · `section-9.tex` (37 lines, PDF pp. 28–29)

| §9.x | Direction | Migration signal |
|------|-----------|------------------|
| 9.1 | LLM agent picks strategy | Replace manual UI controls |
| 9.2 | Preference embeddings from clicks | New data pipeline |
| 9.3 | ANN-first serving, decoupled ingestion, cron agent, GPU LLM | **Core architecture rewrite** |
| 9.4 | Larger labeled corpus | New eval_pairs |
| 9.5 | ESCO/O*NET taxonomy | Replace string skills |

---

### Appendix A · `appendix-recommendations.tex` (PDF p. 29)

Five bullets: lexical baselines; soft embed @0.7; cautious ANN on tiny corpus; backend parity; batch endpoints as first-class.

---

### Back matter

**Supplementary paragraph:** OR 1–3 diagrams + CSV/JSON file list  
**Acknowledgments:** Dr Parteek Kumar (WSU), Thapar Institute  
**Declarations (`declarations.tex`):** Funding (none), competing interests (none), ethics N/A, data+code on GitHub, equal author contributions, supervisor credit  
**References:** 7 BibTeX entries, numeric `sn-mathphys` style

---

## Paper ↔ code discrepancies (critical for migration)

| Topic | Paper says | Code actually does | Action on rewrite |
|-------|------------|-------------------|-------------------|
| RRF four lists | §4: semantic cos, semantic euc, multimodal cos, multimodal euc (all Jaccard) | `paper_progression`: semantic cos, multimodal Jaccard cos, **soft embed cos**, multimodal Jaccard **euc** | Align paper text OR change driver |
| Frontend ensemble | §5.2: four strategy×metric combos | UI selects all 4 (semantic/multimodal × cosine/euclidean) · **matches paper ensemble description** | OK |
| Skills mode API | §5: Jaccard vs embedding selectable | `ResumeRequest` has no `skills_mode`; `compute_multimodal` defaults jaccard | Add API field or fix paper |
| LLM rerank | §4, §5, Fig 6 · Ollama Mistral, parallel 5 calls | **No LLM/Ollama code in backend** | Implement or remove from paper |
| Match endpoints retrieval | §3/§6 imply ANN pool + rerank | `/match-resume` scores **all jobs** in memory (no ANN pre-filter) | ANN-first is future work §9.3 |
| Phase11 skills | Table 10 titled multimodal (Jaccard implied) | phase11 uses default Jaccard, not soft embed | Soft embed numbers come from progression table only |
| Cross-encoder | pool=10, ms-marco-MiniLM-L-6-v2, blend 0.4 | Matches `cross_encoder_rerank.py` | OK |
| Daily recs pool | 120 ANN | `_candidate_jobs_for_resume` uses ANN then scores | OK |

---

## RRF configuration reference

| Context | Lists fused | k |
|---------|-------------|---|
| Paper §4 typical example | sem+cos, sem+euc, mm+cos, mm+euc | 60 |
| `paper_progression.py` | sem cos, mm Jaccard cos w=0.7, soft cos w=0.7, mm Jaccard euc w=0.7 | 60 (`rrf_fuse`) |
| `app.py` ensemble | User-defined `searches[]` with weights | 60 (`rrf_aggregate`) |
| Frontend default | 4 combos: semantic/multimodal × cosine/euclidean, weight 1.0 each | 60 |

---

## Hyperparameter defaults (single reference table)

| Parameter | Paper | Code default | Env override |
|-----------|-------|--------------|--------------|
| Bi-encoder | all-MiniLM-L6-v2 | same | `EMBEDDING_MODEL` |
| Embedding dim | 384 | 384 | · |
| Multimodal α | 0.7 | 0.7 in `compute_multimodal` | request/benchmark args |
| RRF k | 60 | 60 | hardcoded |
| RRF list weight | 1.0 | `SearchConfig.weight` | API |
| Cross-encoder | ms-marco-MiniLM-L-6-v2 | same | `CROSS_ENCODER_MODEL` |
| CE blend α | 0.4 | 0.4 | `blend_alpha` arg |
| CE pool | 10 | 10 | `--rerank-pool` |
| ANN pool (phase11) | 10 | 10 | `--candidate-pool` |
| ANN pool (daily) | 120 | 120 | `candidate_pool` request |
| LLM blend α_r | 0.4 | · | not implemented |
| Top-K eval | 5 | 5 | `--top-k` |
| Bootstrap resamples | · | 5000 | `paired_bootstrap_ndcg` |

---

## Skill catalog (`skill_catalog.py`) · full alias map

react.js/reactjs/react js→react; node.js/nodejs→node; vue.js→vue; ml→machine learning; ai→artificial intelligence; dl→deep learning; nlp→natural language processing; torch→pytorch; tf→tensorflow; k8s/kube→kubernetes; aws lambda/amazon web services→aws; gcp/google cloud platform→google cloud; js→javascript; ts→typescript; postgres→postgresql; powerbi→power bi; ci cd/cicd→ci/cd; ui ux/uiux→ui/ux; figma design→figma; springboot/spring-boot→spring boot; data viz/data visualisation→data visualization; micro services→microservices; sys design→system design.

---

## Declarations & portal Q&A (full)

**Information sheet Q1 · claim:** Separable pipeline stages; multimodal skill blend; RRF; HTTP batch workflows; JAAMAS agentic = orchestrated endpoints with ablatable stages.

**Q2 · evidence:** Dual protocol tables (identical to Table 9/10); artifact list; bootstrap CI; LLM not tabulated.

**Q3 · related work:** Karpukhin, Reimers, Malkov, Cormack, Nogueira/Sun · mapped in §2.

**Q4 · prior publication:** None archival; GitHub + technical report are non-archival companions.

**Cover letter highlights:** JAAMAS fit (agents + IR); soft 0.969 vs semantic 0.911; ANN 0.913 vs 0.884; replication package; synthetic data; Dr Parteek Kumar supervision.

---

## File edit map (when architecture changes)

| If you change… | Update these manuscript files | Update these non-manuscript |
|----------------|------------------------------|----------------------------|
| Layer diagram | `section-3.tex`, Fig1–7 PDFs | README architecture section |
| API surface | `section-5.tex` Table 6, `section-1` bullet | `tests/test_api.py`, frontend |
| Scoring formula | `section-4.tex` | `matching/*`, benchmarks |
| Metrics | `section-6.tex`, `section-7.tex` Tables 9–10 | `paper_progression`, `phase11`, supplementary JSON/CSV |
| Agent workflows | `section-1` `sec:agentic`, `section-5.4` | `app.py` batch routes |
| Abstract numbers | `main.tex` abstract | portal cover letter, information sheet, README |

**Recompile checklist:**
1. `pdflatex` + bibtex on `manuscript/main.tex`
2. `build_cover_letter.sh`, `build_info_sheet.sh`
3. `make_overleaf_zip.sh`
4. Copy fresh metrics JSON/CSV to `supplementary/`

---

## Codebase Encyclopedia · file-by-file

### Repository layout (top level)

```
Agentic-Job-Matching/
├── backend/           FastAPI service, matching, stores, benchmarks, tests
├── frontend/          React 19 + Vite dashboard
├── data/              cvs.json, jobs.json, eval_pairs.json, jobs_live.json (runtime)
├── docs/
│   ├── report/        Technical report PDF + DOCUMENTATION.md
│   ├── latex/         XeLaTeX technical report source
│   └── submission/jaamas/   Manuscript + portal + supplementary
├── README.md
└── knowledge_graph.md   ← this file (gitignored)
```

### Backend · every source file

| File | LOC (approx) | Role | Key exports / entry points |
|------|--------------|------|---------------------------|
| `app.py` | 597 | FastAPI app, global state, 14 routes | `match_resume`, `rrf_aggregate`, `_candidate_jobs_for_resume`, `_build_why_ranked` |
| `ingestion.py` | 78 | Load JSON, validate Pydantic, embed+upsert | `load_data()`, `ingest_data(store, resumes, jobs)` |
| `schemas.py` | 22 | Resume/Job Pydantic models | `Resume`, `Job` |
| `paths.py` | 10 | Stable paths | `DATA_DIR`, `BENCHMARK_OUTPUTS_DIR`, `CHROMA_DB_DIR`, `QDRANT_DB_DIR` |
| `real_jobs_sync.py` | 215 | External jobs API pagination + snapshot | `RealJobsConfig`, `fetch_all_jobs`, `normalize_external_job` |
| **matching/** | | Scoring + text + lexical | |
| `embedding.py` | 61 | Lazy SentenceTransformer singleton | `embed_resume`, `embed_job`, `get_model`, `template_flags` |
| `document_text.py` | 89 | Normative encoder input strings | `resume_document_text`, `job_document_text` |
| `semantic_similarity.py` | 10 | Pairwise bi-encoder similarity | `semantic_similarity_resume_job` |
| `similarity.py` | 28 | Cosine / Euclidean on vectors | `compute_similarity`, `cosine_similarity`, `euclidean_similarity` |
| `similarity_engine.py` | 70 | Strategy orchestration | `compute_semantic`, `compute_multimodal`, `compute_multimodal_weighted` |
| `skills_similarity.py` | 23 | Jaccard on canonical skill sets | `skills_similarity`, `normalize` |
| `soft_skills.py` | 52 | Embedding-based skill overlap | `compute_soft_overlap`, `compute_soft_skill_details`, `_skill_cache` |
| `skill_catalog.py` | 78 | Synonym normalization | `canonical_skill`, `canonicalize_skills`, `_SYNONYMS` dict |
| `lexical_retrieval.py` | 106 | BM25 + TF-IDF ranker | `LexicalRanker`, `_BM25` (k1=1.5, b=0.75) |
| `text_tokenizer.py` | 53 | tiktoken cl100k_base or regex fallback | `tokenize`, `tokenize_fallback` |
| `cross_encoder_rerank.py` | 65 | ms-marco cross-encoder rerank | `rerank_jobs`, blend α=0.4 |
| **stores/** | | Vector index abstraction | |
| `base_vector_store.py` | · | Abstract interface | `add_job`, `add_resume`, `search_jobs`, `search_resumes` |
| `vector_store.py` | 72 | Chroma HNSW collections | `jobs_collection`, `resumes_collection`, `CHROMA_SPACE` |
| `qdrant_vector_store.py` | 171 | Qdrant local path client | UUID5 point ids, `SearchParams(hnsw_ef=…)` |
| `vector_store_factory.py` | 16 | Backend switch | `get_vector_store`, `SUPPORTED_VECTOR_STORES` |
| **benchmarks/** | | Offline evaluation drivers | |
| `paper_progression.py` | 307 | Table 9 ladder + bootstrap + failures | `main()`, `paired_bootstrap_ndcg` |
| `phase11.py` | 529 | Table 10 ANN 40-config sweep | `evaluate_config`, `evaluate_lexical_config` |
| `research_sweep.py` | 199 | Fair pool comparison + paper-style RRF | `rank_exhaustive`, `rank_ann_pool`, `rrf_fuse` |
| `metrics.py` | 68 | Shared P/R/nDCG | `eval_rankings`, `ndcg_at_k`, … |
| `lexical.py` | · | Label loader duplicate for sweep | `load_eval_labels` |
| `bootstrap.py` | · | Bootstrap utilities | |
| `progression.py` | · | Older progression variant | |
| `analyze_gaps.py` | · | Diagnostic script | |
| **scripts/** | | CLI helpers | |
| `print_paper_table.py` | · | Print Table 9 from JSON | |
| `measure_agent_ops.py` | · | Agent endpoint timing | |
| `sync_real_jobs_once.py` | · | One-shot job sync | |
| `benchmark_v1.py` | · | Legacy benchmark | |
| **tests/** | 63 tests | See test inventory below | |

### Algorithm walkthroughs

#### A. Application startup (`app.py` module load)

```
1. get_vector_store() → (store, "chroma"|"qdrant")
2. load_data() → validate Resume/Job from data/cvs.json + jobs.json
3. RealJobsConfig.from_env() → real_jobs_state dict
4. _boot_jobs_from_snapshot_if_available() → may replace jobs from jobs_live.json
5. _reindex_all() → ingest_data: for each job/resume embed + store.upsert
6. Uvicorn serves app with in-memory resumes[], jobs[], store, active_vector_store
```

#### B. POST `/match-resume` (current · exhaustive)

```
Input: { name, top_k, strategy, metric }
1. Find resume by name in resumes[]
2. FOR each job in jobs[]:                    ← O(n_jobs) full scan
     compute_scores_for_pair(resume, job, strategy, metric)
     → semantic: compute_semantic
     → multimodal: compute_multimodal (default skills_mode=jaccard, w=0.7)
3. Sort by similarity DESC
4. Assign rank 1..n
5. Return top_k items with semantic_score, skills_score, similarity, metric_used, strategy_used
Note: Does NOT call store.search_jobs; re-embeds every pair via semantic_similarity_resume_job
```

#### C. POST `/candidate/daily-recommendations` (ANN path)

```
Input: { name, top_k, strategy, metric, candidate_pool=120 }
1. embed_resume(resume) → query vector
2. store.search_jobs(embed, k=min(pool, len(jobs))) → ANN shortlist
3. Map metadatas → job objects via _source_id / id
4. FOR each candidate job: compute_scores_for_pair
5. Sort, attach why_ranked[] bullets, return top_k + metadata counts
```

#### D. Ingestion pipeline (`ingestion.py` + paper OR Fig 8)

```
cvs.json / jobs.json
  → Pydantic Resume(**r).dict() / Job(**j).dict()
  → resume_document_text / job_document_text (canonical skills)
  → SentenceTransformer.encode → 384-d vector
  → _clean_metadata (flatten list fields for Chroma)
  → store.add_job / add_resume (upsert by entity id)
```

#### E. Phase11 per-query evaluation loop

```
FOR each config in 40-grid:
  set env VECTOR_STORE, CHROMA_SPACE or QDRANT_HNSW_*
  get_vector_store → ingest_data (fresh collection with suffix)
  FOR repeat in 1..3:
    FOR query_id in 30 eval queries:
      embed resume (precomputed cache)
      t0 = now; results = store.search_jobs(embed, k=10); latency = now-t0
      FOR each retrieved job in pool:
        score_pair(resume, job, strategy, metric, semantic_weight)
      sort → predicted_ids[:5]
      compute P@5, R@5, nDCG@5 vs eval_map[query_id]
  aggregate means → one CSV summary row
```

#### F. Soft skill overlap computation

```
FOR each required job skill j:
  embed(j) once (cached in _skill_cache)
  best = max cosine(embed(j), embed(r)) for r in resume skills
soft_score = mean(best over all job skills)
final = 0.7 * semantic_cosine + 0.3 * soft_score
```

#### G. Cross-encoder rerank (progression table last row)

```
1. rank_exhaustive with soft embed w=0.7 → full ranking
2. Take top 10 job ids as shortlist
3. cross_encoder.predict([(resume_text, job_text), ...]) for each pair
4. Min-max normalize CE scores within shortlist
5. blended = 0.4 * prior_score + 0.6 * ce_norm
6. Re-sort shortlist by blended score
```

---

### RRF configuration · three sources (important)

| Source | Four lists fused | Matches paper §4 text? |
|--------|------------------|------------------------|
| **Paper §4.4** (typical example) | semantic+cosine, semantic+euclidean, multimodal+cosine, multimodal+euclidean (Jaccard) | Reference text |
| **`research_sweep.py`** | sem cos, mm Jaccard cos w=0.7, sem euc, mm Jaccard euc w=0.7 | **Yes · aligns with paper** |
| **`paper_progression.py`** (Table 9 row) | sem cos, mm Jaccard cos, **soft embed cos**, mm Jaccard euc | **No · includes soft embed** |
| **Frontend ensemble default** | all 4 strategy×metric combos, weight 1.0 | Matches paper §4 example |

Table 9 RRF nDCG 0.935 comes from **paper_progression** driver (soft embed in fusion), not from research_sweep's paper-aligned four-list fusion.

---

### Data layer · schemas and examples

#### `data/cvs.json` · 30 resumes

```json
{
  "id": "cv_01",
  "name": "Rahul Sharma",
  "skills": ["Python", "Machine Learning", "AWS"],
  "experience_years": 3,
  "preferred_salary": 120000,
  "remote_preference": true,
  "summary": "Machine learning engineer with 3 years experience in Python and AWS."
}
```

**IDs:** `cv_01` … `cv_30`. Names are unique lookup keys for API (`name` field).

#### `data/jobs.json` · 15 jobs

```json
{
  "id": "job_01",
  "title": "Machine Learning Engineer",
  "required_skills": ["Python", "Machine Learning", "TensorFlow"],
  "required_experience": 2,
  "budget": 130000,
  "remote_policy": true,
  "description": "Looking for ML engineer with strong Python and TensorFlow experience."
}
```

**Optional fields in JSON** (not in strict `Job` schema but used if present): `company`, `location`, `job_type`, `link`, `posted_at`, `source`. Ingestion passes them to metadata / document_text.

**IDs:** `job_01` … `job_15`. API lookup by `title`.

#### `data/eval_pairs.json`

```json
{
  "version": "1.0",
  "task": "resume_to_jobs",
  "relevance_scale": "0-2",
  "labels": [
    {"query_id": "cv_01", "doc_id": "job_01", "relevance": 2},
    {"query_id": "cv_01", "doc_id": "job_07", "relevance": 1}
  ]
}
```

**Statistics:** 30 query IDs, 47 pairs with rel≥0, 21×rel=2, 26×rel=1, 1–2 relevant jobs per query.

**Example judgments:**
- cv_01 → job_01 (strong ML match), job_07 (partial)
- cv_02 → job_02 (React frontend strong), job_13 (partial)
- cv_06 → job_01 + job_06 (ML + NLP partial)

#### Runtime artifacts

| File | Written by | Content |
|------|------------|---------|
| `data/jobs_live.json` | `real_jobs_sync.write_snapshot` | External API fetch + dedupe |
| `data/daily_recommendations_YYYY-MM-DD.json` | `/agent/run-daily-recommendations` | Batch run payload per user |

---

### API · complete request/response shapes

#### Match (exhaustive)

**POST `/match-resume`**
```json
// Request
{ "name": "Rahul Sharma", "top_k": 5, "strategy": "multimodal", "metric": "cosine" }
// Response item
{
  "job_title": "Machine Learning Engineer",
  "semantic_score": 0.82,
  "skills_score": 0.67,
  "similarity": 0.775,
  "metric_used": "cosine",
  "strategy_used": "multimodal",
  "vector_store_used": "chroma",
  "rank": 1
}
```

**POST `/match-resume-ensemble`**
```json
// Request
{
  "name": "Rahul Sharma",
  "top_k": 5,
  "searches": [
    {"strategy": "semantic", "metric": "cosine", "weight": 1.0},
    {"strategy": "multimodal", "metric": "cosine", "weight": 1.0}
  ]
}
// Response item includes sources[] with per-list rank, rrf_contribution, fused_score
```

**POST `/candidate/daily-recommendations`**
```json
// Response wrapper
{
  "candidate": "Rahul Sharma",
  "generated_from_jobs": 15,
  "evaluated_candidates": 15,
  "candidate_pool": 120,
  "results": [{ "job_title": "...", "why_ranked": ["Matching skills: python, ..."], "rank": 1 }]
}
```

**POST `/agent/run-daily-recommendations`**
```json
// Request defaults: sync_before_run=true, candidate_pool=120, max_users=0 (all)
// Response
{
  "message": "Daily recommendation agent run completed",
  "output_file": "/path/data/daily_recommendations_2026-05-27.json",
  "users_processed": 30,
  "jobs_total_available": 15,
  "generated_at_utc": "2026-05-27T..."
}
```

---

### Frontend encyclopedia (`frontend/src/App.jsx` ~1812 lines)

#### Stack
- React 19, Vite 7, axios, ESLint
- Tailwind configured (`tailwind.config.js`) but primary styling in `App.css` ("FORGE" theme)
- Entry: `main.jsx` → `App.jsx`

#### Subcomponents (in same file)

| Component | Purpose |
|-----------|---------|
| `SearchableSelect` | Type-ahead entity picker (lines ~274+) |
| `ScoreBand` / helpers | Tier labels for similarity bands |
| `App` (default export) | Full dashboard |

#### React state inventory

| State | Default | Purpose |
|-------|---------|---------|
| `theme` | localStorage | light/dark |
| `mode` | `"resume"` | resume→jobs vs job→resumes |
| `options` / `selectedValue` | [] / "" | Entity dropdown |
| `topK` | 5 | Results count |
| `strategy` / `metric` | semantic / cosine | Match config |
| `useEnsemble` | false | RRF mode |
| `selectedSearches` | all 4 combos | Ensemble checkboxes |
| `useLiveRecommendations` | false | Daily rec endpoint |
| `systemConfig` | null | From GET /system-config |
| `vectorStore` | "" | Active backend display |
| `results` | [] | Ranked output cards |
| `savedConfigs` / `recentRuns` | localStorage | Persisted runs |
| `agentRunSummary` | null | Last batch agent response |

#### localStorage keys

| Key | Content |
|-----|---------|
| `jobMatcher.savedConfigs.v1` | Named strategy presets (max 20) |
| `jobMatcher.recentRuns.v1` | Last N match runs with timestamps |
| `jobMatcher.theme.v1` | `"light"` or `"dark"` |

#### UI regions (CSS classes in App.css)

- Dashboard grid: control panel (left) + results panel (right)
- Control panel: mode toggle, entity select, strategy/metric, ensemble chips, top-K slider, vector store switch, ops buttons (sync, agent)
- Results: ranking cards with semantic/skills breakdown, detail drawer, export JSON
- Ops status strip: real jobs status, agent summary

#### Main user actions → API map

| UI action | Endpoint |
|-----------|----------|
| Run match | `/match-resume` or `/match-job` |
| Run ensemble | `/match-*-ensemble` |
| Live recommendations toggle | `/candidate/daily-recommendations` |
| Sync real jobs | `/real-jobs/sync` |
| Run daily agent | `/agent/run-daily-recommendations` |
| Switch vector store | POST `/system-config/vector-store` |

---

### Test inventory (63 tests)

| File | Count | Covers |
|------|-------|--------|
| `test_api.py` | 20 | All 14 routes + error cases + parametrized strategies |
| `test_benchmark_metrics.py` | 5 | nDCG, P/R, eval_rankings, empty aggregate |
| `test_document_text.py` | 5 | Templates, rich mode, canonical flags |
| `test_embedding_config.py` | 4 | Model name env, template_flags, proxy encode |
| `test_integration_data.py` | 3 | eval_pairs load, lexical on corpus, progression JSON exists |
| `test_lexical_retrieval.py` | 5 | BM25, TF-IDF, unknown method |
| `test_research_sweep_utils.py` | 2 | rrf_fuse consensus ordering |
| `test_similarity_engine.py` | 4 | semantic, jaccard blend, embedding mode, invalid weight |
| `test_skill_catalog.py` | 5 | aliases react.js, torch, ml, dedupe |
| `test_skills_similarity.py` | 4 | Jaccard edge cases |
| `test_soft_skills.py` | 3 | soft overlap perfect/empty, details shape |
| `test_text_tokenizer.py` | 3 | fallback tokens, empty input |

**Not tested:** `cross_encoder_rerank.py`, `qdrant_vector_store.py` (isolation), `real_jobs_sync.py` HTTP fetch, frontend.

---

### Bibliography · full entries (`references.bib`)

| Key | Authors | Title | Venue | Year | DOI |
|-----|---------|-------|-------|------|-----|
| karpukhin2020dpr | Karpukhin et al. | Dense Passage Retrieval for Open-Domain QA | EMNLP 2020 | 2020 | 10.18653/v1/2020.emnlp-main.550 |
| reimers2019sbert | Reimers & Gurevych | Sentence-BERT | EMNLP 2019 | 2019 | 10.18653/v1/D19-1410 |
| malkov2018hnsw | Malkov & Yashunin | HNSW ANN | IEEE TPAMI 42(4) | 2018 | 10.1109/TPAMI.2018.2884673 |
| cormack2009rrf | Cormack et al. | Reciprocal Rank Fusion | SIGIR 2009 | 2009 | 10.1145/1571941.1572114 |
| nogueira2019bert | Nogueira & Cho | Passage Re-ranking with BERT | arXiv:1901.04085 | 2019 | 10.48550/arXiv.1901.04085 |
| sun2023chatgptsearch | Sun et al. | Is ChatGPT Good at Search? | EMNLP 2023 | 2023 | 10.18653/v1/2023.emnlp-main.327 |
| wang2020minilm | Wang et al. | MiniLM distillation | NeurIPS 33 | 2020 | 10.48550/arXiv.2012.15829 |

**In-text usage:** §1 agentic cite → sun2023; §2 stacks all seven; MiniLM supports all-MiniLM lineage.

---

### Benchmark & script CLI reference

| Command | Purpose | Key flags |
|---------|---------|-----------|
| `python -m benchmarks.paper_progression` | Table 9 + bootstrap | `--top-k 5`, `--rerank-pool 10`, `--skip-cross-encoder`, `--skip-alt-embedder` |
| `python -m benchmarks.phase11` | Table 10 grid | `--candidate-pool 10`, `--repeats 3`, `--multimodal-weights 0.8 0.7 0.6 0.5` |
| `python -m benchmarks.research_sweep` | Pool 10 vs 15 + paper RRF | `--out research_sweep.json` |
| `pytest tests/ -v` | 63 unit/integration tests | |
| `uvicorn app:app --reload --port 8000` | Dev server | |
| `npm run dev` (frontend) | Vite on :5173 | `VITE_API_BASE_URL` |

---

### Environment variables · complete list

| Variable | Default | Module | Effect |
|----------|---------|--------|--------|
| `VECTOR_STORE` | chroma | factory | chroma \| qdrant |
| `EMBEDDING_MODEL` | all-MiniLM-L6-v2 | embedding | Bi-encoder checkpoint |
| `BENCHMARK_RICH_TEMPLATES` | off | embedding | Longer doc templates |
| `BENCHMARK_NO_CANONICAL_SKILLS` | off | embedding | Skip skill_catalog in templates |
| `CHROMA_SPACE` | cosine | vector_store | cosine \| l2 \| ip |
| `CHROMA_COLLECTION_SUFFIX` | "" | vector_store | Separate collection per sweep |
| `QDRANT_HNSW_EF` | 0 | qdrant | Search-time ef (64, 128 in sweep) |
| `QDRANT_HNSW_M` | 0 | qdrant | Graph connectivity |
| `QDRANT_EF_CONSTRUCT` | 0 | qdrant | Build-time ef_construct |
| `QDRANT_COLLECTION_SUFFIX` | "" | qdrant | e.g. phase11_m16_efc128 |
| `CROSS_ENCODER_MODEL` | ms-marco-MiniLM-L-6-v2 | cross_encoder | Reranker model |
| `REAL_JOBS_ENABLE` | false | real_jobs_sync | Enable sync |
| `REAL_JOBS_BASE_URL` | "" | real_jobs_sync | API root |
| `REAL_JOBS_PATH` | /jobs | real_jobs_sync | List endpoint path |
| `REAL_JOBS_PAGE_LIMIT` | 50 | real_jobs_sync | Pagination (max 50) |
| `REAL_JOBS_TIMEOUT_SEC` | 30 | real_jobs_sync | HTTP timeout |
| `REAL_JOBS_OUTPUT_PATH` | data/jobs_live.json | real_jobs_sync | Snapshot path |
| `VITE_API_BASE_URL` | http://localhost:8000 | frontend | API base |

---

### Manuscript §2–§9 sentence-level themes (quick index)

| Section | Every subsection thesis |
|---------|-------------------------|
| §2.1 | Bi-encoders beat BM25 for paraphrase; MiniLM is fast 384-d choice |
| §2.2 | ANN/HNSW required at scale; Chroma simple, Qdrant tunable |
| §2.3 | Hybrid fixes skill-blind semantic; RRF merges lists without calibration |
| §2.4 | nDCG respects graded + position; P/R are set-based at K |
| §2.5 | Two-stage retrieve→rerank; CE accurate slow; LLM adds explanations, very slow |
| §2.6 | Gap: no integrated stack for noisy skills + dual backends + small graded eval |
| §3.1–3.7 | Layer separation enables ablation; Fig 7 is canonical architecture |
| §4.1–4.5 | Re-implementable algebra; templates are normative |
| §5.1–5.4 | FastAPI stateful prototype; batch agent writes dated JSON |
| §6.1–6.4 | Small corpus caveats; dual drivers; pool size caps recall |
| §7.1–7.5 | Soft embed best exhaustive; ANN Jaccard best store row; bootstrap n.s. |
| §8 | Integrated stack + honest limits + agentic workflows for JAAMAS |
| §9.1–9.5 | Autonomy, preferences, scale, data, taxonomy · migration roadmap |

---

## Ultra-detailed Reference (v4)

### Manuscript abstract · verbatim (`main.tex`)

> Lexical matching fails when resumes and postings use different words for the same skill. Semantic similarity alone can still miss structured constraints unless representation, indexing, fusion, and graded labels are assessed separately.
>
> We present *Agentic Job Matching*, a pipeline that encodes structured resume and job text with all-MiniLM-L6-v2, retrieves with Chroma or Qdrant, and ranks with semantic similarity, multimodal semantic–Jaccard blending, or reciprocal rank fusion over multiple strategy–metric runs. Batch and HTTP-triggered workflows drive daily recommendations, live-job sync, and offline evaluation on the same core.
>
> On our manually graded set (30 queries, 47 labeled pairs at K=5), exhaustive reranking over the 15-job corpus yields nDCG@5 0.969 and R@5 1.000 for multimodal soft skill overlap at w=0.7, versus nDCG@5 0.911 and R@5 0.900 for semantic cosine alone. Bootstrap 95% CI [−0.013, +0.146] (not significant at p<0.05). ANN pool=10: nDCG@5 0.913 (Jaccard w=0.7) vs 0.884 (semantic); Qdrant 0.38 ms vs Chroma 0.81 ms.

**Keywords:** resume–job matching, semantic retrieval, vector databases, software agents, reciprocal rank fusion, reproducible evaluation

---

### Complete evaluation corpus · all 30 resumes

| ID | Name | Skills | Exp | Remote | Summary theme |
|----|------|--------|-----|--------|---------------|
| cv_01 | Rahul Sharma | Python, Machine Learning, AWS | 3 | yes | ML engineer |
| cv_02 | Priya Mehta | React, JavaScript, CSS | 2 | yes | Frontend |
| cv_03 | Arjun Verma | Java, Spring Boot, Microservices | 4 | no | Backend Java |
| cv_04 | Neha Kapoor | Python, Pandas, Data Visualization | 2 | yes | Data analyst |
| cv_05 | Vikram Rao | Docker, Kubernetes, CI/CD | 5 | no | DevOps |
| cv_06 | Sneha Iyer | TensorFlow, Deep Learning, Python | 4 | yes | Deep learning |
| cv_07 | Rohit Singh | Node.js, Express, MongoDB | 3 | yes | Node backend |
| cv_08 | Ananya Das | UI/UX, Figma, Design Systems | 2 | yes | Designer |
| cv_09 | Karan Malhotra | AWS, Terraform, Cloud Architecture | 6 | no | Cloud architect |
| cv_10 | Meera Nair | SQL, Power BI, Data Modeling | 3 | yes | BI analyst |
| cv_11 | Amit Tiwari | Go, Microservices, Distributed Systems | 5 | no | Systems/backend |
| cv_12 | Pooja Shah | Python, NLP, Transformers | 4 | yes | NLP engineer |
| cv_13 | Sahil Gupta | Angular, TypeScript, Frontend Development | 3 | yes | Frontend |
| cv_14 | Ritika Jain | Python, Statistics, Machine Learning | 2 | yes | ML/data science |
| cv_15 | Aditya Rao | C++, Algorithms, System Design | 4 | no | Systems engineer |
| cv_16 | Isha Kapoor | React Native, Mobile Development | 3 | yes | Mobile dev |
| cv_17 | Harsh Vardhan | Kubernetes, AWS, CI/CD | 4 | no | DevOps/cloud |
| cv_18 | Tanvi Sharma | Data Science, Python, Scikit-learn | 3 | yes | Data science |
| cv_19 | Manav Khanna | Cybersecurity, Network Security, Penetration Testing | 5 | no | Security |
| cv_20 | Ayesha Ali | Product Management, Agile, Roadmapping | 6 | yes | Product manager |
| cv_21 | Nikhil Bansal | Python, Flask, Backend Development | 2 | yes | Python backend |
| cv_22 | Simran Kaur | Tableau, Data Analytics, SQL | 3 | yes | Analytics/BI |
| cv_23 | Dev Patel | Android, Kotlin, Mobile Development | 4 | yes | Android mobile |
| cv_24 | Kavya Reddy | Deep Learning, Computer Vision, PyTorch | 3 | yes | CV/deep learning |
| cv_25 | Yash Agarwal | Blockchain, Solidity, Smart Contracts | 4 | no | Blockchain |
| cv_26 | Rhea Thomas | Marketing Analytics, SEO, Google Analytics | 3 | yes | Marketing analytics |
| cv_27 | Kabir Sethi | Data Engineering, Spark, Hadoop | 5 | no | Data engineer |
| cv_28 | Naina Bhatia | HR Management, Recruitment, Talent Acquisition | 6 | yes | HR (weak match domain) |
| cv_29 | Om Prakash | Rust, Systems Programming, Concurrency | 4 | no | Systems/Rust |
| cv_30 | Zoya Khan | UX Research, User Testing, Prototyping | 3 | yes | UX research |

**Salary fields:** `preferred_salary` on each resume (85k–150k range) · stored but **not used in scoring** or encoding templates.

---

### Complete job corpus · all 15 postings

| ID | Title | Required skills | Min exp | Budget | Remote |
|----|-------|-----------------|---------|--------|--------|
| job_01 | Machine Learning Engineer | Python, ML, TensorFlow | 2 | 130k | yes |
| job_02 | Frontend Developer | React, JavaScript | 1 | 95k | yes |
| job_03 | Backend Engineer | Java, Spring Boot | 3 | 125k | no |
| job_04 | Data Analyst | Python, Pandas | 1 | 105k | yes |
| job_05 | DevOps Engineer | Docker, Kubernetes | 4 | 150k | no |
| job_06 | NLP Engineer | Python, NLP, Transformers | 3 | 145k | yes |
| job_07 | Cloud Architect | AWS, Terraform | 5 | 160k | no |
| job_08 | Mobile Developer | React Native, Mobile Development | 2 | 110k | yes |
| job_09 | Cybersecurity Engineer | Cybersecurity, Network Security | 4 | 150k | no |
| job_10 | Data Engineer | Spark, Hadoop | 3 | 145k | no |
| job_11 | Product Manager | Product Management, Agile | 5 | 160k | yes |
| job_12 | Blockchain Developer | Blockchain, Solidity | 3 | 155k | no |
| job_13 | UI/UX Designer | UI/UX, Figma | 2 | 90k | yes |
| job_14 | Systems Engineer | C++, System Design | 3 | 135k | no |
| job_15 | Business Intelligence Analyst | SQL, Power BI | 2 | 100k | yes |

**Corpus design:** Each job targets a distinct role cluster; eval pairs connect resumes with plausible strong (2) and partial (1) matches across overlapping skill domains (ML↔NLP, DevOps↔Cloud, Data↔BI).

---

### Complete graded judgments · all 47 pairs (per query)

| Query | Candidate | rel=2 (strong) | rel=1 (partial) |
|-------|-----------|----------------|-----------------|
| cv_01 | Rahul Sharma | Machine Learning Engineer | Cloud Architect |
| cv_02 | Priya Mehta | Frontend Developer | UI/UX Designer |
| cv_03 | Arjun Verma | Backend Engineer | Systems Engineer |
| cv_04 | Neha Kapoor | Data Analyst | BI Analyst |
| cv_05 | Vikram Rao | DevOps Engineer | Cloud Architect |
| cv_06 | Sneha Iyer | ML Engineer | NLP Engineer |
| cv_07 | Rohit Singh | · | Backend Engineer |
| cv_08 | Ananya Das | UI/UX Designer | · |
| cv_09 | Karan Malhotra | Cloud Architect | DevOps Engineer |
| cv_10 | Meera Nair | BI Analyst | Data Analyst |
| cv_11 | Amit Tiwari | · | Backend Engineer, Systems Engineer |
| cv_12 | Pooja Shah | NLP Engineer | ML Engineer |
| cv_13 | Sahil Gupta | Frontend Developer | · |
| cv_14 | Ritika Jain | ML Engineer | Data Analyst |
| cv_15 | Aditya Rao | Systems Engineer | · |
| cv_16 | Isha Kapoor | Mobile Developer | Frontend Developer |
| cv_17 | Harsh Vardhan | DevOps Engineer | Cloud Architect |
| cv_18 | Tanvi Sharma | ML Engineer | Data Analyst |
| cv_19 | Manav Khanna | Cybersecurity Engineer | · |
| cv_20 | Ayesha Ali | Product Manager | · |
| cv_21 | Nikhil Bansal | · | Data Analyst |
| cv_22 | Simran Kaur | · | BI Analyst, Data Analyst |
| cv_23 | Dev Patel | · | Mobile Developer |
| cv_24 | Kavya Reddy | · | ML Engineer, NLP Engineer |
| cv_25 | Yash Agarwal | Blockchain Developer | · |
| cv_26 | Rhea Thomas | · | BI Analyst |
| cv_27 | Kabir Sethi | Data Engineer | Cloud Architect |
| cv_28 | Naina Bhatia | · | Product Manager |
| cv_29 | Om Prakash | Systems Engineer | · |
| cv_30 | Zoya Khan | · | UI/UX Designer |

**Queries with only partial labels (no rel=2):** cv_07, cv_11, cv_21, cv_22, cv_23, cv_24, cv_26, cv_28, cv_30 · harder for nDCG (ideal ranking mixes 1s only).

**Job label frequency (how often each job is judged relevant):**

| Job | Title | Label count |
|-----|-------|-------------|
| job_01 | ML Engineer | 6 |
| job_04 | Data Analyst | 6 |
| job_07 | Cloud Architect | 5 |
| job_14 | Systems Engineer | 4 |
| job_15 | BI Analyst | 4 |
| job_02 | Frontend Developer | 3 |
| job_13 | UI/UX Designer | 3 |
| job_03 | Backend Engineer | 3 |
| job_05 | DevOps Engineer | 3 |
| job_06 | NLP Engineer | 3 |
| job_08 | Mobile Developer | 2 |
| job_11 | Product Manager | 2 |
| job_09, job_10, job_12 | (each) | 1 |

---

### Measured metrics · exact floats (`paper_progression_summary.json`)

| Method | P@5 (exact) | R@5 (exact) | nDCG@5 (exact) |
|--------|-------------|-------------|----------------|
| TF-IDF (lexical) | 0.3066666666666667 | 0.9833333333333333 | 0.9052232158336745 |
| BM25 (lexical) | 0.3066666666666667 | 0.9833333333333333 | 0.9005019260696712 |
| Semantic cosine | 0.28 | 0.9 | 0.9110935769938718 |
| Multimodal Jaccard w=0.7 | 0.29333333333333333 | 0.95 | 0.9330800418067133 |
| Multimodal soft embed w=0.7 | 0.31333333333333335 | 1.0 | 0.9685150450344648 |
| RRF ensemble (4 lists) | 0.29333333333333333 | 0.95 | 0.9353908232042669 |
| Semantic cosine (rich templates) | 0.30000000000000004 | 0.95 | 0.9220910450535126 |
| Soft embed + cross-encoder (pool=10) | 0.3066666666666667 | 0.9833333333333333 | 0.9392861547735796 |

**Bootstrap soft embed vs semantic (`paper_bootstrap_significance.json`):**

| Field | Value |
|-------|-------|
| baseline | Semantic cosine |
| compare | Multimodal soft embed w=0.7 |
| mean_ndcg_diff | +0.05742146804059303 |
| ci95_lo | −0.013201621554796202 |
| ci95_hi | +0.1463051594069036 |
| n_queries | 30 |
| significant_at_05 | false |

---

### Phase11 · all 40 configurations (`phase11_summary.csv`, exact floats)

| # | Store | Strategy | Metric | w | Space | ef | P@5 | R@5 | nDCG@5 | avg ms | p95 ms |
|---|-------|----------|--------|---|-------|-----|-----|-----|--------|--------|--------|
| 1 | chroma | semantic | cosine | · | cosine | · | 0.2667 | 0.8667 | 0.8845 | 0.805 | 0.891 |
| 2 | chroma | semantic | cosine | · | l2 | · | 0.2667 | 0.8667 | 0.8845 | 0.742 | 0.856 |
| 3 | chroma | semantic | euclidean | · | cosine | · | 0.2667 | 0.8667 | 0.8845 | 0.724 | 0.864 |
| 4 | chroma | semantic | euclidean | · | l2 | · | 0.2667 | 0.8667 | 0.8845 | 0.743 | 0.827 |
| 5 | chroma | multimodal | cosine | 0.8 | cosine | · | 0.2800 | 0.9167 | 0.9010 | 0.753 | 0.871 |
| 6 | chroma | multimodal | cosine | **0.7** | cosine | · | 0.2800 | 0.9167 | **0.9132** | 0.666 | 0.741 |
| 7 | chroma | multimodal | cosine | 0.6 | cosine | · | 0.2800 | 0.9167 | 0.9132 | 0.661 | 0.738 |
| 8 | chroma | multimodal | cosine | 0.5 | cosine | · | 0.2800 | 0.9167 | 0.9132 | 0.662 | 0.727 |
| 9 | chroma | multimodal | cosine | 0.8 | l2 | · | 0.2800 | 0.9167 | 0.9010 | 0.650 | 0.718 |
| 10 | chroma | multimodal | cosine | 0.7 | l2 | · | 0.2800 | 0.9167 | 0.9132 | 0.712 | 0.835 |
| 11 | chroma | multimodal | cosine | 0.6 | l2 | · | 0.2800 | 0.9167 | 0.9132 | 0.731 | 0.837 |
| 12 | chroma | multimodal | cosine | 0.5 | l2 | · | 0.2800 | 0.9167 | 0.9132 | 0.751 | 0.839 |
| 13 | chroma | multimodal | euclidean | 0.8 | cosine | · | 0.2800 | 0.9167 | 0.9132 | 0.786 | 0.902 |
| 14 | chroma | multimodal | euclidean | 0.7 | cosine | · | 0.2800 | 0.9167 | 0.9132 | 0.786 | 0.892 |
| 15 | chroma | multimodal | euclidean | 0.6 | cosine | · | 0.2800 | 0.9167 | 0.9132 | 0.814 | 0.991 |
| 16 | chroma | multimodal | euclidean | 0.5 | cosine | · | 0.2800 | 0.9167 | 0.9132 | 0.779 | 0.870 |
| 17 | chroma | multimodal | euclidean | 0.8 | l2 | · | 0.2800 | 0.9167 | 0.9132 | 0.737 | 0.823 |
| 18 | chroma | multimodal | euclidean | 0.7 | l2 | · | 0.2800 | 0.9167 | 0.9132 | 0.741 | 0.828 |
| 19 | chroma | multimodal | euclidean | 0.6 | l2 | · | 0.2800 | 0.9167 | 0.9132 | 0.785 | 1.000 |
| 20 | chroma | multimodal | euclidean | 0.5 | l2 | · | 0.2800 | 0.9167 | 0.9132 | 0.732 | 0.855 |
| 21 | qdrant | semantic | cosine | · | · | 64 | 0.2667 | 0.8667 | 0.8845 | **0.384** | 0.483 |
| 22 | qdrant | semantic | cosine | · | · | 128 | 0.2667 | 0.8667 | 0.8845 | 0.376 | 0.429 |
| 23 | qdrant | semantic | euclidean | · | · | 64 | 0.2667 | 0.8667 | 0.8845 | 0.364 | 0.405 |
| 24 | qdrant | semantic | euclidean | · | · | 128 | 0.2667 | 0.8667 | 0.8845 | 0.399 | 0.548 |
| 25 | qdrant | multimodal | cosine | 0.8 | · | 64 | 0.2800 | 0.9167 | 0.9010 | 0.413 | 0.572 |
| 26 | qdrant | multimodal | cosine | **0.7** | · | 64 | 0.2800 | 0.9167 | **0.9132** | 0.432 | 0.587 |
| 27 | qdrant | multimodal | cosine | 0.6 | · | 64 | 0.2800 | 0.9167 | 0.9132 | 0.378 | 0.514 |
| 28 | qdrant | multimodal | cosine | 0.5 | · | 64 | 0.2800 | 0.9167 | 0.9132 | 0.438 | 0.615 |
| 29 | qdrant | multimodal | cosine | 0.8 | · | 128 | 0.2800 | 0.9167 | 0.9010 | 0.403 | 0.576 |
| 30 | qdrant | multimodal | cosine | 0.7 | · | 128 | 0.2800 | 0.9167 | 0.9132 | 0.376 | 0.502 |
| 31 | qdrant | multimodal | cosine | 0.6 | · | 128 | 0.2800 | 0.9167 | 0.9132 | 0.390 | 0.524 |
| 32 | qdrant | multimodal | cosine | 0.5 | · | 128 | 0.2800 | 0.9167 | 0.9132 | 0.384 | 0.519 |
| 33 | qdrant | multimodal | euclidean | 0.8 | · | 64 | 0.2800 | 0.9167 | 0.9132 | 0.380 | 0.435 |
| 34 | qdrant | multimodal | euclidean | 0.7 | · | 64 | 0.2800 | 0.9167 | 0.9132 | 0.375 | 0.503 |
| 35 | qdrant | multimodal | euclidean | 0.6 | · | 64 | 0.2800 | 0.9167 | 0.9132 | 0.409 | 0.555 |
| 36 | qdrant | multimodal | euclidean | 0.5 | · | 64 | 0.2800 | 0.9167 | 0.9132 | 0.383 | 0.510 |
| 37 | qdrant | multimodal | euclidean | 0.8 | · | 128 | 0.2800 | 0.9167 | 0.9132 | 0.387 | 0.522 |
| 38 | qdrant | multimodal | euclidean | 0.7 | · | 128 | 0.2800 | 0.9167 | 0.9132 | 0.408 | 0.547 |
| 39 | qdrant | multimodal | euclidean | 0.6 | · | 128 | 0.2800 | 0.9167 | 0.9132 | 0.419 | 0.648 |
| 40 | qdrant | multimodal | euclidean | 0.5 | · | 128 | 0.2800 | 0.9167 | 0.9132 | 0.364 | 0.464 |

**Key observations:**
- All semantic configs (rows 1–4, 21–24) share identical P/R/nDCG · metric choice is cosmetic when space matches.
- Multimodal w≥0.6 ties on nDCG@5=0.9132; w=0.8 drops to 0.9010 for cosine metric only.
- Qdrant HNSW: `_M=16`, `_EF_CONSTRUCT=128` fixed in CSV; only `hnsw_ef` varies (64 vs 128).
- Chroma avg latency ~0.66–0.81 ms (semantic row 1 worst at 0.805); Qdrant ~0.36–0.44 ms (~2× faster).

---

### API · HTTP status and error matrix

| Route | Success | Error conditions | Response body on error |
|-------|---------|------------------|------------------------|
| GET /resumes, /jobs, … | 200 | · | · |
| POST /match-resume | 200 | unknown name | `{"error": "Resume not found"}` (still 200) |
| POST /match-job | 200 | unknown title | `{"error": "Job not found"}` |
| POST /match-*-ensemble | 200 | empty searches | **400** `"At least one search config is required"` |
| POST /real-jobs/sync | 200 | disabled | **400** REAL_JOBS_ENABLE false |
| POST /real-jobs/sync | 502 | network/API fail | HTTPException detail string |
| POST /system-config/vector-store | 200 | invalid store | **422** validation (Pydantic) |
| POST /system-config/vector-store | 400 | bad backend init | HTTPException from factory |

**Pydantic request models (`app.py`):**

```python
ResumeRequest(name: str, top_k=5, strategy="semantic"|"multimodal"|"cosine", metric="cosine"|"euclidean")
JobRequest(title: str, top_k=5, strategy=..., metric=...)
SearchConfig(strategy, metric, weight=1.0)
ResumeEnsembleRequest(name, top_k, searches: List[SearchConfig])
CandidateDailyRecommendationRequest(name, top_k, strategy, metric, candidate_pool=120)
DailyAgentRunRequest(top_k, strategy, metric, sync_before_run=True, candidate_pool=120, max_users=0)
RealJobsSyncRequest(reindex=True)
VectorStoreRequest(vector_store="chroma"|"qdrant")
```

**Missing from API (paper describes but not exposed):** `skills_mode`, `llm_rerank`, `semantic_weight`, `candidate_pool` on standard match.

---

### Ensemble response shape (POST `/match-resume-ensemble`)

Each fused item after `rrf_aggregate`:

```json
{
  "job_title": "Machine Learning Engineer",
  "fused_score": 0.042,
  "similarity": 0.042,
  "semantic_score": 0.71,
  "skills_score": 0.45,
  "strategy_used": "ensemble",
  "metric_used": "mixed",
  "vector_store_used": "chroma",
  "rank": 1,
  "sources": [
    {
      "strategy": "semantic",
      "metric": "cosine",
      "rank": 1,
      "score": 0.82,
      "weight": 1.0,
      "rrf_contribution": 0.01639
    }
  ]
}
```

RRF contribution per source: `weight * (1 / (60 + rank))`.

---

### Daily agent output JSON schema

Written to `data/daily_recommendations_YYYY-MM-DD.json`:

```json
{
  "generated_at_utc": "ISO8601",
  "vector_store": "chroma",
  "strategy": "semantic",
  "metric": "cosine",
  "source_job_count": 15,
  "candidate_pool": 120,
  "max_users": 0,
  "users": [
    {
      "candidate": "Rahul Sharma",
      "evaluated_candidates": 15,
      "top_jobs": [
        {
          "job_id": "job_01",
          "job_title": "Machine Learning Engineer",
          "similarity": 0.85,
          "semantic_score": 0.82,
          "skills_score": null,
          "rank": 1,
          "why_ranked": ["Matching skills: python, ...", "..."]
        }
      ]
    }
  ]
}
```

---

### Frontend · helper function catalog (`App.jsx`)

| Function | Lines | Purpose |
|----------|-------|---------|
| `normalizeSkill` | 10 | lowercase trim for overlap |
| `scoreBand` | 48 | high ≥0.75, mid ≥0.5, else low |
| `confidenceTierLabel` | 54 | Strong / Moderate / Weak labels |
| `strategyLabel` / `metricLabel` | 63–75 | UI display names |
| `buildExplanation` | 100–169 | Client-side why_ranked (parallel to backend `_build_why_ranked`) |
| `SearchableSelect` | ~274+ | Type-ahead dropdown component |
| `scoreStats` useMemo | ~640 | Detect if min-max normalization needed |
| `normalizedResults` | ~660 | Apply normalization |
| `enrichedResults` | ~677 | Attach explanation, band, scorePercent |
| `handleMatch` | ~859 | Route to match / ensemble / daily rec endpoints |
| `handleVectorStoreChange` | · | POST switch + reload config |
| `handleSyncRealJobs` | · | POST /real-jobs/sync |
| `handleRunDailyAgent` | · | POST agent batch |

**localStorage keys (exact):**
- `jobMatcher.savedConfigs.v1`
- `jobMatcher.recentRuns.v1`
- `jobMatcher.theme.v1`

**Score normalization logic (paper §5.2):**

```javascript
requiresNormalization = (max > 1 || min < 0 || max <= 0.2)
if (requiresNormalization && max !== min)
  normalized = (raw - min) / (max - min)
else
  normalized = clamp(raw, 0, 1)
```

Triggered when raw similarities cluster below 0.2 or leave [0,1].

**Backend `_build_why_ranked` thresholds (`app.py`):**
- semantic ≥ 0.65 → "High semantic similarity"
- semantic ≥ 0.5 → "Moderate semantic similarity"
- Skill overlap from raw lowercase set intersection (no skill_catalog on backend explain path)

---

### Module dependency graph (import direction)

```
app.py
 ├── ingestion (load_data, ingest_data)
 ├── matching.embedding (embed_resume)
 ├── matching.similarity_engine (compute_semantic, compute_multimodal)
 ├── stores.vector_store_factory
 └── real_jobs_sync

ingestion.py
 ├── matching.embedding
 └── schemas

matching.similarity_engine
 ├── semantic_similarity → embedding, similarity
 ├── skills_similarity → skill_catalog
 └── soft_skills → embedding

benchmarks.paper_progression
 ├── matching.*, benchmarks.metrics, research_sweep

benchmarks.phase11
 ├── ingestion, stores, similarity_engine, lexical (optional)
```

---

### Chroma vs Qdrant · implementation comparison

| Aspect | Chroma (`vector_store.py`) | Qdrant (`qdrant_vector_store.py`) |
|--------|---------------------------|-----------------------------------|
| Persist | `backend/chroma_db/` | `backend/qdrant_db/` |
| Collections | `jobs_collection{suffix}`, `resumes_collection{suffix}` | same naming |
| Distance | `CHROMA_SPACE`: cosine/l2/ip at create | Fixed COSINE 384-d in code |
| Point ID | job_id / resume_id string | UUID5(`job:{id}`) / UUID5(`resume:{id}`) |
| Metadata lists | Flattened to comma string | Native payload dict |
| Search API | `collection.query(n_results=k)` | `search` or `query_points` fallback |
| HNSW tuning | Via collection metadata at create | `QDRANT_HNSW_EF`, `_M`, `_EF_CONSTRUCT` env |
| Distance in results | Chroma distance | `1 - score` converted to distance list |
| Filter support | `where` dict | `_qdrant_filter` → Range/MatchValue |

---

### Python dependencies (`requirements-min.txt`)

| Package | Version | Role |
|---------|---------|------|
| fastapi | 0.129.0 | HTTP API |
| uvicorn | 0.29.0 | ASGI server |
| numpy | 1.26.4 | Vector math |
| pydantic | 2.9.2 | Validation (v2; `.dict()` deprecated) |
| sentence-transformers | 5.1.2 | MiniLM + cross-encoder |
| chromadb | 0.4.24 | Default vector store |
| qdrant-client | 1.9.1 | Optional Qdrant |
| tiktoken | 0.8.0 | Lexical tokenization |

**Dev:** `requirements-dev.txt` adds pytest, pytest-cov, httpx (TestClient).

---

### Test suite · every test with assertion focus

| Test | Asserts |
|------|---------|
| test_get_resumes | 200, list contains "Rahul Sharma" |
| test_get_resumes_full | skills field present |
| test_get_jobs | contains "Machine Learning Engineer" |
| test_match_resume[semantic/multimodal/cosine] | rank 1, similarity field |
| test_match_resume_not_found | error dict |
| test_match_resume_ensemble | job_title in fused result |
| test_match_resume_ensemble_empty_searches | 400 |
| test_match_job* | candidate_name |
| test_candidate_daily_recommendations | why_ranked present |
| test_agent_run_daily_recommendations | output_file path, 1 user when max_users=1 |
| test_real_jobs_sync_disabled | 400 |
| test_set_vector_store_chroma | 200 chroma |
| test_set_vector_store_invalid | 422 |
| test_perfect_ranking_ndcg | metrics math |
| test_rrf_fuse_orders_by_consensus | RRF ordering |
| test_soft_overlap_perfect_match | soft_skills |
| test_react_js_alias | skill_catalog |
| … | (63 total) |

**conftest fixtures:** `sample_resume`, `sample_job`, `sample_jobs`, `eval_map_simple`, `project_data`; autouse `_reset_embedding_env`.

---

### Architecture migration · expanded checklist

**Phase A · Preserve evaluation contract**
- [ ] Keep `data/eval_pairs.json` byte-identical or version with changelog
- [ ] Keep `benchmarks.paper_progression` and `phase11` drivers runnable
- [ ] Document any new protocol separately (don't overwrite Table 9/10 without re-run)

**Phase B · Resolve paper↔code gaps before resubmit**
- [ ] Implement or remove LLM/Ollama rerank (§4, §5, Fig 6)
- [ ] Add `skills_mode` to API or revise §5.2 frontend claims
- [ ] Align RRF list in `paper_progression.py` with §4 text OR update §4
- [ ] Decide match endpoint: ANN-first vs exhaustive (§9.3)

**Phase C · Manuscript sync**
- [x] 7-section restructure + intro rewrite (`cfae2c2`)
- [x] Portal + build pipeline (`3631bcb`)
- [ ] Fig1/Fig4 re-export (thin PDFs)
- [ ] Author placeholders + `\todo` cleanup
- [ ] Abstract + portal re-sync if metrics change

**Phase D · New architecture documentation**
- [x] Update this knowledge graph (v11 @ `010dadf`)
- [ ] Technical report `docs/latex/body.tex` if still maintained

---

## Table of Contents

- [Module: rewrite (current)](#module-rewrite-current) (58 entries · **start here**)
- [Module: research evaluation](#module-research-evaluation) (16 entries · **offline pipeline**)
- [Module: backend (legacy monolith)](#module-backend-legacy-monolith) (35+ entries · `app.py` removed)
- [Module: frontend (legacy)](#module-frontend) (4 entries · see rewrite for current portals)
- [Module: data](#module-data) (3 entries)
- [Module: submission-pdfs](#module-submission-pdfs) (3 entries)
- [Module: docs/submission/jaamas](#module-docssubmissionjaamas) (manuscript source · see also **JAAMAS Manuscript** section above)
- [Module: docs](#module-docs) (5 entries)
- [Module: root](#module-root) (2 entries)

## Cross-Module Relationships

| From | To | Relationship |
|------|-----|-------------|
| `backend/main.py` | `bootstrap.create_system` | App factory entry |
| `bootstrap.py` | `agents/*`, `stores/factory` | Wires 3 agents + Chroma/Qdrant + SQLite stores |
| `gateway/app.py` | `gateway/routes/*` | FastAPI routers, session middleware, demo seed |
| `gateway/app.py` | `gateway/handlers.py` | Registers global exception handlers on startup |
| `gateway/errors.py` | `gateway/routes/*` | Shared HTTPException helpers `{error, code}` |
| `core/document_parse.py` | `resume_structured_extract`, `job_structured_extract`, `profile_quality` | Unified parse + quality attach on resume upload |
| `core/job_quality.py` | `gateway/routes/employers.py` | `POST /jobs/quality-check`; included in JD parse response |
| `core/profile_quality.py` | `gateway/routes/candidates.py` | `POST /candidates/quality-check`; included in resume upload |
| `shared/skill_catalog.json` | `skill_catalog.py`, `skillCatalog.js` | Single synonym + display source for backend and frontend |
| `hooks/parser.py` | `skill_catalog.normalize_skill_list` | Normalizes skills on profile/job register |
| `frontend/src/components/JobQualityPanel.jsx` | `pages/employer/Jobs.jsx` | Debounced quality check while editing job form |
| `frontend/src/components/ProfileQualityPanel.jsx` | `Onboarding.jsx`, `Profile.jsx` | Completeness, parse confidence, match suggestions |
| `core/scoring.py` | `core/component_scores.py` | Six-signal composite (28/27/10/15/10/10) |
| `frontend/src/utils/matchScoring.js` | `MatchDetailsDrawer.jsx` | Mirrors backend composite weights |
| `gateway/routes/candidates.py` | `agents/candidate_agent` | Profile CRUD, resume upload, quality-check, upsert |
| `gateway/routes/matching.py` | `agents/matchmaking_agent` | Composite/semantic/ensemble match endpoints |
| `agents/matchmaking_agent.py` | `core/matchmaking_scoring.py` | score_pair_advanced, routing, RRF |
| `frontend/src/api/client.js` | `gateway/routes/*` | axios withCredentials; default strategy composite |
| `frontend/src/pages/candidate/Matches.jsx` | `api/client.runMatch` | Profile gate (none/incomplete/stale/ready) + auto-search after onboarding save |
| `frontend/src/utils/profileFields.js` | `api/client.fetchMyProfileOrNull` | Readiness + stale marker mapping for portal gates |
| `auth/store.py` | `gateway/routes/employers.py` | `get_job_owner`, `link_job_if_unowned` on POST /jobs |
| `auth/store.py` | `gateway/routes/candidates.py` | candidate_ownership link for GET/PUT /me |
| `stores/feedback_store.py` | `gateway/routes/feedback.py` | user_feedback UI state (no ranking change) |
| `docs/submission/jaamas/manuscript/main.tex` | `build_all.sh`, section files | JAAMAS entry point, abstract, `\input` chain |
| `docs/submission/jaamas/build_all.sh` | portal scripts, make_overleaf_zip | One-command submission rebuild |
| `scripts/generate_jaamas_figures.py` | `figures/source/*.drawio` | Programmatic draw.io diagram sources |
| `core/match_explanation.py` | `agents/matchmaking_agent.py` | Builds structured `MatchExplanation` on every MatchResult |
| `frontend/src/layouts/PortalShell.jsx` | `page-shell.css`, route pages | Unified 1120px shell for matches/profile/jobs/applications |
| `frontend/src/theme/page-shell.css` | `App.css`, portal pages | Shared max-width, form footer, applicant grid, post-role scroll |
| `frontend/src/pages/employer/Applications.jsx` | `candidate_activity_store` via API | Flat applicant feed · search, role filter, sort, View → matches |
| `frontend/src/pages/employer/Matches.jsx` | `EmployerCandidateResults` | Hero: role dropdown only; stats/refresh inside results card |
| `frontend/src/pages/candidate/Matches.jsx` | `CandidateJobResults` | Hero: title/subtitle only; stats/refresh inside results card |
| `frontend/src/components/MatchDetailsDrawer.jsx` | `MatchExplainability`, result panels | Side drawer 400px · 100dvh · 96px bottom padding |
| `frontend/src/utils/matchFilters.js` | `MatchResultsFilters.jsx` | Client-side filter/sort for match rows |
| `frontend/src/utils/profileEvents.js` | candidate/employer pages | Cross-page invalidation: PROFILE_UPDATED, JOBS_UPDATED |
| `demo_seed.py` | `demo_reset.py`, `gateway/app.py` | Demo accounts + `seed_demo_activity()` sample matches |
| `demo_reset.py` | `gateway/routes/system.py` | `POST /system/demo/reset` reloads corpus + SQLite demo state |
| `frontend/src/components/SystemConfigPanel.jsx` | `api/client.resetDemoData` | Admin demo stats + reset button |
| `agents/matchmaking_agent.py` | `MatchResult` job metadata | Candidate view: job budget, remote, created_at for filters |
| `demo_seed.py` | `auth/store`, corpus | Links demo.candidate → cv_01 Rahul Sharma |
| `benchmarks/paper_progression.py` | `data/eval_pairs.json` | Legacy Table 9 regression |
| `backend/scripts/run_research_pipeline.py` | `benchmarks/research_pipeline.py` | Single-command 9-stage eval |
| `benchmarks/research_pipeline.py` | comparison, ablation, significance, fairness, explainability, paper_tables | Orchestrates offline studies |
| `benchmarks/composite_eval.py` | `core/scoring.compute_composite` | Production composite offline nDCG |
| `docs/research/RESEARCH-PAPER.md` | `backend/reports/research_run_*/` | Manuscript numbers from reports only |
| `README.md` | `docs/design/HLD*.md`, `HANDOFF.md` | Onboarding + architecture pointers |

**Legacy (monolith · removed):** `frontend/App.jsx` → `backend/app.py` (no longer exists)

---

## Module: rewrite (current)

> **Active codebase.** Multi-agent event-driven monolith. Entry: `uvicorn main:create_app --factory --port 8001`.

### Layout

```
backend/
├── main.py                 App factory
├── bootstrap.py            SystemContainer: 3 agents + stores + event bus
├── config.py               Settings (Pydantic): paths, secrets, vector store, demo_mode
├── demo_seed.py            Demo accounts + seed_demo_activity on startup
├── demo_reset.py           Corpus reload + SQLite wipe + full demo reset
├── agents/                 Candidate, Employer, Matchmaking agents
├── bus/                    AgentEventBus + EventType enum
├── core/                   Scoring, resume clean, structured extract, quality intel, skill catalog, real_jobs_sync
├── services/               real_jobs_service (sync orchestration)
├── gateway/                FastAPI app + route modules + errors/handlers + middleware
├── auth/                   Session auth, UserStore, ownership links
├── hooks/                  LLM parser, rule explainer, JsonParser
├── stores/                 Chroma, Qdrant, feedback, activity SQLite
├── contracts/              Pydantic profiles, snapshots, matching DTOs
├── scripts/                run_research_pipeline.py, sync_real_jobs_once.py
└── benchmarks/             research_pipeline, comparison, ablation, significance,
                            fairness_audit, explainability, paper_tables, legacy phase11

frontend/src/
├── api/client.js           All API calls; DEFAULT_CANDIDATE_MATCH uses composite
├── pages/                  candidate/, employer/, admin/ portals
├── components/             MatchDetailsDrawer, MatchExplainability, MatchResultsFilters, quality panels
└── utils/                  profileFields, profileEvents, matchFilters, matchExplainability, matchScoring, skillCatalog
```

---

### backend/main.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Uvicorn factory entry · creates SystemContainer then builds FastAPI gateway.  
**Dependencies:** imports from: `bootstrap`, `gateway.app` | used by: uvicorn CLI  
**Core Logic:** `create_app()` returns `build_gateway(create_system())`. No routes here.  
**Patterns:** factory

---

### backend/bootstrap.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-28  
**Purpose:** Composition root · wires event bus, three agents, vector stores, SQLite feedback/activity, RealJobsService.  
**Key Elements:** `SystemContainer`, `create_system`, `real_jobs`  
**Dependencies:** imports from: `agents/*`, `stores/factory`, `services/real_jobs_service` | used by: `main.py`, tests  
**Core Logic:** Bootstraps corpus from `data/cvs.json` + `data/jobs.json`; `RealJobsService.boot_from_snapshot_if_available()` may replace jobs from `jobs_live.json`; publishes `CorpusBootstrapped`.

#### create_system(settings=None)
**Purpose:** Build and return SystemContainer with all agents initialized.  
**Returns:** SystemContainer with bus, settings, candidate, employer, matchmaker, feedback_store, activity_store.  
**Calls:** `create_store`, agent constructors, `bootstrap_from_file` on both entity agents.

---

### backend/gateway/app.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** FastAPI application assembly · mounts routers, session middleware, read-only guard, demo seed, exception handlers.  
**Key Elements:** `build_gateway`  
**Dependencies:** imports from: route modules, `auth.routes`, `demo_seed`, `ReadOnlyMiddleware`, `handlers` | used by: `main.py`  
**Core Logic:** Stores SystemContainer on `app.state.container`; UserStore on `app.state.auth_store`; calls `seed_demo_accounts` when `SEED_DEMO=true`; when `DEMO_MODE=true` also calls `seed_demo_activity` for pre-populated saved/applied/shortlist. Registers `register_exception_handlers(app)` for consistent error envelopes. Session cookie `jm_session`, 7-day max age.  
**Patterns:** procedural

---

### backend/agents/matchmaking_agent.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Neutral broker · scores candidate–job pairs, ranks, explains; reads snapshots only.  
**Key Elements:** `MatchmakingAgent`, `MatchSession`, `register_handlers`  
**Dependencies:** imports from: candidate/employer agents, `core/matchmaking_scoring`, `core/rrf`, explainer | used by: `bootstrap`, `gateway/routes/matching`  
**Core Logic:** Subscribes to profile update events to invalidate cache. `_score_pair` delegates to `score_pair_advanced`. Attaches `build_match_explanation()` payload on every MatchResult. Candidate→jobs direction includes job metadata (budget, remote, experience, created_at) for frontend filters.  
**Patterns:** OOP, event-driven

#### match_candidate_to_jobs(request) / match_job_to_candidates(request)
**Purpose:** Exhaustive corpus scoring for UI match requests.  
**Params:** MatchRequest with query_key, top_k, strategy (default composite in frontend), metric, skills_mode.  
**Returns:** MatchResponse with ranked MatchResult list including ScoreBreakdown and why_ranked bullets.

---

### backend/core/scoring.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Core scoring functions · semantic, multimodal weighted, and **composite** (product default).  
**Key Elements:** `COMPOSITE_WEIGHTS`, `compute_semantic`, `compute_multimodal_weighted`, `compute_composite`  
**Dependencies:** imports from: `component_scores`, `similarity`, `skills` | used by: `matchmaking_scoring`, benchmarks  
**Core Logic:** Composite blends six signals: semantic 28%, skills 27%, title 10%, experience 15%, compensation 10%, remote 10%; clamps final to [0,1].  
**Patterns:** functional, pure

#### compute_composite(candidate, job, metric, skills_mode)
**Purpose:** Product-facing six-signal score.  
**Returns:** ScoreBreakdown with all component scores + final_score, strategy_used="composite".

---

### backend/core/matchmaking_scoring.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Advanced scoring orchestration · strategy routing, constraints, calibration, feedback boost hook.  
**Key Elements:** `score_pair_advanced`, `resolve_routing`  
**Dependencies:** imports from: `scoring`, `constraints`, `calibration`, `fusion`, `strategy_router` | used by: `matchmaking_agent`  
**Core Logic:** Dispatches strategy string to compute_semantic, compute_multimodal_weighted, compute_composite, or learned fusion path.

---

### backend/core/resume_clean.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Strip PDF artifacts, dedupe lines, join wrapped lines; protect contact spans during cleanup.  
**Key Elements:** `clean_resume_text`, `resume_preview_excerpt`  
**Dependencies:** imports from: `contact_extract` regex patterns | used by: `document_parse.py`, `candidates.py`, frontend `resumeClean.js`  
**Core Logic:** Removes `(cid:N)`, control chars, junk symbols; dedupes consecutive lines; merges hyphen-wrapped line breaks; protects email/URL/phone spans before restore.

---

### backend/core/document_parse.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Unified resume and JD parse pipeline · clean → rule extract → optional LLM merge → quality attach.  
**Key Elements:** `parse_resume_document`, `parse_job_document`  
**Dependencies:** imports from: `resume_clean`, `resume_structured_extract`, `job_structured_extract`, `profile_quality`, `job_quality`, LLM parser | used by: `candidates.py`, `employers.py`  
**Core Logic:** Rule-based fields first; LLM enriches when available; attaches `quality` dict from profile/job quality analyzers on success.

#### parse_resume_document(text, llm_status)
**Purpose:** End-to-end resume parse for upload route.  
**Returns:** dict with structured fields (name, skills, experience, education, projects, summary) plus optional `quality`.

---

### backend/core/resume_structured_extract.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Rule-based resume field extraction from cleaned text · contact, skills, experience, education, projects, summary.  
**Key Elements:** `extract_resume_fields`  
**Used by:** `document_parse.py`, tests

---

### backend/core/job_structured_extract.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Rule-based JD field extraction · title inference from prose, inline skills, education, responsibilities.  
**Key Elements:** `extract_job_fields`  
**Used by:** `document_parse.py`, tests

---

### backend/core/profile_quality.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Candidate profile quality intelligence · completeness score, missing fields, weak summary, salary guidance, parse confidence, match suggestions.  
**Key Elements:** `analyze_profile_quality`  
**Dependencies:** imports from: profile schema helpers | used by: `document_parse.py`, `POST /candidates/quality-check`

#### analyze_profile_quality(profile, llm_status)
**Purpose:** Score profile readiness for matching; emit warnings and actionable suggestions.  
**Returns:** dict with `score`, `level`, `warnings`, `suggestions`, `parsing_confidence`.

---

### backend/core/job_quality.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Employer job posting quality · missing fields, unclear requirements, salary warnings, skill suggestions, experience mismatch.  
**Key Elements:** `analyze_job_quality`  
**Used by:** `document_parse.py`, `POST /jobs/quality-check`

---

### backend/core/skill_catalog.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Canonical skill normalization · synonym lookup, AWS prefix collapse, display names from shared JSON catalog.  
**Key Elements:** `NormalizedSkill`, `canonical_skill`, `normalize_skills`, `normalize_skill_list`, `display_skills`  
**Dependencies:** imports from: `shared/skill_catalog.json` | used by: `hooks/parser.py`, scoring skills overlap  
**Core Logic:** Variant key expansion (dots, dashes, spaces); maps React.js→react, Spring Boot→spring boot, etc.; preserves display casing for UI.

---

### shared/skill_catalog.json
**Language:** json | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Shared skill synonyms and display-name map · single source for backend and frontend dedupe.  
**Key Elements:** `synonyms`, `display`  
**Used by:** `backend/core/skill_catalog.py`, `frontend/src/utils/skillCatalog.js`

---

### backend/gateway/errors.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Shared HTTP error helpers · consistent `{detail: {error, code}}` envelopes for gateway routes.  
**Key Elements:** `api_error`, domain-specific not-found/ownership helpers  
**Used by:** `candidates.py`, `employers.py`, `matching.py`, `feedback.py`

---

### backend/gateway/handlers.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** FastAPI global exception handlers · maps validation, HTTP, KeyError, and unhandled errors to API envelopes.  
**Key Elements:** `register_exception_handlers`  
**Used by:** `gateway/app.py` at startup

---

### backend/core/contact_extract.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Regex extraction of name, email, phone, LinkedIn, GitHub, LeetCode, portfolio, certs from resume text.  
**Key Elements:** `extract_contact_from_text`, `merge_contact_fields`  
**Used by:** resume upload route, LLM parse fallback merge

---

### backend/core/resume_suggestions.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Read-only resume coach · role-targeted improvement tips via LLM for a specific job.  
**Used by:** `POST /candidates/me/resume-suggestions`

---

### backend/core/similar_entities.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Find top-3 similar jobs or candidates by embedding cosine similarity.  
**Used by:** `gateway/routes/similar.py`, MatchDetailsDrawer via SimilarRecommendations

---

### backend/gateway/routes/candidates.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Candidate API · list, get mine, upsert, resume upload, quality-check, saved jobs, applications, resume suggestions.  
**Key Elements:** `_upsert_my_candidate`, `_sanitize_profile_payload`, `upload_resume`, `quality_check`, GET `/me`  
**Dependencies:** imports from: auth deps, candidate agent, `document_parse`, `profile_quality`, `errors` | used by: frontend client  
**Core Logic:** PUT /me always upserts · creates with generated id if no ownership link. GET /me returns 404 `NOT_FOUND` or `PROFILE_NOT_FOUND` for stale recovery. Upload uses `parse_resume_document` (clean → rule → LLM → quality). `POST /quality-check` for debounced form validation.  
**Patterns:** FastAPI router, role-guarded

#### _upsert_my_candidate(raw, request, user)
**Purpose:** Single code path for profile create/update.  
**Calls:** `candidate_agent.register`, `auth_store.link_candidate` · idempotent link.  
**Called by:** PUT /me, POST /candidates when logged-in candidate.

---

### backend/gateway/routes/employers.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Employer job API · list mine, register job, upload JD, parse pasted text, quality-check, update/close jobs.  
**Key Elements:** `register_job`, `parse_job_description`, `quality_check`, `_employer_owns_job`, `_slug_job_id`  
**Core Logic:** POST /jobs auto-slugs id; `link_job_if_unowned` + 403 `JOB_NOT_OWNED` guard. JD paste and file upload use `parse_job_document` with rule extract + LLM merge; responses include `quality`. Debounced `POST /jobs/quality-check` for live form editing.

---

### backend/gateway/routes/matching.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-28  
**Purpose:** Match endpoints · candidate-to-jobs, job-to-candidates, ensemble, daily-batch; pre-syncs live jobs when `sync_before_run` + `REAL_JOBS_ENABLE`. **No auth on routes** — exposes PII on job-to-candidates.  
**Used by:** admin console, portal runMatch, curl smoke tests  
**Security:** Critical if network-exposed · see Security review summary in JAAMAS block.

---

### backend/gateway/routes/real_jobs.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-28  
**Purpose:** External live jobs proxy · `GET /real-jobs/status`, `POST /real-jobs/sync` with `{reindex}`.  
**Dependencies:** imports from: `RealJobsService` on SystemContainer | used by: CLI, daily-batch pre-sync  
**Core Logic:** 400 when disabled; 502 on upstream fetch failure; sync replaces employer corpus and optional full reindex.

---

### backend/core/real_jobs_sync.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-28  
**Purpose:** Upstream provider contract · paginated GET, normalize_external_job, dedupe by id, snapshot read/write.  
**Key Elements:** `RealJobsConfig.from_settings`, `fetch_all_jobs`, `normalize_external_job`, `write_snapshot`, `load_snapshot`  
**Env:** `REAL_JOBS_ENABLE`, `REAL_JOBS_BASE_URL`, `REAL_JOBS_PATH`, `REAL_JOBS_PAGE_LIMIT`, `REAL_JOBS_TIMEOUT_SEC`, `REAL_JOBS_OUTPUT_PATH`  
**Output:** `data/jobs_live.json` (gitignored)

---

### backend/services/real_jobs_service.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-28  
**Purpose:** Sync orchestration · boot from snapshot, fetch upstream, replace employer corpus, reindex candidates+jobs.  
**Key Elements:** `RealJobsService`, `boot_from_snapshot_if_available`, `sync`, `reindex_all`  
**State:** `RealJobsState` (source: local_seed | snapshot | external_api)

---

### scripts/run_tests.sh
**Language:** bash | **Importance:** MEDIUM | **Indexed:** 2026-05-28  
**Purpose:** Unified test runner · `pytest ../tests` + `node --test tests/unit/frontend/test_*.mjs`.

---

### frontend/src/pages/errors/ErrorPage.jsx
**Language:** javascript | **Importance:** MEDIUM | **Indexed:** 2026-05-28  
**Purpose:** Full-screen centered error UX · broken-route SVG, animated background, 502-specific copy.  
**Key Elements:** `ErrorBackground`, `ErrorIllustration`, secondary-first button order for [Go home][Try again]

---

### frontend/src/layouts/PortalShell.jsx
**Language:** javascript | **Importance:** HIGH | **Indexed:** 2026-05-28  
**Purpose:** Candidate/employer portal shell · top nav + mobile tabs + centered page container.  
**Key Elements:** `UNIFIED_SHELL_PREFIXES`, `pageContainerClass`, `linkIsActive`, theme toggle  
**Core Logic:** Routes under matches/profile/saved/jobs/applications share `page-container--jobs` at 1120px max-width. Custom `item.isActive(pathname)` for Jobs tab covering matches + saved routes. Uses `Link` (not NavLink) to avoid `isActive` DOM leak.

---

### frontend/src/theme/page-shell.css
**Language:** css | **Importance:** HIGH | **Indexed:** 2026-05-28  
**Purpose:** Shared portal layout tokens and rhythm · one max-width, form footer, scroll-safe padding.  
**Key Elements:** `--page-max-width: 1120px`, `.main-container`, `.scroll-content`, `.form-footer-inner`, `.post-role-panel`, `.job-meta-grid`, `.applicant-row` patterns  
**Dependencies:** imported by: `App.css` | used by: all portal pages  
**Core Logic:** Hero margin 24px; page bottom padding 96px; employer post-role panel max-height + internal scroll; sticky form footer aligned to form width (760px).

---

### frontend/src/pages/employer/Applications.jsx
**Language:** javascript | **Importance:** HIGH | **Indexed:** 2026-05-28  
**Purpose:** Employer applicant feed · flat list of applications across roles.  
**Key Elements:** search, role filter, sort (newest/match), `applicant-row--interactive`  
**Dependencies:** imports from: `fetchEmployerApplications` | used by: employer portal `/employer/applications`  
**Core Logic:** Client-side filter/sort; each row links to `/employer/matches?job={title}`; columns: candidate, role, match %, date, status + View.

---

### backend/gateway/routes/feedback.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Portal feedback actions (save, apply, not_interested, reject, contact) + legacy pair feedback.  
**Dependencies:** imports from: `FeedbackStore` | used by: frontend `feedbackState.js`

---

### backend/gateway/routes/similar.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** GET similar jobs (candidate auth) and similar candidates (employer auth).

---

### backend/auth/store.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27 (refreshed)  
**Purpose:** SQLite user store + candidate/job ownership links with cross-tenant guards.  
**Key Elements:** `UserStore`, `link_candidate`, `get_candidate_id`, `get_job_owner`, `link_job_if_unowned`, `purge_users_by_email`, `CandidateIdOwnedError`, `JobIdOwnedError`  
**Core Logic:** Idempotent candidate link; job link only when unowned. `purge_users_by_email` deletes demo users (CASCADE ownership) for demo reset. Link preserved on GET 404 so PUT recreates profile at stable id after restart.  
**Patterns:** OOP, sqlite3

---

### backend/stores/candidate_activity_store.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27 (refreshed)  
**Purpose:** SQLite saved jobs and job applications for candidate portal.  
**Key Elements:** `SavedJob`, `JobApplication`, `save_job`, `apply`, `clear_all`  
**Used by:** `gateway/routes/candidates.py`, `demo_seed.seed_demo_activity`, `demo_reset.py`

---

### backend/stores/feedback_store.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27 (refreshed)  
**Purpose:** SQLite tables `user_feedback` (portal UI state) and `match_feedback` (legacy research).  
**Key Elements:** `record_user_action`, `list_latest_for_user`, `clear_all`  
**Core Logic:** Feedback actions do not alter match rankings · UI state only. `clear_all` used by demo reset.

---

### backend/demo_seed.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27 (refreshed)  
**Purpose:** Idempotent demo account seeding + pre-populated sample activity for live demos.  
**Key Elements:** `seed_demo_accounts`, `seed_demo_activity`, DEMO_CANDIDATE_ID=`cv_01` (Rahul Sharma), DEMO_EMPLOYER_JOB_IDS, DEMO_PRIMARY_JOB_ID=`job_01`  
**Core Logic:** Links demo users to corpus IDs. `seed_demo_activity` runs live composite matches, saves top jobs, records application + employer shortlist; skips if activity already exists.  
**Used by:** `gateway/app.py` at startup, `demo_reset.py`

#### seed_demo_activity(container, auth_store, activity_store, feedback_store)
**Purpose:** Make Saved/Applications/shortlist tabs look alive on first demo login.  
**Returns:** dict with saved_jobs, applications, employer_shortlist counts.

---

### backend/demo_reset.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Full demo reset for local testing · reload corpus, wipe demo SQLite, re-seed accounts + activity.  
**Key Elements:** `reload_corpus`, `clear_demo_sqlite`, `reset_demo_data`, `demo_snapshot`  
**Dependencies:** imports from: `demo_seed`, `stores/factory` | used by: `gateway/routes/system.py`  
**Core Logic:** Clears agent memory + recreates vector collections; bootstraps JSON corpus; clears activity/feedback tables; purges demo users; re-runs seed_demo_accounts + seed_demo_activity. `demo_snapshot` returns corpus/activity counts for admin UI.  
**Patterns:** procedural

#### reset_demo_data(container, auth_store)
**Purpose:** Admin-triggered one-click demo restore.  
**Returns:** corpus counts, demo credentials, activity seed stats.

---

### backend/config.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27 (refreshed)  
**Purpose:** Pydantic Settings from `backend/.env` · paths, secrets, feature flags.  
**Key Elements:** `seed_demo`, `demo_mode`, `read_only`, `vector_store`, `sqlite_path`, `cvs_path`, `jobs_path`  
**Core Logic:** `demo_mode=true` enables activity seeding + reset endpoint; `seed_demo=true` creates demo accounts on startup.

---

### backend/core/match_explanation.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Structured explainability payload for every candidate–job match.  
**Key Elements:** `build_match_explanation`  
**Dependencies:** imports from: `contracts/matching`, `core/scoring.build_composite_components` | used by: `matchmaking_agent.py`  
**Core Logic:** Derives matched/missing skills, FitSignal for semantic/experience/compensation/remote, score_breakdown from composite components, human-readable reasons per dimension.

#### build_match_explanation(candidate, job, breakdown, direction)
**Purpose:** Attach rich explanation to MatchResult.  
**Returns:** MatchExplanation pydantic model.

---

### backend/gateway/routes/system.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27 (refreshed)  
**Purpose:** System config API, vector store switch, fairness report, demo reset.  
**Key Elements:** `get_system_config`, `set_vector_store`, `reset_demo`  
**Core Logic:** GET `/system/config` exposes demo_mode, demo_accounts, demo_snapshot. POST `/system/demo/reset` admin-only, guarded by demo_mode and not read_only.

---

### frontend/src/api/client.js
**Language:** javascript | **Importance:** HIGH | **Indexed:** 2026-05-27 (refreshed)  
**Purpose:** Axios API client · all portal HTTP calls with session cookies.  
**Key Elements:** `DEFAULT_CANDIDATE_MATCH`, `resetDemoData`, `upsertCandidateProfile`, `fetchMyProfileOrNull`, `checkProfileQuality`, `checkJobQuality`, `runMatch`  
**Core Logic:** Default match strategy is `composite`. `resetDemoData()` calls POST `/system/demo/reset`. Quality-check endpoints for debounced profile/job panels.

---

### frontend/src/utils/skillCatalog.js
**Language:** javascript | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Frontend mirror of shared skill catalog · canonical dedupe and display names.  
**Key Elements:** imports `shared/skill_catalog.json`, `canonicalizeSkills`, `displaySkill`  
**Used by:** `skills.js`, profile/job forms

---

### frontend/src/utils/matchScoring.js
**Language:** javascript | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Composite score breakdown helpers · mirrors backend six-signal weights for drawer bars.  
**Key Elements:** `COMPOSITE_WEIGHTS`, `scoreContributionPoints`  
**Used by:** `MatchDetailsDrawer.jsx`

---

### frontend/src/components/ExtractedSectionsPanel.jsx
**Language:** javascript | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Shows structured parse output (experience, education, projects) after resume/JD upload.  
**Used by:** `Onboarding.jsx`, `Profile.jsx`, employer job form via `extractedSections.js`

---

### frontend/src/components/ProfileQualityPanel.jsx
**Language:** javascript | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Live candidate profile quality · completeness, warnings, parse confidence, match suggestions.  
**Core Logic:** Debounced `POST /candidates/quality-check` (~450ms) while editing onboarding/profile forms.  
**Used by:** `Onboarding.jsx`, `Profile.jsx`

---

### frontend/src/components/JobQualityPanel.jsx
**Language:** javascript | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Live job posting quality · missing fields, salary warnings, skill suggestions.  
**Core Logic:** Debounced `POST /jobs/quality-check` while editing employer job form.  
**Used by:** `pages/employer/Jobs.jsx`

---

### frontend/src/components/MatchDetailsDrawer.jsx
**Language:** javascript | **Importance:** HIGH | **Indexed:** 2026-05-28  
**Purpose:** Product match detail side panel · score hero, full explainability, resume coach, similar recs.  
**Key Elements:** `MatchDrawerCard`, `drawer-section`, `MatchExplainability` (variant=full), `ResumeImprovementPanel`  
**Used by:** CandidateJobResults, EmployerCandidateResults  
**Core Logic:** Fixed overlay + 400px aside; `100dvh` scroll with 96px bottom padding; Escape closes; body scroll locked.

---

### frontend/src/components/MatchExplainability.jsx
**Language:** javascript | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Renders structured match explanation · compact on cards, full in drawer.  
**Key Elements:** `MatchExplainability`, variants `compact` | `full`  
**Dependencies:** imports from: `utils/matchExplainability.js` | used by: result cards, MatchDetailsDrawer  
**Core Logic:** Shows matched/missing skills, fit signals (experience, compensation, remote), semantic reason, score breakdown.

---

### frontend/src/components/MatchResultsFilters.jsx
**Language:** javascript | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Shared filter bar for candidate jobs and employer candidates result panels.  
**Key Elements:** search, skill chips, remote toggle, salary/budget range, experience range, match score range, sort, clear all  
**Dependencies:** imports from: `matchFilters.js` | used by: CandidateJobResults, EmployerCandidateResults

---

### frontend/src/components/SystemConfigPanel.jsx
**Language:** javascript | **Importance:** HIGH | **Indexed:** 2026-05-27 (refreshed)  
**Purpose:** Admin system panel · vector store switch, demo data stats, reset button.  
**Key Elements:** `handleResetDemo`, demo account list, corpus/activity snapshot  
**Core Logic:** Shows demo_mode, read_only, demo_accounts credentials; Reset demo data calls `resetDemoData()` with confirm dialog (admin, not read-only).

---

### frontend/src/utils/matchExplainability.js
**Language:** javascript | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Client helpers to resolve and format MatchResult.explanation payloads.  
**Key Elements:** `resolveMatchExplanation`, skill list formatters  
**Used by:** MatchExplainability.jsx, matchFilters.js

---

### frontend/src/utils/matchFilters.js
**Language:** javascript | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Client-side filter and sort for match result rows.  
**Key Elements:** `createMatchFilters`, `filterAndSortMatchRows`, `collectSkillOptions`, `hasActiveMatchFilters`  
**Core Logic:** Filters by search text, skills, remote, experience, salary/budget, match score range; sorts best/newest/compensation. Variant-aware for candidate-jobs vs employer-candidates.

---

### frontend/src/utils/profileEvents.js
**Language:** javascript | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Cross-page browser events for profile and job list invalidation.  
**Key Elements:** `PROFILE_UPDATED_EVENT`, `JOBS_UPDATED_EVENT`, `notifyProfileUpdated`, `notifyJobsUpdated`  
**Used by:** Profile, Onboarding, Matches, Saved, employer Jobs/Matches

---

### frontend/src/pages/candidate/Matches.jsx
**Language:** javascript | **Importance:** HIGH | **Indexed:** 2026-05-28  
**Purpose:** Candidate jobs page · profile gates, find/refresh matches, cross-page invalidation.  
**Key Elements:** `invalidateMatches`, `loadProfile({ silent })`, `searchAfterSave`, `PROFILE_UPDATED_EVENT` listener  
**Core Logic:** Hero is title + subtitle only (no duplicate refresh). MatchSummaryCards + toolbar refresh live inside `CandidateJobResults`. Auto-search once when navigated with `searchAfterSave` from onboarding/profile.

---

### frontend/src/pages/candidate/Profile.jsx
**Language:** javascript | **Importance:** HIGH | **Indexed:** 2026-05-27 (refreshed)  
**Purpose:** Candidate profile view/edit · resume re-upload, quality panel, cancel reverts to saved record.  
**Key Elements:** `handleCancelEdit`, `handleSave`, `ProfileQualityPanel`, stale/incomplete empty states  
**Core Logic:** Cancel restores fields from profileRecord. First save navigates to Matches with searchAfterSave; updates notify PROFILE_UPDATED.

---

### frontend/src/pages/candidate/Onboarding.jsx
**Language:** javascript | **Importance:** HIGH | **Indexed:** 2026-05-27 (refreshed)  
**Purpose:** Two-step candidate onboarding · upload or manual entry, quality panel, save.  
**Key Elements:** separate `uploading`/`saving` states, `searchAfterSave` navigation  
**Core Logic:** Continue to jobs navigates with searchAfterSave; notifyProfileUpdated only after save completes (not before navigate).

---

### frontend/src/pages/employer/Jobs.jsx
**Language:** javascript | **Importance:** HIGH | **Indexed:** 2026-05-28  
**Purpose:** Employer job list + post/edit · JD import, JobQualityPanel, optimistic close.  
**Key Elements:** `load({ silent })`, `notifyJobsUpdated`, `post-role-panel`, `form-footer-inner`  
**Core Logic:** Two-column grid (list + form). Posting panel scroll-safe (`max-height`, 120px bottom pad) so sticky footer does not clip fields. After save notifies JOBS_UPDATED.

---

### frontend/src/pages/employer/Matches.jsx
**Language:** javascript | **Importance:** HIGH | **Indexed:** 2026-05-28  
**Purpose:** Employer candidate matching · role picker in hero, results card owns stats + refresh.  
**Key Elements:** `JOBS_UPDATED_EVENT`, `resolveJobSelection`, `autoMatchDone`, `employer-matches-role-field`  
**Core Logic:** Hero: eyebrow, title, subtitle, role dropdown only (no duplicate stats or refresh). `EmployerCandidateResults` shows MatchSummaryCards + MatchResultsFilters refresh. Auto-match on `?job=` param.

---

### frontend/src/components/CandidateJobResults.jsx
**Language:** javascript | **Importance:** HIGH | **Indexed:** 2026-05-28  
**Purpose:** Candidate match results · single stats row, toolbar refresh, collapsed list cards + drawer.  
**Key Elements:** `MatchSummaryCards`, `matches-toolbar`, `runRowAction`, `pendingAction`, `scroll-content`  
**Core Logic:** ResultsPanel with stats then filters (refresh only in toolbar). List cards use `MatchExplainability` variant=list; full breakdown in drawer. Stale-while-revalidate refresh keeps rows visible.

---

### frontend/src/components/EmployerCandidateResults.jsx
**Language:** javascript | **Importance:** HIGH | **Indexed:** 2026-05-28  
**Purpose:** Employer candidate match results · inner stats + toolbar refresh, save/reject/contact guards.  
**Key Elements:** `MatchSummaryCards`, `matches-toolbar`, same refresh/action patterns as CandidateJobResults  
**Used by:** `pages/employer/Matches.jsx`  
**Core Logic:** No hero duplicate stats; refresh label toggles Find candidates / Refresh matches. Removed redundant “Showing matches for” line.

---

### frontend/src/components/EmployerJobCard.jsx
**Language:** javascript | **Importance:** MEDIUM | **Indexed:** 2026-05-28  
**Purpose:** Compact employer job posting card in My jobs list.  
**Key Elements:** title + status + remote badge row, 5-col `job-meta-grid`, skill chips, View candidates / Edit / Close  
**Used by:** `EmployerJobList.jsx`, `pages/employer/Jobs.jsx`

---

### frontend/src/components/ProfileFormFooter.jsx
**Language:** javascript | **Importance:** MEDIUM | **Indexed:** 2026-05-28  
**Purpose:** Sticky profile/onboarding form footer · unsaved status + actions.  
**Key Elements:** `form-footer`, `form-footer-inner--wide`, dirty state text  
**Used by:** `ProfileForm.jsx`, onboarding/profile pages

---

### frontend/src/components/JobPostingForm.jsx
**Language:** javascript | **Importance:** MEDIUM | **Indexed:** 2026-05-28  
**Purpose:** Employer job posting form sections · role basics, work setup, requirements, comp, description.  
**Key Elements:** `FormSection`, `SkillsChipsInput`, `CompensationInput`, `description-field` max-width  
**Used by:** `pages/employer/Jobs.jsx`

---

### frontend/src/pages/candidate/Saved.jsx
**Language:** javascript | **Importance:** MEDIUM | **Indexed:** 2026-05-27 (refreshed)  
**Purpose:** Saved jobs and applications · aligned with Matches feedback API, rollback on unsave error.  
**Key Elements:** `recordFeedbackAction`, `unsavingId`, PROFILE_UPDATED refetch

---

### frontend/src/utils/profileFields.js
**Language:** javascript | **Importance:** MEDIUM | **Indexed:** 2026-05-27 (refreshed)  
**Purpose:** Profile form ↔ API mapping; portal readiness gates for job search.  
**Key Elements:** `profileToPayload`, `profileFromApi`, `hasCandidateProfile`, `isCandidateProfileReady`, `isProfileStale`  
**Core Logic:** Omits empty id on first save. Ready = id + name (queryKey). Stale marker maps to empty form fields for re-save.

---

### frontend/src/components/EmptyState.jsx
**Language:** javascript | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Shared empty-state cards for portals · profile, jobs, employer, no-results variants.  
**Key Elements:** `ProfileNeededEmpty`, `ProfileIncompleteEmpty`, `ProfileStaleEmpty`, `JobsReadyEmpty`, `NoMatchingRolesEmpty`, `EmployerAllClosedEmpty`  
**Core Logic:** `NoMatchingRolesEmpty` uses `filteredOut` prop to distinguish filter-empty vs zero API matches.

---

### frontend/src/components/BackgroundOrnaments.jsx
**Language:** javascript | **Importance:** LOW | **Indexed:** 2026-05-27  
**Purpose:** Subtle animated SVG background variants for candidate, employer, admin portals.  
**Used by:** PortalBackground, ResultsPanel, EmptyState components

---

### README.md
**Language:** markdown | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Primary onboarding doc · architecture, setup, API reference, demo accounts, troubleshooting (602 lines).  
**Dependencies:** links to HLD, SDD, demo script, session notes

---

### HANDOFF.md
**Language:** markdown | **Importance:** HIGH | **Indexed:** 2026-05-28  
**Purpose:** Session continuation doc — goal, git state, manuscript status, UI polish v14, next steps.  
**Core Logic:** Authoritative for “what to do next”; synced with graph v14 handoff block above.

---

### tests/integration/test_demo_reset.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Demo mode integration tests · config snapshot, activity seeding, admin reset, idempotent re-reset.  
**Key Elements:** `test_demo_reset_restores_sample_data`, `test_demo_reset_requires_admin`

---

### tests/integration/test_demo_seed.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Demo account seeding · login, profile link, match smoke, idempotency.

---

### tests/unit/backend/test_real_jobs_sync.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-28  
**Purpose:** Unit tests for normalize_external_job, pagination mock, snapshot roundtrip.

---

### tests/integration/test_real_jobs_api.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-28  
**Purpose:** GET /real-jobs/status; POST /real-jobs/sync returns 400 when disabled.

---

### tests/unit/test_match_explanation.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27 (stale · moved to backend/)  
**Note:** Path is now `tests/unit/backend/test_match_explanation.py`.
**Purpose:** Unit tests for build_match_explanation · skills, fit signals, score breakdown.

---

### tests/unit/test_match_filters.mjs
**Language:** javascript | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Node tests for matchFilters.js · filter, sort, skill options, employer variant.

---

### tests/unit/test_match_explainability.mjs
**Language:** javascript | **Importance:** LOW | **Indexed:** 2026-05-27  
**Purpose:** Node tests for matchExplainability.js client helpers.

---

### tests/integration/test_feature_reverification.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Feature checklist tests · composite scoring, JD parse, feedback, CID cleanup, profile upsert endpoints.

---

## Module: research evaluation

> **Offline only.** Does not change production API defaults. Outputs under `backend/reports/research_run_<timestamp>/`. Manuscript: `docs/research/RESEARCH-PAPER.md`.

### backend/scripts/run_research_pipeline.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** CLI entry for full 9-stage research pipeline (repo-root invocable).  
**Run:** `python backend/scripts/run_research_pipeline.py`  
**Flags:** `--skip-cross-encoder`, `--enable-cross-encoder`, `--data-dir`, `--eval-path`, `--run-id`  
**Dependencies:** imports from: `benchmarks.research_pipeline` | used by: thesis/paper reproducibility  
**Core Logic:** Builds PipelineConfig, calls `run_research_pipeline`, prints step summary, exits 1 on failure.

---

### backend/benchmarks/research_pipeline.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Orchestrates all offline evaluation stages into one timestamped run directory.  
**Key Elements:** `run_research_pipeline`, `PipelineConfig`, `make_run_dir`, `StepResult`  
**Dependencies:** imports from: comparison, composite_eval, ablation, significance, fairness_audit, explainability_eval, paper_tables, dataset_validation, cross_encoder_report | used by: `run_research_pipeline.py` CLI  
**Core Logic:** Sequential steps: (1) validate corpus fail-fast, (2) baseline comparison, (3) production composite eval, (4) ablation, (5) optional CE, (6) bootstrap significance on comparison+ablation per-query, (7) fairness audit, (8) explainability, (9) paper tables. Writes `pipeline_manifest.json`.

#### run_research_pipeline(config)
**Purpose:** Execute all stages; return PipelineResult with per-step status and paths.  
**Returns:** PipelineResult; `valid=False` if validation fails or any step fails.

---

### backend/benchmarks/dataset_validation.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Preflight checks on cvs.json, jobs.json, eval_pairs.json before expensive embedding runs.  
**Key Elements:** `validate_eval_corpus`, `write_validation_report`, `ValidationReport`  
**Core Logic:** Validates IDs, relevance scale, requires ≥1 candidate/job/labeled pair; warns on missing fairness profiles.

---

### backend/benchmarks/comparison.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Lexical vs embedding baseline comparison with per-query latency.  
**Run:** `python -m benchmarks.run_comparison`  
**Outputs:** `comparison_summary.json`, `comparison_table.csv`  
**Strategies:** BM25, TF-IDF, exact overlap, semantic, skills, soft embed, multimodal, RRF.

---

### backend/benchmarks/composite_eval.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Evaluate production `compute_composite` alone on eval_pairs (separate from ablation variants).  
**Outputs:** `composite_eval_report.json`, `composite_summary.csv`, `composite_per_query.csv`  
**Dependencies:** imports from: `core.scoring.compute_composite`, eval_data, rank_utils | used by: research_pipeline step 3

---

### backend/benchmarks/ablation.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Nine-variant component ablation · singles, partial composites, full composite, RRF over singles.  
**Run:** `python -m benchmarks.run_ablation`  
**Outputs:** `ablation_summary.json`, `ablation_summary.md`, `ablation_per_query.csv`  
**Best on demo corpus:** Full composite nDCG@5 0.942.

---

### backend/benchmarks/ablation_scoring.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Offline single/partial composite scorers for ablation; `full_composite` delegates to `compute_composite`.  
**Used by:** ablation.py, not production match path directly.

---

### backend/benchmarks/significance.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Paired bootstrap significance on nDCG@K and MRR (5000 resamples, seed 42).  
**Key Elements:** `run_significance_analysis`, `bootstrap_mean_ci`, `write_significance_report`  
**p-value:** one-sided fraction of bootstrap mean-diffs ≤ 0.

---

### backend/benchmarks/fairness_audit.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Synthetic counterfactual fairness audit · rank stability, score delta, explanation drift.  
**Input:** `data/fairness_audit_profiles.json` (10 pairs). **Strategy:** composite.  
**Outputs:** `fairness_audit_report.json`, `fairness_audit_pairs.csv`, flagged cases CSV.

---

### backend/benchmarks/explainability_eval.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Automated explanation quality on top-5 composite matches (rules vs template explainers).  
**Checks:** skill mention, hallucination, component alignment, consistency Jaccard on synthetic pairs.  
**Outputs:** `explainability_report.json`, flagged/instances CSV.

---

### backend/benchmarks/research_export.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Export benchmark artifacts to `docs/research/evaluation/` with study write-ups and FINDINGS.md.  
**Run:** `python -m benchmarks.run_research_suite` or `bash scripts/run_research_suite.sh`

---

### backend/benchmarks/paper_tables/generators.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Generate copy-paste paper tables (Markdown, CSV, LaTeX booktabs) from report JSON/CSV.  
**Key Elements:** `generate_all_paper_tables`, six table generators (method, ablation, latency, fairness, explainability, qualitative)  
**Labels:** `tab:method-comparison`, `tab:ablation`, etc.

---

### backend/benchmarks/synthetic_dataset/generator.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Generate 100×50 research corpus with graded pairs 0–3 under `data/research/`.  
**Run:** `python -m benchmarks.run_generate_research_dataset`  
**Status:** Generated; full pipeline eval **TODO**.

---

### backend/benchmarks/cross_encoder_report.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Bi-encoder vs two-stage cross-encoder quality/latency report on composite strategy.  
**Finding (demo):** nDCG Δ −0.108, +141 ms CE overhead; disabled in production by default.

---

### backend/benchmarks/framework.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Embedding-only strategy suite runner (`run_eval`); builds strategies from strategies.py.  
**Used by:** legacy significance source=benchmark; superseded by comparison for paper pipeline.

---

### docs/research/RESEARCH-PAPER.md
**Language:** markdown | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Manuscript draft · methodology, architecture, algorithms, evaluation, results, fairness/explainability limits, future work.  
**Rule:** All numbers from `backend/reports/` only; missing studies marked TODO.  
**Primary source run:** `research_run_smoke_test`; CE from root `cross_encoder_report.json`.

---

## Module: backend (legacy monolith)

> **[LEGACY]** Pre-rewrite monolith. `backend/app.py` **removed** · kept for benchmark/scoring algorithm reference and paper artifact cross-links.

### Layout

```
backend/
├── app.py              FastAPI monolith · 14 routes, global state, RRF, agent
├── ingestion.py        JSON load + Pydantic validate + embed upsert
├── schemas.py          Resume/Job Pydantic models
├── paths.py            DATA_DIR, BENCHMARK_OUTPUTS_DIR, CHROMA/QDRANT paths
├── real_jobs_sync.py   External jobs API → jobs_live.json snapshot
├── search.py           Legacy/unused search helper (not wired to app routes)
├── evaluation.py       Legacy eval helper (benchmarks use metrics.py instead)
├── matching/           Scoring, embedding, lexical, cross-encoder
├── stores/             Chroma + Qdrant + factory
├── benchmarks/         paper_progression, phase11, research_sweep, metrics
├── scripts/            CLI utilities (sync, print tables, ops timing)
├── tests/              63 pytest tests
└── benchmark_outputs/  Local JSON/CSV (gitignored except phase11 CSVs)
```

---

### backend/app.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** FastAPI monolith holding in-memory `resumes[]`, `jobs[]`, active vector store, and all HTTP routes. Startup loads data, optionally boots live jobs snapshot, reindexes vectors.  
**Dependencies:** imports from: `ingestion`, `matching.embedding`, `matching.similarity_engine`, `stores.vector_store_factory`, `real_jobs_sync` | used by: `tests/test_api.py`, frontend axios calls  
**Core Logic:** Match routes scan all jobs/resumes in memory (O(n)); daily/agent routes use ANN shortlist via `_candidate_jobs_for_resume`; ensemble routes fuse multiple exhaustive lists with RRF k=60. **No LLM rerank in this file.**  
**Patterns:** procedural, global mutable state, sync handlers  
**Global state at import:** `store`, `active_vector_store`, `resumes`, `jobs`, `real_jobs_config`, `real_jobs_state`

#### compute_scores_for_pair(resume, job, strategy, metric)
**Purpose:** Route strategy string to semantic or multimodal scorer.  
**Params:** `strategy` accepts `"cosine"` as alias for `"semantic"` via `normalize_strategy`.  
**Returns:** `(scores_dict, normalized_strategy)` where scores has `semantic_score`, `skills_score`, `final_score`.  
**Calls:** `compute_semantic` or `compute_multimodal` (always Jaccard skills · no `skills_mode` param exposed).  
**Called by:** all match, ensemble, daily, and agent endpoints.

#### rrf_aggregate(result_runs, key_field, base_k=60)
**Purpose:** Fuse multiple ranked lists via reciprocal rank fusion.  
**Params:** `result_runs` = list of sorted lists; each item must have `similarity`, `weight_used`, `strategy_used`, `metric_used`, and `key_field` (job_title or candidate_name).  
**Returns:** Sorted list with `fused_score`, averaged semantic/skills scores, `sources[]` per contributing list.  
**Formula:** contribution = `weight * (1 / (base_k + rank))`.  
**Called by:** `match_resume_ensemble`, `match_job_ensemble`.

#### _candidate_jobs_for_resume(resume, candidate_pool)
**Purpose:** ANN shortlist for daily recommendations and agent batch.  
**Params:** `candidate_pool` clamped to `[1, len(jobs)]`.  
**Returns:** List of job dicts from ANN search; falls back to first N jobs if search fails or returns empty.  
**Calls:** `embed_resume`, `store.search_jobs`.  
**Called by:** `candidate_daily_recommendations`, `run_daily_recommendations`.

#### _build_why_ranked(resume, job, scores, strategy)
**Purpose:** Generate human-readable ranking bullets for daily/agent output.  
**Returns:** Up to 4 reason strings: skill overlap (raw lowercase set intersection), title/summary token overlap, semantic tier (≥0.65 high, ≥0.5 moderate), multimodal blend note.  
**Note:** Does NOT use `skill_catalog` · raw string intersection only.

#### _sync_real_jobs(reindex=True)
**Purpose:** Fetch external jobs, write snapshot, replace in-memory jobs, optional reindex.  
**Errors:** 400 if `REAL_JOBS_ENABLE` false; 502 on fetch/normalize failure; updates `real_jobs_state.last_error`.

#### match_resume / match_job (route handlers)
**Purpose:** Exhaustive pairwise scoring over entire corpus.  
**Lookup:** resume by `name`, job by `title`. Not-found returns `{"error": "..."}` with HTTP 200.  
**Output fields:** job_title/candidate_name, semantic_score, skills_score, similarity, metric_used, strategy_used, vector_store_used, rank.

#### run_daily_recommendations (route handler)
**Purpose:** Batch agent · optional sync, loop all resumes (or `max_users` subset), write dated JSON to `data/daily_recommendations_YYYY-MM-DD.json`.  
**Default:** `sync_before_run=True`, `candidate_pool=120`, `max_users=0` (all 30 resumes).

#### 14 HTTP endpoints

| Method | Path | Retrieval path |
|--------|------|----------------|
| POST | `/match-resume` | Exhaustive all jobs |
| POST | `/match-job` | Exhaustive all resumes |
| POST | `/match-resume-ensemble` | Exhaustive per search config → RRF |
| POST | `/match-job-ensemble` | Same, job→resume direction |
| POST | `/candidate/daily-recommendations` | ANN pool → score → why_ranked |
| POST | `/agent/run-daily-recommendations` | Batch ANN + JSON file |
| GET | `/resumes`, `/jobs` | Name/title lists |
| GET | `/resumes/full`, `/jobs/full` | Full objects |
| GET | `/real-jobs/status` | Sync config + state |
| POST | `/real-jobs/sync` | External fetch + reindex |
| GET | `/system-config` | Active store, supported options |
| POST | `/system-config/vector-store` | Switch backend + full reindex |

---

### backend/matching/similarity_engine.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Central scoring orchestrator · semantic-only and weighted multimodal blends.  
**Dependencies:** imports from: `semantic_similarity`, `skills_similarity`, `soft_skills` | used by: `app.py`, all benchmark drivers  
**Patterns:** functional, pure scoring (no I/O)

#### compute_semantic(resume, job, metric="cosine")
**Purpose:** Bi-encoder document similarity only.  
**Returns:** `{semantic_score, skills_score: None, final_score, skills_details: None}`.  
**Calls:** `semantic_similarity_resume_job`.

#### compute_multimodal(resume, job, metric="cosine", skills_mode="jaccard")
**Purpose:** Convenience wrapper with fixed w=0.7.  
**Calls:** `compute_multimodal_weighted`.

#### compute_multimodal_weighted(resume, job, metric, semantic_weight=0.7, skills_mode="jaccard")
**Purpose:** Weighted blend · paper's primary scoring function.  
**Params:** `skills_mode`: `"jaccard"` → set Jaccard on canonical skills; `"embedding"` → soft overlap (best nDCG driver).  
**Formula:** `final = w * semantic + (1-w) * skills`.  
**Returns:** Includes `semantic_weight`, `skills_weight`, optional `skills_details` (embedding mode only).  
**Raises:** `ValueError` if semantic_weight ∉ [0, 1].  
**Called by:** `app.compute_scores_for_pair` (Jaccard only), `paper_progression`, `phase11.score_pair`.

---

### backend/matching/embedding.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Lazy singleton SentenceTransformer; encodes resume/job via document templates.  
**Dependencies:** imports from: `document_text` | used by: `ingestion`, `app._candidate_jobs_for_resume`, `semantic_similarity`, `soft_skills`, benchmarks  
**Env:** `EMBEDDING_MODEL` (default `all-MiniLM-L6-v2`), `BENCHMARK_RICH_TEMPLATES`, `BENCHMARK_NO_CANONICAL_SKILLS`

#### get_model()
**Purpose:** Load or reuse SentenceTransformer; reloads if model name env changes.  
**Returns:** 384-d MiniLM by default.

#### embed_resume(cv) / embed_job(job)
**Purpose:** Template text → numpy embedding vector.  
**Params:** Optional `rich`, `canonical_skills` override env flags via `template_flags()`.  
**Calls:** `resume_document_text` / `job_document_text`, then `model.encode`.

#### model (module-level _ModelProxy)
**Purpose:** Lazy proxy so `soft_skills` can call `model.encode(skill)` without eager load.

---

### backend/matching/document_text.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Normative text serialization for bi-encoder and lexical IR · field order matters for reproducibility.  
**Dependencies:** imports from: `skill_catalog` | used by: `embedding`, `lexical_retrieval`, benchmarks  
**Key Elements:** `resume_document_text`, `job_document_text`, `_format_skills`

#### resume_document_text(cv, rich=False, canonical_skills=True)
**Default template lines:** `resume profile`, `name:`, `experience_years:`, `work_mode:`, `skills:`, `summary:`  
**Rich mode:** Longer prose blocks when `BENCHMARK_RICH_TEMPLATES=1` (+0.011 nDCG in progression).

#### job_document_text(job, rich=False, canonical_skills=True)
**Default template lines:** `job description`, `title:`, `company:`, `location:`, `job_type:`, `required_experience_years:`, `work_mode:`, `required_skills:`, `description:`, `apply_link:`

---

### backend/matching/semantic_similarity.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Pairwise bi-encoder score · embeds both documents fresh each call (no vector cache at pair level).  
**Calls:** `embed_resume`, `embed_job`, `compute_similarity(metric)`.

---

### backend/matching/soft_skills.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Embedding-based skill overlap · **best exhaustive nDCG driver** (0.969 @ w=0.7).  
**Dependencies:** imports from: `embedding.model`, `skills_similarity.normalize` | used by: `similarity_engine`, `paper_progression`  
**Module cache:** `_skill_cache` dict keyed by normalized skill string.

#### compute_soft_overlap(resume_skills, job_skills)
**Purpose:** For each required job skill, find max cosine to any resume skill embedding; return mean.  
**Returns:** 0.0 if either skill list empty.

#### compute_soft_skill_details(resume_skills, job_skills)
**Purpose:** Per job-skill best-match pairs for diagnostics/UI.  
**Returns:** `{pairs: [{job_skill, best_resume_skill, score}]}`.

---

### backend/matching/skills_similarity.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Jaccard index on canonicalized skill sets.  
**Key Elements:** `skills_similarity`, `normalize` (lowercase trim)

---

### backend/matching/skill_catalog.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Synonym map before Jaccard/soft overlap and template formatting.  
**Key Elements:** `canonical_skill`, `canonicalize_skills`, `_SYNONYMS` (~30 aliases: react.js→react, ml→machine learning, torch→pytorch, etc.)  
**Used by:** `document_text`, `skills_similarity`

---

### backend/matching/lexical_retrieval.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Full-corpus BM25 and TF-IDF rankers for Table 9 baselines.  
**Key Elements:** `LexicalRanker`, `_BM25` (k1=1.5, b=0.75)  
**Dependencies:** imports from: `document_text`, `text_tokenizer` | used by: `paper_progression`, `phase11.evaluate_lexical_config`

#### LexicalRanker.rank_jobs(resume, method, top_k)
**Params:** `method` ∈ `"bm25"`, `"tfidf"`.  
**Returns:** List of `(job_id, score)` sorted descending over all jobs.

---

### backend/matching/cross_encoder_rerank.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Two-stage rerank on shortlist · ms-marco cross-encoder.  
**Env:** `CROSS_ENCODER_MODEL`  
**Blend:** `0.4 * prior_score + 0.6 * ce_norm` after min-max normalize within pool.  
**Used by:** `paper_progression` last ladder row only (nDCG 0.939, below soft embed 0.969).  
**Not wired to:** HTTP API or frontend.

---

### backend/matching/similarity.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Vector math on precomputed embeddings.  
**Key Elements:** `cosine_similarity`, `euclidean_similarity` (= 1/(1+dist)), `compute_similarity(metric)`

---

### backend/matching/text_tokenizer.py
**Language:** python | **Importance:** LOW | **Indexed:** 2026-05-27  
**Purpose:** tiktoken cl100k_base tokenization with regex fallback for lexical indexing.

---

### backend/ingestion.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Load corpus JSON, validate via Pydantic, embed all entities, upsert to vector store.  
**Dependencies:** imports from: `matching.embedding`, `schemas` | used by: `app.py` startup, `phase11` per-config reindex

#### load_data()
**Returns:** `(resumes, jobs)` as list of dicts from `data/cvs.json` + `data/jobs.json`.  
**Validation:** `Resume(**r).dict()`, `Job(**j).dict()` · extra JSON fields stripped by Pydantic.

#### ingest_data(store, resumes, jobs)
**Side effects:** Prints progress; upserts each entity with `_clean_metadata` (flattens list fields to comma strings for Chroma compatibility).

---

### backend/schemas.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Pydantic v2 models for corpus validation.  
**Resume fields:** id, name, skills, experience_years, preferred_salary, remote_preference, summary  
**Job fields:** id, title, required_skills, required_experience, budget, remote_policy, description  
**Note:** Optional job fields (company, location, link) exist in JSON but not in strict schema · passed through if loaded without validation.

---

### backend/stores/vector_store_factory.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Backend selection from `VECTOR_STORE` env or explicit argument.  
**Returns:** `(store_instance, "chroma"|"qdrant")` tuple.  
**Raises:** `ValueError` for unsupported backend.

---

### backend/stores/vector_store.py (Chroma)
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Default HNSW vector index via chromadb persistent client.  
**Persist:** `backend/chroma_db/` | **Collections:** `jobs_collection{suffix}`, `resumes_collection{suffix}`  
**Env:** `CHROMA_SPACE` (cosine/l2/ip), `CHROMA_COLLECTION_SUFFIX`  
**Implements:** `add_job`, `add_resume`, `search_jobs`, `search_resumes`, `get_all_*`

---

### backend/stores/qdrant_vector_store.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Qdrant local path client · ~2× faster latency in phase11 sweep.  
**Persist:** `backend/qdrant_db/` | **Point IDs:** UUID5 from `job:{id}` / `resume:{id}`  
**Env:** `QDRANT_HNSW_EF`, `QDRANT_HNSW_M`, `QDRANT_EF_CONSTRUCT`, `QDRANT_COLLECTION_SUFFIX`  
**Distance:** Fixed COSINE 384-d; search converts score to distance as `1 - score`.

---

### backend/stores/base_vector_store.py
**Language:** python | **Importance:** LOW | **Indexed:** 2026-05-27  
**Purpose:** Abstract interface documenting expected store methods.

---

### backend/benchmarks/paper_progression.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Table 9 method ladder · exhaustive scoring over all 15 jobs, 30 queries.  
**Run:** `python -m benchmarks.paper_progression`  
**Outputs:** `paper_progression_summary.json`, `paper_progression_per_query.csv`, `paper_bootstrap_significance.json`, `paper_failure_cases.json`

#### main() ladder order
1. TF-IDF, BM25 (LexicalRanker)  
2. Semantic cosine  
3. Multimodal Jaccard w=0.7  
4. Multimodal soft embed w=0.7 ← **best**  
5. RRF over [sem cos, mm Jaccard cos, **soft embed cos**, mm Jaccard euc] ← differs from paper §4 text  
6. Semantic cosine (rich templates)  
7. Soft embed + cross-encoder (pool=10)  
8. Optional: BGE-small embedder ablation

#### paired_bootstrap_ndcg(per_query, baseline, compare)
**Purpose:** 5000 resample bootstrap on nDCG diffs; reports mean diff + 95% CI.

#### failure_cases(...)
**Purpose:** Queries where compare method recovers relevant jobs missed by baseline (BM25 vs soft embed).

---

### backend/benchmarks/phase11.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Table 10 · 40-config ANN sweep (pool=10, 3 latency repeats × 30 queries).  
**Run:** `python -m benchmarks.phase11`  
**Skills mode:** Jaccard only via `score_pair` → `compute_multimodal_weighted` (no soft embed in grid)

#### evaluate_config(...)
**Purpose:** Set env vars for one store/config, reindex fresh collection, loop queries with timed ANN search + rerank.  
**Returns:** `(summary_row, per_query_rows)` for CSV aggregation.

#### get_source_id(results, idx, job_title_to_id)
**Purpose:** Resolve ANN hit to job_id from metadata `_source_id`, `id`, or title fallback.

---

### backend/benchmarks/research_sweep.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Fair pool-size comparison and **paper-aligned RRF** (sem cos, mm Jaccard cos, sem euc, mm Jaccard euc).  
**Key Elements:** `rank_exhaustive`, `rank_ann_pool`, `rrf_fuse`

---

### backend/benchmarks/metrics.py
**Language:** python | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Shared graded IR metrics with rel=2 weighting in DCG.  
**Key Elements:** `precision_at_k`, `recall_at_k`, `ndcg_at_k`, `eval_rankings`, `aggregate_query_metrics`

---

### backend/real_jobs_sync.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Paginated HTTP fetch from external jobs API → normalized snapshot JSON.  
**Key Elements:** `RealJobsConfig.from_env()`, `fetch_all_jobs`, `write_snapshot`, `load_snapshot`  
**Env:** `REAL_JOBS_ENABLE`, `REAL_JOBS_BASE_URL`, `REAL_JOBS_PATH`, `REAL_JOBS_PAGE_LIMIT` (max 50), `REAL_JOBS_OUTPUT_PATH`  
**Output:** `data/jobs_live.json` with dedupe counts and UTC timestamps

---

### backend/paths.py
**Language:** python | **Importance:** LOW | **Indexed:** 2026-05-27  
**Constants:** `DATA_DIR`, `BENCHMARK_OUTPUTS_DIR`, `CHROMA_DB_DIR`, `QDRANT_DB_DIR` · all Path objects relative to repo root.

---

### backend/tests/ (63 tests)
**Importance:** HIGH | **Indexed:** 2026-05-27  
**conftest.py:** `sample_resume`, `sample_job`, `eval_map_simple`, autouse `_reset_embedding_env`  
**Gaps:** No isolated tests for `cross_encoder_rerank`, `qdrant_vector_store`, `real_jobs_sync` HTTP, frontend E2E.

| File | Count | Focus |
|------|-------|-------|
| test_api.py | 20 | All 14 routes, 400/422 errors, parametrized strategies |
| test_benchmark_metrics.py | 5 | nDCG math, perfect ranking |
| test_lexical_retrieval.py | 5 | BM25, TF-IDF ordering |
| test_similarity_engine.py | 4 | semantic, jaccard, embedding mode, invalid weight |
| test_soft_skills.py | 3 | overlap perfect/empty, details shape |
| test_skill_catalog.py | 5 | alias normalization |
| test_document_text.py | 5 | template flags, rich mode |
| test_embedding_config.py | 4 | env model name, proxy encode |
| test_integration_data.py | 3 | eval_pairs integrity, progression JSON exists |
| test_research_sweep_utils.py | 2 | RRF consensus ordering |
| test_skills_similarity.py | 4 | Jaccard edge cases |
| test_text_tokenizer.py | 3 | fallback tokenization |

---

## Module: frontend

> **[LEGACY partial]** Old App.jsx debug console entries below. Current product portals live under `frontend/src/pages/{candidate,employer,admin}/` · see [Module: rewrite (current)](#module-rewrite-current).

### frontend/src/main.jsx
**Language:** javascript | **Importance:** LOW | **Indexed:** 2026-05-27  
**Purpose:** React 19 entry · mounts `<App />` with StrictMode.

---

### frontend/src/App.jsx
**Language:** javascript (React 19) | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Entire dashboard in one ~1812-line file · matching UI, ensemble, ops, theme, persistence.  
**Stack:** React 19, Vite 7, axios; styling via `App.css` (FORGE theme), Tailwind configured but unused for layout.  
**Dependencies:** axios → backend 14 endpoints | used by: browser user  
**Patterns:** hooks, useMemo enrichment pipeline, localStorage persistence

#### State machine (key useState hooks)

| State | Default | Role |
|-------|---------|------|
| `mode` | `"resume"` | resume→jobs vs job→resumes |
| `selectedValue` | `""` | Active entity from dropdown |
| `topK` | 5 | Results count (1–10) |
| `strategy` / `metric` | semantic / cosine | Passed to match API |
| `useEnsemble` | false | Switches to RRF endpoints |
| `selectedSearches` | all 4 combo ids | Ensemble checkbox selection |
| `useLiveRecommendations` | false | `/candidate/daily-recommendations` |
| `results` | [] | Raw API response items |
| `savedConfigs` / `recentRuns` | from localStorage | Presets + history |
| `vectorStore` | from `/system-config` | Display + switch trigger |
| `agentRunSummary` | null | Last batch agent response |

#### handleMatch()
**Purpose:** Primary user action · routes to correct endpoint based on mode/ensemble/live toggles.  
**Live path:** POST `/candidate/daily-recommendations` (resume mode, non-ensemble only).  
**Ensemble path:** Builds `searches[]` from `availableSearches` filtered by `selectedSearches`, weight hardcoded to 1.  
**Standard path:** POST `/match-resume` or `/match-job` with strategy/metric.  
**Post-process:** Sets `results`, appends to `recentRuns`, clears errors.

#### scoreStats / normalizedResults / enrichedResults (useMemo chain)
**Purpose:** Detect clustered low scores and min-max normalize for display.  
**Trigger:** `max > 1 || min < 0 || max <= 0.2` · matches paper §5.2 description.  
**Enrichment:** Adds `label`, `scorePercent`, `band` (high/mid/low), client-side `explanation` via `buildExplanation`.

#### buildExplanation({ item, mode, selectedValue, resumeLookup, jobLookup, normalizedScore })
**Purpose:** Client-side "Why this match?" parallel to backend `_build_why_ranked`.  
**Returns:** `{ headline, topMatchingSkills, missingSkills, semanticNote, confidenceTier }`.  
**Uses:** `normalizeSkill` for overlap; does not call skill_catalog.

#### handleVectorStoreChange(nextStore)
**Purpose:** POST `/system-config/vector-store`, reload config, clear results.  
**UX:** Sets `switchingStore` loading flag; error toast on failure.

#### handleSaveConfig / handleApplyConfig
**Purpose:** Persist/restore full UI snapshot to `jobMatcher.savedConfigs.v1` (max 20 entries).  
**Snapshot fields:** mode, topK, strategy, metric, useEnsemble, selectedSearches, vectorStore.

#### SmoothDropdown (component, ~line 262)
**Purpose:** Accessible type-ahead select for resume/job names · keyboard nav, filtered options.

#### Paper vs UI gaps (not implemented)
- `skills_mode` (Jaccard vs soft embed) · backend supports via `compute_multimodal_weighted` but API doesn't expose it  
- LLM rerank toggle · not in backend or frontend  
- Per-search ensemble weights · always 1.0  
- `candidate_pool` on standard match · only on daily endpoints

---

### frontend/src/App.css
**Language:** css | **Importance:** MEDIUM | **Indexed:** 2026-05-28  
**Purpose:** Primary design system · imports theme layers (tokens, dark-mode, polish, page-shell, candidate-onboarding).  
**Key Elements:** portal panels, match drawer (400px/100dvh), applicant-row grid, employer job cards, match summary cards, responsive breakpoints  
**Core Logic:** `--page-max-width: 1120px`; drawer scrim via tokens; `.scroll-content` 96px bottom pad; compact summary cards (72px min-height).

---

### frontend/src/index.css
**Language:** css | **Importance:** LOW | **Indexed:** 2026-05-27  
**Purpose:** Base Vite/Tailwind reset imports.

---

## Module: data

### data/eval_pairs.json
**Importance:** HIGH  
**Content:** 30 query resumes, 47 labeled pairs (21× rel=2, 26× rel=1); drives all paper metrics.

### data/cvs.json
**Importance:** HIGH | 30 synthetic resumes

### data/jobs.json
**Importance:** HIGH | 15 job postings (small corpus → high lexical R@5 when exhaustive)

---

## Module: submission-pdfs

### docs/submission/jaamas/manuscript/main.pdf
**Language:** pdf | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** Compiled JAAMAS submission (~33 pages local). Source: `main.tex` + 7 section files + `algorithms/` + `tables/tab-*.tex`.  
**Structure:** Abstract → §1 Introduction → §2 Literature Review → §3 Multi-Agent Architecture → §4 Implementation → §5 Quality Metrics → §6 Results and Discussion → §7 Conclusion and Future Scope → Declarations → References.

**Key tables:** `tab-dataset`, `tab-methods`, `tab-progression`, `tab-fusion`, `tab-ablation`, `tab-latency`, `tab-fairness`, `tab-hard-negs`, `tab-model-params`, `tab-workflows` (numbers from committed benchmark artifacts).

---

### docs/submission/jaamas/manuscript/main.tex
**Language:** latex | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** JAAMAS document class, reframed abstract (~163 words), keywords, `\input` chain for 7 sections + declarations.  
**Title:** JobMatch: An Agentic Multi-Role Platform for Explainable Job--Candidate Matching.

---

### docs/submission/jaamas/build_all.sh
**Language:** bash | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Rebuild manuscript PDF, portal PDFs, supplementary SI, and Overleaf zip in one command.

---

### scripts/generate_jaamas_figures.py
**Language:** python | **Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Emit draw.io XML for Figs 1–5 (academic greyscale palette). Export PDF **without `--crop`** — crop produced unusable ~47 pt tall PDFs.

---

### docs/submission/jaamas/manuscript/Agentic Job Matching.pdf
**Language:** pdf | **Importance:** LOW | **Indexed:** 2026-05-24 | **[LEGACY]**
**Purpose:** Old 31-page draft (9 sections). Superseded by `main.pdf`.

---

### docs/submission/jaamas/portal/cover-letter.pdf
**Importance:** MEDIUM | **Indexed:** 2026-05-27  
**Purpose:** Editor cover letter (2–3 paragraphs, JAAMAS fit). Rebuilt via `portal/build_cover_letter.sh`.

---

### docs/submission/jaamas/portal/information-sheet.pdf
**Importance:** MEDIUM | **Indexed:** 2026-05-24  
**Purpose:** Springer mandatory Q&A (3 pages).  
**Authors:** Harsh Kashyap (corresponding), Taranumpreet Kaur Wasu, supervisor Dr Parteek Kumar (WSU).  
**Evidence:** Dual protocol tables identical to README; artifact list (14 endpoints, drivers, datasets, supplementary JSON/CSV).

---

## Module: docs/submission/jaamas

> **Current structure:** See **JAAMAS Manuscript · Complete Architecture Reference** (v2 block at top). Legacy 9-section file index below marked **[LEGACY]**.

### Per-file index (manuscript/ · current)

| File | Responsibility |
|------|----------------|
| `main.tex` | Document class, abstract, keywords, 7-section `\input` chain |
| `jaamas-style.tex` | JTable/JFigure floats, page rhythm |
| `jaamas-macros.tex` | `\modelname`, metrics, `\figcap`, `\figref` |
| `sections/section-1-introduction.tex` | Story intro, Sal Khan vision, 6 contributions (fix “engine”→agent), paper map |
| `sections/section-2-literature-review.tex` | 6 themed subsections, gaps, positioning; 12 citation TODOs |
| `sections/section-3-architecture.tex` | 3 agents, §3.4 communication, Algorithm 1, Figs 1–3 |
| `sections/section-4-implementation.tex` | Gateway, agents, stores, portals, params, reproducibility, Fig 4 |
| `sections/section-5-quality-metrics.tex` | Formulas + metric definitions only; benchmark criteria; no numeric results |
| `sections/section-6-results-discussion.tex` | Narrative results + 8 interpreted tables incl. method-comparison |
| `sections/section-7-conclusion-future.tex` | Decision-support conclusion; 8 future-scope items |
| `algorithms/alg-multi-agent-matching.tex` | Algorithm 1 — 15-step multi-agent matching workflow |
| `sections/declarations.tex` | Springer declarations |
| `tables/tab-*.tex` | 10 tables wired from benchmark JSON |
| `references.bib` | 7 numeric citations |

### figures/ (current)

| Figure | Used in | Depicts |
|--------|---------|---------|
| Fig1.pdf | §3 | Multi-agent system overview |
| Fig2.pdf | §3 | Agent communication / event flow |
| Fig3.pdf | §3 | End-to-end workflow |
| Fig4.pdf | §4 | Implementation / API layer |
| Fig5.pdf | §5 | Metrics / evaluation pipeline |

Sources: `figures/source/FigN.drawio` · regenerate via `scripts/generate_jaamas_figures.py`.

### build/ and scripts (current)

| Script | Output |
|--------|--------|
| `docs/submission/jaamas/build_all.sh` | All submission PDFs + Overleaf zip |
| `archive/dev-scripts/make_overleaf_zip.sh` | `build/jaamas-overleaf-upload.zip` |
| `portal/build_cover_letter.sh` | `portal/cover-letter.pdf` |
| `portal/build_info_sheet.sh` | `portal/information-sheet.pdf` |
| `scripts/generate_jaamas_figures.py` | draw.io sources for Figs 1–5 |

### [LEGACY] Per-file index (9-section draft)

| File | Lines (approx) | Responsibility |
|------|----------------|----------------|
| `sections/section-1.tex` | 42 | Old introduction |
| `sections/section-2.tex` | 69 | Literature (6 subsections) |
| `sections/section-3.tex` | 120 | Architecture + Figs 1–7 |
| `sections/section-4.tex` | 222 | Methodology algebra + schema tables |
| `sections/section-5.tex` | 108 | Realization: API Table 6, frontend, sync, batch |
| `sections/section-6.tex` | 97 | Evaluation protocol + sweep design |
| `sections/section-7.tex` | 119 | Results Tables 8–11 |
| `sections/section-8.tex` | 11 | Conclusion |
| `sections/section-9.tex` | 37 | Future work (5 subsections) |
| `sections/appendix-recommendations.tex` | 14 | Production recommendation bullets |
| `declarations.tex` | 26 | Springer Declarations (funding, data, code, contributions) |
| `acknowledgments.tex` | 2 | Dr Parteek Kumar + Thapar |
| `references.bib` | 7 entries | Numeric citations |

### figures/

| Figure | Used in | Depicts |
|--------|---------|---------|
| Fig1.pdf | §3.2 | High-level modules |
| Fig2.pdf | §3.3 | Presentation layer |
| Fig3.pdf | §3.4 | Application/API layer |
| Fig4.pdf | §3.5 | Matching core |
| Fig5.pdf | §3.6 | Data plane |
| Fig6.pdf | §3.7 | LLM rerank + offline benchmark |
| Fig7.pdf | §3.8 | End-to-end consolidated diagram |
| Fig8–10.pdf | (archive/supplementary) | May exist for SI or legacy · check `figures/README.md` |

### build/ and scripts

| Script | Output |
|--------|--------|
| `archive/dev-scripts/build.sh` | Local `main.pdf` via sn-jnl |
| `archive/dev-scripts/make_overleaf_zip.sh` | `build/jaamas-overleaf-upload.zip` |
| `archive/dev-scripts/build_cover_letter.sh` | `portal/cover-letter.pdf` |
| `archive/dev-scripts/build_info_sheet.sh` | `portal/information-sheet.pdf` |
| `archive/dev-scripts/prepare_manuscript.py` | Legacy body.tex → sections (avoid unless regenerating from report) |

### supplementary/

Shipped with submission; numbers must match `backend/benchmark_outputs/` after re-run.

### portal/

Editor-facing; **must stay metric-consistent** with Table 9/10 and abstract when architecture changes.

---

## Module: docs

### docs/report/Agentic Job Matching.pdf
**Purpose:** Technical report PDF (XeLaTeX from `docs/latex/`). README: “read for detailed understanding.”

### docs/report/DOCUMENTATION.md
**Purpose:** Canonical Markdown report · edit first, sync via `python3 docs/latex/build_from_md.py`

### docs/latex/main.tex
**Engine:** XeLaTeX; `\documentclass` in main.tex; `\raggedbottom`; May 2026 date.

### docs/DOCUMENTATION_HUB.md
**Purpose:** Index for all documentation trees.

---

## Module: root

### README.md
**Language:** markdown | **Importance:** HIGH | **Indexed:** 2026-05-27  
**Purpose:** GitHub landing · full onboarding for multi-agent rewrite: architecture diagram, three-agent model, composite scoring, setup, API reference, demo accounts, tests (208+20), troubleshooting.  
**Dependencies:** links to HLD, SDD, V1-V2 scope, demo script, session notes  
**Note:** Supersedes legacy dual-metric-table README; no longer points to monolith `app.py` on port 8000.

### .gitignore
**Ignores:** `HANDOFF.md`, `.venv311/`, `daily_recommendations_*.json`, local `benchmark_outputs/*` (except phase11 CSVs), `main.pdf`, portal/build aux, latex zips.

---

## Key flows

```
┌─────────────────────────────────────────────────────────────────┐
│ PRODUCT MATCH (rewrite · current)                               │
│ Portal → api/client.runMatch(strategy: composite)              │
│ → gateway/routes/matching → MatchmakingAgent                  │
│ → score_pair_advanced → compute_composite (28/27/10/15/10/10) │
│ → MatchDetailsDrawer (6-bar breakdown + gaps + coach)         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ CANDIDATE ONBOARDING                                            │
│ upload-resume → document_parse (clean → rule → LLM → quality)   │
│ → ExtractedSectionsPanel + ProfileQualityPanel (debounced)      │
│ → review form → PUT /candidates/me (upsert) → link ownership    │
│ → Matches: fetchMyProfileOrNull (null | stale | ready)          │
│ → runMatch(queryKey=name) · auto-search if searchAfterSave      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STALE PROFILE RECOVERY                                          │
│ GET /candidates/me → 404 PROFILE_NOT_FOUND (link kept)          │
│ → client returns PROFILE_STALE_MARKER                           │
│ → Profile/Matches show restore UI → PUT /me recreates in agent  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ EMPLOYER JD INGEST                                              │
│ paste text → parse_job_document (rule + LLM + quality)          │
│ OR upload file → same pipeline via POST /jobs/upload-description│
│ → JobQualityPanel debounced · review JobPostingForm → register  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STARTUP                                                         │
│ main.create_app → bootstrap.create_system                       │
│ → load data/cvs.json + jobs.json → CorpusBootstrapped event     │
│ → seed_demo_accounts (demo.candidate → cv_01 Rahul Sharma)      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ RESEARCH PIPELINE (offline)                                     │
│ run_research_pipeline.py → validate → comparison → composite  │
│ → ablation → [CE] → significance → fairness → explainability  │
│ → paper_tables → backend/reports/research_run_<ts>/             │
│ Manuscript: docs/research/RESEARCH-PAPER.md                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ LEGACY BENCHMARK (preserved)                                    │
│ paper_progression / phase11 → eval_pairs.json → Table 9/10    │
└─────────────────────────────────────────────────────────────────┘
```

## Staleness

**Last refresh:** 2026-05-28 v13 · live jobs API ported; test reorg; error page UX; PortalShell fix · last push `9db6abc` (manuscript committed)  
**Stale sections in graph:** Legacy monolith `real_jobs_sync.py` path under Module: backend (legacy) — current impl is `core/real_jobs_sync.py`  
**Legacy drift:** Module: backend (legacy monolith) still documents removed `app.py` · use for benchmark reference only.  
**Known open items:** Commit product work (live jobs, tests, error UX); ~29 manuscript `\todo`s; 12 §2 citations; author placeholders; `REAL_JOBS_BASE_URL` in deployment; optional admin sync UI; API auth hardening if network-deployed; fix §1 “matchmaking engine” bullet  
**Refresh command:** `/knowledge refresh backend/core/real_jobs_sync.py` or `/knowledge refresh frontend/src/pages/errors/`
