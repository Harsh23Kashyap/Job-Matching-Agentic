# FINAL_NUMERICAL_AUDIT (2026-08-18)

Every headline number in the ESWA manuscript traced to CLAIM → SOURCE ARTIFACT → EXPERIMENT →
VERIFIED. All ranking/calibration numbers are auto-generated from committed artifacts by
`research/experiments/generate_manuscript_tables.py` into `docs/submission/eswa/manuscript/tables/*.tex`
and the manifest `research/results/MANUSCRIPT_NUMBERS.json`. The checker
`research/experiments/verify_paper_numbers.py` passes (no forbidden stale numbers; all canonical
numbers present) and gates `reproduce_all.sh`.

| Claim | Value | Source artifact | Experiment | Verified |
|---|---|---|---|---|
| Composite nDCG@5 | 0.949 | composite_eval_report.json | EXP-001/011 | ✓ manifest + tab:progression |
| Semantic-only nDCG@5 | 0.878 | comparison_table.json | EXP-014/013 | ✓ (was inconsistently 0.911; reconciled to canonical run) |
| RRF ensemble nDCG@5 | 0.913 | comparison_table.json | EXP-014 | ✓ (was inconsistently 0.935; reconciled) |
| Multimodal (best single) nDCG@5 | 0.924 | comparison_table.json | EXP-014 | ✓ |
| BM25 / TF-IDF nDCG@5 | 0.902 / 0.905 | comparison_table.json | EXP-014 | ✓ |
| Cross-encoder nDCG@5 / latency | 0.939 / 141.7 ms | phase11_summary.csv | phase11 | ✓ (tab:latency) |
| Significance composite vs semantic | Δ+0.071, two-sided p=0.10, CI[-0.014,+0.167], fails Holm | significance_corrected.json | EXP-022 | ✓ abstract/§5.1 |
| Calibration ECE (Platt, held-out) | 0.019 | calibration_binary.json | EXP-004 | ✓ (in-sample 0.032 labeled superseded) |
| Calibration methods (raw/Platt/isotonic/temp) | ECE 0.40/0.018/0.024/0.46; BSS -1.25/0.007/0.64/-2.18; AUC 0.967/0.76/0.95/0.967 | calibration_methods.json | EXP-026 | ✓ tab:calibration |
| Structure recovery ratio | 0.907 | structure_recovery.json | EXP-024 | ✓ tab:stage2 |
| Decomposition validity (skills↔required) | 0.996 | structure_recovery.json | EXP-024 | ✓ tab:stage2 |
| Model-selection configs / beat-incumbent | 25 / 0 (after Holm) | model_selection.json | EXP-025 | ✓ §5.7 |
| Generalization candidate/job/both-unseen | 0.929 / 0.929 / 0.927 (all pool=15) | generalization.json | EXP-027 | ✓ §5.7 + tab:stage2 (corrected from inflated 3-job-pool 0.969/0.958) |
| Robustness (synonym / keyword-stuff / format) | invariant / signed -0.089 / \|Δ\|0.117 | robustness_matrix.json | EXP-029 | ✓ §5.7 |
| Explanation comprehensiveness (top/least/rand) | 0.133 / 0 / 0.033 | explanation_faithfulness.json | EXP-028 | ✓ §5.2 |
| Scalability mean ms (15/1k/10k) | 0.8 / 51 / 517 | scalability.json | EXP-031 | ✓ §5.7 (warm, single-thread) |
| Incremental speedup (1/10/100 new jobs) | 767× / 95× / 11× | scalability.json | EXP-032 | ✓ §5.7 (score+merge, not score-only) |
| Counterfactual (recourse / demographic) | 25 recourse rank-null; 9/25 demo flagged, 24/25 top-1 stable | counterfactual_50.json | EXP-005 | ✓ §5.4 tab:counterfactual |
| Corpus stats | 2.97 skills/resume, 2.13 req, no preferred field, 74 vocab | data/cvs.json+jobs.json | measured | ✓ (fabricated 12.3/8.7/4.2/5k corrected, RD-008) |
| NVIDIA grant | 32,000 A100 GPU-hours (Brev) | user-confirmed | RD-008 | KEEP (title-page, unblinded) |

## Forbidden numbers confirmed ABSENT from the manuscript (verifier)
0.969-as-best-single, R@5=1.000, "nine times out of ten", p=0.048, "statistically significant over",
"two independent annotators", 12.3/8.7/4.2 corpus stats, RRF 0.935, "maximize nDCG on labeled pairs".

## Residual note (flag for author, not auto-fixed)
- Title page lists one author (Harsh Kashyap) while the anonymized main.tex CRediT/ORCID references
  "three authors". Author list must be reconciled by the author before submission (identity, not a number).
