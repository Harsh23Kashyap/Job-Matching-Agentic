# JobMatch Manuscript, Review Action Status (FINAL)

Source: `JobMatch Paper Review.pdf` (8 items across Tier 1 + Tier 2, plus 11 inline `\todo{}` markers).
Verified against `docs/submission/jaamas/manuscript/` on **2026-06-06**.

## Bottom line
**All review TODOs are DONE.** 0 `\todo{}` remain in author-written files (the only "TODO" strings left
are inside vendored Springer/package files, `sn-jnl.cls`, `enumitem.sty`, `*.bst`, which never render).
Two items are *environment-blocked here, not content TODOs*: recompiling the PDF and re-running the
cross-encoder (see "Left" at the bottom).

---

## TIER 1, Mandatory

| # | Review comment | Status | Where / how resolved |
|---|----------------|--------|----------------------|
| **1.1** | Remove all `\todo{}` markers (28 total) | ✅ DONE | 0 remain. Section 2 citations (11): cited `Wooldridge2009`, `Reimers2019`+`Manning2008`, `Ribeiro2016` where they fit; softened the other 8 (no fabricated refs). Section 4.6 phase11, Section 5.2 calibration/feedback resolved with real numbers. |
| **1.2** | Add running example in Introduction | ✅ DONE | `section-1-introduction.tex`, "A running example" (Alex walkthrough) before Contributions. |
| **1.3** | Add "Why an agentic architecture?" subsection | ✅ DONE | `section-1-introduction.tex`, service-vs-agent contrast, framed as logical agents in one process. |
| **1.4** | Reorder figures (workflows before deep architecture) | ✅ DONE | `section-3-architecture.tex`, renders 1→2→3→4(workflow)→5(workflow)→6→7→8→9→10; all `\ref` verified. |

## TIER 2, Major

| # | Review comment | Status | Where / how resolved |
|---|----------------|--------|----------------------|
| **2.5** | Reduce repetition across Section 3 | ✅ DONE | `section-3-architecture.tex`, trimmed repeated read-only/ownership statements. |
| **2.6** | Compress Section 3.4 | ✅ DONE | Restructured into 4 subsubsections: Ownership and state · Shared state · Event communication · Human control. |
| **2.7** | Match-scoring figure before Section 5.2 | ✅ DONE | `section-5-quality-metrics.tex`, forward-reference to the scoring-flow figure (Fig 8) before Eq. 6. |
| **2.8** | Strengthen lit-review → architecture transition | ✅ DONE | `section-2-literature-review.tex`, 4-gap→4-solution bridge + "...introduces the multi-agent architecture presented in Section 3." |

## Artifact-backed items (benchmarks run, real numbers wired in)

| Item | Status | Result |
|------|--------|--------|
| Composite ablation under portal weights (28/27/10/15/10/10) | ✅ DONE | full composite nDCG@5 = **0.949** (`tab-ablation.tex`, Section 6, abstract) |
| Statistical significance | ✅ DONE | composite vs semantic **p=0.048**; multimodal/RRF p=0.010/0.009 (Section 6) |
| Explanation-quality table | ✅ DONE | new `tab-explainability.tex` (faithfulness 0.745/0.747, consistency 1.00) |
| Fairness disparate-impact | ✅ DONE | DIR 0.82 (experience) / 0.75 (remote); `benchmark_outputs/fairness_eval.json`; counterfactual updated to 7/10 |
| Calibration ECE/Brier | ✅ DONE | refit on 450 pairs (47 pos + 403 neg) → ECE 0.40→**0.032**; `data/models/calibration.json` (a=0.298, b=−2.116) |
| phase11 ANN latency | ✅ DONE | `benchmark_outputs/phase11_summary.csv` committed; rows added to `tab-latency.tex` |

---

## LEFT (environment-blocked here, not content TODOs)
1. **Recompile the PDFs**, `build/jaamas-manuscript.pdf`, `portal/information-sheet.pdf` are pre-edit; no LaTeX compiler is available offline in this sandbox → **compile on Overleaf** to confirm clean.
2. **Cross-encoder re-run**, the `ms-marco` model isn't cached and the network is blocked here, so the committed CE numbers (0.834, −0.108) stand; Section 6 was worded to avoid implying a stale baseline. Re-run only where the CE model/network is available (optional; was never a review TODO).
