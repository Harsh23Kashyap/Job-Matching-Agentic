# NUMBERS_PASS_FINAL — executed & verified (2026-08-18)

> Section-C deliverable of the Stage-2 plan. Every stale/leaky/phantom number in the ESWA manuscript
> was traced to its experiment→config→dataset→committed output, replaced with the honest value (up AND
> down), and the manuscript recompiled. Verification: `pdflatex` clean (36pp, 0 errors); rendered-PDF
> scan = **0 dangerous overclaims**, 55 honest markers. Seed convention 42; env `backend/.venv`.

| # | Claim | Old → New | Exp / artifact | Manuscript locations | Reason | Verified |
|---|-------|-----------|----------------|----------------------|--------|----------|
| 1 | Calibration ECE | 0.032 → **0.019** (held-out 5-fold, CI[0.010,0.029]) | EXP-004 `calibration_binary.json` (ece_mean 0.01916) | abstract; sec1:46; sec3:135; sec5 (ablation cap, §5.3 prose, reliability cap, §5.6); sec6:9; sec8 | 0.032 was fit-and-eval on same data (leakage) | PDF shows 0.019; 0.032 only in the explicit "earlier single-split" correction note |
| 2 | Best single config | 0.969 / R@5 1.000 → **0.924 / R@5 0.933** (multimodal weighted blend) | `comparison_table.json` (0.9237) | abstract; sec5:10, table row, ablation row, §5.1 discussion; sec8 | 0.969 matched NO committed artifact (phantom) | 0 occurrences of 0.969 in PDF |
| 3 | Learned fusion | 0.968 (in-sample) → **0.917** (held-out 5-fold) | EXP-003 `pointwise_ltr.json` | sec5:11 | fit+judged on same 47 pairs; held-out is the defensible number; 0.968 kept only as labeled upper bound | rendered |
| 4 | Significance | "Δ=+0.071, p=0.048, significant" → **Δ=+0.071, two-sided p=0.10, CI[−0.014,+0.167] crosses 0, fails Holm — NOT significant** | EXP-022 `significance_corrected.json` | abstract; sec5:§5.1 sig para; sec8 | old p was a salted-seed artifact (flips to 0.051); CI crosses 0; nothing survives Holm | rendered; "statistically significant over" = 0 hits |
| 5 | Counterfactual | "7 of 10 pairs, top-1 stable all, max shift 0.017" → **50 pairs: 25 recourse (0 rank changes = null) + 25 demographic (9 flagged, top-1 stable 24/25)** | `counterfactual_50.json` | abstract; sec4:37 setup; sec5:§5.4 prose + tab:counterfactual (caption + body → 2-row summary); sec7:22; sec8 | 10-pair superseded; recourse-null is the honest finding | rendered; table rebuilt |
| 6 | Explanation faithfulness | 0.745 kept, **reframed** as "automated explanation-integrity pass rate" (77% flagged, 25% skill-mention; consistency 1.0 definitional; no human study) | `explainability_report.json` | sec5:§5.2 prose; sec8 | 0.745 is a lint-average, not XAI faithfulness | rendered |
| 7 | Fairness DIR | 0.82/0.75 kept, **reframed** as demographic-proxy sensitivity (not audit); arithmetic fixed (0.82 is within 0.80–0.85, only 0.75 below 0.80) | `fairness_eval.json` | sec5:§5.4 prose; sec8 | proxy groups on demo corpus; caption arithmetic error | rendered |
| 8 | "Trustworthy" (body) | → **"calibrated"** in conclusion body (×2) | — (Stage-2 §Z; RD-012) | sec8:5,11 | evidence doesn't support "trustworthy"; **title kept per user** | rendered |
| 9 | §5.6 sensitivity | in-sample grid-search "0.029–0.041, confirms robust, Table S2" → **held-out 5-fold CI [0.010,0.029]** | `calibration_binary.json` | sec5:§5.6 | grid-search had no committed artifact (audit W) | rendered |
| 10 | Artifact sources | `paper_progression_summary.json`, `calibration_summary.json` (non-existent) → **`comparison_table.json`, `calibration_binary.json`** | — | sec5 ablation caption | cited files did not exist | rendered |

## Held / deferred (documented, not silently changed)
- **Corpus stats** 12.3 skills/resume, 8.7 req + 4.2 pref, ~5,000 vocab (true: 2.97 / 2.13 / no-preferred / 74) — **HELD per user** (revisit in a dedicated pass). Currently still in sec4:11 / sec3:73. FLAGGED.
- **GPU-hours 32,000 A100** — **KEPT** per user (real grant, RD-008).
- **Title** "Explainable and Trustworthy Multi-Agent…" — **KEPT** per user (body "trustworthy" softened).

## Still needs §28 auto-table / §30 figure regeneration (flagged, NOT yet done)
- **tab:progression / tab:latency**: semantic reported as both 0.878 and 0.911 (internal inconsistency) — reconcile to one committed value when regenerating from `comparison_table.json`.
- **fig4 reliability diagram**: image is the in-sample curve (caption now says so + gives held-out 0.019); regenerate from held-out calibration in §30.
- Full auto-generation of all tables/figures from artifacts (§28/AA) remains, so numbers can never drift again.

## Verification
- `pdflatex` (TinyTeX): pass1 0, final 0, **36 pages, 0 errors**.
- Rendered-PDF overclaim scan: **0** of {0.969, "nine times out of ten", "Seven of the ten", "p=0.048", "statistically significant over"}.
- Honest-marker scan: **55** hits of {0.924, 0.019, two-sided, not statistically, held-out, 50-pair, low discrimination, Holm, null result}.
