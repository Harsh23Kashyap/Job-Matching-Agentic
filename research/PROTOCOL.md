# STAGE-3 EVALUATION PROTOCOL — FROZEN 2026-08-18 (before any Stage-3 optimization)
> Written BEFORE running any Stage-3 model-improvement experiment or seeing any Stage-3 test result.
> Purpose: make model selection defensible and prevent the final test set from influencing development.
> Governing rule: MAXIMUM SCIENTIFIC CREDIBILITY, not maximum metric.

## Data hierarchy
- **DEVELOPMENT + VALIDATION** = (a) the synthetic corpus `research/datasets/synthetic_v1/` (500 resumes ×
  75 jobs, transparent latent ground truth) and (b) INNER cross-validation folds of the real corpus
  (`data/eval_pairs.json`, 30 resumes × 15 jobs, 47 labels). All architecture / feature / weight /
  calibration / threshold / embedding / preprocessing choices are made here ONLY.
- **REAL CORPUS = SECONDARY TRANSFER CHECK (NOT an "untouched test").** Correction (panel, 2026-08-18): the
  47 human labels have ALREADY informed Stage-1/2 architecture, weights, diagnostics, and 33 experiments, so
  we do NOT and CANNOT claim them as a pristine untouched test — that would be indefensible. The real corpus
  is reported as a small, underpowered secondary transfer check whose honest finding is "no statistically
  detectable difference" (not "parity", not "superiority"). Learned components are evaluated via
  candidate/job-grouped nested CV with high reported uncertainty. Only GENUINELY-NEW components whose rules/
  thresholds are FROZEN here for the first time (e.g., the skill-semantics matcher) may be pre-registered and
  run on the real corpus ONCE as a prospective check.

## What the final (outer) test MUST NOT influence
feature selection · model/architecture selection · weight tuning · calibration fitting · threshold/K
selection · prompt selection · embedding-model selection · preprocessing selection. All of these are
decided on synthetic + inner-CV only.

## Selection criteria (FROZEN before results)
1. PRIMARY: mean nDCG@5 under inner CV (or synthetic validation for synthetic-only features).
2. A challenger only BEATS the incumbent (fixed 6-channel composite) if its paired-bootstrap 95% CI of the
   per-query nDCG delta EXCLUDES 0 AND survives Holm across the candidate family. (Bootstrap-percentile
   heuristic — reported as such, not as exact FWER; corroborate with a paired sign/permutation test.)
3. Tie-break when statistically indistinguishable: prefer the SIMPLER, more AUDITABLE, more reproducible
   model (fewer fitted params, deterministic, decomposable). Secondary signals: calibration discrimination,
   faithfulness, latency, robustness, stability.
4. Synthetic-only features (e.g. required-vs-preferred, which the real corpus cannot test) are reported as
   controlled-validity evidence and explicitly limited — never presented as a real-corpus result.

## Prospective-check rule (§29) — applies to genuinely-new frozen components
For a genuinely-new component whose rules/thresholds are frozen here for the first time (e.g. the
skill-semantics matcher), the real-corpus prospective check is run ONCE after freezing, and NO further
selection occurs afterward. Any additional real-corpus run must be documented with its reason in
REPRODUCTION_LOG.md. For components that already touched the corpus in Stage-1/2 (the composite, its
weights, calibration), the real-corpus numbers are reported as descriptive secondary transfer results with
wide CIs — never as a clean held-out test.

## Reporting
Report: selected model, selection protocol, validation (synthetic + inner-CV) results, untouched outer-test
results, all baselines, significance + CIs, and ALL negative/parity findings. Numbers stay verifier-gated
(`verify_paper_numbers.py`). If a challenger is not significantly better than the auditable incumbent, that
parity is the reported finding.
