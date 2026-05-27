# Benchmark / research tests

Offline evaluation and regression gates for paper metrics. Slower than unit tests; may read `data/` and `backend/benchmark_outputs/`.

| File | Scope |
|------|--------|
| `test_eval_regression.py` | Golden nDCG gates vs `data/expected/` |
| `test_research_pipeline.py` | End-to-end research driver smoke |
| `test_comparison_baselines.py` | Baseline method comparison |
| `test_composite_eval.py` | Composite scoring ablation |
| `test_ablation.py` | Weight ablation |
| `test_significance.py` | Paired significance tests |
| `test_fairness_audit.py` | Fairness audit report |
| `test_explainability_eval.py` | Explainability metrics |
| `test_paper_tables.py` | LaTeX table generation |
| `test_research_export.py` | Export to `docs/research/evaluation/` |
| `test_dataset_validation.py` | Corpus schema checks |
| `test_synthetic_dataset.py` | Synthetic pair generation |
| `test_benchmark_framework.py` | Shared benchmark helpers |

Run from repo root:

```bash
cd backend && source .venv/bin/activate
pytest ../tests/benchmarks -q
```

Skip slow cross-encoder stages when iterating: use env flags documented in `backend/scripts/run_research_pipeline.py`.
