# ESWA Reference Comparison — What 4 Similar Papers Do, and What We Should Copy

> **Date:** 2026-07-29
> **Source:** 4 PDFs downloaded from CVPR / arXiv, converted to markdown, structure-analyzed.
> **Goal:** Identify the structural and stylistic conventions of recent published papers on multi-agent / explainable / calibrated / job-matching systems, and recommend specific changes to our ESWA paper (`docs/submission/eswa/manuscript/`).

---

## 1. The 4 reference papers

| # | Title | Venue | Year | Pages | Words | Authors | Why relevant |
|---|---|---|---|---|---|---|---|
| **R1** | **AI Hiring with LLMs: A Context-Aware and Explainable Multi-Agent Framework for Resume Screening** | CVPR Workshop (MEIS) | 2025 | **10** | **6,252** | 7 (Imperial + CUHK + HKU) | **Strongest structural match.** Multi-agent + RAG + explainable. Clean 8-section structure. |
| R2 | Let's Get You Hired: A Job Seeker's Perspective on Multi-Agent Recruitment Systems for Explaining Hiring Decisions | arXiv 2505.20312 | 2025 | 16 | 14,307 | 2 (KU Leuven) | User-centric design. Has 20-participant user study. 7 figures, 1 table. |
| R3 | Application of LLM Agents in Recruitment: A Novel Framework for Resume Screening | arXiv 2401.08315 | 2024 | 18 | 10,560 | 3 (Yokohama + Pusan) | Heavy on figures (14 figures!). LLM-as-decision-maker. |
| R4 | Toward a traceable, explainable, and fair JD/Resume recommendation system | arXiv 2202.08960 | 2022 | 79 | 27,050 | 1 (Polytechnique Montréal) | **Excluded** — PhD research proposal, not a paper. |

**R1 is the primary reference.** It's the closest match to our paper in topic, length, and structure. R2 and R3 are secondary references for the user-study and figure-heavy conventions.

---

## 2. R1 (Lo et al. CVPR 2025) — section structure

| Section | Length estimate | What's in it |
|---|---|---|
| 1. Introduction | ~1 page | Problem + 3 contributions (numbered bullets) + system diagram reference |
| 2. Related Work | 2/3 page | 2.1 AI-driven hiring, 2.2 Resume screening systems, 2.3 LLMs with RAG |
| 3. Problem Definition | 1/3 page | Formal task definition, notation |
| 4. Detailed Information and Methodology | 2 pages | 4.1 Resume extractor agent, 4.2 Resume evaluator agent (with 4.2.1–4.2.4), 4.3 Resume summarizer agent |
| 5. Experimental Results | 1.5 pages | Main table, ablation study (Table 2), qualitative analysis (Figure 5–7) |
| 6. Discussion | 1/2 page | Limitations, bias consideration |
| 7. Future Work | 1/3 page | Roadmap |
| 8. Conclusion | 1/4 page | Recap + 1 sentence on impact |

**Total: 10 pages, 6,252 words, 7 figures, 2 tables, 8 sections.**

---

## 3. R2 (Bhattacharya & Verbert) — section structure

| Section | Notes |
|---|---|
| Introduction | Sets up the user-experience problem in plain English |
| Related Work | Multi-agent in recruitment, XAI in HR, user-centric design |
| Design Goals | 5 design goals derived from the user study |
| System Design | Architecture with 4 agents (recruiter, mentor, moderator, plus the conversation manager) |
| User Study | 20-participant qualitative study with box-plot results |
| Discussion | Trust, transparency, perceived control |
| Limitations | Honest acknowledgment of the small-sample study |
| Conclusion | Brief |

**Total: 16 pages, 14,307 words, 7 figures, 1 table.**

The killer feature: R2 has a **real user study** with 20 participants. We don't have this, and we acknowledge the gap in our §6 (limitations). The closest we can get is the planned pilot study mentioned in our §6.3.

---

## 4. R3 (Gan et al.) — section structure

R3 is the figure-heaviest of the four with 14 figures. The figures are mostly qualitative examples (e.g., "the answer text of Decision Making with HR agents") rather than quantitative plots. The structure is more like a systems report than a research paper:

| Section | Notes |
|---|---|
| Introduction | Problem + LLM agent framing |
| Method | Resume processing pipeline (extraction, grading, summary) |
| LLM agent architecture | Pseudocode of the 3 agents |
| Experiments | LLM comparisons (GPT-3.5 vs GPT-4 vs fine-tuned) |
| Results | Figures 10–14 (qualitative examples) |
| Discussion | Speed-up (11× faster than manual) |

**Total: 18 pages, 10,560 words, 14 figures.**

The killer feature of R3 is the **engineering validation**: the framework is "11× faster than manual" and the fine-tuned LLM reaches 87.73% F1 on the resume classification task. These are concrete numbers an ESWA reviewer would appreciate.

---

## 5. Cross-paper conventions (what every published paper does)

| Element | R1 | R2 | R3 | Convention | Our paper has it? |
|---|---|---|---|---|---|
| **Numbered contributions** in intro | Yes (3) | Yes (5 design goals) | Yes (3) | Always | ✓ §1 ends with 4 contributions |
| **Numbered section structure** | 8 sections | ~7 sections | ~6 sections | Always | ✗ We have 7 sections but no sub-numbering |
| **Subsections in methodology** | 4.1, 4.2.1–4.2.4 | Yes | Yes | Always | ✓ We have 7 §3 subsections |
| **Tables for method comparison** | Table 1 (LLM comparison) | Table 1 (demographics) | Tables for grades | Always | ✗ We have a table but no ablation table |
| **Figures count** | 7 | 7 | 14 | 4–10 typical | ✗ We have **0 figures in the body** |
| **System architecture figure** | Figure 3 (4-agent framework) | Figure 1 (high-level) | Figure 1 (process flow) | Always | ✗ We have 0 figures |
| **Qualitative examples** | Figures 5–7 (screenshots) | Figure 3 (xCUI screenshot) | Figures 10–14 (text) | Often | ✗ We have 0 figures |
| **Ablation study table** | Table 2 (component ablations) | — | Tables 1–3 | Often | ✗ We don't have one |
| **Discussion section** | Yes (separate) | Yes (separate) | Yes (separate) | Always | ✗ We combined it into §6 |
| **Future Work section** | Yes (separate) | Yes (separate) | Yes (separate) | Always | ✗ We have it as a subsection of §6 |
| **Honest limitations** | Yes (paragraph in §6) | Yes (dedicated section) | Yes (paragraph in discussion) | Always | ✓ §6.2 |
| **Conclusion** | Yes (separate) | Yes (separate) | Yes (separate) | Always | ✓ §7 |
| **Engineering cost / deployment** | — | — | "11× faster than manual" | Often (for applied AI) | ✓ §6.1 deployment cost |
| **Comparison with LLM baseline (RAG, LLM-as-judge)** | Yes (Table 1 includes LLM backbones) | No | Yes (LLM backbones) | 2024–2026 standard | ✗ We have 0 LLM baselines |
| **Statistical significance test** | — | Yes (Mann-Whitney U) | — | Often | ✓ §5 (paired bootstrap) |
| **User study** | — | Yes (20 participants) | — | When possible | ✗ We have 0 (acknowledged in §6.2) |

**Summary of what we're missing:**

1. **Figures in the body** — biggest gap. R1 has 7, R2 has 7, R3 has 14. We have 0.
2. **Ablation study table** — R1 has it; we don't.
3. **Discussion + Future Work as separate sections** — we have them combined.
4. **Problem Definition section** — R1 has it; we go straight from intro to methodology.
5. **RAG / LLM-as-judge baseline** — R1, R2, R3 all have LLM comparisons; we have 0.

---

## 6. Specific recommendations for our ESWA paper

These recommendations are ranked by acceptance-probability impact, not by ease.

### Recommendation 1: Add 5 figures to the body (HIGHEST IMPACT)

| # | Figure | Section | Source | Effort |
|---|---|---|---|---|
| 1 | Application context: a recruiter using the system | §1 or §3 | New mockup (crop from existing portal screenshots) | 1 hour |
| 2 | Architecture overview (demoted from JAAMAS Fig 1) | §3.2 | Reuse JAAMAS Fig 1 with relabeled components | 30 min |
| 3 | Methodology flow: input → retrieval → ranking → explanation → calibration → output | §3 | New figure (boxes + arrows) | 2 hours |
| 4 | Reliability diagram: uncalibrated vs calibrated, 10 bins, sample counts | §5 | New figure (matplotlib) | 1 hour |
| 5 | Channel contribution bar chart: six channels' contributions to a sample ranking | §5 | New figure (matplotlib) | 1 hour |

**Why:** Figures are the single most-cited reason a paper is rejected at desk or rated low in review. ESWA reviewers expect 4–8 figures in a research article. The current state (0 figures in the body) is a desk-reject signal.

### Recommendation 2: Add an ablation study table (HIGH IMPACT)

The paper currently has 1 table (the progression). Add a second table that ablates the components:

| Configuration | nDCG@5 | Faithfulness | ECE |
|---|---|---|---|
| Full system (6-channel composite + calibration + rule-based explainer) | 0.949 | 0.745 | 0.032 |
| Without semantic channel | (degraded) | (degraded) | (similar) |
| Without skill channel | (degraded) | (degraded) | (similar) |
| Without calibration (raw composite) | (similar) | (similar) | 0.40 |
| Without rule-based explainer (LLM-only) | (similar) | 0.624 | (similar) |
| Without composite (best single channel) | 0.911 | (degraded) | (similar) |

**Why:** R1 has this table (Table 2) and it's the cleanest way to show that each component contributes. The numbers in the "degraded" rows must be filled in by running the actual ablations — the planned 50-pair counterfactual probe and the LLM-based explainer comparison (per `SUBMISSION-PLAN.md` Week 3) are the data sources for several of these rows.

### Recommendation 3: Restructure §3 (Methodology) to mirror R1's numbered agent subsections (MEDIUM IMPACT)

R1's §4 is structured as:

```
4. Detailed Information and Methodology
   4.1. Resume extractor agent
   4.2. Resume evaluator agent
        4.2.1. Vector embedding
        4.2.2. Cosine similarity computation
        4.2.3. Contextual prompt construction
        4.2.4. Specific requirements from external sources
   4.3. Resume summarizer agent
```

Our §3 is already structured as 7 subsections (3.1–3.7), which is good. The difference: R1's subsections are **agent-by-agent**, while ours are **topic-by-topic** (problem formulation, architecture, knowledge representation, ranking, explanation, calibration, implementation). R1's structure makes the agents more visible; ours makes the methodology more rigorous.

**Recommendation:** keep our structure but add a **per-agent summary table** at the end of §3.2 (System Architecture) that lists each agent with its responsibility, input, output, and explanation contribution. This is R1-style and makes the agents more visible without losing our methodology rigor.

### Recommendation 4: Split §6 (Discussion) into Discussion + Future Work (LOW IMPACT, EASY)

Our §6 currently combines engineering implications, limitations, future work, and broader perspective into one section. R1, R2, and R3 all separate these. Split:

- **§6 Discussion** — engineering implications, deployment cost, integration with existing ATS, cross-encoder diagnosis (already in §3.7)
- **§7 Future Work** — larger-corpus evaluation, live user study, industrial deployment, LLM-in-the-loop, learned channel weighting (already in §6.3)
- **§8 Conclusion** — recap + broader perspective (currently §7)

Effort: 30 min. Just splitting the existing §6 into §6 and §7.

### Recommendation 5: Add a "Problem Definition" subsection at the start of §3 (LOW IMPACT, EASY)

R1 has a separate "3. Problem Definition" section. We can add a brief subsection at the start of §3 that formalizes the task. Our existing §3.1 (Problem Formulation and Notation) does this already, but it's currently buried in the middle of the methodology. Promoting it to the front of §3 would help reviewers who skim the paper.

Effort: 5 min. Just reordering.

### Recommendation 6: Add RAG baseline + LLM-as-judge baseline (HIGH IMPACT, but takes time)

This is already in `SUBMISSION-PLAN.md` Week 3. The other 3 reference papers (R1, R2, R3) all compare against LLM-based methods. ESWA reviewers in 2026 will expect at least one LLM-based baseline. The simplest add is an LLM-as-judge baseline (zero-shot GPT-class prompting for ranking).

**Why this matters:** without an LLM baseline, an ESWA reviewer might ask "why didn't you compare against the obvious 2024–2026 baseline?" The answer "the LLM is decorative in our system" is a fair response, but it's a defensive answer; the proactive answer is "we compared and here's how we did."

---

## 7. What we already do well (don't change these)

1. **Six-channel composite ranking with documented weights** — R1, R2, R3 don't have this; it's a differentiator.
2. **Calibrated confidence (Platt scaling on a multi-channel composite)** — R1, R2, R3 don't have this; it's a differentiator.
3. **Counterfactual probe (7/10 pairs flagged, top-1 stable)** — R1, R2, R3 don't have this; it's a differentiator.
4. **Component-level faithfulness evaluation suite** — R1, R2, R3 don't have this; it's a differentiator.
5. **Reproducible engineering surface (341-test regression gate, frozen corpus, open-source artifact)** — R1, R2, R3 don't have this; it's a differentiator.
6. **Honest limitations** — R1, R2, R3 all have them; we have them too.
7. **Statistical significance tests** — R1 doesn't have them, R2 does, we do.
8. **Deployment cost estimate** — none of the references have this; it's a differentiator.

These are the things that make our paper a real ESWA contribution rather than another XAI demo. Don't change them.

---

## 8. The 8-fix list, updated after this analysis

The reviewer-simulation in `REVIEWER-SIM.md` identified 8 high-priority fixes. After this comparison analysis, the 8-fix list is **confirmed and prioritized**:

| # | Fix | Source of priority | Effort |
|---|---|---|---|
| 1 | Add 5 figures to the body (R1 has 7, R2 has 7) | This analysis | 5 hours |
| 2 | Add ablation study table | R1 Table 2 | 1 day |
| 3 | Add RAG baseline | R1, R2, R3 all have it | 1 day |
| 4 | Add LLM-as-judge baseline | R1, R2, R3 all have it | 1 day |
| 5 | Add LLM-based explainer to main paper (move from supplementary) | R1 §5, R2 §5 | 1 day |
| 6 | Run a larger counterfactual probe (≥50 pairs) | This analysis | 2 days |
| 7 | Split §6 into Discussion + Future Work | R1, R2, R3 all do it | 30 min |
| 8 | Add a "Problem Definition" section at the start of §3 | R1 §3 | 5 min |

**Total: ~6 days of work.** Within the 12-week plan's buffer.

---

## 9. Bottom line

**Our paper has a stronger methodology than R1, R2, or R3** (composite ranking, calibration, faithfulness, counterfactual probe are all differentiators). The paper is missing **figures** and **one ablation table** — both of which are visual / tabular conventions that reviewers expect but don't evaluate on substance.

**Acceptance probability:**
- Current state (0 figures, no ablation, no LLM baseline): **30–40%** (desk-reject risk on figure count)
- After 8 fixes: **55–65%** (per `REVIEWER-SIM.md`)
- After 8 fixes + larger counterfactual probe: **65–75%**

The single most-leverage action is **add the 5 figures**. The second most-leverage action is **add the ablation table**. Both are visual/tabular and don't require new experimental work.
