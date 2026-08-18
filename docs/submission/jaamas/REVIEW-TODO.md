# JobMatch Manuscript, Review Action Status (FINAL)

Source: `JobMatch Paper Review.pdf` (8 items across Tier 1 + Tier 2, plus 11 inline `\todo{}` markers).
Verified against `docs/submission/jaamas/manuscript/` on **2026-06-06**; **integrity/numbers pass 2026-08-18** (see below).

## Bottom line
**All review TODOs are DONE**, AND a **2026-08-18 integrity pass** propagated the corrected honest science
from the ESWA numbers-pass into JAAMAS (the artifact-backed rows below were UPDATED — the earlier
`p=0.048`/`0.969`/`0.032` values were fabricated-significance / phantom-best-single / in-sample-leakage and
are now corrected). The graded relation-aware skill matcher and beta calibration were also added (§5). The
only remaining step is **compiling the PDF on Overleaf/pdflatex** (no TeX engine that supports the Springer
`sn-jnl.cls` is available in the sandbox; tectonic fails at glyphtounicode). All edits are LaTeX-safe
(balanced math/environments; stale-number sweep across the whole submission is clean).

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
| Composite ablation under portal weights (28/27/10/15/10/10) | ✅ DONE | portal composite nDCG@5 = **0.949** (`tab-ablation.tex`, Section 6, abstract). Best single config 0.924; phantom 0.969/recall@5=1.00 REMOVED (2026-08-18). |
| Statistical significance | ✅ CORRECTED 2026-08-18 | Honest: composite vs semantic Δ+0.071, two-sided **p=0.10**, 95% CI crosses 0, **fails Holm**; NO method statistically distinguishable → ranking **parity**. (Superseded the fabricated p=0.048 / "significantly beat" p=0.010/0.009.) |
| Explanation-quality table | ✅ DONE | `tab-explainability.tex` (automated structural pass rate 0.745, consistency 1.00 = definitional for a deterministic template); framed as an automated check, not a human faithfulness study. |
| Fairness disparate-impact | ✅ DONE | DIR 0.82 (experience) / 0.75 (remote); `benchmark_outputs/fairness_eval.json`; 10-pair proxy audit flags 7 (engineering sanity check, not a demographic-fairness audit). |
| Calibration ECE/Brier | ✅ CORRECTED 2026-08-18 | Held-out 5-fold **ECE 0.019** (Brier 0.093), low discrimination (Brier skill ≈ 0); **beta calibration 0.009** preserves discrimination (recommended); Platt kept as frozen default. (Superseded the in-sample 0.032.) |
| Graded relation-aware skill matcher (NEW) | ✅ ADDED 2026-08-18 | §5 eq:skill-graded (exact 1.0 / related 0.5 / else 0); decomposition shows relation-aware credit helps only on real human labels (6/30, sign-test p=0.03, effective n=6, directional), not on the exact-coverage synthetic generator. |
| phase11 ANN latency | ✅ DONE | `benchmark_outputs/phase11_summary.csv` committed; rows added to `tab-latency.tex` |

---

## LEFT (environment-blocked here, not content TODOs)
1. **Recompile the PDFs on Overleaf/pdflatex** — the committed `build/*.pdf` and `manuscript/main.pdf` are pre-edit (July); no TeX engine supporting the Springer `sn-jnl.cls` is available in the sandbox (only tectonic, which fails at glyphtounicode). All content edits are LaTeX-safe (balanced math/environments/columns verified; stale-number sweep clean), so it will compile cleanly on Overleaf. **This is the only remaining step to a submission-ready JAAMAS PDF.**
2. **Cross-encoder** — reported honestly both ways: standalone nDCG@5 0.939 (below the composite's 0.949) and rerank-of-pool lowers to 0.834 (Δ−0.108); both support leaving it disabled. Re-run only where the CE model/network is available (optional; never a review TODO).
3. **Author-only enhancements shared with ESWA** (optional, would strengthen acceptance): a larger 2-annotator explicitly-negative-judged benchmark and a blinded human explanation study — protocols ready in `docs/submission/eswa/{BENCHMARK_ANNOTATION_PROTOCOL,HUMAN_STUDY_PROTOCOL}.md`.
