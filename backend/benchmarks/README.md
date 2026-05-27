# Benchmarks

Reproducible evaluation against the fixed 30-CV / 15-job / 47-pair corpus.

## Run (from `backend/` with venv active)

```bash
python -m benchmarks.run_comparison          # lexical + embedding → comparison_table.csv
python -m benchmarks.run_ablation            # composite ablation study → ablation_summary.md
python -m benchmarks.run_significance      # paired bootstrap nDCG/MRR vs baseline
python -m benchmarks.run_eval              # embedding strategies only
python -m benchmarks.smoke_eval              # quick 5-query smoke
python -m benchmarks.paper_progression --skip-cross-encoder
python -m benchmarks.phase11 --stores chroma
```

Or from repo root:
- `bash scripts/run_benchmark.sh` — lexical vs embedding comparison
- `bash scripts/run_benchmark_eval.sh` — embedding-only suite
- `bash scripts/run_ablation.sh` — composite component ablation study
- `bash scripts/run_significance.sh` — paired bootstrap significance (nDCG@K, MRR)
- `bash scripts/run_research_suite.sh` — **full research archive** → `docs/research/evaluation/`
- `bash scripts/run_fairness_audit.sh` — synthetic fairness & bias audit
- `bash scripts/run_explainability_eval.sh` — match explanation quality evaluation
- `bash scripts/generate_research_dataset.sh` — synthetic 100×50 research corpus
- `bash scripts/generate_paper_tables.sh` — paper-ready Markdown/CSV/LaTeX tables
- `bash scripts/run_research_pipeline.sh` — **full pipeline** → `backend/reports/research_run_<timestamp>/`

Outputs:
- **Comparison table:** `backend/reports/comparison_table.csv` (method, metric, top_k, score, latency_ms)
- **Ablation study:** `backend/reports/ablation_summary.md`, `ablation_table.csv`, `ablation_report.json`
- **Significance:** `backend/reports/significance_summary.md`, `significance_report.json`, `significance_comparisons.csv`
- **Embedding reports:** `backend/reports/benchmark_*.json/csv`
- **Legacy progression:** `backend/benchmark_outputs/`

## Key drivers

| Module | Purpose |
|--------|---------|
| `paper_progression.py` | Score-improvement ladder (Table 9 regression) |
| `phase11.py` | ANN sweep, Chroma vs Qdrant latency |
| `smoke_eval.py` | Quick sanity check |
| `run_comparison.py` | **Lexical vs embedding** — BM25, TF-IDF, exact overlap + dense strategies |
| `comparison.py` | Table report writer (method, metric, top_k, score, latency_ms) |
| `baseline_strategies.py` | BM25, TF-IDF cosine, exact skill overlap (offline only) |
| `run_eval.py` | Embedding strategy suite (no lexical) |
| `run_ablation.py` | **Ablation study** — single/partial/full composite + RRF |
| `ablation.py` | Ablation runner + Markdown/CSV/JSON writers |
| `ablation_scoring.py` | Offline single/partial composite scorers |
| `run_significance.py` | **Bootstrap significance** — paired nDCG@K & MRR vs baseline |
| `significance.py` | 5000-resample bootstrap CI, p-value, win/loss/tie |
| `research_export.py` | Export full bundle → `docs/research/evaluation/` |
| `run_research_suite.py` | Run all studies + export paper archive |
| `framework.py` | Benchmark runner and report writers |
| `strategies.py` | Offline strategy registry (isolated from production composite) |
| `metrics.py` | P@K, R@K, MRR, nDCG@K, MAP |
| `eval_data.py` | Load `data/eval_pairs.json` |
| `fairness_eval.py` | Legacy DI baseline on eval corpus (experience/remote proxies) |
| `fairness_profiles.py` | Synthetic controlled profile pairs (no real-user inference) |
| `fairness_audit.py` | **Fairness audit** — rank stability, score delta, explanation drift |
| `run_fairness_audit.py` | CLI for synthetic bias audit |
| `explainability_checks.py` | Automated explanation quality checks |
| `explainability_eval.py` | **Explainability eval** — faithfulness, consistency, specificity |
| `run_explainability_eval.py` | CLI for explanation evaluation |
| `synthetic_dataset/` | **Research corpus generator** (100 CV / 50 jobs / labeled pairs) |
| `run_generate_research_dataset.py` | CLI → `data/research/` |
| `paper_tables/` | **Paper table generator** (Markdown/CSV/LaTeX) |
| `run_paper_tables.py` | CLI → `docs/research/evaluation/paper_tables/` |
| `research_pipeline.py` | **Full pipeline orchestrator** (9 stages, one run folder) |
| `dataset_validation.py` | Corpus validation before benchmarks |
| `composite_eval.py` | Production composite scoring evaluation |
| `run_research_pipeline.py` (in `backend/scripts/`) | CLI → `backend/reports/research_run_<timestamp>/` |

## Regression tests

`tests/benchmarks/test_eval_regression.py` gates against expected floats in `data/expected/`.

Corpus files: [../../data/README.md](../../data/README.md)
