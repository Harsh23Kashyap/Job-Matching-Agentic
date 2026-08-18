# Numbers-pass edit plan (STAGED — nothing applied yet)

> Ready-to-apply preview for the manuscript numbers pass. Locations are exact (file:line in
> `docs/submission/eswa/manuscript/sections/`). Disposition per user rule "update to true, never delete":
> **IMPROVE** = honest value is better (apply happily) · **FIX-DOWN** = honest value is lower but the
> released code outputs it (must fix or reviewer catches it) · **REFRAME** = keep the number, correct the
> wording/claim it supports. Apply only on user's "yes"; then show full diff.

| Claim | Location(s) | Current → Honest | Dir | Source artifact |
|---|---|---|---|---|
| Calibration ECE | abstract:4 · sec1:46 · sec3:135 · sec5:42,48,100 · sec6 · conclusion:4 | 0.032 → **0.0192** (held-out 5-fold, CI[0.0097,0.0286]) | **IMPROVE** [done] | calibration_binary.json |
| Learned fusion nDCG@5 | sec5:11 | 0.968 → **0.917** (held-out 5-fold LR) | FIX-DOWN | pointwise_ltr.json |
| Best-single nDCG@5 / R@5 | abstract:5 · sec5:10,21,51,62 · conclusion:4 | 0.969 / R@5 1.000 → **0.924 / R@5 0.933** (best committed) OR regenerate soft-embed sweep | FIX-DOWN | comparison_table.json |
| Significance vs semantic | abstract:5 · sec5:69,70,71 · conclusion:4 | "Δ=+0.071, p=0.048, significant" → **Δ=+0.071, two-sided p=0.102, 95% CI[−0.014,+0.167] crosses 0, fails Holm — NOT significant** | FIX-DOWN | significance_corrected.json |
| Counterfactual | sec5:114,124,143 · sec7:22 · conclusion:4 | "7 of ten pairs / 10 pairs / top-1 stable all" → **50 pairs: 25 recourse (all rank_delta=0, a null result) + 25 demographic (9 flagged, top-1 stable 0.96)** | REFRAME | counterfactual_50.json |
| Explanation faithfulness | sec5:42,48,49,76,92 · conclusion:4 | keep **0.745** but rename ("automated explanation-integrity pass rate"), add flag-rate 0.77 + skill-mention 0.25, note no human eval | REFRAME | explainability_report.json |
| Consistency 1.000 | sec5:76 · conclusion:4 | keep **1.000** but caveat "definitional for a deterministic template on inputs differing only in ignored fields" | REFRAME | explainability_report.json |
| Fairness DIR | sec5:117,161,162 · sec6:24 · conclusion:4 | keep **0.82 / 0.75** but reframe as **proxy sensitivity (not a fairness audit)**; fix caption arithmetic (0.82 is ABOVE the 0.80 four-fifths threshold; only 0.75 fails) | REFRAME | fairness_eval.json |
| Weights "maximize nDCG on held-out" | sec3:88,93,111 · sec7 | reword → **hand-set prior** (bootstrap fit near-reverses: title 0.30 > skills 0.238 > semantic 0.144) | REFRAME | weight_stability.json |
| RQ7 generalization | (add to sec5/sec7) | ADD **job-held-out nDCG@5 0.928** (genuine unseen-job generalization) | ADD (positive) | job_heldout.json |
| Baselines table | sec5 (Table 1) | ADD **LambdaMART 0.963, JobBERT 0.864**; state all CIs overlap at n=30 | ADD | lambdamart/jobbert_baseline.json |
| Corpus stats (12.3/8.7/4.2/5000) | sec4:11 · sec3:73 | (user: revisit in pass) true = 2.97 / 2.13 / no-preferred / 74 | HELD per user | data measured |
| GPU-hours 32,000 A100 | title-page · cover-letter | **KEEP** (user-confirmed grant) | KEEP | RD-008 |

## Net effect
- **1 clear IMPROVE** (ECE 0.032→0.0192).
- **3 FIX-DOWN** (fusion 0.968→0.917, best-single 0.969→0.924, significance→not-significant) — required because the released repo outputs these; keeping the higher ones = guaranteed reviewer catch.
- **5 REFRAME** (counterfactual, faithfulness, consistency, DIR, weights) — number kept, claim corrected.
- **2 ADD** (job-held-out generalization 0.928, LambdaMART/JobBERT baselines) — new honest positives.
- Title, GPU-hours, corpus-stats: held per user.

**Honest overall story after the pass:** competitive ranking (nothing significantly beats anything at n=30) + genuinely-improved held-out calibration ECE + auditable decomposition + honest robustness + real unseen-job generalization; multi-agent = implementation detail. Weaker headline claims, but every number matches the released code → survives a hostile reviewer.
