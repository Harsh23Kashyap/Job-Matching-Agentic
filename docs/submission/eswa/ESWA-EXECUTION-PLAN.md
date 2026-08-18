# JobMatch → ESWA: End-to-End Pre-Submission Execution Plan

> Saved 2026-08-17. Source: user-authored master plan for the ESWA revision.
> This is the **authoritative execution checklist** (47 phases + 10-stage order).
> Companion docs: `../../../HANDOFF.md` (state), `strategy/ESWA-FIT-ASSESSMENT.md`,
> `strategy/SUBMISSION-PLAN.md`. Audit findings against this plan live alongside it.
>
> Guiding principle: **do not make the paper *look* better while leaving it
> scientifically unchanged.** Every experiment must answer a research question;
> every number must survive a hostile reviewer checking exactly how it was produced.
> No manufactured results, no synthetic-as-human labels, no tuning on test, no
> hidden failed runs, no calling a 10-pair probe a fairness validation.

The work pipeline:

> Code → data → evaluation protocol → experiments → statistical validation →
> diagrams → manuscript → supplementary/artifact → submission package → final audit

---

## Phase 0 — Freeze the current state

### 0.1 Create a clean research branch
- Create branch such as `eswa-final-evaluation`.
- Tag the current manuscript/code state: `pre-eswa-final`.
- Record: current commit SHA, current PDF SHA/hash, dataset version, Python/Node
  versions, model versions, embedding model version, LLM/model configuration, random seeds.

### 0.2 Create a research manifest
```
research/
  MANIFEST.yaml
  configs/
  datasets/
  splits/
  experiments/
  results/
  figures/
  tables/
  logs/
```
`MANIFEST.yaml`: dataset_version, code_commit, python_version, node_version,
embedding_model, llm_model, random_seed, hardware, timestamp.

**Acceptance:** anyone can identify exactly which code/data generated the final tables.

---

## Phase 1 — Audit the current code before changing anything
Establish what the current implementation *actually does* before adding experiments.

### 1.1 Ranking pipeline audit
Trace: raw resume → parser → normalization → candidate representation → job parser →
job representation → matching → six channels → weighted score → ranking.
Verify every step against the paper's equations.

Verify specifically: semantic score, skill overlap, title, experience, compensation,
remote; weight normalization; score range; missing-value handling; tie-breaking;
ranking direction; top-K selection.

**Critical:** one deterministic `score_pair(candidate, job) -> ScoreBreakdown` returning
`{semantic, skill, title, experience, compensation, remote, weighted_components, composite}`.
The explainability claim depends on this decomposition.

---

## Phase 2 — Build a proper evaluation dataset (highest-priority research task)
Current: 30 resumes, 15 jobs, 47 labelled pairs — too sparse for the strongest claims.

- **2.1 Preserve** the existing dataset as `v1_original_47_labels` (never overwrite).
- **2.2 Expand to complete 30×15 = 450 pairs.** Columns: resume_id, job_id, relevance,
  annotator_1, annotator_2, final_label. Keep 4-point ordinal scale
  (0 irrelevant, 1 partial, 2 relevant, 3 strong).
- **2.3 Two independent annotators.** Independent labels, hidden from each other, record
  disagreement, documented reconciliation. Compute Cohen's/weighted κ, raw agreement,
  confusion matrix, agreement by class. **Do not manufacture synthetic labels for the
  final scientific evaluation** — human-labelled data stays the primary ranking benchmark.

---

## Phase 3 — Synthetic data generation (used correctly)
- **3.1** ~500 synthetic resumes: varied experience/skill/job-family, sparse/dense,
  career changers, unusual titles, overlapping skills. Deterministic generator.
- **3.2** 250–500 synthetic jobs: seniority, skill reqs (required vs preferred), salary
  ranges, remote/hybrid/onsite, missing salary/remote, sparse descriptions.
- **3.3 Do NOT use synthetic data as the headline benchmark.** Use for stress testing:
  unseen skills, noisy text, missing/contradictory fields, extreme values, long/short
  resumes, keyword stuffing, parser errors, score perturbations.

---

## Phase 4 — Proper train/validation/test splits (critical)
Current learned fusion is fit on the pairs it is evaluated against (acknowledged
overfitting risk). Fix it.

- **4.1 Split by entity, not random pair.** e.g. TRAIN 20 resumes/10 jobs, VAL 5/2–3,
  TEST 5/2–3, or multiple folds. The same resume must not appear in train and test if
  demonstrating candidate generalization. Run a second experiment with jobs held out.
- **4.2 Report two generalization settings:** candidate generalization (unseen resumes),
  job generalization (unseen jobs), optionally both unseen.

---

## Phase 5 — Re-run the fixed composite scorer
Once the dataset is clean: recompute six components; freeze the six weights; do not tune
on test; evaluate test once. Report nDCG@5, nDCG@10, MRR, Recall@5, Recall@10, P@5
(add complementary metrics beyond the current nDCG@5 focus).

---

## Phase 6 — Add serious ranking baselines
Required (verify same preprocessing/data/test set): BM25, TF-IDF, Sentence-BERT,
Hybrid semantic+skill, Cross-encoder (train only on training data).
Add:
- **Baseline 6 — Learning-to-rank** (LambdaMART / LightGBM Ranker) on the six features.
  Critical comparison: proposed method is fundamentally feature fusion.
- **Baseline 7 — modern recruitment model** (CareerBERT if feasible).
- **Baseline 8 — logistic regression** (learned linear fusion vs manual linear fusion).

---

## Phase 7 — Weight-selection experiment
Current weights: semantic 0.28, skill 0.27, title 0.10, experience 0.15, compensation
0.10, remote 0.10. Don't report one optimization. Run **bootstrap weight stability**
(e.g. 1,000 iterations: sample train, optimize, record). Report mean ± CI per weight.
Answer: are 0.28/0.27 stable, or artifacts of 47 labels?

---

## Phase 8 — Full ablation study
Individual channels; incremental combinations (Semantic → +Skill → +Experience → +Title …);
and remove-one-channel (All, All−semantic, All−skill, …). Remove-one is most informative.

---

## Phase 9 — Parser evaluation (currently under-tested)
LLM is used for parsing/explanation, not the hot ranking path. Build a **gold structured
dataset** (skills, experience, education, title, salary, remote). Measure skill
precision/recall/F1, experience/title/compensation/remote extraction accuracy.

---

## Phase 10 — Parser-error propagation experiment
From a correct profile, inject controlled errors: skill deletion (remove Python), skill
insertion (add Kubernetes), experience corruption (5→2 yrs), salary corruption, remote
corruption. Measure Δ score, Δ rank, Δ top-5 membership, Δ confidence, Δ explanation.

---

## Phase 11 — Adversarial resume experiments
- **11.1** Keyword stuffing (add many skills without changing real experience) → measure rank change.
- **11.2** Irrelevant skill injection → system shouldn't dramatically reward.
- **11.3** Skill synonym attack (ML↔Machine Learning, JS↔JavaScript, Postgres↔PostgreSQL, K8s↔Kubernetes).
- **11.4** Formatting attack (case, punctuation, repeats, buried/table/header skills).

---

## Phase 12 — Cold-start experiment
Cold candidate (1/3 skills, no experience, sparse); cold job (1 required skill, sparse,
no salary/remote); completely unseen skill. Report ranking quality, parsing accuracy,
failure rate, fallback behaviour.

---

## Phase 13 — Calibration redesign (one of the most important fixes)
- **Define the probability** explicitly: p_ij = P(y_ij = 1 | s_ij) or chosen target.
  Remove ambiguity between "pair relevance" vs "top-ranked correctness."
- **Train calibration separately:** train ranking → validation calibration (Platt) →
  untouched test. Never fit Platt on the test set.
- **Compare methods:** raw, Platt, isotonic, (temperature). Report ECE, MCE, Brier,
  reliability diagram, calibration curve, CIs.

---

## Phase 14 — Calibration subgroup analysis
Calibration separately for high/partial/irrelevant relevance, high/low semantic
similarity, experienced/inexperienced. Is 80% confidence actually 80% across groups?

---

## Phase 15 — Explanation evaluation
Keep faithfulness/specificity/consistency; expand. Compare Rule-based vs LLM-template vs
LLM-generated. Add explanation **correctness** (does "strong skill match" match a high
skill score?) and **completeness** (does it mention the dominant factors?).

---

## Phase 16 — Explanation-guided counterfactual experiment
Distinct from the demographic probe. Controlled edits (e.g. add TensorFlow) → predict
skill component ↑ → verify skill ↑, composite ↑, rank consistent, explanation changes
accordingly. Across **30–50 controlled edits**, not just 10.

---

## Phase 17 — Fairness evaluation
Don't call the current 10-pair probe a fairness evaluation (paper itself calls it an
engineering check). Create paired counterfactual profiles identical except name/pronoun/
hometown/email-domain; ≥50 pairs (100+ preferred). Measure rank/score/top-K/confidence/
explanation differences. Add group-level metrics (selection rate, TPR, FPR, equal
opportunity, DIR) **only if demographic data is legitimately available**; otherwise keep
it explicitly as a **proxy sensitivity analysis** (don't invent demographic labels).

---

## Phase 18 — Temporal robustness
Older jobs → train, recent jobs → test (or simulate drift). Test new technologies,
changing salary/titles/remote policies. Measure nDCG degradation, ECE degradation,
skill-normalization failures, rank instability.

---

## Phase 19 — Scalability benchmark
Current latency is on a tiny job pool — don't make <10 ms a production-scale claim.
Benchmark jobs {15, 100, 1K, 10K, 100K, 1M} and candidates {1K, 10K, 100K, 1M}. Measure
p50/p95/p99, throughput, memory, CPU, indexing/retrieval/scoring/explanation/calibration time.

---

## Phase 20 — Incremental update benchmark
One/10/100 resumes or jobs change. Measure re-indexing time, cache invalidation, affected
entities, ranking recomputation, memory overhead. Validates the snapshot/index architecture.

---

## Phase 21 — Multi-agent architecture validation
The ranking path is deterministic; the LLM is on parsing/explanation. Ablate Architecture
A (monolithic) vs B (three separated components). Compare latency, failure isolation,
privacy boundary, maintainability, testability, deployment independence. If no measurable
benefit, stop overselling multi-agent.

---

## Phase 22 — Failure-injection testing
Inject: parser failure, embedding failure, malformed job, missing skill vocabulary,
missing salary/remote, LLM timeout, LLM malformed output, DB unavailable, stale index,
duplicate candidate/job. Define expected behaviour (e.g. LLM timeout → fallback parser →
ranking continues → confidence marked → no crash).

---

## Phase 23 — Security/privacy audit (recruitment domain)
PII handling, resume storage, email handling, candidate/job isolation, logging, LLM API
transmission, secrets, access controls, data retention, artifact contains no real PII.
Run a repo secret scan + PII scan on dataset, logs, fixtures, examples, screenshots, JSON, README.

---

## Phase 24 — Test-suite cleanup
Advertised 302 Python + 39 Node = 341 tests. Categorize (unit/integration/ranking/
calibration/explanation/API/frontend/regression). Add explicit tests per scientific claim:
`test_weight_sum_equals_one`, `test_score_decomposition_sums_to_composite`,
`test_calibration_is_monotonic`, `test_counterfactual_skill_addition_increases_skill_component`,
`test_missing_salary_does_not_crash`, `test_remote_preference_does_not_change_when_unrelated_field_changes`.

---

## Phase 25 — Reproducibility test (brutal)
Fresh machine/container: `git clone` → `pip install` → `npm install` →
`python reproduce_all.py` produces `results/`, `figures/`, `tables/`, `metrics.json` with
no manual intervention. Compare generated numbers against the manuscript.

---

## Phase 26 — Single experiment runner
`python experiments/run_all.py` runs: 01_dataset_validation, 02_baselines, 03_composite,
04_ablation, 05_weight_stability, 06_calibration, 07_explanations, 08_counterfactual,
09_fairness, 10_parser_robustness, 11_adversarial, 12_cold_start, 13_scalability,
14_temporal, 15_statistics. Outputs ranking.csv, calibration.csv, explanations.csv,
counterfactual.csv, fairness.csv, latency.csv, statistical_tests.csv. **Single source of truth.**

---

## Phase 27 — Statistical analysis
Per headline comparison: mean, variance/CI, sample size, effect size, statistical test,
p-value, multiple-comparison correction where appropriate. Revisit Δ=+0.071, p=0.048 — a
borderline p-value must not carry more weight than the underlying evidence.

---

## Phase 28 — Auto-generate tables
Stop typing numbers into LaTeX. Generate `table*.tex` from `results/*.csv`. Same for
figures. Eliminates inconsistent-number problems (e.g. old cross-encoder mismatch).

---

## Phase 29 — Numerical consistency checker
`python verify_paper_numbers.py` checks every headline number against a manifest
(composite_ndcg, best_single_ndcg, cross_encoder_ndcg, faithfulness_rule/llm, ece_before/
after, brier, counterfactual_flagged, …) vs manuscript text.

---

## Phase 30 — Update diagrams (AFTER experiments)
- **Fig 1/2** portals: confidence definition matches new calibration; decomposition
  matches six channels; no unsupported "trustworthy" implication.
- **Fig 3** conceptual architecture: Candidate Agent → Candidate Snapshot →(Matchmaking)←
  Job Snapshot → Ranking → Explanation → Calibration. Don't overstate autonomy.
- **Fig 4** multi-agent: distinguish HOT PATH (deterministic scoring) vs COLD PATH (LLM
  parse/explain).
- **Fig 5/6** components: inputs, outputs, ownership, privacy/failure boundaries.
- **Fig 7** ranking pipeline: actual equations.
- **Fig 8** calibration: raw score → calibration model → calibrated probability → display
  (don't imply calibration changes ranking unless implemented).
- **Fig 9** end-to-end: ingestion→parsing→normalization→indexing→retrieval→ranking→
  explanation→calibration→user.
- **Fig 10** data plane: store, indexes, event bus, cache, ranking/explanation service
  (only implemented components).
- **Fig 11** explanation decomposition: Composite ├ Semantic ├ Skills ├ Title ├ Experience
  ├ Compensation └ Remote (actual contributions).
- **Fig 12** counterfactual: one concrete before/after.
- **Fig 13** calibration curve: regenerate from final experiment (no hand-edited chart).

---

## Phase 31 — Rewrite Results around research questions
RQ1 ranking quality; RQ2 does decomposition explain faithfully; RQ3 is confidence
calibrated; RQ4 sensitivity to controlled changes; RQ5 generalization to unseen
candidates/jobs; RQ6 degradation under parsing/noise/adversarial; RQ7 computational cost.

---

## Phase 32 — Rewrite contribution claims
1. Auditable six-channel ranking decomposition. 2. Calibrated pair-level relevance
confidence. 3. Faithfulness + counterfactual evaluation protocol. 4. Reproducible
recruitment recommendation benchmark and implementation. Don't claim production-ready,
universally trustworthy, domain-agnostic-validated, or fairness-validated unless supported.

---

## Phase 33 — Rewrite title if necessary (decide after experiments)
If fairness stays limited, consider dropping "Trustworthy":
*An Explainable Multi-Agent Architecture for Job-Candidate Recommendation with Calibrated
Confidence*, or *Explainable and Calibrated Job-Candidate Recommendation with Auditable
Multi-Agent Architecture*. "Trustworthy" currently does more work than the evidence supports.

---

## Phase 34 — Rewrite Abstract LAST
After all experiments: update dataset size, exact test protocol, baseline results,
calibration, fairness, latency; remove unsupported claims; state actual generalization
setting and human annotation protocol. Every abstract number must exist in Results.

---

## Phase 35 — Rewrite Limitations (blunt)
Dataset size; judgment coverage; demographic limitations; no live deployment; no user
study; parser dependence; synthetic-data limitations; temporal drift; generalization;
calibration-set size; model/version dependence.

---

## Phase 36 — Update Related Work
Recommendation (neural ranking, two-tower retrieval, LTR); recruitment (CareerBERT, recent
job-matching); explainability (feature attribution, counterfactual, faithful explanations);
calibration (Platt, isotonic, modern); fairness (ranking fairness, recruitment AI fairness);
agents (multi-agent decision support, LLM recruitment). State what existing systems do NOT
combine — novelty lives there.

---

## Phase 37 — Update README
Installation; dataset; data schema; running the system; running evaluation; reproducing
tables/figures; running tests; configuration; model versions; hardware; expected results;
limitations; license.

---

## Phase 38 — Artifact reproducibility
Release configs/, data_schema/, evaluation/, scripts/, results/, figures/, tables/. Don't
necessarily release raw resume data; if 450 labels can't be public, release anonymized IDs,
derived features, label schema, evaluation scripts, hashes, synthetic reproduction dataset.

---

## Phase 39 — DOI / GitHub consistency
DOI resolves + points to exact artifact version; GitHub commit exists and contains the
experiments used; README works; dataset version matches; no uncommitted experiment code;
no missing config; no secrets; no author-identifying info if double-anonymous.

---

## Phase 40 — Final manuscript numerical audit
Spreadsheet: Claim | Source result | Manuscript location | Verified — for nDCG@5, best
single, cross-encoder, faithfulness, specificity, ECE, Brier, counterfactual, DIR, latency,
tests. Search the entire PDF for every number.

---

## Phase 41 — Cross-document consistency audit (mandatory)
Main PDF vs DOCX vs LaTeX vs README vs cover letter vs highlights vs GitHub vs DOI artifact.
No document should disagree.

---

## Phase 42 — Specific current package fixes (immediate, independent of new experiments)
- **Main manuscript:** remove every `PRE-SUBMISSION DRAFT` / internal draft language;
  verify anonymity, affiliations, references, every figure caption, every table.
- **Title page:** remove `ORCID: to be added` (real ORCID or remove field); check
  submission date, author order, corresponding author.
- **Cover letter:** remove fake reviewer placeholders (`[Reviewer 1 — …]`); don't claim
  real deployment / live user validation / fairness audit if none exists; abstract-level
  numbers must match final paper.
- **Highlights:** keep only if still matching final results.

---

## Phase 43 — Figure/table visual QA
Render final PDF; inspect every page: no figure/table overflow; readable axes/legends;
consistent fonts; equations render; references not clipped; captions with figures; no blank
pages/orphan headings/broken symbols; no `??`, `[TODO]`, `TBD`, `PRE-SUBMISSION`, comments/
track changes.

---

## Phase 44 — Search final manuscript for forbidden leftovers
`TODO, TBD, FIXME, draft, pre-submission, placeholder, to be added, reviewer 1, reviewer 2,
anonymous author, XXX, ???` — every hit manually checked.

---

## Phase 45 — Final scientific claim audit
Classify every claim: A experimentally demonstrated (strong language OK); B supported but
limited (qualified language); C hypothesis/design intention ("designed to…"); D future work
(move it). Removes overclaiming.

---

## Phase 46 — Final reviewer attack simulation (3 independent passes)
- **Reviewer 1 (RecSys):** actually a new ranking method? statistically valid? benchmark
  large enough? leakage? competitive baselines?
- **Reviewer 2 (XAI):** explanations actually faithful? correspond to displayed decision?
  counterfactual validates explanation claims? human usefulness demonstrated?
- **Reviewer 3 (applied AI / ESWA):** works in realistic recruitment? generalizes?
  architecture matters? latency meaningful? fairness sufficiently tested? artifact reproducible?
Fix highest-impact criticisms.

---

## Phase 47 — Final submission checklist
**Science:** complete/strong relevance judgments; proper train/val/test; no leakage; strong
baselines incl. CareerBERT/modern; weight stability; ablations; held-out calibration;
explanation eval; counterfactual eval; fairness sensitivity; parser robustness; adversarial
robustness; cold-start; scalability; statistical CIs.
**Code:** clean repo; reproducible env; one-command runner; tests pass; no secrets; no
hard-coded local paths (`/Users/harsh...`); no stale datasets/checkpoints; no dead scripts.
**Paper:** abstract/tables/figures regenerated; Results/Discussion/Limitations/References
updated; claims/numbers/cross-refs audited.
**Submission package:** main manuscript; title page; highlights; cover letter; supplementary;
artifact/DOI; GitHub; author metadata; ORCID; no reviewer placeholders; no draft labels;
genuinely anonymous manuscript.

---

## Execution order (10 stages — do NOT run the 47 phases randomly)

1. **Stage 1:** freeze repo · audit code · audit dataset · build experiment manifest · fix reproducibility
2. **Stage 2:** expand 47→450 labels · two annotators · agreement analysis · train/val/test
3. **Stage 3:** re-run baselines · add LTR · add CareerBERT · re-run six-channel · ablations
4. **Stage 4:** weight stability · calibration · explanation · counterfactual · fairness
5. **Stage 5:** parser robustness · adversarial · cold-start · temporal · synthetic stress
6. **Stage 6:** scalability · incremental updates · failure injection · multi-agent validation
7. **Stage 7:** statistical analysis · auto-generate tables · auto-generate figures · numerical verification
8. **Stage 8:** rewrite Results · Discussion · Limitations · Abstract · contributions
9. **Stage 9:** update diagrams · README · artifact · DOI · supplementary
10. **Stage 10:** PDF visual QA · cross-document QA · anonymity QA · package QA · hostile-review sim

### Explicitly do NOT waste time on yet
- Don't build more agents (contribution isn't the agent architecture per se).
- Don't add more UI (already sufficient to communicate the concept).
- Don't polish prose yet (numbers/tables/figures/abstract/Results/Discussion all change after new evaluation).

### The real target
From *"a carefully engineered prototype with promising results on a small frozen corpus"*
to *"an auditable ranking formulation, evaluated on complete relevance judgments with
strict held-out generalization, strong recruitment baselines, calibrated pair-level
confidence, explanation faithfulness, controlled counterfactual sensitivity, robustness
analysis, and reproducible implementation."* You don't need every experiment to be
spectacular — if CareerBERT beats you on raw nDCG but you win on calibration, faithful
decomposition, latency, and robustness, that's still a defensible ESWA story. The goal is
not a 0.99 number; it's numbers that survive a hostile reviewer checking how they were produced.

---

## COMPLETION STATUS — updated 2026-08-18 (Stage-1 + Stage-2 executed end-to-end)

Evidence lives in `research/EXPERIMENT_REGISTRY.yaml` (EXP-001..033), `research/REVIEW_LOG.md`
(Iterations 0–4), `research/results/*.json`, `research/reports/NUMBERS_PASS_FINAL.md` and
`FINAL_*` deliverables. No git commits (repo constraint). Legend: DONE · PARTIAL (done with caveat) ·
AUTHOR (author-only: identity/logistics that must not be fabricated).

| Phase | Status | Evidence / note |
|---|---|---|
| 0 Freeze + manifest | DONE | control plane under `research/`; env pinned; baseline snapshot in `research/audit/baseline/` |
| 1 Code audit + integrity fixes | DONE | B3 sha256 seed, H8 LTR relabel, B10 ablation meta; NaN-embedding guard added (EXP-033) |
| 2 Dataset expand + agreement | PARTIAL | 47 human labels PRESERVED; LLM-assisted 450-label 2nd pass κ=0.69 (EXP-018) — NOT two human annotators (disclosed as limitation); full 30×15 human relabel not obtainable (single annotator) |
| 3 Synthetic data | DONE | EXP-023 500×75 transparent latent GT; used for recovery/stress/scale, never as human labels |
| 4 Train/val/test splits | DONE | EXP-012/027 job-, candidate-, both-unseen, all leakage-checked |
| 5 Re-run composite | DONE | EXP-011 (0.949, reproduced byte-identical) + P@5/R@5/MRR reported |
| 6 Baselines incl. LTR + domain encoder | DONE | EXP-014 LambdaMART 0.963 / JobBERT 0.864 / two-tower 0.878 (CareerBERT unavailable→JobBERT, RD-007); all CIs overlap |
| 7 Weight-selection stability | DONE | EXP-015 hand-set = prior (bootstrap near-reverses semantic/title) |
| 8 Full ablation | DONE | EXP-013 leave-one-out: only semantic load-bearing; corroborated by EXP-025 |
| 9 Parser eval | PARTIAL | parser_robustness.json (n=30, CIs wide); gold-parse F1 not separately built (LLM off hot path) |
| 10 Parser-error propagation | DONE | folded into robustness matrix EXP-029 (skill delete/insert/corrupt) |
| 11 Adversarial resume | DONE | EXP-029 keyword-stuffing (gaming fails), synonym-invariant, formatting/misspelling weakness reported |
| 12 Cold-start | DONE | EXP-007 cold_start.json (synonym/misspelling/unseen-skill, propagation verified) |
| 13 Calibration redesign | DONE | EXP-026 defined target + raw/Platt/isotonic/temperature on held-out; discrimination reported |
| 14 Calibration subgroups | PARTIAL | discrimination (BSS/AUC/range) reported (EXP-020/026); per-subgroup reliability not separately tabulated (n too small) |
| 15 Explanation eval | DONE | EXP-028 mechanistic ranking-level faithfulness + structural checks (rule vs LLM-template) |
| 16 Counterfactual | DONE | EXP-005 50-pair (recourse-null + demographic-proxy), honest null explained |
| 17 Fairness → sensitivity | DONE | reframed as demographic-proxy sensitivity (§5.4/§6.2), not an audit |
| 18 Temporal | DONE | EXP-030 controlled SIMULATION (labeled as such), emerging-skills -16.5% |
| 19 Scalability | DONE | EXP-031 real timing to 10k jobs (~linear), replaces the 15-job "production" claim |
| 20 Incremental updates | DONE | EXP-032 score+merge vs full re-rank (11–767×) |
| 21 Multi-agent validation | DONE | EXP-019 failure isolation real; no monolith-vs-agent perf benefit → demoted to implementation detail |
| 22 Failure injection | DONE | EXP-033 9/9 no-crash + deterministic; NaN gap found & fixed |
| 23 Security/PII audit | DONE | author home-path scrubbed from ~28 artifacts; real handles anonymized; see FINAL_DOCUMENT_AUDIT |
| 24 Test-suite claim guards | DONE | test_scientific_claims.py 9 pass (weight-sum/decomposition/calibration-monotonic/leakage/NaN-guard) |
| 25 Reproducibility | DONE | determinism byte-identical; reproduce_all.sh wired for EXP-011..033 + table-gen + verifier; deps pinned |
| 26 Single runner | DONE | scripts/reproduce_all.sh (single source of truth) |
| 27 Statistics | DONE | EXP-022 bootstrap CIs + Holm; parity reported, no manufactured significance |
| 28 Auto-generate tables | DONE | generate_manuscript_tables.py → tables/*.tex + MANUSCRIPT_NUMBERS.json |
| 29 Numerical consistency checker | DONE | verify_paper_numbers.py passes (gates the build) |
| 30 Diagrams | PARTIAL | captions corrected (fig4 labeled in-sample + held-out); full figure regen from artifacts pending (figures are illustrative, numbers now sourced from tables) |
| 31 Results around RQs | DONE | §5 rewritten incl. new §5.7 (recovery/generalization/robustness/scale) |
| 32 Contribution claims | DONE | reframed to auditable/calibrated/explainable methodology (not superiority/multi-agent-novelty) |
| 33 Title | DONE 2026-08-18 | CHANGED to "An Auditable, Calibrated, and Explainable Multi-Agent System for Job-Candidate Recommendation" (dropped reviewer-flagged "Trustworthy"; kept honest "Multi-Agent") under the "maximize acceptance" mandate; propagated to main.tex/title-page/cover-letter/form-guide/keywords. Reversible on author request. |
| 34 Abstract | DONE | rewritten to honest numbers + parity + generalization; every abstract number exists in Results |
| 35 Limitations | DONE | §6.2 expanded: corpus/power, single-annotator, calibration discrimination, no human XAI study, robustness gaps, simulated temporal/synthetic, fairness proxy, learned-fusion overfitting |
| 36 Related Work | PARTIAL | positioning intact; a fuller neural-ranking/calibration/XAI survey refresh is optional polish |
| 37 README | DONE | root README.md now has an "ESWA submission — one-command reproduction" section (deps, reproduce_all.sh, artifacts, verifier, provenance, expected results) derived from the repo; FINAL_REPRODUCTION.md companions it |
| 38 Artifact | PARTIAL | configs/data-schema/eval-scripts/results/tables released; raw resume data stays private (synthetic reproduction provided) |
| 39 DOI/GitHub | AUTHOR | "deposit upon acceptance" per RD-008; no live DOI asserted; author to confirm repo |
| 40 Final numerical audit | DONE | FINAL_NUMERICAL_AUDIT.md |
| 41 Cross-document consistency | DONE | FINAL_DOCUMENT_AUDIT.md (author-list mismatch flagged to author) |
| 42 Package fixes | DONE | no PRE-SUBMISSION/placeholder in sections; ORCID via Editorial Manager; NVIDIA grant kept |
| 43 Figure/table visual QA | DONE | PDF compiles 39pp, 0 errors, 0 undefined refs, no ?? / TODO |
| 44 Forbidden leftovers | DONE | grep clean across sections/tables |
| 45 Scientific-claim audit | DONE | claims classified; strong language only where experimentally supported (parity, calibration trade-off, decomposition validity) |
| 46 Reviewer attack sim | DONE | Kiro 4-model panel (Iter 3) + 5-dim code review (Iter 4) + final 5-reviewer ESWA hostile panel (§AD) → FINAL_REVIEW.md |
| 47 Submission checklist | PARTIAL | science/code/paper done; author-only logistics (author list, ORCID, DOI, cover-letter) remain AUTHOR |

**Bottom line:** the science, integrity, reproducibility, and manuscript-evidence alignment are complete
and defensible; the only open items are author-identity/submission logistics I must not fabricate (author
list reconciliation, ORCID/DOI, README polish, optional figure regen + related-work expansion).
