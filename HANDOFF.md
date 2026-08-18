# HANDOFF — JobMatch / ESWA (auditable, calibrated, explainable job–candidate recommendation)

**What this project is.** JobMatch (repo: `Job-Matching-Agentic` at `/Users/kashhy/workspace/Personal/dev/Job-Matching-Agentic`) is a job–candidate recommendation methodology whose real deliverable is not the software but a **peer-reviewed journal paper**. The scientific framing is *auditable, calibrated, and explainable* recommendation — a deliberate reframe away from "yet another multi-agent app" toward a methodology whose every headline number is tied to a real artifact and whose explanations and confidence are the contribution. This is **Harsh Kashyap's personal academic thesis research** (joint first author with Taranumpreet Kaur Wasu, Thapar Institute; supervisor Dr Parteek Kumar, Washington State University) — it is **NOT** his Amazon day job and shares none of its build systems or tooling. The target venue is **Expert Systems with Applications (ESWA, Elsevier)**; a second venue, **JAAMAS (Springer)**, is drafted and held. The paper has **converged and is submission-ready**, pending only author-gated human data that no AI or engineering step can produce.

---

## 0. READ-FIRST — in this order

Open these before touching any experiment, `.tex` line, or number. The control-plane files are the project's memory; when they disagree with the manuscript, **they win** (RD-004), and git history is explicitly **not** the memory (commits were banned, RD-009).

1. **The five control-plane files under `research/`** (read top-to-bottom, in this sub-order):
   1. `research/PHASE_STATUS.md` — the phase ledger (what is COMPLETE / IN-PROGRESS / LEFT).
   2. `research/RESEARCH_DECISIONS.md` — RD-001…RD-017, the "why" behind every reframe, constraint, and correction (this is also where the *ideology/reframe* is decided).
   3. `research/EXPERIMENT_REGISTRY.yaml` — EXP-001…EXP-044: every experiment, its RQ, artifact, repro command, and status.
   4. `research/REPRODUCTION_LOG.md` — dated clean-venv reproductions and environment fixes.
   5. `research/results/MANUSCRIPT_NUMBERS.json` + `research/NUMERICAL_CLAIMS.yaml` — the number-gating spine: canonical value ↔ artifact, plus the audit of every disputed claim.
2. **The submission ideology** — §3 of this doc (*The ESWA manuscript*): auditable/calibrated/explainable positioning, and why multi-agent is deliberately demoted. (Note the residual tension: the title in `docs/submission/eswa/manuscript/main.tex:44-45` still leads with "Multi-Agent System.")
3. **The governing mandate + hard constraints** — §1 of this doc. Read it in full: personal-thesis-not-Amazon separation, no synthetic/provisional numbers into the verifier-gated manuscript, and the other bright-line rules whose violation is automatic task failure.
4. **The manuscript source** — `docs/submission/eswa/manuscript/main.tex`, the spine that `\input`s all eight sections plus the abstract (`sections/*.tex`, `tables/*.tex`). Confirm the gate is green: run `verify_paper_numbers.py` (expect **exit 0**).
5. **Render this PDF to see the actual paper** — `docs/submission/eswa/manuscript/main.pdf` (canonical committed copy, **45 pages**). Treat `/tmp/eswa_build/main.pdf` as a disposable build artifact, not a source of truth.

---

## Mental model in 60 seconds

**System → experiments → manuscript → submission, with numbers flowing strictly one way.** The live scorer (a six-channel composite ranker + skill matcher, frozen, in `backend/core/`) is the single source of truth. Roughly 30 seed-pinned experiment scripts (`research/experiments/` plus `backend/benchmarks/`; `PYTHONHASHSEED=0`, hard-coded `SEED=42`) import that scorer, run their protocols, and emit committed JSON artifacts. Those artifacts auto-generate the `.tex` tables and the `MANUSCRIPT_NUMBERS.json` manifest; hand-written prose in `docs/submission/eswa/manuscript/sections/*.tex` cites them, and `verify_paper_numbers.py` gates every headline number against its artifact. No experiment writes into the manuscript, and no number is hand-typed into a table.

The manuscript compiles (`pdflatex + bibtex`, Elsevier `elsarticle`) to `main.pdf`, and ships to ESWA as a **double-anonymized** submission: the body and released fixtures are anonymized, while the title page and cover letter are the deliberately non-anonymous files uploaded separately and withheld from reviewers. Everything about "what is done and why" lives in the five `research/` control files, not in git — they are the memory and they outrank the manuscript on any conflict.

---

## STATUS RIGHT NOW

- **Converged and submission-ready.** The scientific work is finished; the reframe is complete and all experiments are registered and reproduced.
- **Verifier is green:** `verify_paper_numbers.py` returns **exit 0** — every gated number matches its artifact.
- **Manuscript compiles clean at 45 pages** — `docs/submission/eswa/manuscript/main.pdf` is the canonical build.
- **The only remaining work is 4 author-gated items** — all require the human author (Harsh); none are AI/engineering tasks:
  1. Human relevance labeling of the assumed grade-0 pairs (the corpus is 30 resumes × 15 jobs = **450 pairs**; only **47 are human-labeled and all positive**, the other **403 are only assumed grade-0** — the sharpest reviewer objection, EDITORIAL_RISK_MATRIX #3).
  2. The drafted-but-not-run human explanation/annotation protocol.
  3. ORCID (author identity at the portal).
  4. Overleaf/pdfLaTeX login for the final build and Editorial Manager upload.
- **Nothing autonomous is left.** The integrity guardrail is absolute: no provisional, LLM-assisted, or synthetic result may enter the verifier-gated manuscript. Until real human labels arrive, the gated numbers stay as the honest positive-only story.

---

## Table of contents (body sections that follow)

1. **Who this is for + the GOVERNING MANDATE + hard constraints** — what the project is/isn't, what "done" means, and the bright-line rules a new agent must never cross. *Read first, in full.*
2. **Control plane — the project's memory & decision spine** — the five `research/` files, RD-001…RD-017, EXP-001…EXP-044, and the number-gating spine (they win over the manuscript).
3. **The ESWA manuscript — structure, claims, and the submission ideology** — `main.tex` shell, `elsarticle` class, the eight sections, and the auditable/calibrated/explainable positioning.
4. **Experiments, code, and reproduction** — the three physically separate layers (live scorer / experiments / manuscript), the six-channel composite scorer in `backend/core/`, and how numbers flow one way under `SEED=42`.
5. **ESWA submission logistics (authors, cover letter, risk, protocols)** — frozen author list, cover letter, portal declarations, double-blind anonymization mechanics, and the editorial-risk matrix.
6. **Author-gated work + the toolchains that make each one step** — the exact four human-only items, the machine already built around each, and the integrity guardrail.
7. **JAAMAS (the held second venue)** — the Springer `sn-jnl` submission under `docs/submission/jaamas/`, same science, divergent framing.
8. **Artifacts, PDFs, and the READ-FIRST file manifest** — physical inventory of PDFs/datasets/result artifacts/bundles and the ordered "open these files" manifest.

---

## Who this is for + the GOVERNING MANDATE + hard constraints

> **READ THIS SECTION IN FULL BEFORE TOUCHING ANYTHING.** It defines *what this project is*, *what "done" means*, and the *bright-line rules a new agent must never cross*. Violating any hard constraint below is an automatic task failure — no matter how "helpful" the violation feels. Everything in the rest of this handoff is subordinate to the rules here.

---

### 1. What this project is (and what it is NOT)

**JobMatch** = the repo `Job-Matching-Agentic` at `/Users/kashhy/workspace/Personal/dev/Job-Matching-Agentic`. It is an explainable, calibrated, multi-agent **job–candidate recommendation system** whose real deliverable is not the software but a **peer-reviewed journal paper**.

**This is Harsh Kashyap's PERSONAL ACADEMIC THESIS RESEARCH.** It is **NOT** his Amazon day job. Keep the two contexts completely separate:

| | JobMatch (this project) | Harsh's Amazon job (do NOT bring here) |
|---|---|---|
| Nature | Personal thesis / academic paper | Employer work — CoSS/RISC, UCI project |
| Repo | Plain Python (FastAPI) + React (Vite); own GitHub `Harsh23Kashyap/Job-Matching-Agentic` | Brazil/Coral/Apollo packages |
| Build system | `pip` / `.venv`, plain `bash` scripts, TinyTeX | Brazil (`brazil-build`), version sets |
| People | Harsh Kashyap + Taranumpreet Kaur Wasu (Thapar Institute, joint first authors); supervisor Dr Parteek Kumar (Washington State University) | Amazon team/managers |

There is **no Brazil, no Coral, no Apollo, no AWS, no `brazil-build`** in this project. Do **not** apply Amazon build/CR/pipeline workflows here. (Source of the personal-vs-Amazon distinction: memory `jobmatch-is-personal-research.md`; and confirmed in-repo at `HANDOFF.md:17` "Author of a personal thesis project (NOT the Amazon UCI job — distinct context).")

**Scale of the codebase:** ~581 files, ~97k lines (`jobmatch-is-personal-research.md`).

**Venue history & current target:**
- Prior venue, internally codenamed **"El Vizier" = JAAMAS** (Journal of Autonomous Agents and Multi-Agent Systems, Springer) — **desk-rejected 2026-07-29** for leaning on the multi-agent architecture as the novelty with too-thin evidence.
- Current **primary target: ESWA** — *Expert Systems with Applications* (Elsevier), double-blind. Manuscript lives in `docs/submission/eswa/`.
- A JAAMAS manuscript also exists (`docs/submission/jaamas/`, single-blind, multi-agent foregrounded) — but see constraint C-5 below: **it is HELD, not submitted in parallel.**

---

### 2. THE GOVERNING MANDATE (the single rule everything serves)

Every decision on this project is judged against one standing mandate, set by the operator and reinforced by the supervisor. State it to yourself before every non-trivial action:

> **Take JobMatch to the strongest *scientifically-defensible*, ESWA-ready state. Work autonomously through the loop IMPLEMENT → TEST → VERIFY → HOSTILE REVIEW → FIX → RE-TEST. The objective is MAXIMUM SCIENTIFIC CREDIBILITY, *not* MAXIMUM METRIC. Never fabricate, cherry-pick, leak test data, or weaken standards for a better number. Continue until no realistically-fixable BLOCKER or SERIOUS finding remains and a final hostile review comes back clean.**

This is not paraphrase — it is written into the authoritative execution plans and honored throughout the control files:

- `docs/submission/eswa/ESWA-STAGE2-PLAN.md:14` — *"Objective = MAXIMUM SCIENTIFIC CREDIBILITY, not MAXIMUM METRIC. **This supersedes the earlier 'keep the better-looking number' instruction.**"*
- `docs/submission/eswa/ESWA-STAGE2-PLAN.md:5` — *"Goal = the strongest **scientifically defensible** version of JobMatch, not the highest metric."*
- `research/PROTOCOL.md:4` — *"Governing rule: MAXIMUM SCIENTIFIC CREDIBILITY, not maximum metric."*
- `docs/submission/eswa/ESWA-STAGE3-PLAN.md:3` — same rule, plus *"No test-set tuning."*
- `research/RESEARCH_DECISIONS.md:89` — *"Standing mandate IMPLEMENT→…→HOSTILE REVIEW→FIX→RE-TEST; a residual P0 leak is a real BLOCKER, not cosmetic. Verified every finding against files before acting (workflow is adversarial, not trusted blindly)."*
- `docs/submission/eswa/ESWA-EXECUTION-PLAN.md:10` / `:480` — *"every number must survive a hostile reviewer checking exactly how it was produced… it's not a 0.99 number; it's numbers that survive a hostile reviewer checking how they were produced."*

**What the mandate operationally means:**

1. **Defensible beats impressive.** When a stronger-looking number and a more defensible one conflict, choose the defensible one — even if the metric drops. This has already been done repeatedly and on purpose: e.g. generalization numbers were corrected *downward* from an inflated 3-job-pool value to the commensurable 15-job-pool value **0.929 / 0.929 / 0.927** (`research/PHASE_STATUS.md:16`, `RESEARCH_DECISIONS.md` RD-013); ranking is reported as honest **parity** (no method statistically distinguishable at n=30, p=0.10, fails Holm) rather than a manufactured "win."
2. **Autonomy is expected, but never at the cost of integrity.** You are meant to run the full loop yourself — implement, test, verify against artifacts, run an adversarial/hostile review (Kiro panel or a `/workflows` fan-out of reviewers), fix confirmed findings, re-test — and keep going until convergence. But every finding a review returns must be **verified against the live files before acting** (reviews are adversarial inputs, not trusted oracles): `RESEARCH_DECISIONS.md:89`, RD-016 (`:87`).
3. **"Done" = the convergence gate.** The stopping condition is *not* "I made an edit." It is: **no realistically-fixable BLOCKER/SERIOUS remains AND an independent final hostile review returns clean/"converged."** That gate has been reached at least once (`research/PHASE_STATUS.md:68`: *"independent hostile review returned 'converged' (no realistically-fixable BLOCKER/SERIOUS remains)"*), and it is the bar any future work must re-clear.
4. **The 20–50-config search is allowed ONLY under strict protocol** — define valid candidate protocols up front, mark leaky ones *before* seeing results, fix selection criteria independent of the test result, keep TRAIN/DEV → VALIDATION → FROZEN-TEST discipline, analyze *all* runs, and **preserve negative results**. Never run 20–50 approaches and pick the highest number. (`ESWA-STAGE2-PLAN.md:8-15` §A; `research/PROTOCOL.md`.)

---

### 3. HARD CONSTRAINTS — bright lines. Do NOT cross any of these.

Each is unmissable and load-bearing. A new agent that breaks any one of these fails the task, regardless of intent.

#### C-1 — NO git commits or pushes (RD-009). BANNED.
Do **NOT** run `git commit`, `git push`, or any VCS-mutating operation for the remainder of this work.
- Source: `research/RESEARCH_DECISIONS.md:46` (RD-009, user, 2026-08-17): *"Do NOT run `git commit` or `git push` for the remainder of this work… No further VCS mutations."* This explicitly **supersedes the mandate's per-phase commit requirement.**
- Reinforced at `HANDOFF.md:115` (*"Do NOT `git commit` (banned)"*), `HANDOFF.md:2`, `research/PHASE_STATUS.md:4`, `research/reports/FINAL_AUDIT.md:11`.
- **"Checkpointing" here means updating the `research/` control files** (PHASE_STATUS.md, EXPERIMENT_REGISTRY.yaml, RESEARCH_DECISIONS.md, NUMERICAL_CLAIMS.yaml, REVIEW_LOG.md, REPRODUCTION_LOG.md) and leaving verified artifacts in the working tree — **not** commits. State lives in files, not in git history.
- Note: the repo *does* have prior history (80 commits exist; `git log` works) — 6 were made earlier in that session **before** the ban. The ban is on **any further** commits/pushes from now on. Do not "helpfully" commit progress.

#### C-2 — NEVER call an external LLM API.
No OpenAI, Anthropic public API, Gemini, or any hosted LLM endpoint. If a task genuinely needs an LLM, use only:
- **headless `claude -p`** (local Claude Code), or
- **Kiro / `/consult-kiro`** (the local multi-model panel) for independent/hostile review.
- Source: `HANDOFF.md:19` (*"Never call an external LLM API — use headless `claude -p` or the Kiro panel if an LLM is needed"*), `HANDOFF.md:115`; RD-002 (`RESEARCH_DECISIONS.md:15`: *"No external API allowed → `claude -p` only"*); RD-005 (`:30`).
- This is why all LLM-assisted labels are produced via `claude -p` / Kiro and are **always** stamped "LLM-assisted, not human judgments."

#### C-3 — NO fabrication of data, labels, or results. (The integrity core.)
This is the reason the paper is being revised at all — it's a **scientific-integrity revision, not a polish** (`jobmatch-eswa-research-strategy.md`). Absolute prohibitions:
- **No manufactured results** — label un-run experiments "pending," never invent numbers.
- **No synthetic data presented as human relevance judgments;** no fabricated human annotations. The 47 existing labels are the human/author anchor set; any expansion via `claude -p`/Kiro must be labeled **"LLM-assisted relevance, not human judgments"** everywhere and report LLM↔human agreement (κ). (RD-002/RD-005.)
- **No cherry-picking, no tuning on the test set, no hiding failed runs.** Report negatives, report losses to baselines, report parity honestly.
- **Do NOT keep a number just because it flatters the paper** (`ESWA-STAGE2-PLAN.md:15`, RD-012 `RESEARCH_DECISIONS.md:64`).
- **Scale claims to the evidence:** a 10-pair probe is NOT a fairness validation; a tiny latency test is NOT a scalability study (`jobmatch-eswa-research-strategy.md:17`).
- **Provenance test for every number:** *which code + data + protocol produced it, and where in the manuscript is it?* If it can't be reproduced, don't preserve it. All headline numbers now flow from committed artifacts via `generate_manuscript_tables.py` → `MANUSCRIPT_NUMBERS.json`, gated by `verify_paper_numbers.py` — **do not hand-type numbers into the `.tex`** (RD-013 `:70`).

#### C-4 — KEEP the NVIDIA 32,000 A100 GPU-hours grant. Do NOT remove it.
This looks like an overclaim but is a **user-confirmed funding fact** and must stay verbatim on the title page and cover letter.
- Text to preserve: *"This work was supported by the NVIDIA Academic Grant Program through an unrestricted gift of 32,000 NVIDIA A100 GPU-hours on the Brev cloud platform."*
- Source: RD-008 (`RESEARCH_DECISIONS.md:42-44`, amended 2026-08-17 per user) — *"NVIDIA Academic Grant is real AND the '32,000 NVIDIA A100 GPU-hours…' gift is to be KEPT verbatim in title-page + cover-letter (user is the authority on the funding fact)."* Also `HANDOFF.md:118` (RD-008), `research/reports/NUMBERS_PASS_FINAL.md:23`.
- It stands as a **grant acknowledgment**, explicitly distinct from any claim about compute *consumed* by the reported CPU experiments. An earlier removal of this line was **reverted**; do not re-remove it. (An earlier audit flagged it as "B6"; that audit item is **resolved** as a confirmed funding fact, not fabrication.)

#### C-5 — Do NOT submit ESWA and JAAMAS in parallel. ESWA ONLY, first.
Same dataset / experiments / results / figures / methodology = substantially overlapping → a publication-ethics / self-plagiarism problem even with different framing.
- Supervisor correction (2026-08-18): **NO PARALLEL SUBMISSION.** Pick ONE primary venue → **ESWA first** → submit → await disposition → *then* decide on JAAMAS only if a genuinely non-overlapping novelty exists (needs the Goal-6 multi-agent ablation to stand distinct).
- Source: memory `jobmatch-dual-venue-eswa-jaamas.md:11`; `docs/submission/PROFESSOR_FEEDBACK_PLAN.md:16-18` (Q4) and `:31-40` (OVERLAP VERDICT — decisive: *"submit ESWA ONLY. Hold JAAMAS."*); `RESEARCH_DECISIONS.md:85` (RD-015: *"NO parallel submission; ESWA only."*).
- Consequence for framing: the **substantive science must stay synced** across both manuscripts (same corrected numbers, same graded skill matcher, same calibration story), but the **framing must stay divergent** — do NOT copy the ESWA multi-agent-demotion into JAAMAS, and do NOT anonymize the JAAMAS manuscript (it is single-blind; author names are expected). (`jobmatch-dual-venue-eswa-jaamas.md:18`.)
- Related supervisor directive: **strengthen BEFORE submitting** — the larger explicit-negative, ≥2-annotator benchmark (Goal 2) is the foundational next step; do NOT over-optimize a ranker on the 47 positive labels (`PROFESSOR_FEEDBACK_PLAN.md:13-15`).

#### C-6 — file-organiser requires EXPLICIT user approval before any delete/move.
If you invoke the `file-organiser` skill (or otherwise reorganize the tree), it must **propose** a structure and **execute only after explicit user approval**; it **never deletes files without confirmation.** This protects untracked, gitignored, single-copy artifacts (e.g. `backend/reports/extended_evaluation/*.json`, the ESWA/IUI trees) that would be lost if moved/deleted carelessly. See also RD-003 (`RESEARCH_DECISIONS.md:19`): preserve original state before any modification; *"never overwrite the only copy of an experiment."*

---

### 4. The operator's recurring cron cadence (how this agent is driven)

This work is not one-shot. An operator runs a **recurring cron loop** that re-invokes the agent on a schedule. When you are woken by it, your standing instructions are:

1. **"Always check if something is stuck and fix it."** On each wake, inspect the control plane and any in-flight/background runs. If an experiment, compile, review workflow, or background job is wedged or stalled, unstick it (kill/rerun single-threaded per the torch gotcha, re-run the step, fold in a stalled review's partial results inline) — do not just report it. Precedent: hostile-review panels that stalled were **stopped and re-run inline** rather than blocking (`research/PHASE_STATUS.md:51`, `:88`; RD-017 `:97`).
2. **"Report PHASE_STATUS LIST."** Produce the phase-status roll-up — the COMPLETE / IN-PROGRESS / LEFT breakdown, sourced from `research/PHASE_STATUS.md` (backed by `EXPERIMENT_REGISTRY.yaml`, `NUMERICAL_CLAIMS.yaml`, `REVIEW_LOG.md`, `REPRODUCTION_LOG.md`). Keep it current and honest; author-only blockers stay listed as BLOCKED, not silently closed.
3. **"Keep checking whether the goal is achieved; if not, continue."** The goal is the convergence gate from the mandate (§2 above): no realistically-fixable BLOCKER/SERIOUS remains **and** a final hostile review is clean. If that is not yet true, continue the IMPLEMENT→TEST→VERIFY→HOSTILE-REVIEW→FIX→RE-TEST loop. If it *is* true, the remaining work is **author-only** (see below) — surface those, do not fabricate them.

**What is genuinely left is author-only and must NOT be fabricated** (`research/PHASE_STATUS.md:53-55`, `HANDOFF.md:87-93`): a larger ≥2-annotator explicitly-negative benchmark; a blinded human explanation/usefulness study; author-list reconciliation (title page vs CRediT); a real resolving artifact DOI (currently "deposit upon acceptance"); ORCIDs. The toolchain to make these one-command-ready is already built (`make_annotation_sheet.py`, `merge_annotations.py`, `powered_reeval.py`) — but **the human labels themselves must come from real annotators**, never invented.

---

### 5. One-paragraph orientation for the incoming agent

You are continuing a **scientific-integrity revision** of a personal thesis paper targeting **ESWA**. The paper is currently honest, internally consistent, reproducible (`bash scripts/reproduce_all.sh` → exit 0, numeric gate passes), and has cleared a convergence gate. Your job is to *keep it defensible* and push the review score up **only through legitimate means** (bigger/better human benchmark, human XAI study, sharper novelty framing, discriminating calibrator — see `HANDOFF.md` §H), never by inflating numbers. Before any action, re-read the control files (`research/PHASE_STATUS.md`, `RESEARCH_DECISIONS.md` RD-001..017, `PROTOCOL.md`, `docs/submission/PROFESSOR_FEEDBACK_PLAN.md`). And hold the six hard constraints above as bright lines: **no git commits, no external LLM APIs, no fabrication, keep the NVIDIA grant, ESWA-only (JAAMAS held), and file moves/deletes need explicit approval.**

---

## Control plane — the project's memory & decision spine

Before touching a single experiment or manuscript line, a new session must understand that JobMatch does **not** rely on git history to remember what it did or why (git commits were explicitly banned — see RD-009 below). Instead, the entire state of the project — what is done, why every design choice was made, which experiments exist and what they prove, and how every headline number is tied to a real artifact — lives in five hand-maintained control files under `research/`. These files are the project's memory. When they disagree with the manuscript, **they win** (RD-004). Read them first; everything else is downstream.

The five files, in the order this section walks them:

| File | Role | Size (approx) |
|---|---|---|
| `research/PHASE_STATUS.md` | The phase ledger — what work groups are COMPLETE/IN-PROGRESS/LEFT | ~21 KB, 107 lines |
| `research/RESEARCH_DECISIONS.md` | RD-001…RD-017 — the "why" behind every reframe, constraint, and correction | ~25 KB, 99 lines |
| `research/EXPERIMENT_REGISTRY.yaml` | EXP-001…EXP-044 — every experiment, its RQ, artifact, repro command, status | ~35 KB |
| `research/REPRODUCTION_LOG.md` | Dated log of clean-venv reproductions and environment fixes | ~7 KB |
| `research/results/MANUSCRIPT_NUMBERS.json` + `research/NUMERICAL_CLAIMS.yaml` | The number-gating spine: canonical values ↔ artifacts, and the audit of every disputed claim | 3.7 KB + 5.8 KB |

There are also two supporting control files not in your assigned list but referenced throughout: `research/PROTOCOL.md` (the frozen Stage-3 evaluation protocol) and `research/REVIEW_LOG.md` (hostile-review iteration log). I cite them where the primary files depend on them.

---

### 1. `research/PHASE_STATUS.md` — the phase ledger

This is the top-level "where are we" board. Legend (`PHASE_STATUS.md:3`): **COMPLETE · IN-PROGRESS · LEFT**. It explicitly states evidence lives in the other four control files and that there are **no git commits** by design (`PHASE_STATUS.md:4`, per RD-009). It was last synced 2026-08-18 ("Stage-2 strengthening complete", `PHASE_STATUS.md:1`).

The ledger is organized into completed work-groups (stages), not numbered phases. Every group below is marked **COMPLETE**:

**Foundational — STAGE-1 + numbers-pass (`PHASE_STATUS.md:6-10`).** Built the control plane itself, fixed three code-integrity defects (labelled B3/H8/B10), produced LLM-assisted labels (EXP-018), the job-held-out generalization test (EXP-012), the composite re-run (EXP-011), the RQ1 baseline suite (EXP-014), weight-stability bootstrap (EXP-015), the 6-channel ablation (EXP-013), the architecture-value test (EXP-019), significance+Holm correction (EXP-022), and calibration discrimination (EXP-020).

**STAGE-2 STRENGTHENING (`PHASE_STATUS.md:12-21`, EXP-024…033).** Ten strengthening experiments, each mapped to a manuscript section marker (§F-H, §D-E, §N, §J, §O, §R, §S, §T-U, §V/§W). Highlights: structure recovery ratio 0.907 on synthetic data (EXP-024); a 25-config protocol-gated model search where **no** config beat the incumbent after Holm correction (EXP-025); the calibration-methods trade-off study (EXP-026); generalization corrected **downward** to 0.929/0.929/0.927 from inflated 3-job-pool values (EXP-027); mechanistic explanation faithfulness (EXP-028); an 11-perturbation robustness matrix (EXP-029); a temporal-drift *simulation* (EXP-030); scalability at ~0.048 ms/pair (EXP-031/032); and a failure-injection matrix that found and fixed a NaN→1.0 scoring bug (EXP-033).

**MANUSCRIPT INTEGRITY PASS (`PHASE_STATUS.md:23-27`).** Removed a false "two independent annotators" claim (→ single author + LLM-assisted, κ=0.69, disclosed); corrected four fabricated corpus statistics (12.3→2.97 skills/resume, 8.7→2.13 required, 4.2→0 preferred, ~5,000→74 vocab); fixed the weight-tuning claim three times (→ "hand-set prior"); reframed unjudged pairs as a closed-world caveat.

**FINAL STAGE — Iterations 4–5 (`PHASE_STATUS.md:29-40`).** Code review (§X, 37 findings, all BLOCKER/SERIOUS fixed); reproduction validated end-to-end (`bash scripts/reproduce_all.sh` → exit 0, byte-identical determinism); manuscript rebuild (§Z, multi-agent demoted); auto-generated tables/figures (§AA); numerical audit gating the build (§AB); document audit + PII scrub (§AC); a 5-reviewer hostile ESWA panel (§AD); and a final PDF at **39 pages, 0 errors, 0 undefined refs, 0 dangerous overclaims / 176 honest markers**.

**STAGE-3 MODEL-IMPROVEMENT + ACCEPTANCE CAMPAIGN (`PHASE_STATUS.md:42-51`, EXP-034…036 + 024b).** Froze `research/PROTOCOL.md`; built the graded 4-class skill matcher (EXP-034, macro-F1 0.81) + a de-circularized objective benchmark (EXP-034b); derived-feature fusion on synthetic data (EXP-035/036); a non-additive by-construction control (EXP-024b, recovery 0.891, Δ−0.016); reframed the paper (P12) to foreground *auditable relation-aware skill matching* and demote multi-agent to implementation; produced `EDITORIAL_RISK_MATRIX.md` (P13, 14 criticisms).

**STAGE-3B ACCEPTANCE-CAMPAIGN CYCLE (`PHASE_STATUS.md:62-71`, EXP-043/044).** Wired the graded relation-aware skill channel into the *live* scorer (`core.skills.graded_coverage_skills`); ran the by-construction audit (required-coverage correlates **1.000** with the latent generator) and the pre-specified decomposition isolating the novelty. An independent 6-agent hostile panel returned "converged"; the reproducibility gate passed byte-identical (SYN 0.917/0.949/0.944, REAL 0.949/0.942/0.992). Also EXP-041: added adaptive (equal-mass) ECE + beta calibration, resolving the calibration-vs-discrimination trade-off (beta ECE 0.009, BSS 0.67, AUC 0.96).

**JAAMAS SECOND-VENUE INTEGRITY PASS (`PHASE_STATUS.md:73-80`).** The JAAMAS manuscript (`docs/submission/jaamas/`, multi-agent foregrounded, single-blind) is the *original* and carried the same integrity defects the ESWA numbers-pass fixed; the corrected science was propagated while keeping the multi-agent framing. (Note: JAAMAS cannot compile locally — needs pdflatex; the author builds via Overleaf.)

**REVISION-VERIFICATION + SUPERVISOR ROUNDS (`PHASE_STATUS.md:82-101`).** RD-016 closed a surviving label-leakage phrase in §3.2; RD-017 applied the supervisor's round-2 polish; a final user-decision pass dropped the unverifiable `chen2023causal` citation and settled the author list.

**The BLOCKED section (`PHASE_STATUS.md:53-60`) is the most important thing a new session must not misread.** These are author-only items that **must NOT be fabricated**: the author-list reconciliation, a real resolving DOI (now "deposit upon acceptance"), and the disclosed small-corpus/single-annotator ceiling. Critically, the full annotation *toolchain* is built and validated (G2: `make_annotation_sheet.py` → 403 unjudged pairs, `merge_annotations.py`, `powered_reeval.py`) so the moment two human annotators fill the sheet, the powered ESWA re-analysis is one command. It also records the **provisional** LLM-assisted re-test (`PHASE_STATUS.md:58`): composite-vs-semantic Δ+0.082, perm-p=0.039 → *nominally* significant but explicitly flagged PROVISIONAL because it hinges on 11 LLM-judged positives and human annotation is authoritative. **A new session must treat these as not-yet-done and never invent the missing human labels.**

The final **Tally (`PHASE_STATUS.md:103-107`)** confirms: ESWA fully verified + reproduced; JAAMAS numbers corrected (author compiles the PDF).

---

### 2. `research/RESEARCH_DECISIONS.md` — the decision spine (RD-001…RD-017)

**This is the single most important file for understanding *why* the project is shaped as it is.** Format (`RESEARCH_DECISIONS.md:3`): `DATE · DECISION · OPTIONS · WHY · EVIDENCE · CONSEQUENCE`. Summary of each:

- **RD-001 (`:5`) — Reframe the ESWA paper to what the evidence supports.** Anchor on the auditable six-factor decomposition + honest held-out calibration + honestly-reported robustness/counterfactual. Drop from the headline: multi-agent novelty, "Trustworthy", the fairness-*audit* framing, scalability/deployment claims, GPU-hours, the phantom 0.969, and the leaky 0.032/0.968. *Why:* the prior venue rejected architecture-over-evidence; a defensible weaker paper beats an indefensible stronger one. *Consequence:* title loses "Trustworthy" and the multi-agent lead.

- **RD-002 (`:12`) — Human relevance labels will not be fabricated.** Keep the 47 existing author labels; build an annotation harness; any LLM-assisted expansion is labelled explicitly LLM-assisted (never human). Real two-annotator IAA remains a stated limitation. *Consequence:* RQ1 benchmark stays thin until human labels arrive.

- **RD-003 (`:19`) — Preserve original state before any modification.** Work on branch `eswa-final-evaluation`; snapshot gitignored artifacts to `research/audit/baseline/`; never overwrite the only copy of an experiment; no GitHub push. *Consequence:* re-runs can safely overwrite outputs because the baseline diff is always available.

- **RD-004 (`:25`) — Experiment wins over manuscript on any disagreement.** When a re-run number differs from the `.tex`, the artifact wins and the manuscript is updated; every discrepancy is logged in `NUMERICAL_CLAIMS.yaml`. *Consequence:* **no manuscript number survives without a matching committed artifact.**

- **RD-005 (`:29`, user) — Label expansion is LLM-assisted, not human.** Expand toward 450 pairs with headless `claude -p` (no external API); report Cohen's κ vs the 47 anchors; label the set "LLM-assisted relevance, not human judgments" everywhere. Supersedes RD-002's default.

- **RD-006 (`:33`, user) — Keep multi-agent, but EARN it with a Phase-21 ablation.** Retain the multi-agent contribution only if EXP-019 measures a real benefit. **RESOLVED (`:36`):** the architecture gives real failure isolation (ranking path is provably LLM-independent) and a fast deterministic hot path (0.045 ms/pair) but **no** measured latency/throughput/accuracy benefit → **demote multi-agent to an implementation detail**.

- **RD-007 (`:38`, user) — Full baseline suite for RQ1.** Add held-out LambdaMART (xgboost/lightgbm) + a dense two-tower (MiniLM) + a recruitment-domain encoder (CareerBERT/JobBERT). *Consequence:* if CareerBERT is unavailable, document why and substitute the closest obtainable encoder (no silent omission) — this is why JobBERT was used.

- **RD-008 (`:42`, user) — Funding real, DOI unverified.** The NVIDIA Academic Grant and the "32,000 A100 GPU-hours" gift are kept verbatim (user is the authority on the funding fact, distinct from compute actually consumed). The Dataverse DOI is unverified → change to "artifact deposited upon acceptance"; remove the anonymity-leaking DOI+commit from the blinded body. Audit finding B6 resolved as "user-confirmed funding fact," not fabrication.

- **RD-009 (`:46`, user) — No git commits or pushes (banned).** State/checkpointing is tracked via the `research/` control files and the working tree, not commits. Supersedes the mandate's per-phase-commit rule. **This is why the control plane exists at all.**

- **RD-010 (`:51`, user) — Do NOT alter or remove manuscript numbers now.** (A temporary hold.) Continue *recording* true/verified values in `NUMERICAL_CLAIMS.yaml` (nothing lost) but do not edit `.tex` numbers until the user opens the numbers pass.

- **RD-011 (`:57`, user) — Pause ALL manuscript content edits; "update if better, don't remove anything."** Shift execution to the experiment/code track. Left an open anonymity note: DOI + commit `02a700e` remained in the blinded body, flagged for the anonymity pass.

- **RD-012 (`:63`, user Stage-2 mandate) — Full integrity reinstated; honest numbers pass authorized.** The Stage-2 plan supersedes the earlier "only change a number if it improves" instruction. Governing rule becomes **"MAXIMUM SCIENTIFIC CREDIBILITY not MAXIMUM METRIC"**: apply corrections up *and* down, never manufacture significance, prefer the defensible result. Authorizes the 20–50-config search **only** under strict protocol (criteria fixed before results, test never influences selection, all negatives preserved).

- **RD-013 (`:67`) — Stage-2 strengthening executed + adversarial code-review fixes.** Completed EXP-024…033; corrected the fabricated corpus stats to measured values (2.97 / 2.13 / no-preferred / 74-vocab); fixed all BLOCKER/SERIOUS code-review findings; corrected generalization numbers **down** (0.969/0.958 → 0.929/0.927) for defensibility. *Consequence (`:70`):* all manuscript numbers now flow from artifacts via `generate_manuscript_tables.py` + `MANUSCRIPT_NUMBERS.json`, gated by `verify_paper_numbers.py` — **do not hand-type numbers into the `.tex`.**

- **RD-014 (`:73`) — Stage-3: graded skill channel, fusion by-construction correction, title decision.** (1) Added the frozen relation-aware graded channel (`core.skills.graded_coverage_skills`: exact=1.0, same-group=0.5, else 0.0; credits fixed a priori, not tuned). (2) **Integrity correction:** EXP-044 proved the EXP-035/036 "+derived fusion" gain (0.917→0.99) is largely a by-construction artifact — `required_coverage` correlates 1.000 with the synthetic latent factor; retracted the prior claim; the defensible finding is base6 *nonlinear* fusion. (3) **Title changed** to "An Auditable, Calibrated, and Explainable Multi-Agent System for Job-Candidate Recommendation" (dropped "Trustworthy").

- **RD-015 (`:81`) — Supervisor manuscript review: P0/P1 airtight-claims revisions.** Resolved the weight-selection contradiction (weights are "hand-set domain priors, not fitted"); rewrote calibration to the honest trade-off; kept ranking language as explicit parity; reframed explanation faithfulness as structural + mechanistic; made the dataset limitation (30/15/47, single annotator, positive-only) prominent in the abstract; added the Contribution→Mechanism→Evaluation table. Provisional LLM/synthetic-v2 results stay **out** of the verifier-gated manuscript.

- **RD-016 (`:87`) — Revision-verification findings folded in.** A 4-agent adversarial workflow found a **surviving P0.1 label-leakage phrase** in the newly-inserted §3.2 ("weights ... fixed by the nDCG@5 optimization on the labeled subset") that the RD-015 scrub missed; rewrote it and **widened the verifier gate** so it can never recur (self-test confirms it now catches the old phrasing). Plus a roadmap-renumber fix, a regulatory-overclaim softening, and three MINORs.

- **RD-017 (`:92`) — Supervisor round-2 review: near-submission-ready polish.** Verdict: "close to submission-ready." Three must-fix (beta-CI relabelled to its own bootstrap CI [0.012,0.032] verified against `calibration_methods.json`; abstract 7/8; Table-10 verification) + citation-integrity work: **fixed CareerBERT's wrong bib authors**, and **flagged `chen2023causal`** as unlocatable (not silently replaced). **RESOLVED (`:98`):** per user decision the unverifiable `chen2023causal` row/citation/prose was dropped everywhere; re-test clean.

The through-line: RD-001/RD-012 set the *credibility-over-metric* mandate; RD-004/RD-013 make numbers artifact-gated; RD-009 explains why this file exists instead of git; RD-002/RD-005 forbid fabricating human labels; RD-006 explains why "multi-agent" is demoted; RD-014/RD-016 show integrity corrections being made *against* the project's own interest.

---

### 3. `research/EXPERIMENT_REGISTRY.yaml` — every experiment proves something

Rule at the top (`EXPERIMENT_REGISTRY.yaml:1`): **"every experiment has an ID; no result without one."** Environment (`:4`): Python 3.11.15, venv `backend/.venv`, seed convention 42, darwin arm64 (CPU). Status vocabulary (`:2-3`): `EXISTS-UNVERIFIED | REPRODUCED | LEAKY | MISSING | PLANNED | BLOCKED | SUPERSEDED`. Most entries carry a `repro_cmd` you can paste to regenerate the artifact.

**Original/baseline experiments (EXP-001…010)** — mostly `EXISTS-UNVERIFIED`, several with damning notes:

| EXP | What it is | Status | What it proves / note |
|---|---|---|---|
| 001 (`:7`) | Composite offline eval, fixed 6-channel weights | EXISTS-UNVERIFIED | nDCG@5 **0.949**, the anchor number |
| 002 (`:15`) | Composite 5-fold CV | EXISTS-UNVERIFIED | 0.949 CI[0.870,0.993]; "vacuous generalization for FIXED weights" |
| 003 (`:22`) | Pointwise LTR (LogisticRegression), held-out | EXISTS-UNVERIFIED | 0.917; **mislabeled as XGBoost/pairwise**; does NOT beat composite |
| 004 (`:29`) | Held-out Platt calibration | EXISTS-UNVERIFIED | ECE **0.0192**; supersedes the leaky in-sample 0.032; near-degenerate |
| 005 (`:36`) | Counterfactual + demographic probe (50 pairs) | EXISTS-UNVERIFIED | recourse **null** (rank_delta=0 all); pronoun perturbation is a no-op |
| 006 (`:43`) | Parser robustness | EXISTS-UNVERIFIED | all CIs cross zero (n=30) |
| 007 (`:49`) | Cold-start (unseen skill/synonym/misspelling) | **REPRODUCED** | synonym-invariant; misspellings shift composite −0.078/pair but not top-5 rank |
| 008 (`:57`) | Paired-bootstrap significance | **LEAKY** | non-reproducible salted `hash()` seeding; CI crosses zero; no correction |
| 009 (`:62`) | Fairness DIR proxy | EXISTS-UNVERIFIED | proxy groups, NOT a demographic audit |
| 010 (`:69`) | Explainability suite | EXISTS-UNVERIFIED | "faithfulness" = mean of 3 lint checks; tautological; no human eval |

**Strengthening & Stage-2/3 experiments (all `REPRODUCED` unless noted):**

| EXP | What it is | What it proves |
|---|---|---|
| 011 (`:77`) | Reproduce EXP-001…010 in clean venv | PASS 2026-08-17; 0.949/0.0192/0.917/CF-50 match byte-for-byte |
| 012 (`:78`) | Job-held-out generalization | Learned LTR generalizes to unseen jobs (0.928, STRICT 0.930) |
| 013 (`:86`) | Leave-one-channel-out ablation | Only **semantic** is provably load-bearing (drop +0.080); do NOT claim "all six matter" |
| 014 (`:94`) | Full RQ1 baselines | LambdaMART 0.963 / composite 0.949 / TFIDF 0.905 / BM25 0.902 / MiniLM 0.878 / JobBERT 0.864 — **all CIs overlap; no method significantly better** |
| 015 (`:113`) | Weight-stability cluster bootstrap | Hand-set weights are a *prior*, not a fitted optimum (confirms B11) |
| 016 (`:121`) | Scalability (old) | SUPERSEDED by EXP-031/032 |
| 017 (`:122`) | Explanation faithfulness (old) | SUPERSEDED by EXP-028 |
| 018 (`:123`) | Benchmark expansion 47→450 via `claude -p` | LLM-assisted (not human); Cohen's κ **0.691**, within-1 agree 1.0 |
| 019 (`:153`) | Architecture-value (RQ8) | Real failure isolation + 0.045 ms/pair hot path; **no** monolith-vs-agents benefit → demote multi-agent (resolves RD-006) |
| 020 (`:161`) | Calibration discrimination | BSS 0.0066, AUC 0.758, confidence squashed to [0.11,0.14]; refutes "0.9 ⇒ 9/10" (confirms B8) |
| 021 (`:131`) | Composite on the denser LLM set | Ranking holds (~0.93); denser labels de-saturate R@5 (confirms B12) |
| 022 (`:137`) | Reproducible significance + Holm | Δ=+0.071, p_one-sided 0.051, **NONE of 8 survive Holm** — overturns the "significant p=0.048" headline |
| 023 (`:145`) | Synthetic corpus w/ latent ground truth | 500 resumes × 75 jobs, 37,500 pairs; enables recovery/power/scale tests |
| 024 (`:169`) | Structure recovery on synthetic | recovery ratio 0.907; decomposition tracks known latent factors |
| 024b (`:177`) | Non-additive latent recovery control | 0.891 (Δ−0.016) — refutes the "recovery is by construction" objection |
| 025 (`:186`) | 25-config protocol-gated model search | **No** challenger beats the incumbent after Holm; only drop-semantic significant; incumbent kept by parsimony |
| 026 (`:194`) | Calibration methods (raw/Platt/isotonic/temperature) | Platt lowest-ECE but degenerate; isotonic preserves discrimination; report the trade-off |
| 027 (`:202`) | Generalization (unseen cand/job/both) | 0.929/0.929/0.927; **corrected down** from inflated 3-job-pool values |
| 028 (`:210`) | Mechanistic explanation faithfulness | Directionally faithful (comprehensiveness top>least>random; skill-edit attribution 1.0); replaces B9 lint-average |
| 029 (`:218`) | Robustness matrix (11 perturbations) | Synonym-invariant, gaming-resistant; formatting/misspelling weaknesses disclosed |
| 030 (`:226`) | Temporal drift (SIMULATION) | Emerging-skills −16.5%; titles −3.1%; salary ~0 |
| 031_032 (`:234`) | Scalability + incremental | ~0.048 ms/pair (~linear); incremental 500× cheaper than full re-rank |
| 033 (`:242`) | Failure-injection matrix | 9/9 no-crash + deterministic; found & FIXED a NaN→1.0 bug (`core.scoring._safe_vec`) |
| 034 (`:251`) | Graded 4-class skill matcher + benchmark | macro-F1 0.81; graded credit works; SEMANTIC tier exploratory only (circularity caveat) |
| 034b (`:259`) | De-circularized objective skill benchmark | orthographic/synonym exact-recall 1.0; 7/8 hard negatives kept distinct; Angular/AngularJS over-merge disclosed |
| 035_036 (`:267`) | Derived features + fusion (synthetic) | base6 nonlinear fusion beats fixed composite (0.947/0.961); **+derived gain retracted as by-construction** |
| 041 (`:287`) | Adaptive-ECE + beta calibration | beta ECE 0.009 + preserves discrimination (BSS 0.673, AUC 0.964) — resolves the trade-off |
| 043_044 (`:275`) | Graded channel in live scorer + by-construction audit | required-coverage corr **1.000** with latent; decomposes coverage-FORM vs RELATION-AWARE credit; real-corpus novelty gain is directional (6/30, sign-test p=0.031, effective n=6) |
| 037/038/039/040/042 (`:283-295`) | Two-stage retrieval, embedding comparison, hard-neg mining, counterfactual-100, human study | **PLANNED** (not run) |

The registry is disciplined about honesty: it marks `LEAKY`/`SUPERSEDED` entries, records that numbers were corrected *downward* for defensibility (027, 013), and retracts its own prior claims (035/036 note explicitly says "RETRACTED").

---

### 4. How numbers are gated to artifacts (REPRODUCTION_LOG + MANUSCRIPT_NUMBERS.json + NUMERICAL_CLAIMS.yaml)

These three files, plus two scripts, form a closed loop that makes it **structurally impossible** for a fabricated or stale number to reach the PDF.

**`research/REPRODUCTION_LOG.md`** — the dated evidence that experiments actually re-run cleanly.
- Environment build (`REPRODUCTION_LOG.md:3-7`): `python3.11 -m venv backend/.venv`; installed torch 2.13.0, sentence-transformers 5.1.2, chromadb 0.4.24, scikit-learn 1.9.0, numpy 1.26.4. Notes a repro gap (sklearn/scipy/matplotlib were not pinned) and that `pdflatex` is absent locally.
- EXP-011 clean-venv reproduction (`:9-18`): **PASS** with `PYTHONHASHSEED=0` — kfold composite 0.949236 == baseline, calibration ECE/Brier (0.019156, 0.092836) == baseline, xgb_ranker 0.916653 == baseline, counterfactual-50 (12, 9, 0.96) == baseline, all byte-for-byte.
- One-command runner added (`:20-24`): `scripts/reproduce_all.sh`.
- Threading-hang fix (`:26-29`): on a loaded machine torch/tokenizers block at 0% CPU on startup; fix is to force single-thread (`OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false`), now baked into the runner.
- Anonymity passes (`:31-39`): path scrub of released artifacts, then the full Stage-3 identity scrub across test fixtures (author identity → "Jordan Rivera" placeholder), plus the runnable `scripts/anonymize_reviewer_bundle.py`.

**`research/results/MANUSCRIPT_NUMBERS.json`** — the machine-readable canonical value ↔ source map. Every entry is `{value, source}`. Examples: `composite_ndcg5` = 0.949 ← `composite_eval_report.json`; the full baseline ladder (`ndcg5::BM25` 0.902, `TF-IDF` 0.905, `Semantic cosine` 0.878, `Multimodal weighted blend` 0.924, `RRF ensemble` 0.913) ← `comparison_table.json`; the entire calibration matrix (raw/platt/isotonic/temperature/beta/constant, each with `ece`/`adaptive_ece`/`bss`/`auc`) ← `calibration_methods.json` — e.g. `calib::platt::ece` 0.0179 with `adaptive_ece` 0.084, `calib::beta::ece` 0.0089; `recovery_ratio` 0.9066 ← `structure_recovery.json`; `gen_both_unseen` 0.927462 ← `generalization.json`; `ece_platt_heldout` 0.019156… ← `calibration_binary.json`. This file is regenerated by `research/experiments/generate_manuscript_tables.py` (per RD-013's "numbers flow from artifacts") and consumed by the verifier.

**`research/NUMERICAL_CLAIMS.yaml`** — the human-readable audit of every disputed headline number. Verdict vocabulary (`NUMERICAL_CLAIMS.yaml:2`): `REPRODUCIBLE | LEAKED | PHANTOM(no artifact) | NON-REPRODUCIBLE | STALE | HELD-OUT-AVAILABLE`. It records the ground-truth corpus meta (`:6-8`: 30 resumes / 15 jobs / 47 labels; synthetic 500×75). Each claim carries `value`, `source_artifact`, `heldout_artifact`, `manuscript_loc`, `verdict`, `action`, and often a `corrected` value. Key entries:

| Claim | Stated value | Verdict | Corrected / action |
|---|---|---|---|
| composite nDCG@5 (`:11`) | 0.949 | **REPRODUCIBLE** | keep; anchor here |
| best-single soft-embed (`:19`) | 0.969 / R@5 1.000 | **PHANTOM** (no artifact) | replace with Multimodal 0.924; delete fake file cites |
| learned fusion (`:27`) | 0.968 | **LEAKED** | → held-out 0.917; does NOT beat composite |
| significance vs semantic (`:35`) | Δ+0.071, p=0.048 | **NON-REPRODUCIBLE** (salted hash seed) | pin seed; report two-sided p + CI + correction |
| cross-encoder (`:42`) | 0.939 / 141.7ms | **PHANTOM** (CE never run) | run+commit OR remove |
| calibration ECE (`:49`) | 0.40 → 0.032 | **LEAKED** (fit-on-eval) | → held-out 0.0192 |
| Brier calibrated (`:58`) | 0.093 | **REPRODUCIBLE** but near-degenerate | DONE via EXP-020 (BSS 0.0066, AUC 0.758) |
| explanation faithfulness (`:64`) | 0.745 / 0.747 | **STALE** (lint mean, tautological) | rename metric; real sufficiency test |
| counterfactual flagged (`:71`) | 7/10 | **STALE** | adopt 50-pair; report recourse null |
| fairness DIR (`:80`) | 0.82 / 0.75 | **STALE** (proxy, not demographic) | reframe; fix caption arithmetic |
| corpus stats (`:87`) | 12.3 / 8.7+4.2 / ~5000 | **PHANTOM** (fabricated vs data) | → 2.97 / 2.13 + no-preferred / ~7–63 |
| NVIDIA A100 GPU-hours (`:95`) | 32000 | **PHANTOM** | verify grant (kept per RD-008) |
| tests (`:102`) | 302 pytest + 39 node | **UNVERIFIED** | re-count in clean venv |

**The gate itself** — `research/experiments/verify_paper_numbers.py` (`verify_paper_numbers.py:1-9`) scans every manuscript `.tex` under `docs/submission/eswa/manuscript/{sections,tables}` and does two things: (1) asserts a **FORBIDDEN** list of stale/phantom/fabricated patterns is absent (unless inside an explicit "superseded"/"earlier"/"no longer" correction note), and (2) confirms a **REQUIRED** list of canonical numbers is present. The FORBIDDEN regexes (`verify_paper_numbers.py:24-40`) literally encode the audit: `0.969` best-single, `R@5=1.000`, "nine times out of ten", "p = 0.048", "two independent (reviewers|annotators)", "12.3 skills", "8.7 required", "4.2 preferred", and the B11 weight-tuning phrasings (including the widened `nDCG@5 (maximi|optimi)[sz]ation on` and `(fixed|set|tuned|chosen|optimized) by (the )?nDCG` patterns added in RD-016). The REQUIRED list (`:42-49`) pins the canonical numbers that must appear: 0.949, 0.878, 0.913, 0.924, 0.019, 2.97, 2.13, plus Stage-3 numbers 0.917/0.944/0.992/0.942/0.947/0.961 and calibration 0.009/0.084. **Any forbidden hit or missing canonical number exits non-zero and fails the build.**

**The loop, end to end** — `scripts/reproduce_all.sh` (`reproduce_all.sh:1-16`) runs, deterministically (`PYTHONHASHSEED=0`, seed 42, single-threaded), EXP-011…036 + 043/044, then `generate_manuscript_tables.py` (regenerates `tables/*.tex` + `MANUSCRIPT_NUMBERS.json`), then `make_reliability_fig.py`, then `verify_checks.py` (weight-sum/decomposition/leakage acceptance checks), then `verify_paper_numbers.py` (the numeric gate). PHASE_STATUS records this runs to **exit 0 with byte-identical determinism** (`PHASE_STATUS.md:31,69`). So the chain is: **artifact JSON → `MANUSCRIPT_NUMBERS.json` → manuscript `.tex` → verifier gate → PDF**, and RD-004/RD-013 forbid hand-typing any number into the `.tex`.

---

### Read these first, in this order (control plane)

1. **`research/PHASE_STATUS.md`** — get the current state in one read: what's COMPLETE, what's BLOCKED (author-only, do-not-fabricate), and the tally.
2. **`research/RESEARCH_DECISIONS.md`** (RD-001…RD-017) — the *why* behind every reframe and constraint. Non-negotiable to read before changing anything; RD-004, RD-009, RD-012, RD-013 govern how you're allowed to work.
3. **`research/NUMERICAL_CLAIMS.yaml`** — the audit of every headline number (what's REPRODUCIBLE vs PHANTOM/LEAKED/STALE and the corrected value to use).
4. **`research/results/MANUSCRIPT_NUMBERS.json`** — the canonical value↔artifact map that the paper and the verifier both read.
5. **`research/EXPERIMENT_REGISTRY.yaml`** — look up any EXP-### to find its artifact, status, and one-line `repro_cmd`.
6. **`research/REPRODUCTION_LOG.md`** — proof the numbers re-run clean, plus the environment gotchas (single-thread flags, missing pdflatex).
7. Supporting, when needed: **`research/PROTOCOL.md`** (frozen Stage-3 selection rules) and **`research/experiments/verify_paper_numbers.py`** + **`scripts/reproduce_all.sh`** (the gate and the one-command reproduction).

---

## The ESWA manuscript — structure, claims, and the submission ideology

This section maps the LaTeX source of the paper the team is submitting to *Expert Systems with Applications* (Elsevier). Everything below is grounded in the actual `.tex` files under `docs/submission/eswa/manuscript/`. The build is `pdflatex + bibtex` on the Elsevier `elsarticle` class; the compiled output is `main.pdf` (and a `main.docx` export). If you open one file first, open `main.tex` — it is the spine that `\input`s all eight sections plus the abstract.

### Document shell and metadata (`main.tex`)

- **Title:** "An Auditable, Calibrated, and Explainable Multi-Agent System for Job-Candidate Recommendation" (`main.tex:44-45`). Note the title still leads with "Multi-Agent System" even though the body deliberately demotes the multi-agent aspect (see the ideology subsection) — this is a residual tension a reviewer might notice.
- **Class / format:** `\documentclass[preprint,review,3p,times,twocolumn,authoryear]{elsarticle}` (`main.tex:10`), targeted at 8–10K words, two-column Elsevier preprint-review layout (`main.tex:1-6`).
- **Anonymized for review:** authors/affiliation are `Anonymous Authors` / `Anonymous Institution` (`main.tex:47-48`); acknowledgments are withheld (`main.tex:74-77`).
- **Keywords** (`main.tex:56-60`): Recommender systems; Explainable AI; Confidence calibration; Skill matching; Job-candidate matching; Auditable ranking; Recruitment.
- **Section include order** (`main.tex:64-71`): abstract → §1 Introduction → §2 Related Work → §3 Methodology → §4 Experimental Setup → §5 Results → §6 Discussion → §7 Future Work → §8 Conclusion.
- **Mandatory Elsevier declarations** (`main.tex:79-115`): a generative-AI disclosure stating GPT-4/ChatGPT was used only for copy-editing, figure-caption drafting, and lit-review edits (`main.tex:80-90`); a CRediT statement for three anonymous authors (`main.tex:92-98`); a competing-interest declaration (`main.tex:100-103`); and a **data-availability** statement (`main.tex:105-115`) promising a Harvard Dataverse deposit with a citable DOI on acceptance, releasing the frozen 30/15/47 corpus, the synthetic corpus + generator, the evaluation scripts, the explanation generator, the calibration layer, the regression benchmark, the one-command reproduction script, the auto-generated tables, per-experiment JSON artifacts, and figure source scripts.

### (a) Per-section map — what each `.tex` contains

| File | Section | Core content |
|---|---|---|
| `sections/abstract.tex` | Abstract | Sub-250-word abstract framing four contributions (decomposable composite + relation-aware skill matcher; calibrated-confidence layer with an honest calibration–discrimination trade-off; structural + mechanistic faithfulness checks + 50-pair counterfactual probe; reproducible regression-gated artifact). Explicitly states evaluation is "deliberately controlled but small" and establishes "methodological *feasibility*, not population-level ranking superiority." Carries the headline numbers verbatim. |
| `sections/section-1-introduction.tex` | §1 Introduction | Frames the problem as an *engineering/accountability gap* in opaque ATS ranking (§1.1), the regulatory/engineering context with an explicit "we do not claim compliance with any specific statutory provision" caveat (§1.2), three families of existing AI approaches and their limits (§1.3–1.4), the research gap (§1.5), and the fourfold contribution (§1.6) — with the parenthetical that the multi-agent decomposition is "an engineering/failure-isolation choice, not the scientific contribution." Contains **Table 1** `tab:contrib` ("contribution at a glance," `section-1-introduction.tex:50-67`) whose caption says the novelty is "the auditable *integration* and its property-by-property evaluation, not a new ranking algorithm." §1.7 walks the prototype UI (Figs. `fig:app`, `fig:app2`, `fig:portal-survey`/Fig10, `fig:hld`); §1.8 is the roadmap. |
| `sections/section-2-related-work.tex` | §2 Related Work | Six research streams: AI-based recommendation, semantic matching, knowledge-driven AI, LLM agents, XAI for recommendation, trustworthy AI/calibration. Positions against ESWA-published recruitment work (CareerBERT `lavi2025careerbert`, Saito & Sugiyama `saito2024leveraging`), a 2025 systematic review of 85 person–job studies (`tang2025explainable`), recent multi-agent recruitment systems (`lo2025hiring`, `bhattacharya2025xcui`), and the calibrated-explanations framework (`lofstrom2024calibrated`). Repeatedly disclaims novelty of individual components: "we make no novelty claim for the act of calibrating a multi-channel score" (`section-2:50`); the novelty is "in their composition and in the evaluation methodology." |
| `sections/section-3-methodology.tex` | §3 Methodology | Problem formulation/notation (§3.1: resume tuple $(S_i,E_i,C_i,P_i)$, job tuple, scoring function $f$, 6-dim decomposition $d$, confidence $c\in[0,1]$); glance (§3.2); **multi-agent architecture** (§3.3: candidate-side / employer-side / read-only matchmaking components, role boundary = privacy boundary, LLM on cold path only); knowledge representation and 4-channel hybrid retrieval (§3.4: BM25, Sentence-BERT `all-MiniLM-L6-v2` d=384, Jaccard, RRF k=60/K=10, vocabulary V≈5,000); **composite ranking** (§3.5) with the fixed-weight equation and the **relation-aware graded skill matcher** definition (exact=1.0 / related=0.5 / unrelated=0); explanation generation (§3.6); confidence calibration (§3.7: Platt on 21 strong + 26 partial labels, uncalibrated ECE 0.40 → calibrated 0.019, Brier 0.093); implementation (§3.8: 302 Python + 39 Node = 341 tests, ±0.04 nDCG CI gate, latency profile); engineering surface/integration (§3.9: illustrative 200–300 eng-hours estimate); cross-encoder diagnosis (§3.10: 0.939 vs 0.949, ~340× slower). |
| `sections/section-4-experimental-setup.tex` | §4 Experimental Setup | Dataset (§4.1: 30 resumes / 15 jobs / 47 pairs = 21 strong grade-2 + 26 partial grade-1, **no grade-0**; single author-annotator primary labels; LLM-assisted second pass at quadratic Cohen's κ=0.69; 74-skill vocabulary; closed-world grade-0 assumption disclosed as limitation). Baselines (§4.2: BM25, TF-IDF, Sentence-BERT, hybrid 0.7/0.3, RRF, cross-encoder + two reference points). Metrics (§4.3: nDCG@5/P@5/R@5, faithfulness, ECE over n=450 held-out 5-fold base-rate 0.104, counterfactual robustness). Protocol (§4.4: paired bootstrap N=5,000 seed 42; 50-pair counterfactual probe = 25 recourse + 25 demographic-proxy; latency on 2.4 GHz Xeon E5-2680 v4). |
| `sections/section-5-results.tex` | §5 Results | The evidentiary core. §5.1 ranking (composite 0.949) + `tab:progression`; ablation table (`tab:ablation`, in-file at `:20-37`); **statistical-significance subsubsection** ($p=0.10$, nothing survives Holm); §5.2 faithfulness (0.745 structural + mechanistic probe 13.3% vs 0% vs 3.3%) + `tab:explainability` (in-file `:64-78`); §5.3 calibration + `tab:calibration`; §5.4 counterfactual + adversarial + `tab:counterfactual`, `tab:fairness` (both in-file); §5.5 latency + `tab:latency`; §5.6 Platt sensitivity; **§5.7 "Structure recovery, generalization, robustness, and scale"** — the largest subsection, holding synthetic structure recovery, 25-config model-selection search, generalization, robustness, scale/failure-isolation, the **relation-aware skill-matching decomposition**, and fusion-headroom probe + `tab:stage2`. |
| `sections/section-6-discussion.tex` | §6 Discussion | Engineering implications (§6.1, four points + deployment cost estimate §6.1.1); **positioning table** `tab:positioning` (§6.pos, in-file `:21-39`) — the "all-checkmark" table; **limitations** (§6.2 — eight explicitly enumerated, "all stated explicitly and not hedged"); broader perspective (§6.3, domain-agnostic pipeline claim). |
| `sections/section-7-future-work.tex` | §7 Future Work | Larger corpus (target 1,000+/500+/5,000+), live user study, industrial deployment, LLM-in-the-loop ranking, LLM-explainer A/B, RAG + LLM-as-judge baselines, larger counterfactual probe, and a "comparison with prior multi-agent systems" note reasserting the contribution "is not in the agent architecture per se." |
| `sections/section-8-conclusion.tex` | §8 Conclusion | Restates every headline number in one dense paragraph (`section-8:4`), reasserts multi-agent = "implementation choice that buys failure isolation, not a source of measured ranking benefit," lists the four stated limitations, and repeats the broader-perspective paragraph (§8.10–8.14, near-verbatim duplicate of §6.3). |

**Tables and where they live.** Four tables are externalized under `tables/` and `\input`'d; the rest are inline. The four externalized ones:
- `tables/tab-progression.tex` (`tab:progression`, ranking quality) — auto-generated from `comparison_table.json` / `composite_eval_report.json`; caption warns "Auto-generated; do not hand-edit."
- `tables/tab-calibration.tex` (`tab:calibration`, five calibration maps) — from `calibration_methods.json`.
- `tables/tab-latency.tex` (`tab:latency`, quality–latency trade-off) — from `comparison_table.json` / `phase11_summary.csv`.
- `tables/tab-stage2.tex` (`tab:stage2`, Stage-2 strengthening evidence) — synthetic + held-out probes.

Inline tables: `tab:contrib` (§1), `tab:ablation` / `tab:explainability` / `tab:counterfactual` / `tab:fairness` (§5), `tab:positioning` (§6). Figures are PNGs under `figures/` generated by `figures/make_figures.py` and `figures/make_fig10_eswa.py`; the UI shots (`fig1_application.png`, `fig2_employer_view.png`, `Fig10.png`) plus architecture/methodology figures (`Fig1`–`Fig7`, `fig3_methodology_flow.png`, `fig4_reliability_diagram.png`, `fig5_channel_contribution.png`).

### (b) The headline claims and their exact numbers

Every number below is copied from the source; where the same number appears with a rounding nuance, that is flagged.

**1. Ranking: parity, not superiority (nDCG@5).** From `tab:progression` (`tables/tab-progression.tex:9-17`) and §5.1 (`section-5-results.tex:9-11`):

| Configuration | P@5 | R@5 | nDCG@5 |
|---|---|---|---|
| Portal-default composite (proposed) | 0.293 | 0.933 | **0.949** |
| Multimodal weighted blend (w=0.7) | 0.287 | 0.933 | 0.924 |
| RRF ensemble (4 list views) | 0.293 | 0.950 | 0.913 |
| TF-IDF (lexical) | 0.307 | 0.983 | 0.905 |
| BM25 (lexical) | 0.307 | 0.983 | 0.902 |
| **Semantic cosine (baseline)** | 0.267 | 0.867 | **0.878** |
| Soft skill embedding | 0.280 | 0.900 | 0.869 |
| Skills Jaccard | 0.233 | 0.733 | 0.748 |

- **The load-bearing significance claim** (`section-5-results.tex:49-52`): composite over the pure-semantic baseline is Δ = **+0.071**, two-sided **p = 0.10**, 95% CI **[−0.014, +0.167] crossing zero**. Multimodal blend and RRF have smaller one-sided p-values (0.010 and 0.009) but "none of the comparisons survive Holm–Bonferroni correction at n = 30." Lexical baselines don't differ significantly from semantic (p > 0.25). Explicit sentence: "we do not claim a statistically established ranking advantage, and the contribution rests on decomposition, calibration, and auditability rather than on beating baselines."
- **Learned fusion is reported honestly** (`section-5-results.tex:11`): held-out 5-fold nDCG@5 = 0.917 (does *not* beat 0.949); in-sample 0.968 is explicitly treated as "an optimistic upper bound rather than a result."
- **Ablation** (`tab:ablation`, `section-5-results.tex:28-34`): full 0.949 / faithfulness 0.745 / ECE 0.019; removing Platt leaves nDCG 0.949 but ECE jumps to 0.400 (~20×); cross-encoder 0.939; best single channel 0.924; RRF 0.913; semantic-only 0.878; BM25-only 0.902.
- **Cross-encoder** (§3.10, `tab:latency`): nDCG@5 0.939 at 141.70 ms/query vs the bi-encoder composite ~0.4 ms — ~340× slower, "correctly disabled."
- **25-config protocol-gated search** (§5.7, `section-5-results.tex:186-193`; `tab:stage2` "24 / 0"): no configuration significantly outperforms the fixed composite after Holm; the only channel whose removal *significantly* degrades ranking is the semantic channel (Δ = −0.080, 95% CI [−0.163, −0.017], survives Holm).

**2. Calibration: the honest calibration-vs-discrimination trade-off.** From `tab:calibration` (`tables/tab-calibration.tex:9-14`), n=450, base rate 0.104:

| Calibration map | ECE ↓ | Adaptive ECE ↓ | Brier ↓ | Brier skill ↑ | ROC-AUC ↑ |
|---|---|---|---|---|---|
| Raw composite (uncalibrated) | 0.400 | 0.412 | 0.210 | −1.247 | 0.967 |
| **Platt scaling (deployed default)** | **0.018** | **0.084** | 0.093 | +0.007 | **0.758** |
| Isotonic regression | 0.024 | 0.019 | 0.034 | +0.640 | 0.950 |
| Temperature (1-param) | 0.461 | 0.504 | 0.297 | −2.177 | 0.967 |
| **Beta calibration (recommended)** | **0.009** | **0.009** | 0.030 | +0.673 | 0.964 |
| Constant base-rate (floor) | 0.000 | — | 0.093 | +0.000 | 0.500 |

- Note the rounding nuance across files: the **abstract and §1.6/§6 say Platt equal-width ECE = 0.019**; the table says **0.018**; §5.3 reconciles them as "0.018–0.019 held-out across the two calibration experiments EXP-026/EXP-004, which agree to within rounding" and supersedes an earlier single-split 0.032 measured on fitting data (`section-5-results.tex:84`).
- The core narrative (`section-5-results.tex:83-87`): raw score discriminates (AUC 0.967) but is badly miscalibrated (ECE 0.40); Platt attains the lowest *equal-width* ECE but "shrinks the confidence into a razor-thin band near the base rate ([0.11, 0.14])," Brier skill ≈ 0, pooled AUC collapses to **0.76** — "barely better than the constant base-rate predictor." The **adaptive (equal-mass) ECE of 0.084** is "the more honest aggregate here." **Beta calibration** (`kull2017beta`) is "the best map on every axis" (0.009/0.009, Brier skill 0.67, AUC 0.96).
- **The deliberate refusal to swap** (`section-5-results.tex:87`): they keep the frozen Platt map because re-selecting the calibrator on the same held-out comparison "would be choosing the calibration map on the evaluation — the very leakage this protocol avoids"; beta's ECE CI [0.012, 0.032] overlaps Platt's [0.000, 0.044], so beta's advantage is "directional rather than statistically separated." Beta is presented as a "recommended upgrade to be confirmed and adopted on the larger explicitly-judged benchmark," **not** a post-hoc deployment switch. Platt parameters: a ≈ 0.30, b ≈ −2.12 (§3.7, §5.6); §5.6 held-out ECE 0.019 with bootstrap 95% CI [0.010, 0.029].

**3. Graded relation-aware skill decomposition (§5.7, the novel component).** The matcher (exact=1.0 / related=0.5 / unrelated=0, credits fixed a priori) is decomposed into two pre-specified steps — (a) Jaccard → asymmetric required-coverage form, and (b) coverage → relation-aware partial credit (`section-5-results.tex:233-260`):
- **Synthetic corpus (n=500):** the *coverage form* accounts for the entire gain — Jaccard **0.917 → exact-coverage 0.949** (paired permutation p < 0.001) — while the relation-aware credit slightly *hurts*: exact-coverage 0.949 → graded 0.944 (p = 0.014). Expected, "since the generator has no notion of related skills."
- **Real human corpus (n=30):** the pattern *reverses* — coverage form changes nothing detectable (Jaccard 0.949 → exact-coverage 0.942, p = 0.50), but the relation-aware credit **improves six of thirty queries and worsens none**: exact-coverage **0.942 → graded 0.992**, sign/permutation **p = 0.03**.
- **The fragility is stated openly** (`section-5-results.tex:252-260`): 24 of 30 per-query scores are exact ties, the other six all move positive, so the test has "an effective n of six and p = 0.03 is the *smallest* value it can return for six concordant pairs — a direction-only certificate, not an effect size, and a single query reversing would raise it to p ≈ 0.22." The mean gain is "dominated by one query that binary overlap had ranked entirely incorrectly," near the metric ceiling. Read as "a directional signal only"; binary overlap is retained in the primary composite.
- De-circularized benchmark result (`section-5-results.tex:219-231`): orthographic/synonym variants collapsed to exact with **recall 1.00**; **seven of eight** non-equivalent look-alikes kept distinct (Java vs JavaScript, React vs React Native, C vs C++), with the one false merge (Angular/AngularJS) flagged as a catalog-data issue.

**4. Positioning table `tab:positioning` — the all-checkmark claim (§6.pos, `section-6-discussion.tex:21-39`).** Three prior systems + JobMatch across six properties (✓ = reported, — = not reported):

| System | Decomposable expl. | Calibrated conf. | Relation-aware skill | Faithfulness measure | Counterfactual probe | Reproducible artifact |
|---|---|---|---|---|---|---|
| CareerBERT (`lavi2025careerbert`) | — | — | ✓ | — | — | partial |
| Saito & Sugiyama (`saito2024leveraging`) | — | — | — | — | — | — |
| Calibrated Explanations (`lofstrom2024calibrated`) | ✓ | ✓ | — | — | ✓ | ✓ |
| **JobMatch (this work)** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

The caption pre-empts the obvious reviewer objection: "✓ = reported; -- = not reported. … the entries reflect what each system *reports*, not a claim that a property is impossible for it. The point is not that any single property is new … but that the auditable combination, the relation-aware skill layer, and the property-by-property evaluation methodology are, to our knowledge, not jointly reported." (The task brief calls this "Table-10"; in the source it is `tab:positioning` — the tenth numbered table only in final render order, not a literal `\label`.)

**Other supporting numbers worth carrying forward:**
- Faithfulness (`tab:explainability`, §5.2): rule-based structural pass 0.745, specificity 0.627, skill-mention 25.3%, no-hallucination 98.0%, component alignment 100.0%, consistency 1.000; LLM-template 0.747 / 0.633 / 26.7% / 97.3% / 100% / 1.000. Mechanistic probe: dropping the top-attributed channel displaces top-1 in **13.3%** of cases vs **0%** (least-attributed) vs **3.3%** (random); credited-skill contribution rises in 100% of controlled skill-add edits.
- Counterfactual (`tab:counterfactual`, §5.4): 25 recourse edits → 0 rank changes (12 flagged, max Δ 0.091, top-1 stable 25/25 — "a ranking-coarseness null rather than score insensitivity"); 25 demographic-proxy edits → 9 flagged, 1 rank change, top-1 stable 24/25.
- Fairness (`tab:fairness`, §5.4): disparate-impact ratio 0.82 (experience tier), 0.75 (remote preference) — remote falls below the 0.80 four-fifths threshold; explicitly "a sensitivity signal, not a demographic-fairness finding."
- Stage-2 (`tab:stage2`): structure recovery ratio 0.907 (nDCG@5 0.917, skills↔required Spearman 0.996); model-selection 24/0; generalization candidate-unseen 0.929 / job-unseen 0.929 / both-unseen 0.927; scalability 516.9 ms/query at 10,000 jobs; simulated temporal-drift nDCG loss 0.149.
- Corpus: 30 resumes (avg 2.97 skills), 15 jobs (avg 2.13 required skills), 74 canonical skills, 47 labeled pairs (21 grade-2 + 26 grade-1, no grade-0); LLM second-pass κ=0.69, within-one-grade 100%.
- Engineering: 302 Python + 39 Node = **341 tests**, ±0.04 nDCG CI gate; bi-encoder ~0.4 ms, cross-encoder 141.7 ms, end-to-end < 10 ms; illustrative integration 200–300 eng-hours.

### (c) The submission ideology — "maximum scientific credibility, not maximum metric"

This manuscript is written to a single governing philosophy, and it is worth stating plainly for the next session because it explains almost every wording choice: **the paper optimizes for scientific credibility and reviewer trust, not for the biggest headline number.** The claimed contribution is an *auditable integration + an evaluation methodology*, explicitly **not a better ranker**. Once you internalize that, the otherwise-surprising choices (reporting parity when 0.949 > 0.878 looks like a win, keeping the *worse* calibrator as the default, spending the longest results subsection undercutting the team's own novel component) all become deliberate and coherent. Concretely, the ideology shows up as five recurring moves in the prose:

**1. Ranking is reported as PARITY, never superiority.** The composite reaches 0.949 vs the semantic baseline's 0.878 — a Δ that a less careful paper would headline as a win. Instead the abstract says results establish "methodological *feasibility*, not population-level ranking superiority" (`abstract.tex:4`); §5.1 says "we do not claim a statistically established ranking advantage" (`section-5-results.tex:52`); §6.2 says "we report ranking *parity*, not superiority" (`section-6-discussion.tex:43`). The p=0.10 / Holm-non-survival result is stated in the abstract, §5.1, §6.2, and §8 — four times, never buried. The paper even reframes the *inability to beat baselines* as itself a finding: parity is "partly a property of the measurement instrument, not only of the methods … 'this instrument cannot discriminate these methods at this scale'" (`section-5-results.tex:53`).

**2. The contribution is auditable INTEGRATION + evaluation methodology, not a new algorithm.** Every borrowed component is explicitly disclaimed as non-novel. `tab:contrib`'s caption: "The novelty is the auditable *integration* and its property-by-property evaluation, not a new ranking algorithm" (`section-1-introduction.tex:53`). §2 closing: "the individual components (BM25, Sentence-BERT, RRF, Platt scaling, rule-based explanation) are well-known, and the novelty is in their composition and in the evaluation methodology" (`section-2:58`). On calibration specifically: "we make no novelty claim for the act of calibrating a multi-channel score" (`section-2:50`, `section-3-methodology.tex:130`). The contribution is repeatedly labeled "an integration contribution, not a methodological breakthrough" (`section-7-future-work.tex:30`).

**3. Multi-agent is demoted to an engineering detail.** Despite the title, the multi-agent architecture is framed everywhere as failure-isolation/privacy plumbing, not science. §1.6: "the agent decomposition is an engineering/failure-isolation choice, not the scientific contribution" (`section-1-introduction.tex:42`). §3.3: role separation is "a design-for-accountability choice," the role boundary "is also the privacy boundary." §7: "the contribution is not in the agent architecture per se … The role separation … is a privacy-and-accountability choice, not a contribution to the agent architecture literature" (`section-7:25-28`). §8: "The multi-agent decomposition is an implementation choice that buys failure isolation, not a source of measured ranking benefit" (`section-8:3`). This is the ESWA-specific framing recorded in the project memory (ESWA demotes multi-agent; the JAAMAS variant foregrounds it).

**4. Every limitation is stated openly, up front, and un-hedged.** §6.2 opens "all stated explicitly and not hedged" (`section-6-discussion.tex:42`) and enumerates eight: (i) small corpus + positive-only labels + statistical power (30/15/47, no grade-0, closed-world grade-0 assumption "can only lower-bound the true relevance"); (ii) single author-annotator primary labels, LLM second pass at κ=0.69 is "not a second independent human rater"; (iii) the deployed Platt map's low discrimination (Brier skill ≈ 0); (iv) no human explanation study — "automated structural validation, not a demonstrated trust property"; (v) robustness gaps (not invariant to misspellings, mean |Δ| ≈ 0.12); (vi) simulated (not real) temporal/scale evidence; (vii) narrow fairness probe on synthetic proxy groups — "not a demographic-fairness audit"; (viii) learned-fusion overfitting. The same limitations recur in the abstract, §1, §3, §4, and §8 — the paper is engineered so a reviewer cannot find a weakness the authors haven't already named. Notably, the authors even undercut their *own* novel component: §5.7 spends a full paragraph explaining that the relation-aware p=0.03 "is the *smallest* value it can return for six concordant pairs — a direction-only certificate, not an effect size."

**5. Anti-fabrication / anti-leakage discipline is visible in the text itself.** Synthetic results are always flagged "never presented as human judgments" (`section-5-results.tex:163`, `tab:stage2` caption). In-sample numbers are shown then explicitly discounted (learned fusion 0.968 in-sample → "optimistic upper bound rather than a result," `section-5-results.tex:11`). The refusal to swap Platt→beta is justified precisely as leakage-avoidance ("choosing the calibration map on the evaluation — the very leakage this protocol avoids," `section-5-results.tex:87`). Structure recovery is stress-tested against its own construction bias — re-graded with a non-additive multiplicative latent and shown to still recover 0.891 — then still reported "NOT as evidence of general ranking superiority" but "a controlled validity check for the decomposition" (`section-5-results.tex:172-184`). Fixed weights are "hand-set domain priors, not fitted to the labeled pairs," stated in §3.2, §3.5 (twice), §5.7, and §7. Cost/deployment numbers are labeled "*illustrative* … not from a measured production deployment" (`section-3-methodology.tex:155`, `section-6-discussion.tex:14`). Even the demographic-proxy probe carries a construction caveat that two edit types "do not modify any field the deterministic ranker actually consumes, so their invariance is true *by construction*" (`section-5-results.tex:101`).

**Net effect for the next reader.** This is a paper whose rhetorical strategy is radical honesty as a credibility instrument: it repeatedly declines available "wins" (a nominal ranking lead, a better calibrator, a positive synthetic result, a p=0.03 novelty) and instead reports them as parity / directional / to-be-confirmed. When you edit or extend this manuscript, the strongest failure mode is *accidentally strengthening a claim* — e.g., calling parity "superiority," dropping a "directional signal" qualifier, promoting beta from "recommended upgrade" to "adopted," or letting the multi-agent framing creep back toward "scientific contribution." Any such change contradicts the submission ideology baked into every section and would be exactly what a hostile reviewer is primed to catch.

---

## Experiments, code, and reproduction

> Repo root for every path below: `/Users/kashhy/workspace/Personal/dev/Job-Matching-Agentic`. Citations are written repo-relative as `path:line` so you can jump straight there. Everything in this section is deterministic: `PYTHONHASHSEED=0` plus a hard-coded `SEED = 42` in every experiment script.

### 0. Mental model: three layers

The reproduction story has three physically separate layers, and confusing them is the single biggest onboarding trap:

| Layer | Location | What it is | Mutable? |
|---|---|---|---|
| **Live scorer** (production code) | `backend/core/` | The actual composite ranker + skill matcher the app and every experiment import | Frozen; weights are the single source of truth |
| **Experiments** | `research/experiments/` (+ `backend/benchmarks/`) | ~30 scripts that call the live scorer, run protocols, and emit JSON artifacts | Add-only; each is seed-pinned |
| **Manuscript** | `docs/submission/eswa/manuscript/{sections,tables}/*.tex` | LaTeX; tables are *auto-generated*, prose is hand-written | Tables regenerated; prose gated by a verifier |

Numbers flow strictly one way: **live scorer → experiment script → committed JSON artifact → auto-generated `.tex` table + `MANUSCRIPT_NUMBERS.json` manifest → hand-written prose → `verify_paper_numbers.py` gate**. No experiment ever writes into the manuscript directly, and no number is hand-typed into a table.

---

### 1. The six-channel composite scorer

**Where it lives:** `backend/core/scoring.py`. The weights are a module-level dict and are the *single source of truth* — every experiment imports `COMPOSITE_WEIGHTS` rather than re-declaring weights.

`backend/core/scoring.py:14-21`:

```python
COMPOSITE_WEIGHTS = {
    "semantic": 0.28,
    "skills": 0.27,
    "title": 0.10,
    "experience": 0.15,
    "compensation": 0.10,
    "remote": 0.10,
}
```

These six weights sum to exactly **1.0** (0.28 + 0.27 + 0.10 + 0.15 + 0.10 + 0.10). That sum is not a comment — it is an *executable acceptance check* (see §8, `verify_checks.py`).

**The composite function** is `compute_composite(...)` at `backend/core/scoring.py:107-151`. It computes each channel independently, blends linearly with the fixed weights, and clamps to `[0, 1]`:

`backend/core/scoring.py:127-135`:
```python
final = (
    COMPOSITE_WEIGHTS["semantic"] * semantic
    + COMPOSITE_WEIGHTS["skills"] * skills
    + COMPOSITE_WEIGHTS["title"] * title
    + COMPOSITE_WEIGHTS["experience"] * exp
    + COMPOSITE_WEIGHTS["compensation"] * comp
    + COMPOSITE_WEIGHTS["remote"] * remote
)
final = max(0.0, min(1.0, final))
```

The six channels, what each measures, its weight, and where it is computed:

| Channel | Weight | Function | File:line | Semantics |
|---|---|---|---|---|
| **semantic** | 0.28 | `compute_semantic` → `compute_similarity` | `scoring.py:61-76` | Cosine similarity of MiniLM (`all-MiniLM-L6-v2`) doc embeddings. `_safe_vec` (`scoring.py:52-58`) zeroes any NaN/inf so a corrupted embedding can't score as a spurious perfect match. |
| **skills** | 0.27 | `skills_score` (dispatch) | `skills.py:89-99` | Default `jaccard`; can be swapped to `graded` or `embedding` (see §2) |
| **title** | 0.10 | `title_similarity_score` | `component_scores.py:110-129` | Token overlap of job title vs candidate summary+skills after stopword strip; blend `0.6*coverage + 0.4*jaccard` |
| **experience** | 0.15 | `experience_score` | `component_scores.py:42-52` | Step function on the years-gap: gap≤0→1.0, ≤1→0.8, ≤2→0.6, ≤3→0.4, else 0.2 |
| **compensation** | 0.10 | `compensation_score` | `component_scores.py:61-94` | 1.0 inside budget band; graceful decay on overshoot/undershoot |
| **remote** | 0.10 | `remote_preference_score` | `component_scores.py:97-102` | 1.0 if candidate doesn't need remote or job allows it; 0.4 on conflict |

**Decomposition / explainability.** `build_composite_components` (`scoring.py:33-49`) attaches a `ScoreComponentDetail` per channel with `weight`, `score`, and `contribution = weight * score`. `COMPOSITE_COMPONENT_SPECS` (`scoring.py:23-30`) maps weight-key → breakdown attribute → human label. The invariant that Σ contributions reconciles to `final_score` (except when the `[0,1]` clamp fires) is enforced by `verify_checks.py` (§8).

There are also two simpler strategies in the same file the manuscript uses as baselines: `compute_semantic` (semantic-only) at `scoring.py:61` and `compute_multimodal_weighted` (2-channel blend, default `semantic_weight=0.7`) at `scoring.py:79-104`.

---

### 2. The graded, relation-aware skill matcher

**Where it lives:** `backend/core/skills.py`, backed by `backend/core/skill_catalog.py` (canonicalization + synonyms) and `backend/core/skill_taxonomy.py` (ESCO-lite groups).

The skill channel has **three interchangeable modes**, dispatched by `skills_score(...)` at `skills.py:89-99`:

- `"jaccard"` (default, incumbent) → `jaccard_skills` (`skills.py:6-13`): symmetric binary set-overlap `|A∩B| / |A∪B|` over *canonicalized* skills.
- `"embedding"` → `soft_overlap` (`skills.py:16-25`): for each job skill, best cosine over resume-skill embeddings, averaged.
- `"graded"` → `graded_coverage_skills` (`skills.py:57-86`): the novelty.

**The graded matcher** (`skills.py:57-86`) is *asymmetric* (coverage-oriented: how well the candidate covers the job's requirements) and *relation-aware*. For each job skill it takes the best graded credit from any resume skill:

- exact canonical match → `GRADED_EXACT_CREDIT = 1.0`
- same ESCO-lite taxonomy group → `GRADED_RELATED_CREDIT = 0.5`
- otherwise → 0.0

then averages over the job skills. The two credit constants are **frozen a priori** at `skills.py:51-55` (explicitly "NOT tuned on any evaluation" — this is load-bearing for the paper's anti-overfitting story). The `related_credit` argument exists *only* for the reported robustness sweep, never for tuning on the test corpus.

**Canonicalization** (`skill_catalog.py`): `canonical_skill` (`skill_catalog.py:63-75`) lower-cases, applies synonym maps loaded from `shared/skill_catalog.json` (`skill_catalog.py:10`), tries punctuation/spacing variants (`_variant_keys`, `skill_catalog.py:42-52`), and collapses any `aws …`/`amazon …` prefix to `"aws"` (`skill_catalog.py:72-73`).

**Taxonomy** (`skill_taxonomy.py`): a hand-built ESCO-lite map of 7 parent groups → member canonical skills (`skill_taxonomy.py:7-30`): `programming`, `ml_ai`, `data`, `web_frontend`, `web_backend`, `devops_cloud`, `mobile`. `skill_groups` (`skill_taxonomy.py:33-39`) maps a skill list to the set of groups it touches; two skills are "related" iff their group sets intersect.

**The three-way gain decomposition** (this is the reviewer-hardened design). Because a naive "jaccard vs graded" comparison confounds the *coverage form* (symmetric→asymmetric) with the *relation-aware credit*, the experiments always split it into three pre-specified variants:

- `jaccard_symmetric` — incumbent
- `exact_coverage_asymmetric` — graded with `related_credit=0.0` (isolates the coverage-form effect)
- `graded_coverage_asymmetric` — `related_credit=0.5` (isolates the relation-aware effect on top)

---

### 3. The experiment suite

Every experiment is a standalone `python3` script under `research/experiments/`; `reproduce_all.sh` runs them in dependency order. Each carries its own `SEED = 42`, writes exactly one JSON to `research/results/` (or `backend/reports/extended_evaluation/`), and prints a summary. Full inventory as driven by the orchestrator (`scripts/reproduce_all.sh:24-52`):

| EXP | Script | RQ | Output artifact |
|---|---|---|---|
| EXP-011 | `backend/benchmarks/extended_evaluation.py` | core | `backend/reports/extended_evaluation/*.json` (kfold_cv, pointwise_ltr, calibration_binary, counterfactual_50, parser_robustness, cold_start) |
| EXP-012 | `research/experiments/job_heldout.py` | RQ7 | `research/results/job_heldout.json` |
| EXP-013 | `research/experiments/leave_one_out_ablation.py` | RQ2 | `leave_one_out_ablation.json` |
| EXP-014a | `research/experiments/lambdamart_baseline.py` | RQ1 | `lambdamart_baseline.json` |
| EXP-014b | `research/experiments/jobbert_baseline.py` | RQ1 | `jobbert_baseline.json` |
| EXP-015 | `research/experiments/weight_stability.py` | RQ2 | `weight_stability.json` |
| EXP-019 | `research/experiments/architecture_value.py` | RQ8 | `architecture_value.json` |
| EXP-020 | `research/experiments/calibration_discrimination.py` | RQ3 | `calibration_discrimination.json` |
| EXP-022 | `research/experiments/significance_corrected.py` | RQ1 | `significance_corrected.json` |
| EXP-023 | `research/experiments/synthetic/generate_synthetic.py` | §F-G | `research/datasets/synthetic_v1/*.json` (**must run first**) |
| EXP-024 | `research/experiments/synthetic/structure_recovery.py` | §F-H | `structure_recovery.json` |
| EXP-024b | `research/experiments/synthetic/structure_recovery_nonadditive.py` | control | `structure_recovery_nonadditive.json` |
| EXP-025 | `research/experiments/model_selection/search.py` | §D-E | `model_selection.json` |
| EXP-026 | `research/experiments/calibration_methods.py` | §N | `calibration_methods.json` |
| EXP-027 | `research/experiments/generalization.py` | §J | `generalization.json` |
| EXP-028 | `research/experiments/explanation_faithfulness.py` | §O | `explanation_faithfulness.json` |
| EXP-029 | `research/experiments/robustness_matrix.py` | §R | `robustness_matrix.json` |
| EXP-030 | `research/experiments/temporal_drift.py` | §S | `temporal_drift.json` |
| EXP-033 | `research/experiments/failure_injection.py` | §V | `failure_injection.json` |
| EXP-034 | `research/experiments/skill_semantics.py` | P1 | `skill_semantics.json` |
| EXP-034b | `research/experiments/skill_semantics_objective.py` | P1 | `skill_semantics_objective.json` |
| EXP-035/036 | `research/experiments/synthetic/feature_fusion_synth.py` | P2/P3 | `feature_fusion_synth.json` |
| EXP-043/044 | `research/experiments/graded_skill_channel.py` | Stage-3 | `graded_skill_channel.json` |
| — | `research/experiments/generate_manuscript_tables.py` | §AA | `tables/*.tex` + `MANUSCRIPT_NUMBERS.json` |
| — | `research/experiments/make_reliability_fig.py` | §30 | `fig4` reliability figure |
| — | `research/experiments/verify_checks.py` | gate | acceptance checks (exit code) |
| — | `research/experiments/verify_paper_numbers.py` | gate | number consistency (exit code) |

**Two things deliberately NOT in the default pipeline** (`scripts/reproduce_all.sh:9-12, 56-58`):
- **Scalability micro-benchmark** (duplicate-15-jobs) is opt-in via `RUN_SCALABILITY=1` — it's flagged non-defensible by the audit and superseded by EXP-016.
- **EXP-018 LLM-assisted labels** (`llm_label_expansion.py`) needs a local `claude -p` binary and is not deterministic, so it's run explicitly and separately.

**The three governing experiment scripts you were asked to understand:**

**`calibration_methods.py` (EXP-026)** — `research/experiments/calibration_methods.py`. Compares five calibration maps against a *defined* probability target `p_ij = P(y=1 | s_ij)` where `y=1` iff graded relevance ≥ 1 and `s` is the fixed 6-channel composite (`calibration_methods.py:4-16`). Protocol: held-out 5-fold over resumes, fit on train folds, evaluate on pooled held-out predictions, **never fit on test** (`calibration_methods.py:135-162`). Maps: `raw`, `platt` (`core.PlattCalibrator`), `isotonic` (`sklearn.IsotonicRegression`), `temperature` (1-param NLL fit, `fit_temperature` at line 91), and `beta` (Kull et al. 2017, logistic on `[ln s, −ln(1−s)]`, `fit_beta` at line 75). Reports ECE (10-bin), *adaptive* equal-mass ECE (`ece_adaptive`, line 59 — added because composite scores cluster in a narrow band and equal-width bins understate miscalibration), MCE, Brier, Brier-skill-score vs the constant base-rate floor, ROC-AUC, reliability curve, and a 2000-sample bootstrap CI on ECE (`bootstrap_ece_ci`, line 106). The corpus is n=450 pairs, base rate 0.104. Headline result (from `research/results/MANUSCRIPT_NUMBERS.json`): raw ECE 0.3995 / AUC 0.967 but BSS −1.25 (razor-thin), Platt ECE 0.0179 but **adaptive** ECE 0.084 (exposes discrimination collapse, AUC 0.7577), **beta** ECE **0.0089** / adaptive **0.0093** / BSS 0.6734 / AUC 0.964 (the winner — low ECE under *both* binnings while preserving discrimination), isotonic a close second.

**`graded_skill_channel.py` (EXP-043/044)** — `research/experiments/graded_skill_channel.py`. Two questions under the frozen `research/PROTOCOL.md` discipline (develop on synthetic; touch the real corpus ONCE). **(A) By-construction audit** (`by_construction_audit`, line 107): shows `required_coverage`/`preferred_coverage` are (up to canonicalization) *identical* to the synthetic latent generative factors (weights 0.40 + 0.12 = 0.52 of the latent score) — so the `+derived` fusion win is largely by construction and is honestly discounted; the defensible gain is base6 nonlinear fusion. Result: `corr_required_coverage_vs_latent_required = 1.0`, base6-semantic-vs-latent only 0.5435. **(B) Graded channel** swaps only the skill channel in the fixed composite (all other weights unchanged) and reports the three-way decomposition on synthetic (n=500, `graded_channel_synthetic`, line 177) and on the real corpus in one prospective run (n=30, `graded_channel_real`, line 238). Real-corpus result (`graded_skill_channel.json`): jaccard 0.94924 → exact_coverage 0.94223 → graded 0.99237; the relation-aware step (graded vs exact) is +0.05014, CI [0.00424, 0.12599], perm-p 0.0312, improving 6/30 queries and worsening 0. Stats use `bootstrap_paired` (3000-boot CI + 20000-perm sign-flip test, line 64).

**`powered_reeval.py` (Goal-2 enablement)** — `research/experiments/powered_reeval.py`. Self-contained; does **not** modify `reproduce_all.sh`. It's a "ready when the negatives arrive" harness: once explicitly-negative-judged labels exist (annotate `annotation_sheet_unjudged.csv` → `merge_annotations.py` → `data/eval_pairs_expanded.json`), one command reports the label distribution, per-method nDCG@5, the composite-vs-semantic significance re-test, and the jaccard/exact/graded decomposition with real statistical power. Eval-file resolution (`_resolve_eval_path`, line 40): `argv[1]` → `EVAL_PAIRS` env → `data/eval_pairs_expanded.json` if present → `data/eval_pairs.json`. Until negatives exist it prints a NOTE that the current corpus is positive-only and the test is a tooling smoke-test (line 146-148). This is the honest "we can't over-claim on a positive-only corpus" hedge baked into runnable code.

---

### 4. The synthetic corpus generator

**`research/experiments/synthetic/generate_synthetic.py` (EXP-023).** Deterministic (seed 42), versioned. Default `synthetic_v1` = **500 resumes × 75 jobs** (`generate_synthetic.py:22-25`), overridable via `SYNTH_VERSION`/`SYNTH_N_RESUMES`/`SYNTH_N_JOBS` env vars (a `synthetic_v2` of 2000×200 is supported). Ten job families, each with a core skill pool plus adjacent-family "noise" skills injected to create HARD overlaps (`FAMILIES`, line 29-40; `_skills_for`, line 51).

The crux is a **transparent, known latent relevance function** (NOT an LLM) so the paper can test whether the ranker *recovers known structure*. `latent_relevance` (line 102-115) computes seven factors (required-skill coverage, preferred coverage, seniority, experience, family, work-mode, compensation) and blends them with fixed weights `LW` (line 48):

```
required 0.40 · preferred 0.12 · seniority 0.15 · experience 0.13 · family 0.10 · workmode 0.05 · comp 0.05
```

`to_grade` (line 118) buckets the latent into graded relevance {0,1,2,3} at thresholds 0.40/0.60/0.80, then 8% controlled label noise is applied (line 132). Outputs `synthetic_resumes.json`, `synthetic_jobs.json`, `synthetic_relevance.json` (every label carries `latent_score`, `latent_factors`, `clean_grade`, noisy `relevance`), and a `manifest.json`, all under `research/datasets/synthetic_v1/`. Provenance strings hard-label the data `SYNTHETIC / CONTROLLED — NOT human judgments` so it can never be misrepresented (line 142). This artifact **must be generated before** EXP-024/030/035/043 (they read it) — hence its position in `reproduce_all.sh:35`.

The **real human corpus**, by contrast, is `data/cvs.json` (30 resumes) × `data/jobs.json` (15 jobs) = **450 pairs** with `data/eval_pairs.json` graded relevance — the "30×15/450" figures that appear throughout the manuscript and match the calibration n=450 / base-rate 0.104.

---

### 5. Reproducing everything

**Prerequisites.** A Python venv at `backend/.venv`. Dependencies are pinned in `backend/requirements-min.txt` (runtime) and `backend/requirements-research.txt` (scikit-learn, scipy, xgboost, matplotlib used by the evaluation scripts) — see `scripts/reproduce_all.sh:7-8`.

**The one command** (`scripts/reproduce_all.sh`):

```bash
bash scripts/reproduce_all.sh
```

What it does mechanically (`reproduce_all.sh:13-22`): sets `set -euo pipefail`, `cd`s into `backend/`, uses `./.venv/bin/python`, and exports a determinism-and-stability environment:

```
PYTHONHASHSEED=0  PYTHONPATH=.  OMP_NUM_THREADS=1  MKL_NUM_THREADS=1  TOKENIZERS_PARALLELISM=false
```

The single-threading of the numeric/tokenizer stacks is not cosmetic: the header notes that on a loaded machine torch/tokenizers otherwise hang at 0% CPU on startup (`reproduce_all.sh:17-18`). It then runs each EXP in dependency order (§3 table), regenerating `backend/reports/extended_evaluation/*.json` and `research/results/*.json`, auto-generating the manuscript tables, regenerating fig4, and finally running both verifiers. It prints `=== DONE ===` and reminds you of the two opt-in extras.

**The standalone number-consistency gate** (can be run alone, matches the exact invocation in the file docstring `verify_paper_numbers.py:8`):

```bash
PYTHONHASHSEED=0 python3 research/experiments/verify_paper_numbers.py
```

---

### 6. What the verifier gates (REQUIRED + FORBIDDEN) and why

`research/experiments/verify_paper_numbers.py` scans **every `.tex`** under `docs/submission/eswa/manuscript/sections/` and `.../tables/` and exits non-zero (so it can gate a build) if anything is wrong. It enforces two lists.

**FORBIDDEN** (`verify_paper_numbers.py:23-39`) — stale/phantom/fabricated numbers and over-claims that must NOT appear, unless the surrounding line is an explicit correction note (the checker whitelists lines containing `superseded|earlier|no longer|we report the held-out|optimistic upper`, `verify_paper_numbers.py:68`). These encode specific audit findings the paper was caught on:

| Forbidden pattern | Why it's banned |
|---|---|
| `0.969` "best single" / `R@5 = 1.000` | phantom best-single-method numbers |
| "nine times out of ten" | over-claimed 0.9 → 9/10 |
| "Seven of the ten" / "7 of 10" | superseded 10-pair counterfactual |
| `p = 0.048` | salted-seed significance |
| "statistically significant over" | unsupported significance claim |
| "two independent reviewers/annotators" | false two-annotator claim (there was one) |
| `12.3 skills`, `8.7 required`, `4.2 preferred` | fabricated corpus statistics |
| "maximize nDCG@5 on held-out", "weights fixed/tuned by nDCG" | the **B11 leak** — claiming weights were fitted to the eval metric (they are frozen a priori) |
| `RRF … 0.935` | stale RRF number |

**REQUIRED** (`verify_paper_numbers.py:41-45`) — canonical numbers that MUST appear somewhere in the manuscript:

```
0.949, 0.878, 0.913, 0.924, 0.019, 2.97, 2.13,     # core ranking + significance
0.917, 0.944, 0.992, 0.942, 0.947, 0.961,          # EXP-043/044 graded-skill + EXP-035/036 fusion
0.009, 0.084                                        # EXP-041 beta ECE + adaptive-ECE exposure of Platt
```

It additionally cross-checks three headline manifest entries (`ndcg5::Semantic cosine`, `ndcg5::RRF ensemble`, `composite_ndcg5`) against `research/results/MANUSCRIPT_NUMBERS.json` and confirms they appear verbatim in the prose (`verify_paper_numbers.py:78-84`). On any FORBIDDEN hit or MISSING canonical number it prints `=== PROBLEMS ===` and returns 1.

**The second gate — `verify_checks.py`** (`research/experiments/verify_checks.py`) — is executable acceptance testing, not prose scanning. It asserts (1) `COMPOSITE_WEIGHTS` sum == 1.0 to 1e-12 (`verify_checks.py:23-25`), (2) the displayed score decomposition Σ contributions reconciles to `final_score` except where the `[0,1]` clamp fires, and surfaces clamp/negative-component events (audit H11) (`verify_checks.py:27-63`), and (3) a reusable train/test entity-overlap leakage checker with a self-test (`verify_checks.py:65-73`). Exits non-zero on any FAIL.

---

### 7. How numbers flow: artifact → table → manuscript

`research/experiments/generate_manuscript_tables.py` is the **single source of truth** for every table number. It reads committed JSON artifacts and writes both the `.tex` tables and the machine-checkable manifest (`generate_manuscript_tables.py:1-8`). Every number it emits is recorded via `rec(key, value, source)` (`generate_manuscript_tables.py:28-30`) into `research/results/MANUSCRIPT_NUMBERS.json` as `{value, source-artifact}` — so any manuscript number is traceable to the file that produced it.

Key sources it standardizes on (this fixed the audit's number-drift, e.g. semantic 0.878 vs 0.911, RRF 0.913 vs 0.935 — caused by different document-text templates):
- Ranking table `tab-progression.tex` ← `backend/reports/research_run_20260606T150509Z/comparison_table.json` (the canonical single-template run) + `composite_eval_report.json` for the composite reference (nDCG@5 = **0.949**).
- Latency table `tab-latency.tex` ← same `comparison_table.json`.
- Calibration table `tab-calibration.tex` ← `research/results/calibration_methods.json` + `backend/reports/extended_evaluation/calibration_binary.json`.
- Stage-2 evidence `tab-stage2.tex` ← `structure_recovery.json`, `model_selection.json`, `generalization.json`, `scalability.json`, `temporal_drift.json`.

The manifest currently pins, among others: `composite_ndcg5 = 0.949`, `ndcg5::Semantic cosine = 0.878`, `ndcg5::RRF ensemble = 0.913`, `ndcg5::Multimodal weighted blend = 0.924`, `calib::beta::ece = 0.0089`, `calib::platt::adaptive_ece = 0.084`, `recovery_ratio = 0.9066`, `ece_platt_heldout = 0.019…`. These are exactly the values `verify_paper_numbers.py` then requires to be present in the prose — closing the loop.

**End-to-end chain:** live scorer (`backend/core/`) → experiment script (`research/experiments/…`) → `research/results/*.json` + `backend/reports/**/*.json` → `generate_manuscript_tables.py` → `docs/submission/eswa/manuscript/tables/*.tex` + `MANUSCRIPT_NUMBERS.json` → hand-written `sections/*.tex` → `verify_paper_numbers.py` + `verify_checks.py` gate the whole thing.

---

### 8. COMMANDS (copy-paste)

```bash
# ---- 0. repo root ----
cd /Users/kashhy/workspace/Personal/dev/Job-Matching-Agentic

# ---- 1. one-command deterministic reproduction of the full ESWA extended evaluation ----
#   regenerates backend/reports/extended_evaluation/*.json and research/results/*.json,
#   auto-generates docs/submission/eswa/manuscript/tables/*.tex, and runs both gates.
bash scripts/reproduce_all.sh

# ---- 2. run the manuscript number-consistency gate on its own (FORBIDDEN + REQUIRED) ----
PYTHONHASHSEED=0 python3 research/experiments/verify_paper_numbers.py

# ---- 3. run the executable acceptance checks (weight-sum / decomposition / leakage) ----
cd backend && PYTHONPATH=. .venv/bin/python ../research/experiments/verify_checks.py; cd ..

# ---- 4. run a single experiment (env mirrors reproduce_all.sh; run from backend/) ----
cd backend
export PYTHONHASHSEED=0 PYTHONPATH=. OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false
./.venv/bin/python ../research/experiments/calibration_methods.py            # EXP-026 calibration
./.venv/bin/python ../research/experiments/graded_skill_channel.py           # EXP-043/044 graded skill
./.venv/bin/python ../research/experiments/synthetic/generate_synthetic.py   # EXP-023 (run FIRST)
./.venv/bin/python ../research/experiments/powered_reeval.py                 # Goal-2 (positive-only until negatives merged)
cd ..

# ---- 5. regenerate the manuscript tables + MANUSCRIPT_NUMBERS.json from artifacts ----
cd backend && PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/generate_manuscript_tables.py; cd ..

# ---- 6. opt-in / non-default extras ----
# scalability micro-benchmark (audit-flagged, off by default):
cd backend && RUN_SCALABILITY=1 PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python benchmarks/extended_evaluation.py; cd ..
# LLM-assisted labels (needs local `claude -p`; NOT deterministic, run separately):
cd backend && PYTHONPATH=. .venv/bin/python ../research/experiments/llm_label_expansion.py; cd ..
# larger synthetic corpus (optional):
cd backend && SYNTH_VERSION=synthetic_v2 SYNTH_N_RESUMES=2000 SYNTH_N_JOBS=200 \
  PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/synthetic/generate_synthetic.py; cd ..

# ---- 7. powered re-eval against a specific eval file (once real negatives exist) ----
cd backend && EVAL_PAIRS=$PWD/data/eval_pairs_expanded.json \
  PYTHONHASHSEED=0 PYTHONPATH=. OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false \
  .venv/bin/python ../research/experiments/powered_reeval.py; cd ..
```

---

### 9. Gotchas for the next session

- **Always regenerate the synthetic corpus first.** EXP-024/030/035/043 read `research/datasets/synthetic_v1/`; `reproduce_all.sh` orders this correctly but a manual single-run will crash without it.
- **Run experiments from `backend/`** with `PYTHONPATH=.` — they import `config`, `core.*`, `contracts.*`, and `benchmarks.*` as top-level modules.
- **Weights are frozen and singular.** Never re-declare weights in an experiment; import `COMPOSITE_WEIGHTS` from `backend/core/scoring.py`. The B11 forbidden patterns in `verify_paper_numbers.py` exist specifically to catch any prose implying the weights were tuned on the eval metric.
- **The real corpus is positive-only and tiny (30×15=450).** That's why `powered_reeval.py` exists and why the graded-channel real run is a single prospective touch. Do not present synthetic numbers as human judgments — the generator hard-labels provenance for exactly this reason.
- **If a build/gate fails**, the two gates tell you where: `verify_checks.py` = code invariant broken (weights/decomposition/leakage); `verify_paper_numbers.py` = a manuscript number drifted from its artifact or a forbidden/over-claim phrase reappeared. Fix the artifact + rerun `generate_manuscript_tables.py`, don't hand-edit the `.tex` tables (they say "Auto-generated; do not hand-edit").

---

## ESWA submission logistics (authors, cover letter, risk, protocols)

This section is the operational "who / where / how" of the *Expert Systems with Applications* (ESWA, Elsevier) submission: the frozen author list and contact details, the cover letter, every declaration the portal requires, the double-blind anonymization mechanics, the editorial-risk matrix that drives the accept/reject strategy, and the two author-gated human/annotation protocols that are drafted but not yet run. All facts below are lifted verbatim from the committed submission files under `docs/submission/eswa/` and `scripts/`. Where a decision superseded an earlier one, the current state is called out.

> **One governing fact to carry into every subsection:** ESWA is a **double-anonymized (double-blind)** venue. The manuscript body and released test fixtures are anonymized; the **title page and cover letter are the deliberately NON-anonymous parts** and are uploaded as separate files that Editorial Manager withholds from reviewers (`scripts/anonymize_reviewer_bundle.py:5-8`, `docs/submission/eswa/title-page.tex:1-2`).

---

### 1. Final author list, affiliations, and contacts

The author list is **frozen** and is identical across the title page (`title-page.tex:38-68`), the cover letter (`cover-letter.md:5-6,15`), and the submission-form guide (`SUBMISSION-FORM-GUIDE.md:56-89`). Do not change it without supervisor sign-off — the supervisor explicitly deferred author-list resolution "separately from contribution history (author-only)" (`docs/submission/PROFESSOR_FEEDBACK_PLAN.md:25`, question 7).

| Order | Name | Role | Affiliation | Email | Corresponding? |
|---|---|---|---|---|---|
| 1 | **Harsh Kashyap** | Joint first author | Dept. of Computer Science and Engineering, Thapar Institute of Engineering and Technology, Patiala, Punjab 147004, India | `hkashyap_be19@thapar.edu` | **YES** |
| 2 | **Taranumpreet Kaur Wasu** | Joint first author | Same (Thapar Institute) | `twasu_be20@thapar.edu` | No |
| 3 | **Parteek Kumar** | Research supervisor | School of Electrical Engineering and Computer Science, Washington State University, Pullman, WA 99164, USA | `parteek.kumar@wsu.edu` | No |

Key points:
- **Joint first authorship.** Kashyap and Wasu "contributed equally to this work (joint first authors)" — both carry the `$^{1,*}$` marker and the footnote at `title-page.tex:40-41,50`. The cover letter states this explicitly: "joint-first-authored by Harsh Kashyap and Taranumpreet Kaur Wasu … under the supervision of Parteek Kumar" (`cover-letter.md:15`).
- **Corresponding author = Harsh Kashyap**, `hkashyap_be19@thapar.edu` (`title-page.tex:58-61`; `cover-letter.md:5,43`; `SUBMISSION-FORM-GUIDE.md:5,61,213`). Editorial Manager login is under this same address (`SUBMISSION-FORM-GUIDE.md:5`).
- **Affiliation split:** authors 1–2 are Thapar Institute (India); author 3 (supervisor) is Washington State University (USA) (`title-page.tex:44-48`). Note this is a cross-institution, two-country author set — relevant for the DOI/COI forms.
- **Optional corresponding-email note:** if Harsh prefers a current WSU or Apple email for the corresponding field, that is allowed — "The DOI form only requires that an institutional email be on file" (`SUBMISSION-FORM-GUIDE.md:89`). Default stays the Thapar address.

**ORCIDs are deferred.** The title page does NOT print ORCID numbers; it states "ORCID identifiers for all three authors are provided in the Editorial Manager submission system" (`title-page.tex:71`). The form guide flags ORCID for the *corresponding* author as the one that must be registered before submission (Harsh registers at orcid.org, ~5 min, free), while co-authors' ORCIDs are optional/blank-if-unregistered (`SUBMISSION-FORM-GUIDE.md:62,71,82,172`). Earlier drafts had `[to be added]` ORCID placeholders that Step 0 tells the submitter to replace (`SUBMISSION-FORM-GUIDE.md:23-28`).

**CRediT contribution statement** (`title-page.tex:94-100`):
- **Harsh Kashyap:** Conceptualization, Methodology, Software, Investigation, Writing – original draft, Writing – review & editing.
- **Taranumpreet Kaur Wasu:** Conceptualization, Software, Investigation, Data Curation, Writing – original draft, Writing – review & editing.
- **Parteek Kumar:** Conceptualization, Supervision, Writing – review & editing, Funding acquisition.

---

### 2. Paper title, article type, and submission coordinates

| Field | Value | Source |
|---|---|---|
| **Title** | **An Auditable, Calibrated, and Explainable Multi-Agent System for Job-Candidate Recommendation** | `title-page.tex:29-30`; `cover-letter.md:6,13`; `SUBMISSION-FORM-GUIDE.md:46,199` |
| Article type | Research Article (NOT Review) | `title-page.tex:21`; `SUBMISSION-FORM-GUIDE.md:36` |
| Section/Category | Applications | `SUBMISSION-FORM-GUIDE.md:37` |
| Journal | *Expert Systems with Applications* (Elsevier) | `title-page.tex:19` |
| Editor-in-Chief | Prof. Ling Wang, PhD | `cover-letter.md:3`; `SUBMISSION-FORM-GUIDE.md:222` |
| Portal | Elsevier Editorial Manager, `editorialmanager.com/eswa/` | `SUBMISSION-FORM-GUIDE.md:4,223` |
| Submission date | August 17, 2026 (Monday) | `title-page.tex:20`; `cover-letter.md:7`; `SUBMISSION-FORM-GUIDE.md:6` |
| Keywords (7) | recommender systems; explainable AI; confidence calibration; skill matching; job-candidate matching; auditable ranking; recruitment | `SUBMISSION-FORM-GUIDE.md:48,201-207` |
| Manuscript size | 36 pp, ~9,643 body words, 13 figures, 6 tables, 41 references; abstract 184 words | `SUBMISSION-FORM-GUIDE.md:208-212` |
| Code commit | `02a700e` | `SUBMISSION-FORM-GUIDE.md:219` |
| APC | $0 (subscription) / $3,490 (gold OA) / $698 (India GPOA) | `SUBMISSION-FORM-GUIDE.md:226` |

**Title history — do not revert.** The word "Trustworthy" was deliberately **dropped** from the title. Editorial-risk item #9 (a HIGH-probability "multi-agent / trustworthy overclaim" flag raised 3× across review rounds) records the fix on 2026-08-18: `"trustworthy"→"calibrated"` in the body, title changed to the current wording, "kept honest 'Multi-Agent'," and propagated to `main.tex`, `title-page.tex`, `cover-letter.md`, and `SUBMISSION-FORM-GUIDE.md` (`EDITORIAL_RISK_MATRIX.md:18`). The supervisor confirmed keeping this title and only flagged an open question of whether "Multi-Agent System" should *lead* the title given that ESWA's strongest story is the methodology/auditability, "decide against the actual abstract" (`PROFESSOR_FEEDBACK_PLAN.md:19-21`).

> **CAUTION (submission-timing note):** the guide's dates (submit Aug 17; first-decision ~Aug 22; reviewer decision ~mid-Oct) describe the *original* "submit now" plan. The **governing** supervisor plan of 2026-08-18 (§5 below) says **HOLD submission** until the larger benchmark is annotated. Treat the Aug 17 date on the title page/cover letter as a template value, not a completed action.

---

### 3. Cover letter (`cover-letter.md`)

The cover letter is an **unblinded** ~1-page letter to EiC Ling Wang. Its structure and load-bearing claims:

- **Header block** (`:3-7`): To Ling Wang; From Harsh Kashyap (corresponding); co-authors Wasu + Kumar; Research Article; dated Aug 17, 2026.
- **Authorship paragraph** (`:15`): confirms joint-first + supervision, corresponding author, and that "All three authors have read and approved the submitted version."
- **Real-world problem** (`:17`): opaque single-score rankings in hiring create an accountability gap.
- **AI methodology contribution** — four numbered claims (`:19-23`):
  1. Composite score decomposing into **six explicit channels** (semantic similarity, skill overlap, title fit, experience tier, compensation fit, remote policy), each with a documented weight.
  2. Platt-scaled calibrated confidence reducing **held-out 5-fold ECE from 0.40 (raw) to 0.019**, with the honest caveat of "limited discrimination" and comparison against isotonic + temperature scaling.
  3. Component-level faithfulness suite + counterfactual probe.
  4. Reproducible artifact: prototype, **frozen demo corpus (30 resumes, 15 jobs, 47 labeled pairs)**, explanation generator, calibration layer, and a **341-test regression-gated benchmark**.
- **Application consequence + honest parity** (`:25`): composite reaches **nDCG@5 = 0.949** (strongest single configuration 0.924); improvement over baselines is "positive but *not* statistically significant (two-sided *p* = 0.10, no comparison survives Holm correction)"; frames the contribution as "auditable, calibrated, explainable methodology rather than ranking superiority."
- **Why ESWA fits** (`:27`): intelligent system validated in a controlled application setting; reproducible via one-command script; artifact deposited with citable DOI **upon acceptance**; anonymized copy available to reviewers during review.
- **Funding** (`:29`): the NVIDIA grant (see §4, verbatim); "No external funding was received for the development of the ESWA manuscript."
- **Originality & approvals** (`:31`): original, not under consideration elsewhere, all authors approved, "We declare no competing interests."
- **Institutional email** (`:33`): all three authors' institutional emails are in Editorial Manager and on the title page.
- **Sign-off** (`:39-43`): Harsh Kashyap, corresponding, Thapar Institute, `hkashyap_be19@thapar.edu`.

A rendered `cover-letter.docx` (13,171 bytes, dated Aug 18) sits beside the Markdown for upload; the form guide says to convert `cover-letter.md` → docx and upload it as file type "Cover letter" (`SUBMISSION-FORM-GUIDE.md:21,101`).

---

### 4. Declarations (all on the title page + the DOI form)

Because ESWA is double-blind, **all declarations live on the separate unblinded title page** (`title-page.tex:77-124`), NOT in the manuscript body. The five declaration blocks:

1. **Acknowledgments / NVIDIA grant (KEEP VERBATIM)** (`title-page.tex:78-85`). This exact wording must be preserved across title page, cover letter, and the DOI form:
   > "This work was supported by the NVIDIA Academic Grant Program through an unrestricted gift of 32,000 NVIDIA A100 GPU-hours on the Brev cloud platform."
   The full acknowledgment also thanks "the JobMatch development team at Thapar Institute of Engineering and Technology for portal implementation and evaluation," reviewers, and both institutions. The cover letter repeats the grant verbatim (`cover-letter.md:29`), and the form guide's DOI merged statement repeats it again (`SUBMISSION-FORM-GUIDE.md:120-126`). The grant is classified as **non-financial support** ("Non-financial (32,000 A100 GPU-hours on Brev cloud)"), received by "Harsh Kashyap (and the project as a whole)" (`SUBMISSION-FORM-GUIDE.md:117-120`).

2. **Declaration of competing interest** (`title-page.tex:88-91`): "The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper." → **No competing interests.**

3. **CRediT authorship contribution statement** (`title-page.tex:94-100`) — see §1.

4. **Data availability** (`title-page.tex:103-111`): the frozen demo corpus (30 resumes, 15 job descriptions, 47 labeled pairs), the synthetic corpus + generator, evaluation scripts, explanation generator, calibration layer, and the regression benchmark **"will be deposited in a public repository (Harvard Dataverse) with a citable DOI upon acceptance; an anonymized copy … is available to reviewers during review."** The release includes the one-command reproduction script, auto-generated tables, per-experiment JSON artifacts, and figure source scripts. **Do NOT assert a live DOI before it resolves** — the form checklist is explicit about this (`SUBMISSION-FORM-GUIDE.md:169`, `:218` "to be minted upon acceptance").

5. **Declaration of generative AI** (`title-page.tex:114-123`): the authors used **OpenAI ChatGPT (GPT-4 model)** as a language-model assistant for copy-editing selected paragraphs, drafting figure captions from a structured outline, and suggesting literature-review edits; all technical content is the authors' own; authors reviewed/edited and take full responsibility. Repeated in the DOI form (`SUBMISSION-FORM-GUIDE.md:171,221`).

**Ethics statement** (`SUBMISSION-FORM-GUIDE.md:133-135`): "Not applicable. Evaluation uses synthetic and manually curated demo profiles; no human subjects recruitment data were collected for this study." (This holds only as long as the §6 human study is NOT run before submission.)

**Per-author DOI form** (`SUBMISSION-FORM-GUIDE.md:114-127`): each of the 3 authors completes the Declaration of Interests separately — Research Support = YES (NVIDIA, non-financial), Other Support / IP / Other Activities = None. Each author receives an authorship-confirmation email link (14-day window) that Harsh forwards (`SUBMISSION-FORM-GUIDE.md:128-131,187`).

---

### 5. Double-blind anonymization mechanics (`scripts/anonymize_reviewer_bundle.py`)

ESWA double-anonymized review requires the reviewer-facing bundle to carry zero author identity. The split:

- **Already anonymous:** the manuscript body and the released test fixtures (`anonymize_reviewer_bundle.py:4`).
- **Deliberately NOT anonymized (never touched by the script):** the ESWA title page and cover letter — these are the correct non-anonymous parts, uploaded as separate files Editorial Manager withholds from reviewers (`anonymize_reviewer_bundle.py:5-6`; `SUBMISSION-FORM-GUIDE.md:106-108`).
- **The gap the script closes:** the project README + design docs still carry author identity and the real repo URL, and must be scrubbed in the copy shipping alongside the anonymized manuscript.

**What the script does:**
- Reads `README.md`, `docs/design/HLD-multi-agent-system.md`, `docs/design/SDD-multi-agent-system.md`, `docs/design/V1-V2-SCOPE.md` (`:25-30`).
- Writes scrubbed copies under `build/anon/` and **never mutates the working tree** — so real attribution survives for the public release on acceptance (`:8-9,56-59`).
- Applies ordered regex substitutions (`:33-44`): the real GitHub repo `github.com/Harsh23Kashyap/…` → `https://anonymous.4open.science/r/JobMatch`; LinkedIn → `linkedin.com/in/anonymous`; "Harsh Kashyap" → "Anonymous Author"; "Taranumpreet Kaur Wasu" → "Anonymous Author"; "Parteek Kumar" → "Anonymous Supervisor"; "Thapar Institute…" → "Anonymous Institution"; "Washington State University" → "Anonymous University"; residual "Kashyap"/"Taranum…" → "Anonymous".
- **Self-verifies:** after writing, it greps each output for leak patterns `kashyap`, `taranum`, `thapar`, `harsh23kashyap`, `linkedin.com/in/harsh`, `parteek` (case-insensitive) (`:47,72-74`). **Exit 0 = clean; non-zero = a residual identifier remains** (`:11-12,76-82`).
- Run command: `python3 scripts/anonymize_reviewer_bundle.py` (`:11`).

The anonymized public repo alias used in review is **`https://anonymous.4open.science/r/JobMatch`** (4open.science double-blind hosting). The real repo is `github.com/Harsh23Kashyap/…`.

**Submission-guide anonymization checks** (`SUBMISSION-FORM-GUIDE.md:165-166,97`): main manuscript PDF/DOCX must have "no author names anywhere"; title page is uploaded as a separate unblinded file that "Editorial Manager will keep … from the reviewers."

---

### 6. Editorial risk matrix — top risks (`EDITORIAL_RISK_MATRIX.md`)

Synthesized 2026-08-18 from three hostile-reviewer lenses (RecSys/ranking, XAI/calibration, applied-ESWA) across every review round (`:1-6`). Probability = likelihood a reviewer raises it; Severity = impact on the decision; sorted HIGH×HIGH first. The **four HIGH×HIGH risks** are the strategic core:

| # | Criticism | P×S | Status / how it is answered |
|---|---|---|---|
| **1** | **Novelty is thin** — a weighted 6-channel composite + Platt is not new | HIGH×HIGH | Reframed as a *combination*: auditable relation-aware skill matching (EXP-034/034b) + calibrated-with-discrimination confidence + factor-grounded explanation + reproducible protocol. **Remaining fix:** finish "P12 reframe" so relation-aware graded skill matching leads the abstract/intro/title; add a related-work table showing the combination is underexplored. Called the "largest single lever." (`:10`) |
| **2** | **Ranking parity, not superiority** (n=30, CIs overlap, fails Holm) | HIGH×HIGH | Disclosed everywhere; reframed as instrument limitation (all-positive labels, 15-job pool at @5); synthetic headroom shown honestly (EXP-035/036; the +derived 0.99 jump disclosed as by-construction, EXP-044). Keep the "no statistically detectable difference" framing. (`:11`) |
| **3** | **Tiny, single-annotator corpus** (30×15 / 47 labels) | HIGH×HIGH | Disclosed; LLM-assisted 2nd pass κ=0.69 (non-human). **Remaining fix:** a larger, 2-annotator, explicitly-negative-judged benchmark (author-only, costly) — see §7. Short of that, state as the headline limitation. "Caps the ceiling." (`:12`) |
| **4** | **"Untouched test" is indefensible** (corpus informed 33 experiments) | MED×HIGH | FIXED: PROTOCOL.md reframes the real corpus as a *secondary transfer check*; only newly-frozen components get a one-shot prospective check. Ensure the manuscript never calls the 47 labels a clean held-out test. (`:13`) |

Notable MED/lower risks and their resolution:
- **#5** synthetic recovery "by construction" — FIXED (EXP-024b non-additive latent, recovery 0.891 vs 0.907) (`:14`).
- **#6** calibration low discrimination — EXP-026 reports ECE+BSS+AUC; isotonic keeps discrimination (BSS 0.64 / AUC 0.95); optionally lead with isotonic (`:15`).
- **#7** explanation faithfulness not human-validated — EXP-028 mechanistic only; **the human study (§6 protocol) is the "strongest remaining empirical add per panel"** (`:16`).
- **#8** skill-benchmark circularity (MiniLM labeling MiniLM) — FIXED via EXP-034b de-circularization (`:17`).
- **#9** multi-agent/"trustworthy" overclaim — DONE 2026-08-18 (title fix, §2) (`:18`).
- **#10** fairness proxy-only, **#11** weak baselines, **#12** reproducibility (LOW-prob, HIGH-sev — one-command `reproduce_all.sh` + verifier gate + pinned deps; real DOI at acceptance), **#13** misspelling non-robustness, **#14** temporal/scalability simulated (`:19-23`).

**Priority actions (HIGH×HIGH order)** (`:25-28`): (1) P12 reframe around auditable relation-aware skill matching; (2) own the corpus limitation as the headline caveat; (3) the two author-gated additions — the human explanation study (#7) and the larger 2-annotator benchmark (#3).

**Residual honest ceiling** (`:30-34`): "Even with all fixable items closed, the paper is a small-corpus methodological contribution whose real-world ranking claim is 'no detectable difference.'" **Defensible target: Major → Minor Revision.** A clear **Accept** "realistically needs the larger judged benchmark and/or the human explanation study (author-gated)."

---

### 7. Supervisor's governing plan — HOLD, don't submit in parallel

`docs/submission/PROFESSOR_STATUS.md` was the honest status snapshot sent for review; `docs/submission/PROFESSOR_FEEDBACK_PLAN.md` is the **governing plan** that came back and now supersedes the earlier "submit both venues in parallel" approach (`PROFESSOR_FEEDBACK_PLAN.md:1-5`). The decisive rulings a new reader must respect:

- **Strengthen BEFORE submitting** (`:13-15`): priority order = (1) larger explicit-negative ≥2-annotator benchmark → (2) re-run ranking/ablation/calibration through the verifier-gated pipeline → (3) human explanation study if feasible → (4) submit. "Ground truth is the foundational weakness."
- **NO PARALLEL SUBMISSION** (`:16-18,31-40`): ESWA and JAAMAS are "two framings of ONE contribution, NOT two distinct contributions." The empirical core is byte-identical (same 30×15/47 corpus, same method, every headline number matches). Parallel submission = redundant publication / self-plagiarism. **Submit ESWA ONLY; hold JAAMAS.** JAAMAS becomes separable only with a new empirical core testing the agent claim (monolith-vs-multi-agent ablation, Goal 6) + an architecture-specific contribution + explicit cross-citation of the ESWA paper (`:42-50`).
- **Primary venue = ESWA first** (`:27-29`).
- **Keep honest ranking PARITY** — do not hunt for p<0.05 (`:8-10`); relation-aware matcher is part of the *combination*, not the sole novelty, and is directional/underpowered (6/30 queries, p=0.03, one query dominant, effective n≈6) (`:11-12`).
- **Beta vs Platt** (`:23-24`): don't hide beta; frame Platt = deployed baseline, beta = stronger post-hoc result + recommended upgrade, and give a concrete reason Platt stays deployed.
- The plan carries an **8-goal research program** (G1 ranking, G2 ground-truth [foundational], G3 relation-aware matching, G4 calibration, G5 explanation human study, G6 multi-agent ablation, G7 robustness, G8 fairness) with an autonomous-vs-author-gated split (`:52-79`).

Corroborating status figures from `PROFESSOR_STATUS.md`: corpus 30×15/47 positive-only labels, κ=0.69 corroboration pass (`:16`); ranking numbers portal-default nDCG@5 0.949 / strongest single 0.924 / semantic 0.878 / RRF 0.913 / BM25 0.902 / TF-IDF 0.905 / cross-encoder 0.939 at ~340× latency (`:17`); parity Δ+0.071, p=0.10 (`:18`); artifact = one-command `reproduce_all.sh` + verifier + 184 unit + 12 scientific-claim + 29 integration + 10 frontend tests (`:35`).

---

### 8. The two author-gated protocols (drafted, ready-to-run, NOT yet run)

Both protocols exist so the two highest-leverage acceptance additions can be executed the moment the author has resources/ethics clearance. Neither has been run; both "fabricate nothing" and only specify collection.

#### 8a. Human explanation study — `HUMAN_STUDY_PROTOCOL.md`
Purpose: convert the explanation contribution from *automated* faithfulness (EXP-028) to *human-validated* usefulness — the single highest-leverage empirical addition (risk-matrix #7) (`:1-7`). It is a **pre-registered** protocol (hypotheses + analysis plan fixed before data collection).

- **Five pre-registered hypotheses** RQ-H1…H5 (`:9-27`): decision quality, efficiency/time-to-decision (non-inferiority margin 0.05), appropriate reliance / trust calibration (the condition×correctness interaction), perceived faithfulness (tracks EXP-028), usefulness/actionability. "Report all five regardless of outcome (including nulls)."
- **Design** (`:29-36`): mixed — between-subjects EXPLANATION CONDITION {score-only, generic-template, factor-grounded (JobMatch)} × within-subjects ITEM CORRECTNESS {system-correct, system-wrong}; Latin-square counterbalancing.
- **Participants & power** (`:38-48`): practising recruiters/HR screeners (≥1 yr); power analysis for H1 (Cohen's h≈0.4, α=0.05, power 0.80, one-sided) → ~78/arm, rounded to **n=90 per arm, 270 total**; pre-specified exclusions (failed attention checks, median item time <3 s, incomplete). If underpowered, pre-register as a pilot — never run underpowered then claim significance.
- **Materials** (`:50-61`): the SAME frozen real corpus (30×15, `data/eval_pairs.json`); three renderings of the *identical* ranking (only explanation text differs), factor-grounded produced by `build_composite_components` + the explanation generator; equal-layout control.
- **Honest "system-wrong" items** (`:63-70`): use the model's *actual* ranking errors, or a pre-registered skill-swap perturbation labeled by reference labels — never hand-picked/fabricated.
- **Measures** (`:72-82`): precision@k vs labels, time-to-decision, agree-when-right / override-when-wrong, perceived faithfulness, ResQue usefulness, candidate-view actionability, Cahour-Forzy trust, optional NASA-TLX.
- **Analysis** (`:92-102`): mixed-effects logistic regression (H1/H3 = condition×correctness interaction), LMM on log(time), McNemar/mixed logistic (H4), ordinal mixed model (H5), Holm-Bonferroni across five families, effect sizes+CIs always, nulls reported as nulls, fixed n / no optional stopping.
- **Author must provide** (`:118-121`): IRB/ethics approval, participant recruitment + compensation, the actual responses. Everything structural is generatable from the frozen corpus.

#### 8b. Larger judged benchmark annotation — `BENCHMARK_ANNOTATION_PROTOCOL.md`
Purpose: address the headline ceiling (risk-matrix #3): the tiny single-annotator all-positive corpus. Builds a larger, **two-annotator, explicitly-negative-judged, graded-relevance** benchmark (`:1-7`).

- **Quick-start path — explicit negatives from the EXISTING corpus, no new data** (`:9-28`): only 47 of the 30×15 = 450 pairs are judged; **the other 403 are merely assumed grade-0 (closed-world)**. `research/experiments/make_annotation_sheet.py` generates `research/datasets/annotation_sheet_unjudged.csv` (403 pairs, hard-negative stratum hint = 10 hard / 393 easy, blank `grade_annotator1/2`, `adjudicated_grade`, `annotator_rationale`). End-to-end loop: `make_annotation_sheet.py` (✔ generated) → 2 annotators + adjudicator fill 0–3 (the only human step) → `merge_annotations.py` → `data/eval_pairs_expanded.json` (unions with the 47, never overwrites, validates 0–3; ✔ built + self-test passes) → re-run the existing `comparison_table` / `graded_skill_channel` / `extended_evaluation` harness. "The entire pipeline except the human grading is ready and validated."
- **Target scale (fresh benchmark)** (`:30-38`): ≥60 query resumes × a shared 30-job pool, ≥900 judged pairs including mandatory explicit negatives; graded relevance restores power for nDCG@k / MRR / Recall@k.
- **Sampling** (`:40-46`): pre-registered, spanning 10 job families × 4 seniority tiers plus deliberate HARD pairs (same-title/wrong-skills, same-skills/wrong-seniority, high-semantic/wrong-domain — the EXP-039 hard-negative families); freeze item IDs before labeling.
- **Annotators** (`:48-52`): ≥2 independent recruiting-background annotators + a third adjudicator; blind to each other and the model; 20-pair calibration set first.
- **Two rubric scales (supervisor 2026-08-18)** (`:54-70`): existing-corpus 403 unjudged pairs use the current **0–3** scale (merges cleanly with the 47); the fresh larger benchmark uses the finer **0–4** scale (0 irrelevant / 1 weak / 2 relevant / 3 strong / 4 excellent). "Report which scale each split uses; do not mix them within one nDCG computation."
- **Agreement/adjudication** (`:72-77`): quadratic-weighted Cohen's κ (target ≥0.6) + exact-agreement; disagreements >1 grade go to the adjudicator; keep both raw labels; label distribution must NOT be all-positive.
- **Anti-leakage** (`:79-83`): new test set split into development + held-out-once; the existing 30×15 stays a separate legacy set — do not merge for a "clean test" claim.
- **Cost** (`:93-97`): ~900 pairs × 2 annotators ≈ 1,800 judgments ≈ 15 annotator-hours + adjudication; feasible with 2 paid annotators over a few days.
- **Author must provide** (`:99-103`): the human annotators + adjudicator + their time + any IRB/data-use clearance, and real (or consented synthetic) resume/job content at scale. Everything structural (sampling script, guideline PDF, agreement/adjudication tooling, harness wiring) is generatable from the current codebase.

---

### 9. Highlights and remaining file inventory

**Highlights** — the canonical, corrected (2026-08-18) version lives at `docs/submission/eswa/strategy/highlights-eswa.md:11-19` (the top-level `highlights.md` is empty; a rendered `highlights.docx`, 10,942 bytes, is the upload). Five bullets, each ≤85 chars, present tense, no ranking-superiority claim:
1. Auditable six-channel composite ranking with documented channel weights
2. Graded relation-aware skill matcher: exact, related, and unrelated skills
3. Platt-scaled confidence with held-out ECE 0.019 (low discrimination)
4. Component-level explanations bound to the six scoring channels
5. Open-source, regression-gated artifact; one-command reproduction, 30/15/47

The header note warns which numbers are **superseded/forbidden**: in-sample ECE 0.032, the retired 0.745 faithfulness figure, and the "7 of 10" counterfactual (`highlights-eswa.md:3-7`); canonical anchors are composite nDCG@5 0.949 / strongest single 0.924 / semantic 0.878 / RRF 0.913, held-out ECE 0.019, parity p=0.10 (fails Holm), 50-pair recourse-null counterfactual, DOI upon acceptance.

**Files-to-prepare (5 total, per `SUBMISSION-FORM-GUIDE.md:13-21`), uploaded in this order** (`:93-108`): (1) `main.pdf` anonymized (3.28 MB, 36 pp), (2) `main.docx` anonymized (3.34 MB), (3) `title-page.pdf` unblinded (100 KB, 2 pp), (4) `highlights.docx` (11 KB), (5) `cover-letter.docx`; optional (6) supplementary ZIP (`paper_progression_summary.json`, `calibration_summary.json`, `explainability_report.json`, `fairness_eval.json`). Editorial Manager item order: Manuscript (anonymized) → Title page (unblinded, withheld from reviewers) → Highlights → Cover letter.

**Physical files in `docs/submission/eswa/`:** `title-page.tex` / `.pdf` / `.aux` / `.log` / `.out` (compiled build), `cover-letter.md` + `.docx`, `highlights.md` (empty) + `.docx` + `highlights-check.txt` (empty), `EDITORIAL_RISK_MATRIX.md`, `HUMAN_STUDY_PROTOCOL.md`, `BENCHMARK_ANNOTATION_PROTOCOL.md`, `SUBMISSION-FORM-GUIDE.md`, plus planning docs (`ESWA-EXECUTION-PLAN.md`, `ESWA-STAGE2-PLAN.md`, `ESWA-STAGE3-PLAN.md`), a `strategy/` subdir (`ESWA-FIT-ASSESSMENT.md`, `POSITIONING.md`, `pre-submission-inquiry.md`, `REVIEWER-SIM.md`, `SUBMISSION-PLAN.md`, `related-work/`), and `figures/`, `manuscript/`, `supplementary/`. The two `PROFESSOR_*.md` files live one level up in `docs/submission/`. The anonymization script is `scripts/anonymize_reviewer_bundle.py`.

---

## Author-gated work + the toolchains that make each one step

This section is the definitive map of everything that is **NOT** an AI/engineering task — the work that only the human author (Harsh) can perform because it requires human judgment, human participants, an ORCID account, or an Overleaf/pdfLaTeX login. For each blocked item, the project has already built and validated the *entire* surrounding machine so that the human step is reduced to the smallest possible action, and a single command turns the human's output into the final artifact.

There is a hard integrity rule wrapped around all of this (detailed in §"The integrity guardrail" below): **no provisional, LLM-assisted, or synthetic result is ever allowed into the verifier-gated manuscript.** The tooling is built so the author can drop in real human labels and re-run; until then the gated numbers stay as the honest positive-only story.

### The starting point: why these items are blocked

The frozen real corpus is **30 resumes × 15 jobs = 450 candidate/job pairs**, but only **47 pairs are human-labeled** and all 47 are *positive* (relevance 1 or 2), single-annotator, on a 0–2 scale. See `data/eval_pairs.json:1-84` — `"relevance_scale": "0-2"`, `"notes": "Starter labeled set for Phase 1.1..."`, 47 label objects. The other **403 of the 450 pairs are only *assumed* grade-0 under a closed-world assumption** — never explicitly judged. This is the single sharpest reviewer objection (logged as EDITORIAL_RISK_MATRIX #3 and #7). Fixing it and the explanation-usefulness gap requires humans, so four items are gated on the author.

| # | Blocked-on-user item | Why only a human can do it | The one command that unblocks it |
|---|---|---|---|
| 1 | Two-annotator human grading of the 403 unjudged pairs | Requires real recruiter judgment (0–3 relevance) + a second annotator + adjudicator; cannot be fabricated | `merge_annotations.py` → then `powered_reeval.py` |
| 2 | Blinded human explanation study (45 stimuli) | Requires IRB clearance + ~270 recruited human participants making shortlisting decisions | Stimuli already generated by `make_explanation_renderings.py`; author runs the study per `INSTRUMENT.md` / `HUMAN_STUDY_PROTOCOL.md` |
| 3 | Optional ORCID iDs on the title page | Author-owned identifiers; deferred to Editorial Manager at submission | Paste ORCID iDs into the title page (optional) |
| 4 | JAAMAS PDF build / Overleaf upload | Springer `sn-jnl.cls` needs pdfLaTeX; cannot compile in this environment | Upload `jaamas_overleaf_ready.zip` to Overleaf, set main doc + compiler, click Recompile |

---

### Item 1 — Human annotation of the 403 pairs (the powered re-test)

This is a fully-built, three-stage pipeline where **only stage 2 (filling in grades) is human**. Stages 1 and 3 are deterministic scripts that "fabricate nothing" (their own words, see `make_annotation_sheet.py:7` and `merge_annotations.py:9`).

#### Stage 1 — generate the blank sheet (already done)

`research/experiments/make_annotation_sheet.py` reads `data/cvs.json`, `data/jobs.json`, and the 47 existing labels from `data/eval_pairs.json`, then emits every currently-unjudged (cv, job) pair to `research/datasets/annotation_sheet_unjudged.csv` (`make_annotation_sheet.py:51-97`). The output has **403 data rows + 1 header** (confirmed: `wc -l` = 404) and **15 columns**:

`query_id, doc_id, candidate_skills, candidate_experience_years, candidate_summary, job_title, job_required_skills, job_required_experience, job_remote_policy, shared_skill_count_HINT, stratum_HINT, grade_annotator1, grade_annotator2, adjudicated_grade, annotator_rationale`

The last four columns are **blank** (verified: all 403 rows have empty `grade_annotator1/2`, `adjudicated_grade`, `annotator_rationale`) — those are exactly what the two annotators + adjudicator fill. The script only fills in *real* corpus context plus two clearly-labeled **HINT** columns to help annotators stratify effort — a hint is explicitly "NOT a label" (`make_annotation_sheet.py:39-48`):

- `shared_skill_count_HINT` — count of overlapping skills (Jaccard numerator).
- `stratum_HINT` — one of `easy_negative` (no shared skills), `hard_negative` (partial skill signal, the interesting middle), or `likely_relevant` (strong overlap; may be a missed positive).

Verified strata distribution of the committed sheet: **`hard_negative` = 10, `easy_negative` = 393, `likely_relevant` = 0** (total 403). Rows are sorted hard-negatives first, then likely-relevant, then easy (`make_annotation_sheet.py:88-89`) so annotators hit the informative pairs first. Sample rows (from the file header + first two data lines):

```
cv_01,job_04,...,Data Analyst,Python; Pandas,1,True,1,hard_negative,,,,
cv_01,job_06,...,NLP Engineer,Python; NLP; Transformers,3,True,1,hard_negative,,,,
```

Regeneration command (from `make_annotation_sheet.py:13`):
```
cd backend && PYTHONHASHSEED=0 PYTHONPATH=. .venv/bin/python ../research/experiments/make_annotation_sheet.py
```

#### Stage 2 — the ONLY human step

Two independent annotators with recruiting/technical-screening background grade each of the 403 pairs **0–3** (blind to each other and to the model's scores), a third adjudicates, and the final value goes in the `adjudicated_grade` column. The rubric is fixed in `docs/submission/eswa/BENCHMARK_ANNOTATION_PROTOCOL.md:63-70`:

- **3 (strong)** — meets required skills and seniority; clearly advance.
- **2 (plausible)** — meets most requirements; advance with minor gaps.
- **1 (weak)** — notable gaps (missing a key required skill OR wrong seniority band); usually would not advance.
- **0 (unqualified)** — wrong domain or missing most requirements; would not advance.

Annotators judge content only (ignore names/gender/age/location for fairness), weight required over preferred skills, and record a one-line rationale (`BENCHMARK_ANNOTATION_PROTOCOL.md:68-70`). Agreement target: quadratic-weighted Cohen's κ ≥ 0.6; disagreements > 1 grade go to the adjudicator (`BENCHMARK_ANNOTATION_PROTOCOL.md:72-77`). Cost estimate for the *full* larger benchmark is ~1,800 judgments ≈ 15 annotator-hours (`BENCHMARK_ANNOTATION_PROTOCOL.md:94-95`), but the 403-pair existing-corpus pass is the fast path.

#### Stage 3 — merge, then re-test (two commands)

`research/experiments/merge_annotations.py` reads the filled `adjudicated_grade` column, unions those grades with the existing 47 labels, and writes `data/eval_pairs_expanded.json` (`merge_annotations.py:29-52`). It is "deterministic glue" that fabricates nothing:

- Skips blank rows (`merge_annotations.py:37-38`).
- Validates every grade is 0–3, raising `ValueError` otherwise (`merge_annotations.py:40-41`).
- **Never overwrites an existing judged label** (`merge_annotations.py:43-44`).
- If zero grades are filled, it prints "No adjudicated grades filled … Fill the `adjudicated_grade` column (0-3), then re-run" and exits 0 without writing (`merge_annotations.py:91-94`).
- Ships a `--selftest` that validates the merge logic on a synthetic 4-row sheet (explicit-0 merged, grade-3 merged, blank skipped, existing label preserved) with no files written (`merge_annotations.py:55-81`).

> Note: `data/eval_pairs_expanded.json` **does not exist yet** in the repo — confirmed absent. That is the expected state: it is the *output* of the human annotation, so its absence is the signal that Item 1 is still blocked.

The exact unblock sequence (as specified in `BENCHMARK_ANNOTATION_PROTOCOL.md:22-28`):

```
# stage 1 (already done, regenerate if needed)
python3 research/experiments/make_annotation_sheet.py
# --- human fills adjudicated_grade 0-3 in annotation_sheet_unjudged.csv ---
# stage 3a: merge
python3 research/experiments/merge_annotations.py
# stage 3b: powered re-test (from backend/)
cd backend && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false PYTHONHASHSEED=0 \
  PYTHONPATH=. .venv/bin/python ../research/experiments/powered_reeval.py
```
Or point the harness explicitly: `EVAL_PAIRS=data/eval_pairs_expanded.json python3 research/experiments/powered_reeval.py`.

`research/experiments/powered_reeval.py` is the "one-command" powered re-evaluation harness (`powered_reeval.py:1-16`). Eval-file resolution order (`powered_reeval.py:40-46`): `argv[1]` → `$EVAL_PAIRS` → `data/eval_pairs_expanded.json` if it exists → else `data/eval_pairs.json`. It computes:

- **Label distribution** and whether explicit negatives (grade 0) are present (`powered_reeval.py:77-80`) — this is the whole point of Goal-2.
- **nDCG@5** for four methods: `composite_jaccard`, `composite_graded_exact`, `composite_graded_related`, `semantic_only` (`powered_reeval.py:113-119`).
- **Paired bootstrap CI (3,000 resamples) + permutation p (20,000 perms)** for `composite_vs_semantic`, `graded_vs_jaccard`, and `relation_aware_vs_exact_coverage` (`powered_reeval.py:49-61, 131-133`).

Its built-in interpretation guard (`powered_reeval.py:134-139, 146-148`) states that if `explicit_negatives_present` is False the run is the positive-only baseline and **NOT yet powered** — it prints "NOTE: no explicit negatives yet → this is the positive-only baseline run (tooling smoke-test)." The design instruction is to "report parity honestly if the composite still does not significantly beat semantic."

---

### Item 2 — the blinded human explanation study (45 stimuli)

`research/experiments/make_explanation_renderings.py` is the Goal-5 stimulus generator (`make_explanation_renderings.py:1-20`). It renders, straight from the live scorer, **15 jobs × 3 explanation conditions = 45 self-contained HTML "shortlist screens"** into `research/datasets/explanation_study/` (verified: 45 `*.html` files present, plus `manifest.csv`, `INSTRUMENT.md`, and a `SIDE_BY_SIDE_sample.html` preview). Each screen shows one job and its **top-5 ranked candidates** (`TOP_K = 5`, `make_explanation_renderings.py:37`). The three conditions (`CONDITIONS`, `make_explanation_renderings.py:38`; render logic `make_explanation_renderings.py:58-78`) hold layout/length equal and vary **only the explanation text**:

| Condition | File suffix | What the recruiter sees |
|---|---|---|
| **A. score_only** (control: no explanation) | `jobX__score_only.html` | rank + composite score only |
| **B. generic_template** (control: any text vs none) | `jobX__generic_template.html` | rank + score + fixed sentence "This candidate is a strong overall match for the role." |
| **C. factor_grounded** (JobMatch's explanation) | `jobX__factor_grounded.html` | rank + score + the six-channel decomposition (weight × score = contribution bar) + matched/missing required skills + a confidence band |

The six channels shown in condition C (`_CHANNEL_LABELS`, `make_explanation_renderings.py:49-50`): Semantic fit, Skills coverage, Title fit, Experience, Compensation, Remote fit. Confidence banding: ≥0.66 High, ≥0.4 Medium, else Low (`make_explanation_renderings.py:53-55`). Each screen ends with the embedded instrument block (`make_explanation_renderings.py:81-87`): advance-decision checkboxes, decision confidence (1–7), information usefulness (1–7), perceived top factor (free text), trust (1–7).

`manifest.csv` (46 lines = header + 45 rows) tags each stimulus with `job_id, condition, n_candidates, shortlist_has_labeled_relevant, top1_candidate, top1_score` (`make_explanation_renderings.py:121-123`). Every one of the 15 jobs currently has `shortlist_has_labeled_relevant = True` (e.g. `job_01` → top1 `cv_14` score 0.7342; `job_06` → top1 `cv_12` score 0.905).

`INSTRUMENT.md` (`research/datasets/explanation_study/INSTRUMENT.md`) specifies the between-subjects design (each participant sees ONE condition across all screens), the per-screen measures, and the analysis model: mixed-effects `outcome ~ condition + (1|participant) + (1|screen)` with Holm correction. **Both `INSTRUMENT.md:5` and the generator (`make_explanation_renderings.py:136-137`) carry the same critical caveat:** valid *system-wrong* items (needed for the trust-calibration test, RQ-H3) require the Item-1 explicit negatives; until then `shortlist_has_labeled_relevant` is only a **coarse proxy**. So Item 2 is partly gated on Item 1.

The full author-executable protocol lives at `docs/submission/eswa/HUMAN_STUDY_PROTOCOL.md`. Highlights the human must own:

- **Pre-registered hypotheses RQ-H1…H5** (`HUMAN_STUDY_PROTOCOL.md:9-27`): decision quality, efficiency, appropriate reliance/trust-calibration, perceived faithfulness (triangulated against EXP-028 mechanistic faithfulness), usefulness/actionability. All five reported regardless of outcome; a null is still publishable.
- **Power**: two proportions at Cohen's h ≈ 0.4, α 0.05, power 0.80 → ~78/arm, rounded to **n = 90 per arm, 270 total** (`HUMAN_STUDY_PROTOCOL.md:42-46`).
- **System-wrong items constructed honestly** — real model ranking errors on the frozen corpus, or a pre-registered required-skill swap; never hand-picked/fabricated (`HUMAN_STUDY_PROTOCOL.md:63-70`).
- **What only the author can provide** (`HUMAN_STUDY_PROTOCOL.md:118-121`): IRB/ethics approval, participant recruitment + compensation, and the actual responses. Everything structural (items, renderings, instruments, analysis-code skeleton) is already generated.

Regenerate the stimuli (from `make_explanation_renderings.py:19-20`):
```
cd backend && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false PYTHONHASHSEED=0 \
  PYTHONPATH=. .venv/bin/python ../research/experiments/make_explanation_renderings.py
```

---

### Item 3 — optional ORCID iDs on the title page

The author metadata is already reconciled and matches the title page: corresponding author = Harsh Kashyap; Harsh and Taranumpreet are joint-first with an explicit `\textsuperscript{*}` equal-contribution footnote; affiliations Thapar/WSU; no competing interests; CRediT×3; data-on-acceptance (`research/PHASE_STATUS.md:99`). **The only remaining author-metadata task is optionally adding ORCID iDs, which is deferred to Editorial Manager at submission** (`PHASE_STATUS.md:99`, and listed among external blockers in `research/PROJECT_STATUS.md:28`: "external DOI/ORCID/GitHub/submission"). This is optional and author-owned — nothing in the repo blocks on it.

---

### Item 4 — JAAMAS Overleaf upload / PDF build

The ESWA manuscript compiles clean locally, but the **JAAMAS** manuscript uses Springer's `sn-jnl.cls`, which needs a full pdfLaTeX toolchain that this environment cannot run (tectonic is incompatible with `sn-jnl.cls` at the `glyphtounicode` startup) — see `research/PHASE_STATUS.md:80`. So the JAAMAS build is the **one remaining author step** for that venue.

The upload artifact is already built and committed: **`docs/submission/jaamas/jaamas_overleaf_ready.zip`** (verified present, 3,783,897 bytes ≈ 3.8 MB, Aug-synced). It uses a parent directory structure so `../figures/` resolves; the stale July `main.pdf` was excluded (`PHASE_STATUS.md:101`). Upload instructions the author follows on Overleaf: set **main document = `manuscript/main.tex`**, **compiler = pdfLaTeX**, then Recompile (`PHASE_STATUS.md:101`). All numbers across the JAAMAS tex/md have already been swept clean and reconciled to the honest parity story; the correction over-optimistic-best-single and over-stated-significance issues are fixed (`docs/submission/PROFESSOR_STATUS.md:29-33, 53`). A DOI is deposited on acceptance (also author-only).

---

### The PROVISIONAL LLM-assisted result — real, disclosed, and deliberately OUT of the gated manuscript

To de-risk Item 1 (prove the tooling works and preview whether real negatives change the story), the project ran an LLM-assisted dry run — **but this is explicitly disclosed as provisional and is NOT human ground truth.**

`research/experiments/llm_annotate.py` graded all 403 unjudged pairs via two distinct model families (`gpt-5.6-sol` and `deepseek-3.2`) through consult-kiro, adjudicating agreement→grade, |diff|=1→round(mean), |diff|≥2→flag+conservative-min (`llm_annotate.py:1-13, 34`). Results from `research/results/llm_annotation.json`:

- Coverage **403/403** (100%), **inter-model quadratic κ = 0.541**, only **2** pairs flagged with disagreement ≥ 2.
- Adjudicated distribution of the 403: **392 grade-0, 7 grade-1, 4 grade-2, 0 grade-3** → **392 explicit negatives added** (which *validates* the closed-world assumption) plus **11 previously-missed positives**.
- Output: `data/eval_pairs_llm_expanded.json` (47 human + 403 LLM = **450 labels**; combined distribution `{0: 392, 1: 33, 2: 25}`, `notes` field literally says "LLM-ASSISTED expansion … **PROVISIONAL, not human ground truth; author review pending before submission**").

Running `powered_reeval.py` on that provisional file produced `research/results/powered_reeval.json` (`eval_file: data/eval_pairs_llm_expanded.json`, `explicit_negatives_present: true`, 30 queries scored):

| Comparison | Δ (mean nDCG@5) | 95% bootstrap CI | perm-p | verdict |
|---|---|---|---|---|
| **composite_jaccard vs semantic_only** | **+0.08203** | **[0.00707, 0.15240]** (excludes 0) | **0.039** | nominally significant |
| composite_graded_related vs composite_jaccard | +0.04100 | [-0.00240, 0.11347] | 0.1537 | not significant |
| relation_aware vs exact_coverage | +0.04347 | [-0.00209, 0.11737] | 0.1321 | not significant |

nDCG@5 by method: `composite_graded_related` 0.98339, `composite_jaccard` 0.94239, `composite_graded_exact` 0.93992, `semantic_only` 0.86036.

The honest reading (`research/PHASE_STATUS.md:58`): the composite-vs-semantic **Δ+0.082, p=0.039** is *nominally* significant (vs the positive-only corpus where p≈0.10–0.15) — **PROMISING but PROVISIONAL**, and it hinges on the 11 LLM-judged positives, so the author's human pass is authoritative. Meanwhile the graded-vs-jaccard (p=0.15) and relation-aware-vs-exact (p=0.13) comparisons are **no longer significant** with more labels — which *confirms* the professor's "directional / underpowered / one-query-dominated" caution and means the team must **not overclaim** the relation-aware skill-channel benefit.

### The integrity guardrail

This is the load-bearing rule the next session must never violate:

> **Provisional LLM-assisted / synthetic results stay OUT of the verifier-gated manuscript (integrity guard) pending the author's human annotation** — `research/RESEARCH_DECISIONS.md:85`.

Concretely:
- The manuscript's headline numbers are all auto-generated from committed artifacts and **verifier-gated** (`docs/submission/PROFESSOR_STATUS.md:29`; `research/PROTOCOL.md:46`, "Numbers stay verifier-gated"). The verifier is a gate in `reproduce_all.sh` that fails the build if the tex numbers drift from the artifacts.
- `data/eval_pairs_llm_expanded.json` and `research/results/powered_reeval.json` are **not** wired into that gated pipeline. They live as disclosed research artifacts only. `powered_reeval.py` is deliberately "Self-contained (does NOT modify the reproduce_all pipeline)" (`powered_reeval.py:9`).
- The gated manuscript therefore still reports the honest positive-only parity story. When the author supplies the real two-annotator labels (Item 1), `merge_annotations.py` produces `data/eval_pairs_expanded.json`, `powered_reeval.py` re-runs on *that*, and only then may the powered numbers be promoted into the manuscript — replacing, never supplementing, the provisional ones.

**Bottom line for the next session:** all four author-gated items have their machinery finished and validated. Do not fabricate human labels, do not fold `eval_pairs_llm_expanded.json` into the gated numbers, and do not overclaim the relation-aware skill benefit. Hand the author the blank sheet (Item 1), the 45 stimuli + protocol (Item 2), the ORCID note (Item 3), and the Overleaf zip (Item 4); each is genuinely one human action away from done.

---

## JAAMAS (the held second venue)

### What JAAMAS is, and where it lives on disk

JAAMAS is the *Journal of Autonomous Agents and Multi-Agent Systems* (Springer Nature). It is the **second, held target venue** for the JobMatch paper. The entire JAAMAS submission lives under `/Users/kashhy/workspace/Personal/dev/Job-Matching-Agentic/docs/submission/jaamas/`, structured as:

| Path | Purpose |
|------|---------|
| `manuscript/main.tex` | Root LaTeX file (Springer `sn-jnl` class). |
| `manuscript/sections/section-{1..7}-*.tex`, `declarations.tex` | The seven body sections + declarations, `\input` from `main.tex:50-57`. |
| `manuscript/tables/tab-*.tex` (15 files) | Result/param tables (ablation, fusion, latency, fairness, explainability, etc.). |
| `manuscript/algorithms/alg-multi-agent-matching.tex` | The multi-agent matching algorithm listing. |
| `manuscript/sn-jnl.cls`, `sn-mathphys-num.bst`, `references.bib` | Springer class, bibliography style, refs. |
| `manuscript/jaamas-macros.tex`, `jaamas-style.tex` | Custom `\JFig*` figure macros + `JFigure`/`JTable` environments. |
| `manuscript/*.sty` (cuted, threeparttable, wrapfig, appendix, enumitem) | Vendored LaTeX deps for minimal-TeX compatibility. |
| `figures/Fig{1..7}.png` + `figures/screenshots/ui-*.png` | Rendered figures + 8 portal screenshots (Figure 10). |
| `figures/source/*.drawio`, `figures/scripts/*` | Editable diagram sources + generation scripts. |
| `portal/` | Cover letter + information sheet (`.tex`/`.pdf`). |
| `supplementary/` | Supplementary-information PDF + source. |
| `build/` | Older staging + PDFs (stale). |
| `jaamas_overleaf_ready.zip` | **The one artifact to upload to Overleaf** (3.8 MB, dated 2026-08-18 15:14). |
| `REVIEW-TODO.md` | Final review-action status log. |
| `build_all.sh`, `archive/dev-scripts/make_overleaf_zip.sh` | Build scripts (require a real pdfLaTeX; see below). |

The manuscript is titled *"JobMatch: An Agentic Multi-Role Platform for Explainable Job--Candidate Matching"* (`manuscript/main.tex:21`), authored by Harsh Kashyap, Taranumpreet Kaur Wasu (joint first authors), and Parteek Kumar (`main.tex:25-32`).

### The dual-venue decision: ONE contribution, single-venue, ESWA FIRST, JAAMAS HELD

**This is the single most important thing to understand about JAAMAS: it is NOT being submitted right now, and it must NOT be submitted in parallel with ESWA.** JobMatch has *two* complete manuscripts — one under `docs/submission/eswa/` and one under `docs/submission/jaamas/` — but they describe **one and the same contribution**: the same dataset (30 resumes × 15 jobs × 47 graded pairs), the same experiments, the same results, the same figures.

A supervisor correction on **2026-08-18** governs the whole strategy (recorded in the project memory `jobmatch-dual-venue-eswa-jaamas.md:11`):

> **"NO PARALLEL SUBMISSION."** Same dataset/experiments/results/figures = substantially overlapping even with different framing → a publication-ethics issue. Pick ONE primary venue (**ESWA first**), submit, await disposition, THEN decide JAAMAS only on genuinely non-overlapping novelty (which would require the Goal-6 multi-agent ablation to stand distinct).

Concretely, the sequencing rule the next session must honor:

1. **ESWA is the primary venue and goes first.** Elsevier's *Expert Systems with Applications*.
2. **JAAMAS is HELD.** Do not submit until ESWA reaches a disposition (accept/reject/major-revision).
3. **Reviving JAAMAS is conditional**, not automatic: it may only proceed if JobMatch can present genuinely non-overlapping novelty for an agents journal — the plan names the *Goal-6 multi-agent ablation* as the piece that would have to stand on its own for JAAMAS to be a distinct contribution rather than a duplicate submission.
4. Before *either* venue, the strengthening priority is the larger explicit-negative, ≥2-annotator benchmark (Goal 2) — not over-optimizing a ranker on the current 47 positive labels.

The governing plan is `docs/submission/PROFESSOR_FEEDBACK_PLAN.md` (memory alias `[[jobmatch-professor-feedback-plan]]`). The user's own words on JAAMAS's status: *"we will try for JAAMAS again"* (2026-08-18) — i.e. it is a future, contingent attempt, not a live submission.

### How the JAAMAS framing differs from ESWA

The two manuscripts share **synced science but divergent framing**. The governing rule (`jobmatch-dual-venue-eswa-jaamas.md:18`): *the substantive science must stay synced across both; the framing must stay divergent.* Do NOT copy the ESWA framing into JAAMAS.

| Dimension | JAAMAS (`docs/submission/jaamas/`) | ESWA (`docs/submission/eswa/`) |
|-----------|-----------|------|
| **Positioning** | Multi-agent architecture **FOREGROUNDED** — it *is* an agents journal. The original, fuller manuscript. | Multi-agent **DEMOTED** to an implementation detail; reframed as an auditable/calibrated/explainable *recommendation methodology*. |
| **Title** | "JobMatch: An Agentic Multi-Role Platform for Explainable Job--Candidate Matching" | "An Auditable, Calibrated, and Explainable Multi-Agent System for Job-Candidate Recommendation" |
| **Review model** | **Single-blind** → author names EXPECTED, **NO anonymization**. | **Double-blind** → author identity must be scrubbed (`scripts/anonymize_reviewer_bundle.py`; fixtures already scrubbed). |
| **Publisher** | Springer Nature (`sn-jnl.cls`). | Elsevier. |

The multi-agent foregrounding is visible throughout the JAAMAS text:
- The Introduction opens by splitting the market into three logical agents — Candidate Agent, Employer Agent, and a neutral read-only Matchmaking Agent (`sections/section-1-introduction.tex:8-12`), and lists each agent as a first-class contribution (`section-1-introduction.tex:26-30`).
- The paper carries a full "Why an agentic architecture?" service-vs-agent framing and a dedicated multi-agent architecture section (Section 3), plus `algorithms/alg-multi-agent-matching.tex`.
- Keywords lead with "multi-agent systems" (`main.tex:46`).

**Because JAAMAS is single-blind, the manuscript is deliberately NOT anonymized** — this is the opposite of the ESWA requirement. `sections/declarations.tex` intentionally exposes author identity: full author-contribution statement naming Harsh Kashyap and Taranumpreet Kaur Wasu as joint first authors and Dr Parteek Kumar as supervisor (`declarations.tex:35-37`), institutional acknowledgments to Thapar Institute and Washington State University (`declarations.tex:5`), and the public repository URL `https://github.com/Harsh23Kashyap/Job-Matching-Agentic` (`declarations.tex:33`). **The next session must NOT run the ESWA anonymizer on the JAAMAS tree and must NOT strip these names** — doing so would break the single-blind expectation.

### JAAMAS numbers are integrity-synced with ESWA

On **2026-08-18** an integrity pass propagated the corrected, honest numbers from the ESWA numbers-pass into JAAMAS. The manuscripts must carry identical headline figures. The canonical synced numbers (per `jobmatch-dual-venue-eswa-jaamas.md:20`, and reflected in the JAAMAS abstract `main.tex:34-44`):

- Portal-default six-channel **composite nDCG@5 = 0.949** (weights 28/27/10/15/10/10).
- Semantic 0.878, RRF 0.913; **strongest single configuration 0.924**.
- **No method is statistically distinguishable** at n=30: composite vs semantic Δ+0.071, two-sided **p=0.10**, 95% CI crosses 0, **fails Holm** → reported as ranking **parity**, not superiority.
- Cross-encoder reranking nDCG@5 = 0.939 at ~141.7 ms/query — does *not* beat the composite, stays disabled in the default portal.
- Held-out 5-fold **Platt ECE 0.019** (Brier 0.093); **beta calibration ECE 0.009** recommended (preserves discrimination); Platt kept as frozen default.
- Hard-negative mining: 150 pairs, zero label conflicts. Synthetic fairness audit flags 7/10 fabricated pairs — an engineering check, DIR 0.82 (experience) / 0.75 (remote), explicitly *not* a demographic-fairness audit.
- Corpus: 30 resumes, 15 jobs, 47 graded relevance pairs, 2.97 skills/resume, 74-token vocab, no preferred field.

The 2026-08-18 pass **removed fabricated results** that had been in the earlier JAAMAS draft (see `REVIEW-TODO.md:7-13, 39-44`): the fabricated-significance `p=0.048`, the phantom "best single" `0.969`/recall@5=1.00, and the in-sample-leakage calibration `0.032` are all gone. The graded relation-aware skill matcher (exact 1.0 / related 0.5 / else 0) and beta calibration were also added to §5. **Maintenance rule for the next session:** any correction made to ESWA science must also be made to JAAMAS (and vice-versa) — but framing must stay divergent.

### JAAMAS CANNOT be compiled locally with tectonic — build it on Overleaf

The Springer `sn-jnl.cls` requires **pdfLaTeX**. `main.tex:3` declares `\documentclass[pdflatex,sn-mathphys-num]{sn-jnl}` and `main.tex:4` calls `\input{glyphtounicode}`. The only TeX engine available in the working sandbox is **tectonic**, which **fails at `glyphtounicode`** and cannot process `sn-jnl.cls`. This is the documented blocker (`REVIEW-TODO.md:11-12, 50`):

> No TeX engine that supports the Springer `sn-jnl.cls` is available in the sandbox (only tectonic, which fails at glyphtounicode) ... **This is the only remaining step to a submission-ready JAAMAS PDF.**

All content edits have been verified LaTeX-safe (balanced math/environments/columns; stale-number sweep clean), so the document will compile cleanly on a full TeX distribution. The `manuscript/main.log` confirms it *does* compile under real pdfTeX (TeX Live 2026) — that log was produced on a machine with full TeX Live, dated 30 JUL 2026, and shows `sn-jnl.cls` and `glyphtounicode.tex` loading successfully.

**Exact Overleaf build steps (the intended path to a PDF):**

1. Upload **`docs/submission/jaamas/jaamas_overleaf_ready.zip`** to Overleaf via *New Project → Upload Project*.
2. In Overleaf *Menu → Settings*, set **Compiler = pdfLaTeX** (NOT XeLaTeX/LuaLaTeX — `sn-jnl` is invoked in pdflatex mode).
3. Set **Main document = `manuscript/main.tex`**.
4. **Recompile twice** so BibTeX resolves: Overleaf runs pdfLaTeX → BibTeX → pdfLaTeX automatically, but a second manual *Recompile* is needed to settle cross-references and the bibliography (the local `build_all.sh:10-13` mirrors this — pdflatex, bibtex, pdflatex, pdflatex).
5. **Preserve the parent directory structure.** Figures are included with a `../figures/` relative path, e.g. `\begin{JFigure}{../figures/Fig1.png}` through `Fig7.png` in `sections/section-3-architecture.tex:8,24,46,51,67,73,107`. The zip is laid out with `manuscript/` and `figures/` as **siblings** at the project root precisely so that `../figures/` resolves from inside `manuscript/`. Do not flatten or move the `manuscript/` folder — if you do, every figure will break.

Note on figure format: the current manuscript sources reference the **`.png`** figures (Fig1–Fig7), which are bundled in the zip under `figures/`. (The older `make_overleaf_zip.sh` and `figures/README.md` describe a `.pdf`-based layout with Fig8/Fig9; the *actual* `jaamas_overleaf_ready.zip` and the live `.tex` sources use PNGs, so it is self-consistent as shipped.)

### The zip deliberately excludes the stale Jul-30 main.pdf

The committed `manuscript/main.pdf` is **stale** — it is dated **30 Jul 2026 21:17** (pre-edit, before the 2026-08-18 integrity pass), so it still contains the old/fabricated numbers. **`jaamas_overleaf_ready.zip` intentionally contains NO PDF files at all** (verified: `unzip -l` returns no `main.pdf` and no `Fig*.pdf`) — only the LaTeX sources, `.png` figures, drawio sources, and screenshots. This is deliberate: the PDF is meant to be regenerated fresh on Overleaf from the corrected sources, so no stale/out-of-sync PDF ships with the upload. The other stale PDFs to ignore are `build/jaamas-manuscript.pdf` (22 Jul) and `build/jaamas-supplementary.pdf` (18 Jul); `build/jaamas-overleaf-upload.zip` is the older, superseded packaging — use `jaamas_overleaf_ready.zip`, not the `build/` one.

### Bottom line for the next session

All review TODOs (Tier 1 + Tier 2, 8 items) and all inline `\todo{}` markers are resolved, and the numbers are integrity-synced with ESWA (`REVIEW-TODO.md:6-13`). JAAMAS is **content-complete but HELD**. Do not submit it; do not submit it in parallel with ESWA. The only outstanding *mechanical* step, if/when a PDF is needed, is compiling `jaamas_overleaf_ready.zip` on Overleaf with pdfLaTeX per the steps above. The only outstanding *strategic* gate before JAAMAS can ever be revived is ESWA reaching a disposition plus a genuinely distinct multi-agent (Goal-6) contribution.

---

## Artifacts, PDFs, and the READ-FIRST file manifest

This section is a complete physical inventory of the *outputs* of the JobMatch project — the compiled PDFs, the datasets, the machine-readable result artifacts, and the submission bundles — followed by a definitive, ordered "open these files in this order" manifest so a brand-new agent can orient in minutes. Every path below is repo-relative to `/Users/kashhy/workspace/Personal/dev/Job-Matching-Agentic` unless it begins with `/tmp`. All sizes/page-counts were read off disk on 2026-08-18.

---

### 1. The built ESWA manuscript PDF (the paper itself)

There are **two byte-for-content-identical copies** of the current ESWA manuscript, both **45 pages**:

| Path | Pages | Bytes | Modified | Role |
|---|---|---|---|---|
| `docs/submission/eswa/manuscript/main.pdf` | 45 | 3,236,349 | 2026-08-18 15:07 | **Canonical committed copy.** This is the one to open. |
| `/tmp/eswa_build/main.pdf` | 45 | 3,236,794 | 2026-08-18 17:33 | Ephemeral tectonic build output (2h newer, not under version control; lives in `/tmp`). |

- **RENDER THIS to see the actual paper:** `docs/submission/eswa/manuscript/main.pdf`. It is the newest committed 45-page build and always survives a reboot. The `/tmp/eswa_build/main.pdf` is the freshest tectonic re-render but is disposable — treat it as a build artifact, not a source of truth. The two are the same manuscript; the tiny byte delta is just a later re-compile.
- **How it is built:** the ESWA manuscript uses Elsevier's `elsarticle` class — `\documentclass[preprint,review,3p,times,twocolumn,authoryear]{elsarticle}` (`docs/submission/eswa/manuscript/main.tex:10`). The document title is *"An Auditable, Calibrated, and Explainable Multi-Agent System for Job-Candidate Recommendation"* (`main.tex:44`), authors anonymized for double-blind (`main.tex:47`). `main.tex` `\input`s eight section files plus the abstract (`main.tex:53,64-71`): `sections/abstract.tex`, `section-1-introduction.tex` … `section-8-conclusion.tex`, under `docs/submission/eswa/manuscript/sections/`.
- **tectonic vs pdflatex — important nuance.** The ESWA paper compiles cleanly under **tectonic** (this is what produced `/tmp/eswa_build/main.pdf`, exit 0, 45pp, 0 undefined refs — see `research/PHASE_STATUS.md:87,95,98` and `research/RESEARCH_DECISIONS.md:97`). `HANDOFF.md:104` documents an alternative TinyTeX `pdflatex` path (`export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"; cd docs/submission/eswa/manuscript && pdflatex -interaction=nonstopmode -halt-on-error main.tex`, run twice for refs). Either engine works for `elsarticle`. **The JAAMAS paper is the opposite:** tectonic *fails* on Springer's `sn-jnl.cls` at glyphtounicode startup, so JAAMAS must be built on Overleaf/pdflatex (`research/PHASE_STATUS.md:80`, `docs/submission/jaamas/REVIEW-TODO.md:12,50`).
- **Build side-artifacts** in `/tmp/eswa_build/`: `main.log` (50 KB compile log), `main.blg` (BibTeX log). In-tree LaTeX intermediates live beside the source: `docs/submission/eswa/manuscript/main.aux`, `.bbl`, `.blg`, `.out`, `.log`, `.spl`.
- **STALENESS WARNING:** `HANDOFF.md:13` still says the manuscript is "39pp". That is out of date — the current manuscript is **45 pages** (confirmed by `mdls` on the committed PDF and by the tectonic logs referenced in `PHASE_STATUS.md`). Trust 45. Also note `docs/submission/eswa/manuscript/main.docx` is explicitly STALE (`HANDOFF.md:122`) — never cite it; use the PDF.

---

### 2. Every other committed PDF under `docs/submission/`

| Path | Pages | Bytes | What it is |
|---|---|---|---|
| `docs/submission/eswa/manuscript/main.pdf` | 45 | 3.24 MB | **ESWA manuscript (the paper).** |
| `docs/submission/eswa/title-page.pdf` | 2 | 85 KB | Unblinded ESWA title page (author "Harsh Kashyap"); body is double-blind (`HANDOFF.md:35`). Source: `title-page.tex`. |
| `docs/submission/jaamas/manuscript/main.pdf` | 26 | 1.49 MB | JAAMAS manuscript (prior venue, Springer). Title: *"JobMatch: An Agentic Multi-Role Platform for Explainable Job–Candidate Matching"* (`jaamas/manuscript/main.tex:21`). Dated Jul 30. |
| `docs/submission/jaamas/build/jaamas-manuscript.pdf` | 26 | 1.49 MB | Byte-identical July build of the JAAMAS manuscript. |
| `docs/submission/jaamas/supplementary/supplementary-information.pdf` | 9 | 1.43 MB | JAAMAS supplementary information. |
| `docs/submission/jaamas/build/jaamas-supplementary.pdf` | 9 | 1.43 MB | Build copy of the JAAMAS supplementary. |
| `docs/submission/jaamas/portal/cover-letter.pdf` | 2 | 61 KB | JAAMAS portal cover letter (built by `portal/build_cover_letter.sh`). |
| `docs/submission/jaamas/portal/information-sheet.pdf` | 3 | 142 KB | JAAMAS portal information sheet (built by `portal/build_info_sheet.sh`). |
| `docs/submission/iui2027/manuscript/main.pdf` | 22 | 1.82 MB | IUI 2027 variant of the paper (a third venue framing; dated Aug 1). |
| `archive/jaamas-overleaf-prev-2026-05-28/manuscript_PREV/main.pdf` | — | — | Archived pre-May-28 JAAMAS manuscript (historical only). |

Related-work reference PDFs (the four papers the related-work section is built against, each with a paired extracted-text `.md`) live in `docs/submission/eswa/strategy/related-work/`: `01_lo_cvpr2025_ai_hiring_llms.pdf`, `02_arxiv_2505_20312_jobseeker_multigent.pdf`, `03_arxiv_2401_08315_llm_resume_screening.pdf`, `04_arxiv_2202_08960_traceable_jd_resume.pdf`.

> Note: the JAAMAS committed PDFs are pre-edit July builds; per `docs/submission/jaamas/REVIEW-TODO.md:50`, the only remaining JAAMAS step is a fresh Overleaf recompile. The ESWA line is the live one.

---

### 3. The JAAMAS Overleaf ZIPs

Three ZIPs exist; they are complete, self-contained Overleaf upload bundles (class files, `.sty`, sections, tables, algorithms, figures):

| Path | Bytes (approx) | Figures format | Freshness | Use |
|---|---|---|---|---|
| `docs/submission/jaamas/jaamas_overleaf_ready.zip` | ~3.5 MB | **PNG** figures (`Fig1`,`Fig4-7.png`) + `Fig2.drawio` + 8 UI screenshots | Sections/tables updated **2026-08-18** | **Newest — upload this to Overleaf.** |
| `docs/submission/jaamas/build/jaamas-overleaf-upload.zip` | ~2.4 MB | **PDF** figures (`Fig1-8.pdf`) + screenshots | 2026-07-12 (all files same timestamp) | Older self-consistent July snapshot. |
| `archive/jaamas-overleaf-prev-2026-05-28/jaamas-overleaf-upload_PREV.zip` | — | — | 2026-05-28 archive | Historical only. |

Both live bundles contain `manuscript/main.tex`, `manuscript/sections/section-1…7`, `manuscript/tables/tab-*.tex` (workflows, fairness, latency, dataset, model-params, ablation, methods, explainability, progression, fusion, hard-negs, implementation-*), `manuscript/algorithms/alg-multi-agent-matching.tex`, and Springer support files (`sn-jnl.cls`, `sn-mathphys-num.bst`, `threeparttable.sty`, `wrapfig.sty`, `enumitem.sty`, `appendix.sty`, `cuted.sty`, `jaamas-style.tex`, `jaamas-macros.tex`).

---

### 4. Key data files

#### 4a. Real human evaluation corpus — `data/` (this is the corpus the paper's headline numbers come from)

| File | Bytes | Shape | Contents |
|---|---|---|---|
| `data/eval_pairs.json` | 3,189 | dict `{version, task, relevance_scale, notes, labels[47]}` | **The 47 graded human relevance labels** over 30 CVs × 15 jobs, scale 0–2 (only grades 1,2 present; 403/450 implicit-0 — `NUMERICAL_CLAIMS.yaml:7`). The primary/secondary transfer-check corpus. |
| `data/cvs.json` | 8,627 | list[30] | 30 structured candidate profiles. |
| `data/jobs.json` | 4,137 | list[15] | 15 structured job postings. |
| `data/eval_pairs_llm.json` | 39,391 | dict, `labels` list | LLM-assisted labels (EXP-018). |
| `data/eval_pairs_llm_expanded.json` | 45,365 | dict, `labels` list | Expanded LLM-assisted label set. |
| `data/fairness_audit_profiles.json` | — | — | 10 synthetic counterfactual profile pairs for the offline bias audit. |
| `data/expected/paper_progression_summary.json` | — | — | Expected values for the progression table (regression check). |
| `data/models/calibration.json` | 57 | dict (2 keys) | Fitted calibration params used in production scoring. `data/models/calibration.json.preneg.bak` is a pre-negation backup. |
| `data/models/fusion.json` | 381 | dict (2 keys) | Fitted fusion weights. |

#### 4b. Synthetic research corpora

| File | Bytes | Scale | Notes |
|---|---|---|---|
| `data/research/eval_pairs.json` | 1,582,279 | 5,000 labeled pairs (relevance 0–3 + rationale) | Large synthetic eval set; `data/research/manifest.json` records seed 42, 100 candidates, 50 jobs, 8 role families. |
| `data/research/cvs.json` | 39,480 | 100 candidates | |
| `data/research/jobs.json` | 25,689 | 50 jobs | |
| `research/datasets/synthetic_v1/` | — | 500 resumes × 75 jobs | Transparent latent ground truth (`synthetic_jobs.json`, `synthetic_resumes.json`, `synthetic_relevance.json`, `manifest.json`). This is the dev/validation corpus in `research/PROTOCOL.md`. |
| `research/datasets/synthetic_v2/` | — | **2,000 resumes × 200 jobs = 400,000 pairs** | `manifest.json`: seed 42, latent weights (required 0.4, preferred 0.12, seniority 0.15, experience 0.13, family 0.1, workmode 0.05, comp 0.05), grade thresholds `3≥0.80,2≥0.60,1≥0.40`, 8% label noise, 104,674 positive pairs. Backs EXP-024/026 structure-recovery & calibration. |

#### 4c. Human-study stimuli / annotation sheets

- `research/datasets/explanation_study/` — 45 rendered HTML stimuli = **15 jobs × 3 explanation conditions** (`__factor_grounded`, `__generic_template`, `__score_only`), plus `INSTRUMENT.md`, `manifest.csv`, `SIDE_BY_SIDE_sample.html` — the ready-to-run human explanation-usefulness study (Option B in the handoff).
- `research/datasets/annotation_sheet_llm_prefilled.csv`, `annotation_sheet_unjudged.csv` — annotation sheets for expanding the benchmark (Option A).

---

### 5. Machine-readable result artifacts — `research/results/` (28 JSON files)

Every headline number in the manuscript traces to one of these. Two are load-bearing:

- **`research/results/MANUSCRIPT_NUMBERS.json`** (3,660 bytes) — the **single source of truth** for headline numbers, auto-generated by `research/experiments/generate_manuscript_tables.py` and enforced by `research/experiments/verify_paper_numbers.py` (the build's numeric gate). Keys include `composite_ndcg5`; nine `ndcg5::<baseline>` entries (BM25, TF-IDF cosine, Exact skill overlap, Semantic cosine, Semantic euclidean-derived, Skills Jaccard, Soft skill embedding, Multimodal weighted blend, RRF ensemble); the full `calib::{raw,platt,isotonic,temperature,beta,constant_base_rate}::{ece,adaptive_ece,bss,auc}` grid; `recovery_ratio`; `gen_both_unseen`; `ece_platt_heldout`; `latency_softskill_ms`.
- **`research/results/calibration_methods.json`** (11,219 bytes, EXP-026) — the calibration study (§5/§N). Records `n_pairs=450`, `base_rate_positive=0.1044`, protocol "held-out 5-fold over resumes … seed 42; never fit on test", and per-method `ece / adaptive_ece / mce / brier / brier_skill_score / roc_auc / confidence_range / reliability_curve[]`. The `raw` method shows ECE 0.3995, BSS −1.2473, AUC 0.967; this file is what proves the "isotonic preserves discrimination (BSS 0.64/AUC 0.95) while Platt goes near-degenerate" finding.

Other notable result files (all in `research/results/`): `architecture_value.json` (EXP-019), `calibration_discrimination.json` (EXP-020), `explanation_faithfulness.json` (EXP-028), `failure_injection.json` (EXP-033), `feature_fusion_synth.json` / `feature_fusion_synthetic_v2.json`, `generalization.json` (EXP-027), `graded_skill_channel.json`, `job_heldout.json` (EXP-012), `jobbert_baseline.json`, `lambdamart_baseline.json`, `leave_one_out_ablation.json`, `llm_annotation.json` / `llm_label_expansion.json` (EXP-018), `model_selection.json` (EXP-025), `powered_reeval.json`, `robustness_matrix.json` (EXP-029), `scalability.json` (EXP-031/032), `significance_corrected.json` (EXP-022, Holm), `skill_semantics.json` / `skill_semantics_objective.json`, `structure_recovery.json` / `structure_recovery_nonadditive.json` (EXP-024), `temporal_drift.json` (EXP-030), `weight_stability.json` (EXP-015).

---

### 6. READ-FIRST, IN THIS ORDER

A new agent with zero context should open files in exactly this sequence. The logic is **control plane → ideology → manuscript → constraints**: first learn *where everything is and what state it's in*, then *the rule that governs every edit*, then *the actual paper*, then *the hard limits you must not cross*.

| # | Open this file | Layer | Why it's here / what you extract |
|---|---|---|---|
| 1 | `HANDOFF.md` | control plane (map) | Master entry point. Own "read-first" table (§0), who the user is, tools/env, the reproduction commands (§K), machine gotchas (torch hang, heredoc hang, zsh glob), and §H — the score-improvement discussion. **Correct one stale fact yourself: it says 39pp; the paper is 45pp.** |
| 2 | `research/PHASE_STATUS.md` | control plane (state) | Current truth of the world: all 47 phases + Stage-2 (EXP-024…033) marked COMPLETE, only author-only items open. Synced 2026-08-18. |
| 3 | `research/reports/FINAL_REVIEW.md` then `research/reports/FINAL_AUDIT.md` | control plane (verdict) | The 5-reviewer hostile ESWA panel verdict + the honest ceiling (what caps the score). `FINAL_AUDIT` is the §AH 26-item master summary of everything done and every claim rejected as non-defensible. |
| 4 | `research/EXPERIMENT_REGISTRY.yaml` | control plane (evidence) | Every experiment EXP-001…033: RQ, dataset, output artifact, result, seed (42), status, and exact `repro_cmd`. Nothing is claimed without an ID here. |
| 5 | `research/results/MANUSCRIPT_NUMBERS.json` + `research/NUMERICAL_CLAIMS.yaml` | control plane (numbers) | Every headline number → its source artifact and verdict (REPRODUCIBLE / LEAKED / PHANTOM / STALE). Read before touching any number in the paper; `verify_paper_numbers.py` gates against `MANUSCRIPT_NUMBERS.json`. |
| 6 | `docs/submission/eswa/ESWA-STAGE2-PLAN.md` | **ideology** | The governing mandate: **"maximum scientific credibility, not maximum metric."** §A is the non-negotiable rule (never run 20–50 configs and pick the best; preserve negative results; no manufactured significance). This overrides all earlier "keep the better-looking number" instructions and must inform every edit. |
| 7 | `research/RESEARCH_DECISIONS.md` | ideology (locked decisions) | RD-001…015 — decisions not to re-litigate (RD-001 reframe to auditable/calibrated/explainable; RD-009 no git; RD-012 honest numbers; RD-013 corrected corpus/generalization values; RD-015 tectonic build loop). |
| 8 | `docs/submission/eswa/manuscript/main.pdf` **(render this)** | **manuscript** | The actual 45-page paper. This is the deliverable everything else supports. Render the committed copy; `/tmp/eswa_build/main.pdf` is the same build, newer but disposable. |
| 9 | `research/PROTOCOL.md` | **constraints** | The FROZEN Stage-3 evaluation protocol: the data hierarchy (synthetic_v1 + inner CV = dev; real 47-label corpus = secondary transfer check, NOT a pristine test) and the list of choices the outer test MUST NOT influence. Read this before running anything new so you don't leak. |
| 10 | `research/reports/FINAL_REPRODUCTION.md` + `scripts/reproduce_all.sh` | constraints (repro) | How to regenerate everything deterministically (`bash scripts/reproduce_all.sh`, exit 0 = pass) and the single-threaded env vars required to avoid the torch hang. |

**Fastest possible orientation (if you read only three):** `HANDOFF.md` → `research/reports/FINAL_REVIEW.md` → render `docs/submission/eswa/manuscript/main.pdf`. That gives you the map, the honest ceiling, and the paper. `HANDOFF.md:124` ("Recovery — if lost") confirms this: read `FINAL_REVIEW.md` + `FINAL_AUDIT.md`, then ask the user which score-option (A/B/C/D) to pursue before starting any corpus expansion or novelty rewrite.

**Which PDF to render:** always `docs/submission/eswa/manuscript/main.pdf` (canonical, committed, 45pp). Use `/tmp/eswa_build/main.pdf` only if you want the most recent tectonic re-render and understand it is not persisted. Do **not** open `main.docx` (stale) or the JAAMAS/IUI PDFs unless you are specifically working the JAAMAS or IUI venue — the live scientific line is ESWA.

## Appendix A — Commands & gotchas (copy-paste)

```bash
# repo root
cd /Users/kashhy/workspace/Personal/dev/Job-Matching-Agentic

# 1. Number-integrity gate (MUST be exit 0 before trusting the manuscript)
PYTHONHASHSEED=0 python3 research/experiments/verify_paper_numbers.py

# 2. Full reproduction (experiments -> tables -> verifier), deterministic
bash scripts/reproduce_all.sh

# 3. Build the ESWA PDF (tectonic works for ESWA; ~45pp, 0 undefined refs)
cd docs/submission/eswa/manuscript && mkdir -p /tmp/eswa_build &&   tectonic main.tex --keep-logs -o /tmp/eswa_build

# 4. After human annotation arrives (the #1 author-gated lever):
python3 research/experiments/merge_annotations.py
EVAL_PAIRS=data/eval_pairs_expanded.json python3 research/experiments/powered_reeval.py

# 5. JAAMAS build: Overleaf ONLY (tectonic CANNOT build Springer sn-jnl.cls).
#    Upload docs/submission/jaamas/jaamas_overleaf_ready.zip -> compiler=pdfLaTeX
#    -> main document = manuscript/main.tex -> recompile twice (BibTeX).
```

**Gotchas that will bite a new agent:**
- **tectonic cannot build JAAMAS** (Springer `sn-jnl.cls` chokes at `\input{glyphtounicode}`). ESWA builds fine with tectonic; JAAMAS needs pdfLaTeX/Overleaf.
- **Never hand-type a number into a `.tex`.** Numbers flow artifact -> `MANUSCRIPT_NUMBERS.json` -> tables -> prose, gated by `verify_paper_numbers.py`. The verifier has a FORBIDDEN list (stale/phantom numbers, label-leakage phrasing) and a REQUIRED list — edit those if a legitimate number changes.
- **Provisional/synthetic/LLM-assisted results must NOT enter the verifier-gated manuscript.** `eval_pairs_llm_expanded.json` (LLM-assisted, Δ+0.082 p=0.039) is DISCLOSED-provisional and stays out until real human labels arrive.
- **No git commits** (RD-009) and **no external LLM APIs** (use headless `claude -p` or Kiro/`consult-kiro` only).
- **`main.pdf` in the JAAMAS dir is stale (Jul 30)** — rebuild; don't trust it. `/tmp/eswa_build/main.pdf` is a disposable ESWA build.
- **Workflow scripts:** `${VAR}` in a template literal interpolates at construction — define every referenced const, or the workflow fails instantly (learned the hard way building this handoff).

## Appendix B — Recovery (if you're lost)
Re-read, in order: `research/PHASE_STATUS.md` -> `research/RESEARCH_DECISIONS.md` (RD-001..RD-017) -> this file's §1 (mandate/constraints) -> render `docs/submission/eswa/manuscript/main.pdf`. Then run the verifier (Appendix A #1); if it is exit 0, the manuscript is intact and the only real work left is the 4 author-gated items in §6. Do not start new experiments or "improve the metric" — the governing rule is MAXIMUM SCIENTIFIC CREDIBILITY, not maximum metric.

---
_This handoff was assembled from an 8-reader + synthesis workflow over the live repo on 2026-08-18. If a fact here conflicts with the `research/` control files, the control files win (RD-004)._
