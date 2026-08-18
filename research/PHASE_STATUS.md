# PHASE_STATUS  (synced 2026-08-18, Stage-2 strengthening complete)

Legend: COMPLETE · IN-PROGRESS · LEFT. Evidence = research/EXPERIMENT_REGISTRY.yaml,
NUMERICAL_CLAIMS.yaml, REVIEW_LOG.md, REPRODUCTION_LOG.md. No git commits (RD-009).

## STAGE-1 + numbers-pass — COMPLETE (see prior sync + NUMBERS_PASS_FINAL.md)
Control plane, code-integrity fixes (B3/H8/B10), LLM-assisted labels (EXP-018), job-held-out
(EXP-012), composite re-run (EXP-011), RQ1 baselines (EXP-014), weight-stability (EXP-015),
6-channel ablation (EXP-013), architecture value (EXP-019), significance+Holm (EXP-022),
calibration discrimination (EXP-020), scientific-claim tests, numbers pass (§C).

## STAGE-2 STRENGTHENING — COMPLETE (2026-08-18, EXP-024..033)
- EXP-024 structure recovery (synthetic): recovery ratio 0.907; decomposition validity (skills↔required 0.996, comp↔comp 0.985, exp↔exp 0.867); degrades on hard/adversarial. §F-H DONE.
- EXP-025 model-selection search (25 configs, protocol-gated, criteria frozen pre-result): NO config beats incumbent after Holm; only drop-semantic significant; incumbent selected by parsimony. §D-E DONE.
- EXP-026 calibration methods (raw/Platt/isotonic/temperature, defined target): Platt low-ECE-but-degenerate, isotonic preserves discrimination (BSS 0.64/AUC 0.95), temperature fails; honest trade-off. §N DONE.
- EXP-027 generalization (candidate/job/both-unseen, all rank full 15-job pool, leakage-checked): 0.929/0.929/0.927 vs composite 0.949 (corrected from inflated 3-job-pool values in Iter-4). §J DONE.
- EXP-028 explanation faithfulness (mechanistic, non-tautological): comprehensiveness top>least>random; skill-edit attribution 1.0; structural guarantees separated. §O DONE.
- EXP-029 robustness matrix (11 perturbations): synonym-invariant, gaming-resistant, formatting/misspelling weaknesses reported. §R DONE.
- EXP-030 temporal drift (SIMULATION): emerging-skills -16.5%, titles -3%, salary ~0. §S DONE.
- EXP-031/032 scalability+incremental: ~0.048 ms/pair linear; incremental 500x cheaper than full re-rank. §T-U DONE.
- EXP-033 failure injection: 9/9 no-crash + deterministic; found+FIXED NaN->1.0 gap (core.scoring._safe_vec) + regression test. §V/§W DONE.

## MANUSCRIPT INTEGRITY PASS — DONE (Kiro-panel flagged, Iteration 3)
Removed false "two independent annotators" (→ single author + LLM-assisted κ=0.69, disclosed);
corrected 4 fabricated corpus stats (12.3→2.97 skills/resume, 8.7→2.13 req, 4.2→0 pref, 5k→74 vocab);
fixed B11 weight-tuning claim ×3 (→ hand-set prior); B12 unjudged-pairs reframed (closed-world caveat);
hybrid baseline "tuned"→"fixed 0.7/0.3".

## FINAL STAGE — COMPLETE (2026-08-18, Iterations 4–5)
- §X code review (5-dim workflow, 37 findings) — DONE; all BLOCKER/SERIOUS + claim-affecting MODERATE fixed.
- §Y reproduction — DONE + VALIDATED: `bash scripts/reproduce_all.sh` runs EXP-011..033 → table/figure gen → numeric verifier GATE end-to-end, exit 0 ("ALL PASS"); determinism byte-identical.
- §Z manuscript rebuild — DONE: abstract/§1/§3/§4/§5(+new §5.7)/§6/§8 rewritten to evidence; multi-agent demoted, calibration/explanation reframed, limitations expanded.
- §AA auto tables/figures — DONE: generate_manuscript_tables.py → tables/*.tex + MANUSCRIPT_NUMBERS.json; fig4 regenerated from held-out data.
- §AB numerical audit — DONE: verify_paper_numbers.py passes (gates the build); FINAL_NUMERICAL_AUDIT.md.
- §AC document audit — DONE: FINAL_DOCUMENT_AUDIT.md; PII/home-path + real-handle scrub; cover-letter + highlights corrected; DOI→"upon acceptance".
- §AD final hostile review — DONE: 5-reviewer ESWA panel; all returned BLOCKER/SERIOUS fixed; FINAL_REVIEW.md.
- §AG FINAL_* deliverables — DONE (5 reports + NUMBERS_PASS_FINAL).
- /clean-slop — DONE: deliverables + session research docs emoji-free.
- §37 README — DONE: ESWA one-command reproduction section added.
- PDF QA — DONE: 39pp, 0 errors, 0 undefined refs, rendered 0 dangerous overclaims / 176 honest markers.

## STAGE-3 MODEL-IMPROVEMENT + ACCEPTANCE CAMPAIGN — COMPLETE (2026-08-18, EXP-034..036 + 024b)
- P4 protocol — DONE + integrity-corrected: research/PROTOCOL.md (real 30x15/47 corpus = secondary transfer check, NOT untouched test; selection on synthetic + inner CV only).
- P1 skill-semantics — DONE: EXP-034 graded 4-class matcher (EXACT/RELATED/SEMANTIC/UNRELATED, graded credit, macro-F1 0.81) + EXP-034b de-circularized objective benchmark (orthographic/synonym exact-recall 1.0; 7/8 hard negatives kept distinct; Angular/AngularJS over-merge + misspelling brittleness disclosed). The foregrounded NEW contribution.
- P2/P3 derived features + fusion — DONE (synthetic, development-only): EXP-035/036 derived skill-coverage features + monotonic-GBM/LambdaMART beat fixed composite 0.917->0.978-0.990; gain survives dropping synthetic-only preferred feature (0.978/0.969); framed as headroom, NOT a real-world gain.
- By-construction control — DONE: EXP-024b non-additive (multiplicative/gated) latent recovers 0.891 (Δ−0.016 vs additive 0.907) — refutes the "recovery is by construction" objection.
- P12 reframe — DONE (body): abstract/§1/§5.7/§6/§8 foreground auditable relation-aware skill matching + honest parity/instrument framing + synthetic headroom; multi-agent demoted to implementation.
- P13 EDITORIAL_RISK_MATRIX.md — DONE: 14 criticisms × prob × sev × evidence × fix × impact, HIGH×HIGH prioritized.
- P14 final-bundle refresh — DONE: Stage-3 addenda folded into FINAL_AUDIT.md + FINAL_REVIEW.md; REVIEW_LOG Iterations 6–7; ESWA-STAGE3-PLAN.md completion status.
- Manuscript — 41pp clean, 0 undefined refs, verifier passes (all numbers artifact-sourced + gated).
- Kiro panel: Stage-3 plan panel returned 4/4 (unanimous reframe); 10-model cross-family paper panel stalled twice (gateway degraded) and was NOT relied upon — salvaged completed models + own analysis instead.

## BLOCKED (author-only — must NOT be fabricated)
- Author list reconciliation (title page 1 vs CRediT 3); a real resolving artifact DOI (now "deposit upon acceptance"); the disclosed small-corpus / single-annotator ceiling (stated, not removable).
- Highest-leverage author-only ADDITIONS a clear Accept needs: a larger 2-annotator explicitly-negative-judged benchmark; a blinded human explanation/usefulness study; the title decision (DONE 2026-08-18, dropped "Trustworthy").
- ENABLEMENT DONE — FULL G2 TOOLCHAIN built + validated (reduces the #1 author-only item to just "assign annotators"): (1) make_annotation_sheet.py -> annotation_sheet_unjudged.csv (403 unjudged pairs, real context + hard-negative hints, BLANK grades). (2) merge_annotations.py -> data/eval_pairs_expanded.json (self-test passes; unions filled grades with the 47, never overwrites, validates 0-3). (3) powered_reeval.py -> one-command powered re-test (label distribution incl. explicit negatives, per-method nDCG@5, composite-vs-semantic significance, jaccard/exact/graded decomposition; smoke-test on current corpus reproduces canonical 0.949/0.878/0.992 and correctly flags "not yet powered"). So the instant 2 annotators fill the sheet, the powered ESWA re-analysis is one command. Governing plan: PROFESSOR_FEEDBACK_PLAN.md (supervisor: strengthen-then-submit ONE venue; overlap verdict = ESWA & JAAMAS are one contribution -> ESWA only, hold JAAMAS).
- SYNTHETIC_v2 POWERED FUSION CONFIRMATION (2026-08-18, user "maximise synthetic"): generated synthetic_v2 (2000x200=400k pairs, graded 0-3, 295k explicit negatives; v1 preserved for reproduction). feature_fusion on v2 (5-fold CV, n=2000) CONFIRMS the v1 finding at 8x scale with tight CIs: nonlinear base6 fusion beats the fixed composite (lambdamart-base6 0.933 Δ+0.059, monotonic-gbm-base6 0.922 Δ+0.048, CI-excl-0) while LINEAR learned fusion does NOT (logreg-base6 0.840 Δ-0.035, ridge-base6 0.798 Δ-0.076) -> hand weights near-optimal linearly; headroom is nonlinear interaction. +derived still by-construction (disclosed). Development evidence; feeds the final paper after human annotation.
- LLM-ASSISTED ANNOTATION + PROVISIONAL POWERED RE-TEST (2026-08-18, user-directed; DISCLOSED, NOT human ground truth): llm_annotate.py graded all 403 unjudged pairs via Kiro gpt-5.6-sol + deepseek-3.2 (inter-model quadratic kappa 0.541); adjudicated 392 grade-0 (explicit negatives -> validates the closed-world assumption) + 7 grade-1 + 4 grade-2 (11 previously-missed positives). Built data/eval_pairs_llm_expanded.json (47 human + 403 LLM). powered_reeval.py on it: composite-vs-semantic Δ+0.082 CI[0.007,0.152] perm-p=0.039 -> NOMINALLY SIGNIFICANT (vs positive-only p~0.10-0.15) — PROMISING but PROVISIONAL (LLM labels; hinges on 11 LLM-judged positives; author's human pass before submission is authoritative). graded-vs-jaccard Δ+0.041 p=0.15 and relation-aware-vs-exact p=0.13 -> NO LONGER significant with more labels, CONFIRMING the professor's "directional/underpowered, one-query-dominated" caution -> do NOT overclaim the relation-aware benefit. Human annotation pending (user, pre-submission).
- G5 STIMULUS ENGINE built + validated (make_explanation_renderings.py -> research/datasets/explanation_study/): 45 self-contained HTML "shortlist screens" (15 jobs x 3 explanation conditions) + manifest.csv + INSTRUMENT.md. Conditions hold the RANKING constant and vary only the explanation: score_only (control) / generic_template (control) / factor_grounded (six-channel decomposition = weight x score, matched/missing required skills, confidence band; verified faithful — contributions sum to the composite). Ready for the blinded human study; INSTRUMENT.md notes valid system-wrong items still need the G2 explicit negatives.
- Panel-DEMOTED optional-deepen (low acceptance-impact): counterfactual 50->100 with per-channel monotonicity, adaptive-ECE/beta calibration, scalability->1M.

## STAGE-3B ACCEPTANCE-CAMPAIGN CYCLE — COMPLETE (2026-08-18, EXP-043/044 + independent hostile panel)
- System improvement: graded relation-aware skill channel wired into the live scorer (core.skills.graded_coverage_skills, frozen a-priori credits), 3 new regression tests (12/12 pass).
- EXP-043/044: by-construction audit (required-coverage corr 1.000 with latent generator -> corrected EXP-035/036) + pre-specified variant DECOMPOSITION isolating the novelty: synthetic gain is coverage-FORM (0.917->0.949, p<0.001) while relation-aware credit hurts there (0.949->0.944); on the REAL corpus the form is null (0.949->0.942, p=0.50) and the RELATION-AWARE credit drives the gain (0.942->0.992, 6/30 improved 0 worsened, sign-test p=0.03, effective n=6, one-query-dominated -> directional signal only).
- Author-only deliverables authored: title changed (dropped "Trustworthy", propagated everywhere) + HUMAN_STUDY_PROTOCOL.md + BENCHMARK_ANNOTATION_PROTOCOL.md.
- Independent 6-agent hostile ESWA panel run; ALL realistically-fixable BLOCKER/SERIOUS/MODERATE/MINOR addressed: novelty isolated (credit=0 ablation), graded matcher defined in §3 + contribution lists reconciled (§1/§5/§8), ANONYMITY LEAK scrubbed (author identity removed from 9 released test fixtures + stale main.log), §6 positioning table + ESCO/O*NET prior art + taxonomy-coarseness limitation, §4.3 ECE definition fixed, §5.4 recourse wording fixed, "first Platt" overclaim removed, verifier + reproduce_all.sh hardened for Stage-3 numbers, provenance docs corrected.
- Manuscript recompiles clean (0 undefined refs, 0 hard errors); verify_paper_numbers.py passes (now gates 6 new Stage-3 numbers); 184 unit + 12 scientific-claim + 29 integration + 10 frontend tests green. RD-014 + REPRODUCTION_LOG updated.
- CONVERGENCE GATE: independent hostile review returned "converged" (no realistically-fixable BLOCKER/SERIOUS remains); a read-only consistency agent's findings all fixed (stale highlights, keywords, ECE definition, cover-letter/plan title, reliability-diagram framing). Anonymization made runnable: scripts/anonymize_reviewer_bundle.py (verified 0 residual identity).
- REPRODUCIBILITY GATE PASSED: `bash scripts/reproduce_all.sh` ran end-to-end (EXP-011..036 + 043/044 + table-gen + fig-regen + verifier) -> exit 0; regenerated graded-channel numbers BYTE-IDENTICAL to the manuscript (SYN 0.917/0.949/0.944, REAL 0.949/0.942/0.992); determinism confirmed.
- CALIBRATION IMPROVEMENT (EXP-041, no new data): added adaptive (equal-mass) ECE + beta calibration to EXP-026. Adaptive ECE EXPOSES that Platt's equal-width 0.019 understates miscalibration (adaptive 0.084); BETA calibration (Kull 2017) attains lowest ECE under both binnings (0.009) AND preserves discrimination (BSS 0.67/AUC 0.96) -> RESOLVES the calibration-vs-discrimination trade-off the paper listed as a limitation. Deployed Platt RETAINED as frozen default; beta RECOMMENDED. tab:calibration regenerated (5 maps + adaptive-ECE column), §5.3/§6.1/§6.2 + Kull citation updated; verifier gates 0.009/0.084; determinism re-confirmed byte-identical; changed pipeline segment (calib->tablegen->verifier) re-validated composes end-to-end. fig4 reliability diagram REGENERATED to include the beta curve (visually shows Platt collapsing to a razor-band point vs beta tracking the diagonal); caption updated; clean build (0 undefined/overfull).
- Residual (unfixable ceiling, honestly owned): net methodological novelty is modest (small hand-built taxonomy + off-the-shelf components) -> repositioned as an auditable-integration + evaluation-methodology contribution; a clear Accept still needs author-only additions (larger 2-annotator benchmark, human explanation study).

## JAAMAS SECOND-VENUE INTEGRITY PASS — DONE (2026-08-18; user: "we will try for JAAMAS again")
The JAAMAS manuscript (docs/submission/jaamas/, multi-agent FOREGROUNDED — correct for that venue, single-blind so NOT anonymized) is the ORIGINAL and carried the SAME integrity problems the ESWA numbers-pass fixed. Propagated the corrected science while keeping the multi-agent framing:
- Phantom best-single removed everywhere: 0.969 / recall@5=1.000 ("every resume retrieves all relevant") -> honest composite 0.949, best-single 0.924, semantic 0.878, RRF 0.913. Fixed in abstract (main.tex), §1, §6 (prose + progression table), §7 conclusion, tab-progression, tab-fusion, portal cover-letter (.tex+.md), portal information-sheet (.tex+.md).
- FABRICATED SIGNIFICANCE removed: "significantly improves...p=0.048...significantly beat (p=0.010/0.009)" -> honest parity (p=0.10, fails Holm, no method statistically distinguishable at n=30) + instrument-limitation caveat.
- In-sample leakage fixed: learned fusion 0.968 -> held-out 0.917 (does not beat composite; optimistic-upper-bound note); in-sample ECE 0.032 -> held-out 0.019 + beta 0.009 + low-discrimination disclosure (tab-model-params).
- Cross-encoder reconciled: standalone 0.939 (< composite 0.949) + rerank-pool lowers to 0.834 (Δ−0.108), consistent across §6/tab-latency/abstract.
- NEW CONTRIBUTIONS ADDED to JAAMAS (matching ESWA's strengthened science, multi-agent framing kept): §5 now defines the graded relation-aware skill matcher (eq:skill-graded, exact=1.0/related=0.5/else 0) with the honest coverage-form-vs-relation-aware DECOMPOSITION (synthetic gain is coverage form; relation-aware credit helps only on real human labels, 6/30, sign-test p=0.03, effective n=6, directional); and the beta-vs-Platt calibration trade-off (Platt ECE 0.019 low-discrimination; beta 0.009 preserves discrimination, recommended, Platt kept as frozen default).
- All edits LaTeX-safe (balanced math, cases 3/3, consistent columns); comprehensive stale-number sweep across ALL jaamas tex/md = CLEAN. CANNOT compile here (JAAMAS build_all.sh needs pdflatex; tectonic incompatible with Springer sn-jnl.cls at glyphtounicode startup) -> AUTHOR builds via Overleaf/pdflatex (only remaining JAAMAS step).

## REVISION-VERIFICATION CLOSURE — DONE (2026-08-18, RD-016)
Adversarial 4-agent revision-verify workflow on the RD-015 P0/P1 edits returned "FIXES — not clean" (8 findings); verified each against live files, fixed the confirmed ones:
- BLOCKER: P0.1 label-leakage SURVIVOR in the new §3.2 summary ("weights ... fixed by the nDCG@5 optimization on the labeled subset") — the RD-015 scrub caught §7/§3.5 but missed this fresh copy; rewrote to "fixed hand-set domain priors, not fitted"; WIDENED the verifier gate (max/optimization + optional article) — gate self-test confirms it now catches the old phrasing, passes the new.
- MODERATE ×2: §3 roadmap refs off-by-one after the §3.2 insertion (bumped all six + added 3.2 pointer; all sec:3.x now resolve); §2.5 "regulatory requirement ... satisfied" overclaim softened to "engineering prerequisite" (matches §1.2 disclaimer).
- MINOR ×3 fixed (abstract 7/8 look-alike qualifier; tab:stage2 "25 configs" label; §5.3 beta-CI upward-bias clause); 0.018-vs-0.019 accepted-with-rationale (already reconciled §5.3:84).
- RE-TEST: verifier exit 0 with widened gate; residual sweep clean; tectonic compile exit 0, 45pp, 0 undefined refs / 0 hard errors / 0 overfull. Closes the RD-015 loop.
- CONVERGENCE CONFIRMATION (2 independent adversarial passes): Agent-1 (fix-verify + new-contradiction sweep) returned CLEAN on all six fixes and caught ONE pre-existing stale-calibration inconsistency (§2:50 "Platt lowest ECE / isotonic preserves discrimination" — contradicted §5.3/tab-calibration where BETA is lowest-ECE + discrimination-preserving) → FIXED (§2:50 now foregrounds beta). Agent-2 (fresh-eyes full-manuscript BLOCKER scan) stalled ~9min with no verdict → stopped and its scan re-run INLINE across all 5 red-flag axes (significance/superiority, best/outperforms, two-annotator/ground-truth, phantom numbers, regulatory-meets-requirement): ALL CLEAN — every hit is honest parity-framing or an explicit disclaimer/superseded note. Final RE-TEST after §2:50 fix: verifier exit 0, compile exit 0, 45pp, 0 undefined refs. Convergence gate satisfied on the corrected manuscript.

## SUPERVISOR ROUND-2 POLISH — DONE (2026-08-18, RD-017)
Supervisor re-read (45pp) verdict: "close to submission-ready." 3 must-fix + 3 recommended executed; no new scope ("stop major surgery"):
- MUST: (1) beta-CI relabelled to beta's OWN-ECE bootstrap CI [0.012,0.032] + bias note; line-87 mislabel ("advantage" CI) corrected to overlap-with-Platt [0.000,0.044] (verified vs calibration_methods.json). (2) abstract 7/8 already done. (3) Table-10 verification (per-paper web-checked): Lofstrom "Calibrated Explanations" Counterfactual --→\checkmark (title/abstract/repo report counterfactuals; arXiv:2305.02305 + github Moffran/calibrated_explanations); "Counterfactual" column caption generalized; §6.pos "one or two"→"a subset" (Lofstrom 4/6, JobMatch uniquely 6/6).
- CITATION INTEGRITY: FIXED CareerBERT authors (bib "Lavi & Zschech" → real Rosenberger, Wolfrum, Weinzierl, Kraus, Zschech; arXiv:2503.02056). FLAGGED (author-only) chen2023causal — "Causal debiasing for job recommender systems, RecSys 2023" NOT locatable in Crossref/OpenAlex/arXiv/DBLP/Semantic-Scholar (DBLP timeout + S2 429 on retry); NOT silently replaced.
- RECOMMENDED: faithfulness wording (§1.6 "automated ... not a human faithfulness study"); caveat-trim (§5.1 instrument-parity duplication compressed, full detail kept in §6.2).
- RE-TEST: verifier exit 0; tectonic exit 0, 45pp, 0 undefined refs/citations, 0 hard errors.

## USER-DECISION EXECUTION — DONE (2026-08-18, menu-driven answers)
- chen2023causal → DROPPED (Table-10 row + citation + §2 prose reworded); RE-TEST clean (verifier 0, tectonic 0, 45pp, 0 undefined refs). Integrity item CLOSED.
- Authors: decisions match title page (corr=Harsh Kashyap; Harsh & Taranumpreet joint-first — added explicit \textsuperscript{*} equal-contribution footnote; Thapar/WSU; no competing interests; CRediT×3; data-on-acceptance). Only ORCIDs optionally remain (deferred to Editorial Manager).
- Annotation: user chose TWO annotators — sheet + pipeline staged, awaiting filled grades (then IAA + powered_reeval one-command).
- JAAMAS: user chose PURSUE NOW. Re-sync confirmed NO propagation needed (no chen cite, no beta-CI mislabel, positioning is prose). Built docs/submission/jaamas/jaamas_overleaf_ready.zip (3.8MB, Aug-synced; parent structure so ../figures/ resolves; set main doc=manuscript/main.tex, compiler=pdfLaTeX). Stale main.pdf (Jul 30) excluded.

## Tally: Stage-1 + numbers-pass + Stage-2 (33 exp) + code review + hostile review + manuscript rebuild
+ auto-artifacts + reproduction validation + cleanup + STAGE-3 (EXP-034/034b/035/036/024b) + STAGE-3B
(EXP-043/044, graded channel, independent hostile panel, all fixes) + EXP-041 (beta calibration) + JAAMAS
integrity pass ALL COMPLETE. ESWA fully verified+reproduced; JAAMAS numbers corrected (author compiles PDF).
