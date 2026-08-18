# PROJECT_STATUS — JobMatch → ESWA revision

**Branch:** `eswa-final-evaluation` (baseline `02a700e`) · **Updated:** 2026-08-17
**Control plane:** `research/` · **Baseline audit:** `research/reports/BASELINE_AUDIT.md`

## Environment (verified 2026-08-17)
- Python 3.11.15 venv at `backend/.venv` — torch 2.13.0, sentence-transformers 5.1.2, chromadb 0.4.24, scikit-learn 1.9.0, scipy, numpy 1.26.4 **import OK → experiments runnable**.
- node v24.18.0 OK · `pdftotext` OK · **`pdflatex` ABSENT (LaTeX build blocked)** · ollama present, no models pulled.
- No external LLM/API calls permitted — LLM needs route through headless `claude -p` / Kiro.

## Where we are
- **Phase 0 (freeze + control plane): COMPLETE** — branch created, baseline snapshot (68 files → `research/audit/baseline/`), control files created, baseline audit written.
- **Phase 1 (code audit): COMPLETE via 9-agent audit** — 12 BLOCKER, ~15 HIGH findings; see BASELINE_AUDIT.md.
- **Next: Phase 1 reproducibility verification** (re-run existing benchmarks in the fresh venv, compare to snapshot) → then blocker-first remediation.

## Blocker-first execution order (deviates from strict 1→47; dependency-driven)
1. **Reproduce baseline numbers** in the clean venv (confirm 0.949/0.0192/0.917/50-pair are real & deterministic). [repro gate]
2. **Fix integrity code bugs** (B3 hash-seed, B10 5-vs-6-channel, B8/B12 calibration target + closed-world disclosure, H8 XGBoost→LR naming, H11 decomposition/semantic bounds, tie-break). Add automated leakage/weight-sum/decomposition checks + tests.
3. **Wire `extended_evaluation.py` into a runner + CI**, run to completion (incl. missing `scalability.json`), commit artifacts. [H9]
4. **Add job-held-out fold** (H3) + real baselines where feasible (LambdaMART/two-tower; CareerBERT if model obtainable) (H4).
5. **Benchmark expansion** (Phase 2) — build annotation harness; LLM-assisted label proposal via `claude -p` (clearly non-human); **human labels = user blocker**.
6. **Regenerate all tables/figures from artifacts** (Phase 20/28) + numerical-claims verifier.
7. **Rewrite manuscript to honest numbers + reframe** (drop multi-agent/trustworthy/fairness-audit/GPU-hours/phantom 0.969); scrub paths/watermark/placeholders/anonymity.
8. **Figures/diagrams** to match implementation (drawio + dataviz).
9. **Final QA**: PDF (blocked on pdflatex), cross-document, anonymity, placeholder scan; final hostile review + reproducibility audit.

## Open user-blockers
- Human annotation (Phase 2) · LaTeX toolchain (PDF build) · external DOI/ORCID/GitHub/submission. See BASELINE_AUDIT §"Genuine blockers".
