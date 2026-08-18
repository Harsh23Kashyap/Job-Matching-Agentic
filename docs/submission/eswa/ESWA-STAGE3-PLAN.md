# JobMatch → ESWA — STAGE 3: MODEL-IMPROVEMENT + ACCEPTANCE CAMPAIGN
> Saved 2026-08-18. Continues ESWA-EXECUTION-PLAN.md (47 phases DONE) + ESWA-STAGE2-PLAN.md.
> Governing rule (unchanged): MAXIMUM SCIENTIFIC CREDIBILITY, not maximum metric. No test-set tuning,
> no post-hoc seed selection, no invented/synthetic-as-human labels, no favorable-only reporting, no
> metric-swapping. This stage improves the METHODOLOGY through legitimate experimentation, then reframes
> and re-reviews. Prioritized by acceptance-impact-per-effort, grounded in the constraints below.

## Reality constraints (verified 2026-08-18) — these shape everything
- Real human corpus is TINY + FIXED + SINGLE-ANNOTATOR: 30 resumes × 15 jobs, 47 graded labels, 74-skill
  vocab, **no preferred-skills field (0/15 jobs)**. More human labels not obtainable this campaign.
- Ranking is already at statistically-indistinguishable PARITY (all CIs overlap, nothing survives Holm).
- Offline/CPU-only. Cached embedders: **all-MiniLM-L6-v2 (384d) + JobBERT only** (new downloads may fail).
- No external LLM API (headless `claude -p` only). No git.

## Strategic call (the honest acceptance path)
On a 30×15/47 single-annotator corpus at parity, **methodology gains will show mainly on the SYNTHETIC
corpus (controlled, known ground truth)**; the real corpus stays the UNTOUCHED test and will most likely
remain parity. So acceptance comes from: (1) genuinely-new, defensible methodology developed+selected on
synthetic under nested CV (skill-semantics; required/preferred; monotonic fusion); (2) real corpus reported
honestly as untouched test; (3) reframing the contribution around the COMBINATION + the new skill-semantics
layer; (4) EDITORIAL_RISK_MATRIX + hostile review. **Backfire risk to avoid at all costs: chasing a higher
real-corpus nDCG = test-set tuning = forbidden.** (Pending: Kiro 4-model panel critique — fold in when it lands.)

## PRIORITIES (by acceptance impact)

### Tier 1 — genuine new methodology (develop on synthetic; real corpus = untouched test)
- **P1 · Skill-semantics pipeline (§8).** Highest-value NEW contribution. Distinguish EXACT / RELATED /
  SEMANTICALLY-SIMILAR / UNRELATED; graded (not full) credit for related; synonym+abbrev+misspelling
  normalization on top of `skill_catalog.py`/`skill_taxonomy.py`. Build a CONTROLLED skill-matching
  benchmark and report precision/recall/F1 per match class. EXP-034.
- **P2 · Required-vs-preferred + derived skill features (§9/§4).** New job representation: required-coverage,
  preferred-coverage, skill-deficit, skill-importance (idf-like). **Validate on SYNTHETIC only** (real has
  no preferred field — state as a limitation). EXP-035.
- **P3 · Fusion upgrade under nested CV (§4/§7).** Extend EXP-025 with the derived features + monotonic GBM /
  shallow MLP / elastic-net, selected by nested CV; keep the 6-channel decomposition as the explanation
  layer even if a learned model ranks. Report win OR defensible parity (negative result is fine). EXP-036.

### Tier 2 — evaluation rigor (raises reviewer trust)
- **P4 · Nested-CV protocol + freeze the 47-label test (§1/§29).** DO FIRST. Document dev/val/test discipline
  BEFORE any optimization; the 47 labels are the untouched final test; selection happens on synthetic +
  inner CV only. Write `research/PROTOCOL.md`. (This directly answers the "test influence" reviewer concern.)
- **P5 · Two-stage retrieval + K sweep (§6).** retrieve→rerank at K∈{10,25,50,100,250} on the synthetic pool;
  recall/nDCG/latency trade-off. EXP-037.
- **P6 · Embedding comparison (§3B).** Bounded to cached MiniLM + JobBERT + lexical; ATTEMPT to add
  mpnet/bge-small if network allows, else report the offline limit honestly. EXP-038.
- **P7 · Hard-negative mining expansion (§10).** same-title/wrong-skills, same-skills/wrong-seniority,
  high-semantic/wrong-experience — on synthetic; report separately. EXP-039.

### Tier 3 — deepen existing baselines
- **P8 · Counterfactual 50→100+ with monotonicity checks (§16).** Extend EXP-005; test expected-direction
  monotonicity per channel; don't assume every edit must move final rank. EXP-040.
- **P9 · Calibration campaign + adaptive ECE + beta (§13).** Extend EXP-026 (add beta calibration, adaptive
  ECE, calibration-by-position). EXP-041.
- **P10 · Explanation metrics (§15) + human-study ATTEMPT.** Automated attribution-correctness/completeness/
  contradiction/counterfactual-consistency; small human study only if participants feasible — otherwise
  document as the key remaining gap. EXP-042.
- **P11 · Scalability to 100K/1M (§20).** Extend EXP-031 via replication; p50/p95/p99/throughput/memory.

### Tier 4 — acceptance packaging (after evidence frozen)
- **P12 · Restructure manuscript around RQ1–8 (§23), strengthen novelty via the COMBINATION (§24), related-work
  audit (§25), claim classification SUPPORTED/LIMITED/DESIGN/FUTURE (§26), title decision (§27).**
- **P13 · EDITORIAL_RISK_MATRIX.md (§28):** 3 hostile reviewer sims (RecSys / XAI+calibration / applied-ESWA) →
  CRITICISM × PROBABILITY × SEVERITY × EVIDENCE × FIX × IMPACT; prioritize HIGH×HIGH.
- **P14 · Final deliverable bundle (§30):** best selected model + protocol + val + untouched-test + baselines +
  significance + CIs + calibration + explanation + counterfactual + robustness + generalization + scalability +
  architecture + NEGATIVE findings + limitations + final ESWA recommendation. Then final hostile review.

## SKIP / low-value here (theater given the constraints — justify in the writeup)
- §11/§12 parser gold-eval + uncertainty propagation: the LLM is OFF the ranking hot path; a full parser
  study is high-effort, low acceptance-impact for THIS paper. Do a LIGHT parser-robustness note only.
- §19 real temporal: no real timestamps → SIMULATION only (already EXP-030), keep labeled as such.
- §5 recruitment-specific transformer / large cross-encoder training: bounded by offline/CPU; report the
  existing cross-encoder + JobBERT honestly, don't overreach.

## Protocol gate (§29) — FROZEN before any test evaluation
Development + all model selection use: (a) the synthetic corpus, and (b) INNER cross-validation on the real
corpus. The 47 real labels are the UNTOUCHED outer test, evaluated ONCE per final candidate. Selection
criteria fixed in `research/PROTOCOL.md` before results are seen. Nothing (features, weights, calibration,
thresholds, embedding, preprocessing) is chosen on the outer test.

## Status control
New experiments EXP-034..042 in EXPERIMENT_REGISTRY.yaml; decisions in RESEARCH_DECISIONS (RD-014+);
REVIEW_LOG Iteration 6+ for the Stage-3 hostile review; all numbers stay verifier-gated (§AB).

## STAGE-3 COMPLETION STATUS (updated 2026-08-18)
- **P1 skill-semantics — DONE:** EXP-034 (graded 4-class matcher, macro-F1 0.81) + EXP-034b (de-circularized objective benchmark: orthographic/synonym exact-recall 1.0, 7/8 hard negatives distinct; misspelling brittleness + Angular/AngularJS false-merge reported honestly).
- **P2/P3 derived features + fusion — DONE + CORRECTED (EXP-044 by-construction audit):** on synthetic, the DEFENSIBLE finding is base6 NONLINEAR fusion (0.917→0.947/0.961, CIs exclude 0); the +derived jump to ~0.99 is LARGELY BY CONSTRUCTION (required-coverage corr 1.000 with the latent generator) and is NOT claimed as a methodology gain. Learned LINEAR fusion does not beat the hand weights. Framed as development-only headroom.
- **P4 protocol — DONE + integrity-corrected:** PROTOCOL.md (real corpus = secondary transfer check, NOT untouched test).
- **By-construction control — DONE:** EXP-024b non-additive latent recovery 0.891 (Δ−0.016 vs additive) — refutes the objection.
- **P12 reframe — DONE (body):** abstract/§1/§5.7/§6/§8 foreground auditable relation-aware skill matching + honest parity/instrument framing + synthetic headroom; multi-agent demoted to implementation. TITLE change remains an AUTHOR decision (kept per prior instruction; flagged in EDITORIAL_RISK_MATRIX #9).
- **P13 EDITORIAL_RISK_MATRIX.md — DONE** (14 criticisms × prob × sev × evidence × fix × impact; HIGH×HIGH prioritized).
- **Manuscript — 41pp clean, 0 undefined refs, verifier passes.** REVIEW_LOG Iterations 6–7.
- **LEFT:** P14 final-bundle refresh (fold Stage-3 into FINAL_* deliverables); optional deepen (counterfactual→100 with monotonicity, adaptive-ECE/beta, scalability→1M) — panel-demoted, low acceptance-impact; author-only (larger 2-annotator benchmark, human explanation study, real DOI, title, author list).
- **SKIPPED as theater/scope-creep (panel-endorsed):** more fusion search on the real 30-query corpus, preferred-skill scoring as a real contribution, hard-negative-mining-as-training, parser gold study + uncertainty, K-sweep on 15 jobs, additional reviewer sims, constrained-LLM realization, more synthetic scale as a headline.
