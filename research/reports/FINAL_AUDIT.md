# FINAL_AUDIT — JobMatch → ESWA (2026-08-18)

Master §AH final report. Companions: FINAL_NUMERICAL_AUDIT, FINAL_REPRODUCTION, FINAL_DOCUMENT_AUDIT,
FINAL_REVIEW; evidence in EXPERIMENT_REGISTRY.yaml (EXP-001..033), REVIEW_LOG.md (Iter 0–5),
NUMBERS_PASS_FINAL.md. Governing rule honored throughout: **maximum scientific credibility, not maximum
metric** — where a stronger-looking number and a more defensible one conflicted, the defensible one was chosen.

## 1. Phases complete / blocked
- 47-phase plan: see `docs/submission/eswa/ESWA-EXECUTION-PLAN.md` completion table. Science/code/paper-
  evidence complete; open items are author-only logistics (author list, ORCID/DOI, README polish, optional
  figure/related-work polish). No git commits (repo constraint, RD-009).

## 2. Experiments run / rejected / negative (all registered)
- Run & reproduced: EXP-001..033. Genuine NEGATIVE/parity results kept (not hidden): ranking parity (no
  method beats composite after Holm), recourse-null counterfactual, near-degenerate Platt calibration,
  JobBERT < MiniLM, temperature-calibration failure, modest explanation comprehensiveness, formatting/
  misspelling non-robustness, no monolith-vs-agent perf benefit.
- Rejected as non-defensible: the phantom best-single 0.969/R@5=1.000, in-sample ECE 0.032 as headline,
  in-sample fusion 0.968 as a result, the 15-job "production-scale" latency claim, the 3-job-pool
  generalization numbers (0.969/0.958) — all replaced by defensible values.

## 3. Datasets
- Real (primary): 30 resumes × 15 jobs, 47 human-labeled pairs (single author-annotator; LLM-assisted
  450-label second pass κ=0.69 as corroboration, disclosed non-human).
- Synthetic (controlled): EXP-023, 500 resumes × 75 jobs, transparent latent ground truth (never presented
  as human judgments) — for structure recovery, stress, and scale only.

## 4. Train/val/test
- Entity-level held-out throughout: candidate-unseen, job-unseen (STRICT), both-unseen; all leakage-checked
  programmatically; per-resume aggregation before bootstrap.

## 5. Baselines
- BM25 0.902, TF-IDF 0.905, semantic 0.878, multimodal 0.924, RRF 0.913, LambdaMART 0.963, JobBERT 0.864,
  cross-encoder 0.939 — identical eval set; CareerBERT unavailable → JobBERT (RD-007, disclosed).

## 6. Ranking result
- Composite nDCG@5 0.949; all methods' CIs overlap; **no method is statistically superior (parity)**.

## 7. Significance
- Composite vs semantic Δ+0.071, two-sided p=0.10, CI[-0.014,+0.167], fails Holm (EXP-022). No manufactured
  significance.

## 8. Calibration
- Defined target P(y=1|s); held-out. Platt lowest ECE 0.018 but near-degenerate (BSS 0.007, AUC 0.76);
  isotonic ECE 0.024 preserves discrimination (BSS 0.64, AUC 0.95); temperature fails. Reported as a trade-off.

## 9. Explanation
- Exact additive decomposition (by construction); mechanistic ranking-level faithfulness (top-attributed
  channel displaces top-1 more than least/random: 0.133 vs 0/0.033); skill-add attribution strictly increases
  (mean Δ +0.186). No human study (stated).

## 10. Counterfactual
- 50-pair: 25 recourse (rank-null, explained), 25 demographic-proxy (9 flagged, top-1 stable 24/25).

## 11. Fairness
- Demographic-proxy SENSITIVITY only (DIR 0.82/0.75), explicitly not an audit.

## 12. Robustness
- Synonym-invariant, gaming-resistant (stuffing lowers score); NOT invariant to formatting/misspelling
  (|Δ|≈0.12) — reported as a limitation.

## 13. Generalization
- Candidate/job/both-unseen all ≈0.93 (pool=15, commensurable), overlapping composite 0.949; zero leakage.

## 14. Structure recovery (synthetic)
- Recovery ratio 0.907; per-channel decomposition validity (skills↔required 0.996, comp↔comp 0.985); degrades
  on hard/adversarial.

## 15. Scalability / incremental
- ~0.05 ms/pair (linear); 0.8 ms @15 → 517 ms @10k jobs (warm, single-thread); incremental score+merge
  11–767× cheaper than full re-rank. Production ANN prefilter noted as not-implemented.

## 16. Failure injection
- 9/9 no-crash + deterministic; found & FIXED a NaN-embedding→perfect-score gap (embedding sanitization +
  regression test).

## 17. Architecture
- Failure isolation real; no measured monolith-vs-agent benefit → multi-agent demoted to implementation detail.

## 18. Tests
- test_scientific_claims.py 9/9 (weight-sum, decomposition, calibration-monotonic, leakage, NaN-guard).

## 19. Reproduction
- reproduce_all.sh covers EXP-011..033 + table-gen + fig-regen + numeric verifier; deps pinned; determinism
  byte-identical; PDF compiles 39pp/0 errors.

## 20. Numerical discrepancies
- All headline numbers auto-generated from artifacts + verifier-gated; semantic 0.878 / RRF 0.913 reconciled;
  corpus stats corrected to true 2.97/2.13/74. Zero forbidden numbers in the rendered PDF.

## 21. Manuscript inconsistencies fixed
- False "two independent annotators"; B11 weight-tuning (×3); B12 unjudged-pairs reframe; "trustworthy"→
  "calibrated" (body); fig4 in-sample→held-out; tab:progression/latency template mismatch.

## 22. Remaining weaknesses (honest)
- Tiny corpus / single annotator / parity not superiority; calibration low-discrimination; no human XAI or
  user study; formatting/misspelling non-robustness; temporal & scale evidence is simulated/synthetic;
  fairness is proxy-only.

## 23. Integrity / anonymity
- Author home-path + real handles scrubbed; main manuscript anonymized + separate title page; NVIDIA grant
  kept (title page); DOI = "deposit on acceptance."

## 24. Author-only opens
- Reconcile author list (title page 1 vs CRediT 3); ORCID/emails via Editorial Manager; README refresh;
  optional non-fig4 diagram regen + related-work expansion.

## 25. Reviewer simulations
- Iter 3 Kiro 4-model panel; Iter 4 5-dimension code review (37 findings fixed); Iter 5 5-reviewer ESWA
  hostile panel → FINAL_REVIEW.md.

## 26. Final ESWA recommendation (evidence-based)
- The EVIDENCE now supports the reframed claims (auditable/calibrated/explainable methodology; honest
  parity; reproducible artifact). Realistic venue outlook: **Major→Minor Revision territory** — defensible
  and internally consistent, with the honest ceiling being corpus size / single-annotator / no user study
  (disclosed, not hidden). See FINAL_REVIEW.md for the panel's decision and any surviving must-fix items.

## STAGE-3 ADDENDUM (model-improvement + acceptance campaign, 2026-08-18)
- **New methodology:** relation-aware graded skill matcher (EXP-034/034b) — de-circularized objective
  benchmark: orthographic/synonym variants → exact (recall 1.0), 7/8 hard negatives kept distinct
  (Angular/AngularJS over-merge flagged), misspelling brittleness disclosed. This is the paper's foregrounded
  contribution.
- **Feature/fusion headroom (synthetic, development-only):** derived skill-coverage features + monotonic/
  LambdaMART fusion beat the fixed composite on the high-power synthetic corpus (0.917→0.978–0.990; gain
  survives dropping the synthetic-only preferred feature) — reported as motivation for a larger judged
  benchmark, NOT a real-world gain.
- **Objections closed with evidence:** by-construction recovery (EXP-024b non-additive latent → 0.891,
  Δ−0.016); instrument-parity (reframed §5.1/§6.2); "untouched test" over-claim (PROTOCOL.md corrected to a
  secondary transfer check); skill-benchmark circularity (EXP-034b, embedding tier marked exploratory).
- **Deliverables:** EDITORIAL_RISK_MATRIX.md (14 criticisms, HIGH×HIGH prioritized); manuscript reframed
  (abstract/§1/§5.7/§6/§8), 41pp clean, verifier passes; REVIEW_LOG Iterations 6–7.
- **Reviews:** Stage-3 Kiro plan panel (4/4, unanimous reframe) + prior 5-reviewer panel; the 10-model paper
  panel stalled twice (Kiro gateway degraded) and was not relied upon.
- **Net effect on outlook:** the reframe + the new skill-matching contribution + closing the two sharp
  Opus-5 objections strengthen the case within the same **Major→Minor Revision** band; a clear Accept still
  requires the author-only additions (larger 2-annotator benchmark and/or human explanation study).
