# Larger Judged Benchmark — Annotation Protocol (author-executable)

> Purpose: address the paper's headline ceiling (EDITORIAL_RISK_MATRIX #3): a tiny, single-annotator,
> all-positive-labeled real corpus (30 resumes x 15 jobs, 47 labels). This protocol specifies how to build
> a larger, TWO-annotator, explicitly-negative-judged benchmark with graded relevance, so the ranking and
> skill-semantics claims can be tested with real statistical power. It fabricates nothing — it defines the
> sampling, labeling, adjudication, and reporting so the resulting corpus is defensible.

## 0. Quick start — explicit negatives from the EXISTING corpus (no new data needed)
Before sourcing new resumes/jobs, close the sharpest reviewer objection (positive-only labels) using the
corpus we already have: only 47 of the 30×15=450 pairs are judged; the other **403 are merely assumed
grade-0 (closed-world)**. `research/experiments/make_annotation_sheet.py` generates
`research/datasets/annotation_sheet_unjudged.csv` — those 403 pairs with real candidate/job context, a
hard-negative **stratum hint** (10 hard-negatives, 393 easy), and **blank** `grade_annotator1/2`,
`adjudicated_grade`, `annotator_rationale` columns (nothing fabricated). Have two annotators + an
adjudicator fill 0–3 per the rubric in §4; combined with the existing 47 labels this yields the full
450-pair **explicitly-judged** benchmark and lets §5's ranking/skill-channel results be re-run with real
power and real negatives. This is the fastest path to the powered re-test; the larger multi-corpus effort
below (§1–§9) is the follow-on.

**End-to-end loop (tooling ready + validated):**
1. `make_annotation_sheet.py` → `annotation_sheet_unjudged.csv` (403 pairs, blank grades). ✔ generated.
2. Two annotators + adjudicator fill `adjudicated_grade` (0–3). ← the only human step.
3. `merge_annotations.py` → `data/eval_pairs_expanded.json` (unions the filled grades with the existing 47;
   never overwrites, skips blanks, validates 0–3). ✔ built + self-test passes.
4. Re-run the existing harness (`comparison_table` / `graded_skill_channel` / `extended_evaluation`) pointed
   at `eval_pairs_expanded.json` for the powered, explicitly-negative-judged re-test. ✔ existing tooling.
So the entire pipeline except the human grading is ready and validated; drop in the filled sheet and run.

## 1. Target scale and why
- **>= 60 query resumes x a shared 30-job pool**, with **>= 900 judged (resume, job) pairs** including
  explicit negatives. Rationale: the current n=30 all-positive design gives near-ceiling nDCG and no
  discrimination at @5 (a reviewer's core objection). A larger pool with judged negatives restores power
  and lets nDCG@k, MRR, and Recall@k actually separate methods.
- **Graded relevance 0-3** (0 = clearly unqualified, 1 = weak, 2 = plausible, 3 = strong), matching the
  existing schema so the new corpus is a drop-in for the current harness.
- **Explicit negatives are mandatory:** each query must include judged 0/1 pairs, not only positives — this
  is the specific gap that makes the current corpus a weak test.

## 2. Sampling (pre-registered, to avoid selection bias)
- Draw resumes and jobs to span the 10 job families and 4 seniority tiers already used, plus deliberate
  HARD pairs: same-title/wrong-skills, same-skills/wrong-seniority, high-semantic-similarity/wrong-domain
  (the hard-negative families from EXP-039). Record the sampling frame and counts per stratum.
- For each query resume, include: its true-family jobs (candidate positives), 2-3 adjacent-family jobs
  (candidate hard negatives), and 2-3 random-family jobs (easy negatives). This guarantees a mix of grades.
- Freeze the sampled item IDs BEFORE labeling; no post-hoc addition/removal of items based on results.

## 3. Annotators and independence
- **>= 2 independent annotators** with recruiting/technical-screening background; a third as adjudicator.
- Annotators label the SAME pairs independently, blind to each other and to the model's scores/ranking.
- Provide written guidelines (§4) + a calibration set of 20 pairs with discussed gold answers before the
  main task, to align interpretation.

## 4. Labeling guidelines (the rubric annotators apply)

**Scale note (supervisor 2026-08-18):** two scales, chosen for consistency.
- **Existing-corpus explicit-negatives (§0, the 403 unjudged pairs):** use the current **0–3** scale below,
  so the new labels merge cleanly with the existing 47 (which are on 0–3). This is the fastest powered re-test.
- **Fresh larger benchmark (§1–§9, new resumes/jobs):** use the finer **0–4** scale the supervisor suggested
  — 0 irrelevant · 1 weak · 2 relevant · 3 strong · 4 excellent — graded from scratch by ≥2 annotators.
  Report which scale each split uses; do not mix them within one nDCG computation.

Grade a (resume, job) pair on fit for advancing to a first interview:
- **3 (strong):** meets required skills and seniority; clearly advance.
- **2 (plausible):** meets most requirements; reasonable to advance with minor gaps.
- **1 (weak):** notable gaps (missing key required skill OR wrong seniority band); usually would not advance.
- **0 (unqualified):** wrong domain or missing most requirements; would not advance.
Instructions: judge on the resume/job content only; ignore names, gender, age, location cues (fairness);
required skills weigh more than preferred; do not reward keyword stuffing. Record a one-line rationale per
pair (supports later error analysis and faithfulness grounding).

## 5. Agreement and adjudication
- Report **inter-annotator agreement**: quadratic-weighted Cohen's kappa (graded) and exact-agreement rate.
  Target weighted kappa >= 0.6; if lower, refine guidelines on the calibration set and re-label.
- **Adjudication:** disagreements > 1 grade go to the third annotator; final label = adjudicated value.
  Keep both raw annotator labels in the release for transparency.
- Report the label distribution across grades (must NOT be all-positive) and per-stratum.

## 6. Anti-leakage and reuse discipline
- This benchmark is a NEW test set. Once built, it is split into a development portion (for any future
  tuning) and a **held-out portion evaluated once**. The existing 30x15 corpus stays as a separate legacy
  set; do not merge them for a "clean test" claim.
- Any model selection continues on synthetic + development folds only (PROTOCOL.md discipline carries over).

## 7. What it buys the paper (report whatever the data show)
- Powered re-test of the composite vs baselines (does parity hold, or does a method separate?).
- Powered, non-underpowered re-test of the graded skill channel (EXP-043) — replaces the current n=30
  one-query-dominated real-corpus result with a real effect-size estimate.
- Real required-vs-preferred skill features become testable (the synthetic-only limitation in EXP-035/036).
- Honest negatives welcome: if the composite is still at parity on a powered corpus, that is a strong,
  publishable finding about the ceiling of lightweight composite ranking.

## 8. Cost / feasibility notes for the author
- ~900 pairs x 2 annotators ~= 1800 judgments; at ~30 s/judgment ~= 15 annotator-hours total plus
  adjudication. Feasible with 2 paid annotators over a few days, or a small partner TA team.
- Deliverables to deposit with the artifact: item IDs + frozen sampling frame, per-annotator labels,
  adjudicated labels, guidelines, agreement statistics, and the pre-registration.

## 9. What the author must provide (cannot be automated here)
- The two human annotators + adjudicator, their time, and (if applicable) IRB/data-use clearance.
- Real resume/job content at the larger scale (or consented synthetic-augmented content, clearly labeled).
- Everything structural (sampling script over the existing corpora, guideline PDF, agreement/adjudication
  tooling, and the harness wiring) can be generated on request from the current codebase.
