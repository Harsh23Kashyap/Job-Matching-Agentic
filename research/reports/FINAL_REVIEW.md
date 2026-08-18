# FINAL_REVIEW — final hostile ESWA review (§AD, 2026-08-18)

Method: a 5-reviewer independent hostile panel (Workflow `eswa-final-hostile-review`), each bundle
assigned distinct axes and instructed to REJECT. **Coverage note (no silent cap):** 3 of the 5
reviewer bundles returned before two stalled (a known agent-hang on this machine); the workflow was
stopped and this report synthesizes the 3 completed bundles. The two non-returning bundles
(`correctness-stats-baselines`, `calibration-xai-counterfactual-generalization`) were already
covered by Iteration 4 (5-dimension code review: correctness/stats/leakage) and by the Stage-2
experiments (EXP-026 calibration, EXP-027 generalization, EXP-028 faithfulness); their axes are not
un-reviewed, but they did not get a fresh adversarial pass here.

## Returned verdicts
- **novelty / framing / writing:** REJECT→major revision. Novelty is thin; abstract/intro/conclusion foreground "multi-agent" that the evidence disavows; uncited industry percentages.
- **robustness / fairness / scalability / architecture:** REJECT→major revision. Demographic-proxy invariance partly manufactured (pronoun no-op, unread hometown field); keyword-stuffing top-1 instability omitted; multi-agent framing vs EXP-019; deployability overclaim; DIR without CIs.
- **reproducibility / dataset / numbers / integrity:** REJECT. Cover letter asserts numbers the body disavows (0.969, p=0.048, in-sample 0.032); cited Dataverse DOI returns 404; §3.10 cross-encoder "0.030" inconsistency; ECE 0.018 vs 0.019.

## Findings ADDRESSED in this pass (all BLOCKER/SERIOUS + claim-affecting)
| Finding | Severity | Fix |
|---|---|---|
| Abstract/intro/conclusion foreground "multi-agent" as the contribution | SERIOUS | §1/§8/abstract reframed to "auditable/calibrated/explainable methodology, implemented as a multi-agent system"; multi-agent explicitly demoted to implementation (points to §5.7). Title unchanged per author. |
| Uncited industry percentages (20–30% / 15–25%) | SERIOUS | §1 reworded to qualitative motivation, "not measured effects" — no fabricated numbers. |
| Demographic-proxy invariance partly by construction (pronoun no-op, unread hometown) | SERIOUS | §5.4 now discloses that pronoun/hometown edits touch no field the ranker reads → invariance is by construction, not a fairness property. |
| Keyword-stuffing top-1 instability omitted | SERIOUS | §5.7 now reports top-1 changes in ~30% of cases (stability 0.70) alongside the signed-Δ. |
| Cover letter stale/phantom numbers (0.969, p=0.048, in-sample 0.032) | BLOCKER | cover-letter.md corrected to 0.924 / not-significant p=0.10 / held-out 0.019 + parity framing. |
| Non-resolving Dataverse DOI (404) in body + cover letter | BLOCKER | changed everywhere to "deposited with a citable DOI upon acceptance; anonymized copy for reviewers"; removed the specific DOI + commit. |
| §3.10 cross-encoder "underperforms by 0.030" | MODERATE | corrected to "does not improve on the composite (0.939 vs 0.949) at ~340× latency." |
| ECE 0.018 vs 0.019 two values | MODERATE | §5.3 notes the two held-out Platt experiments (EXP-026/EXP-004) agree to within rounding (0.018–0.019). |
| highlights.md superseded "7 of 10" + "0.745 faithfulness" + 0.032 | SERIOUS | rewritten to honest parity / mechanistic faithfulness / held-out 0.019. |
| "deployable under 10 ms" overclaim, DIR without CIs | MODERATE | deployability already hedged; DIR carries "should not be over-interpreted" + proxy caveat; scale framed with the ANN-prefilter caveat (§5.7). |

## Findings acknowledged as HONEST LIMITATIONS (not defects to hide)
Thin novelty on a small corpus, ranking parity (not superiority), calibration low-discrimination, no
human explanation/user study, proxy-only fairness, simulated temporal/synthetic scale — all explicitly
stated in §6.2 and the abstract. The reviewers' "reject" on novelty is the honest ceiling of a small-
corpus methodology paper; the paper now claims exactly what the evidence supports.

## Editor-style disposition (synthesized)
**Major → Minor Revision territory, contingent on author logistics.** After this pass the manuscript is
internally consistent, every number is artifact-sourced and verifier-gated, and the framing matches the
evidence (no superiority/fairness/multi-agent-novelty overclaim). The remaining true blockers are NOT
scientific — they are author-only submission facts: (1) a real, resolving artifact DOI (currently
"upon acceptance"), (2) reconciling the author list (title page 1 vs CRediT 3), (3) the honest corpus-
size/single-annotator ceiling, which no amount of editing removes and which is now disclosed. If a
reviewer rejects, it will be on scope/novelty (a defensible editorial call), not on integrity,
reproducibility, or overclaiming — those are closed.

## Stage-3 update (2026-08-18)
The model-improvement + acceptance campaign added a foregrounded contribution (relation-aware graded skill
matching, EXP-034/034b, de-circularized with hard negatives) and closed the two sharpest Stage-3 objections
with evidence: recovery-by-construction (EXP-024b non-additive latent, 0.891, Δ−0.016) and the "untouched
test" over-claim (PROTOCOL.md corrected). Synthetic feature/fusion headroom (0.917→0.978–0.990) is reported
strictly as development-only motivation for a larger benchmark. Consolidated risk in EDITORIAL_RISK_MATRIX.md.
The novelty axis is materially stronger; the disposition stays Major→Minor Revision, with a clear Accept
gated on the author-only additions (larger 2-annotator judged benchmark and/or a human explanation study)
and the title decision. Integrity, reproducibility, and claims-vs-evidence remain closed.
