# JobMatch → ESWA — STAGE 2 EXECUTION PLAN (authoritative)

> Saved 2026-08-17. Companion to `ESWA-EXECUTION-PLAN.md` (the 47-phase plan). This is the
> SECOND major stage: SCIENTIFIC STRENGTHENING → COMPLETE REMAINING PHASES → MANUSCRIPT REBUILD
> → ARTIFACT VALIDATION → FINAL HOSTILE REVIEW. Goal = the strongest **scientifically defensible**
> version of JobMatch, not the highest metric.

## A. Non-negotiable scientific rule
Do NOT optimize for favorable results. You may explore many legitimate designs/baselines/seeds/configs,
but NEVER run 20–50 approaches and pick the highest number. Instead: (1) define valid candidate
protocols; (2) identify invalid/leaky ones BEFORE selecting on results; (3) define selection criteria
independent of the final test result; (4) run; (5) analyze all; (6) select by the predefined criteria;
(7) report the selection process; (8) preserve negative results. If a competitor beats JobMatch, report it.
If JobMatch isn't significantly better, don't manufacture significance. Objective = MAXIMUM SCIENTIFIC
CREDIBILITY, not MAXIMUM METRIC. **This supersedes the earlier "keep the better-looking number" instruction.**

## B. Read current state first
Inspect all control files (PHASE_STATUS, PROJECT_STATUS, EXPERIMENT_REGISTRY, NUMERICAL_CLAIMS,
RESEARCH_DECISIONS, REPRODUCTION_LOG, REVIEW_LOG, BASELINE_AUDIT, HONEST_NUMBERS, NUMBERS_PASS_PLAN),
experiment outputs, manuscript/PDF/tables/figures, code, tests. Reconstruct: complete / partial / failed /
corrected / remaining; which manuscript claims depend on each result; which are unsupported. Don't redo
completed work unless a dependency invalidates it.

## C. Numbers pass — FIRST
Proceed with `NUMBERS_PASS_PLAN.md` but independently verify every replacement (old→manuscript loc→
experiment→config→dataset→output→verify→replace→update dependent claims→regenerate tables/figures→
numerical audit). Produce `research/reports/NUMBERS_PASS_FINAL.md` with columns: Claim, Old, New, Experiment
ID, Dataset, Seed, Source output, Manuscript locations, Reason, Verification status. Do not preserve an old
number just because it's better.

## D. Search 20–50 legitimate improvement configurations (NOT cherry-picking)
Create `research/experiments/model_selection/` + a registry. Explore ~20–50 legitimate configs to test
whether the current result is an artifact / has a better-justified config / the benchmark is too small /
the model is sensitive / a stronger protocol reveals a real contribution. Dimensions: ranking (fixed
6-channel / learned linear / logreg / LambdaMART / feature subsets / normalized-vs-not / learned-vs-prior /
regularized), semantic representation (embedding/pooling/normalization), skill matching (exact/synonym/
fuzzy/ontology/semantic), retrieval (lexical/dense/hybrid/rerank), calibration (Platt/isotonic/alt/split
strategies), explanation (deterministic/contribution/constrained-LLM/template). Hierarchy: TRAIN/DEV options
→ VALIDATION selection → FINAL FROZEN TEST. Never let the test set influence selection.

## E. Model-selection rule
Define selection criteria BEFORE seeing final test results. PRIMARY nDCG@5; SECONDARY MRR/Recall@5/
calibration/faithfulness/latency/stability. A candidate can't win on nDCG alone — weigh statistical
uncertainty, complexity, reproducibility, calibration, interpretability, cost, robustness. If two are
statistically indistinguishable, prefer the simpler, more auditable one. Document it.

## F–H. Large synthetic dataset (~500 resumes + large job pool), KNOWN ground truth, power/stress
Deterministic, versioned generator. Structured resume/job attributes. Difficulty levels EASY/MODERATE/
HARD/ADVERSARIAL. Relevance from a TRANSPARENT latent-compatibility generator (skill/seniority/experience/
title/location/comp satisfaction) with stored latent ground truth + deliberate noise — NOT random LLM
labels. Test whether ranking recovers known structure. Always label SYNTHETIC/CONTROLLED; never present as
human judgments. Use for pool-growth, noise, sparse/unseen/irrelevant/parser-error/missing-field/
contradictory/synonym/misspelling/keyword-stuffing/long-short/new-family stress + variability. Do NOT use
synthetic to manufacture a favorable headline nDCG.

## I. Human data = primary real-world eval
Preserve the human labels. Expand if technically possible (full 30×15 = do it). If not obtainable, document
the limitation. Never substitute synthetic for missing human labels while calling it real-world eval.

## J. Generalization
Finish/strengthen unseen-job, unseen-candidate, and both-unseen generalization. Verify zero leakage. Record
per split: #candidates/#jobs/#pairs/relevance dist/overlap checks. Multiple seeds or bootstrap CIs.

## K. Ranking evaluation (final real data)
Report nDCG@5, nDCG@10, MRR, Recall@5, Recall@10, P@5 where meaningful. Compare vs BM25, TF-IDF, semantic,
hybrid, pointwise-LR, LambdaMART, cross-encoder, recruitment-specific model if feasible. Identical eval
sets, fair tuning, don't weaken baselines.

## L. Statistics
Every important comparison: bootstrap CIs, paired test, effect size, sample size, multiple-comparison
correction (Holm). Never report p<0.05 as sole evidence. If CIs overlap and paired test NS → "not
statistically established."

## M. Weight analysis
Determine if the six weights are priors / manual / validation-selected / learned / stable. Bootstrap
stability; report mean ± uncertainty. If learned ≠ hand-set, don't pretend hand-set is optimal — either
justify as domain priors OR replace with a properly learned+validated formulation.

## N. Calibration
Define the probability target precisely (e.g. P(relevant|candidate,job,score)), not vague "confidence".
Evaluate raw/Platt/isotonic/alt on a separate calibration set, test on untouched data. Report ECE, Brier,
calibration curve, reliability diagram, discrimination/AUC, CI, score/prob distribution. Investigate the
degenerate [0.11,0.14] range. Don't celebrate low ECE if the model emits near-constant probabilities; test
vs a trivial constant predictor.

## O. Explanation evaluation
Don't call 0.745 a strong faithfulness result if it's only lint-style checking. Rebuild: attribution
correctness, score-component consistency, completeness, specificity, contradiction rate, counterfactual
consistency. Small controlled human study if possible; else clearly describe as automated structural
validation. Don't overclaim.

## P. Counterfactuals
Complete the 50-pair experiment (baseline / edit / expected / actual component / composite / ranking /
explanation / confidence effects). A null result is valid. Investigate WHY rank is insensitive (correct
stability / insufficient perturbation / saturation / pool effects / bug) with evidence.

## Q. Fairness / proxy sensitivity
Don't call it fairness validation. Expand matched-profile demographic-proxy tests where appropriate. Measure
score/rank/top-K/confidence/explanation differences. Use "demographic-proxy sensitivity analysis" unless
evidence supports stronger terms.

## R. Robustness matrix
Parser perturbation, missing/extra/irrelevant skills, synonyms, misspellings, capitalization, formatting,
missing comp/remote, contradictory fields, sparse/long resumes, keyword stuffing, adversarial injection.
Measure Δ score/rank/top-K/confidence/explanation. Build a matrix.

## S. Temporal robustness
Real temporal data if it exists; else a controlled simulation (emerging skills / changing titles / salary /
remote / new categories). Don't claim real temporal validation if simulated.

## T. Scalability (real)
Increasing candidates/jobs/queries → p50/p95/p99/throughput/memory/CPU/indexing/retrieval/ranking/
explanation latency. Don't call a 15-job benchmark production-scale. Use the 500 synthetic resumes + larger
job pools.

## U. Incremental updates
1/10/100/batch resume+job updates → index update / cache invalidation / affected recs / recomputation /
latency.

## V. Failure injection
LLM timeout / malformed LLM / parser failure / missing embedding / missing skill / malformed job / DB
failure / stale index / duplicate candidate+job → verify fallback, failure isolation, no silent corruption,
predictable errors.

## W. Multi-agent claim
Currently: failure isolation yes, no monolith-vs-agent perf benefit. Don't manufacture one. Measure
isolation/modularity/privacy/testability/independent-scaling/fault-containment; if none measurable, DEMOTE
multi-agent to an implementation architecture, not an algorithmic contribution.

## X. Code quality
Full review: duplicated/dead code, hard-coded paths/data, seeds, hidden state, exceptions, type safety,
dependency versions, config, logging, security, PII, API keys, determinism. No `/Users/harsh...` in
reproducible scripts.

## Y. Reproduction (fresh clone)
Clone→install→prepare→run→reproduce→regenerate figures/tables→compile PDF, as a stranger. Any mismatch vs
the manuscript = blocker until explained.

## Z. Manuscript rebuild (only after evidence finalized)
Rewrite Abstract/Intro/Contributions/Related Work/Method/Setup/Results/Discussion/Limitations/Conclusion —
rewrite CLAIMS to match evidence, not just numbers. Emphasize auditable ranking, explicit factor
decomposition, calibrated relevance confidence, explanation eval, counterfactual analysis, robustness,
generalization, reproducibility. Don't oversell superiority/fairness/trustworthiness/generalization/
production-readiness/multi-agent novelty.

## AA. Figures & tables
Regenerate ALL from experiment outputs (no manual number editing). Update architecture/ranking/calibration/
explanation/counterfactual/robustness/scalability/workflow. Captions must describe what's actually measured.

## AB. Numerical claim audit
Every quantitative claim (abstract/intro/method/results/discussion/conclusion/tables/captions/appendix/
supplementary): CLAIM→SOURCE→EXPERIMENT→DATASET→CONFIG→OUTPUT→VERIFIED. No orphan numbers.

## AC. Final document audit
manuscript/PDF/README/supplementary/artifact/GitHub/DOI/cover-letter/highlights → same title/numbers/
dataset/model-names/claims/limitations, correct refs, no stale text/placeholders/draft-labels/author-leaks.

## AD. Final hostile review
Strict ESWA reviewer, attempt to reject. Evaluate 16 axes (novelty, correctness, dataset, eval validity,
baselines, statistics, generalization, calibration, faithfulness, counterfactual, robustness, fairness,
scalability, architecture, reproducibility, writing). Classify BLOCKER/SERIOUS/MODERATE/MINOR. Don't finish
with fixable BLOCKER/SERIOUS open. If it still deserves rejection, say so.

## AE. Final loop
DISCOVER→IMPLEMENT→RUN→VERIFY→REVIEW→FIX→RE-RUN→RE-VERIFY→RE-REVIEW. Multiple configs/seeds where
appropriate. Don't stop after one run or because a metric improved. Stop only when scientifically justified
and reproducible.

## AF. Status control
Update PHASE_STATUS / EXPERIMENT_REGISTRY / RESEARCH_DECISIONS / NUMERICAL_CLAIMS / REVIEW_LOG after the
corresponding work. No "complete" without evidence.

## AG. Final deliverables
FINAL_AUDIT.md, FINAL_NUMERICAL_AUDIT.md, FINAL_REPRODUCTION.md, FINAL_REVIEW.md, FINAL_DOCUMENT_AUDIT.md,
NUMBERS_PASS_FINAL.md + final manuscript/PDF/figures/tables/supplementary/repro-scripts/synthetic-generator/
synthetic-dataset/eval-configs/README/artifact.

## AH. Final report (26 items)
phases complete/blocked, experiments run/rejected(+why)/negative, final real+synthetic datasets, train/val/
test sizes, baselines, ranking results, significance, calibration, explanation, counterfactual, fairness,
robustness, generalization, scalability, failure-injection, architecture, test count, reproduction result,
numerical discrepancies, manuscript inconsistencies fixed, remaining weaknesses, final ESWA recommendation.
Report whether the EVIDENCE supports submission — not merely that the workflow completed.

**Standing rule:** when choosing between a stronger-looking result and a more defensible one → choose defensible.
