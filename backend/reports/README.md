# Benchmark reports

Generated offline evaluation artifacts from the research benchmark framework.

## Full research pipeline (recommended)

One command runs all nine stages into a timestamped folder:

```bash
python backend/scripts/run_research_pipeline.py
# → backend/reports/research_run_<timestamp>/
```

From repo root: `bash scripts/run_research_pipeline.sh`

Stages: dataset validation → baseline comparison → composite scoring → ablation → cross-encoder (if enabled) → significance → fairness → explainability → paper tables.

Use `--skip-cross-encoder` to skip the slow CE step, or `--enable-cross-encoder` to force it.

## Generate reports (individual)

### Lexical vs embedding comparison (table-ready)

```bash
python -m benchmarks.run_comparison
# → comparison_table.csv  (method, metric, top_k, score, latency_ms)
```

From repo root: `bash scripts/run_benchmark.sh`

### Embedding strategies only

```bash
python -m benchmarks.run_eval
bash scripts/run_benchmark_eval.sh
```

Optional flags:

```bash
python -m benchmarks.run_comparison --top-k 5 --prefix exp1
python -m benchmarks.run_comparison --embedding-only   # skip BM25/TF-IDF/exact overlap
```

## Output files

| File | Contents |
|------|----------|
| `comparison_table.csv` | **Table-ready:** method, metric, top_k, score, latency_ms |
| `comparison_table.json` | Same rows + meta |
| `comparison_summary.json` | One row per method with all metrics + latency |
| `benchmark_report.json` | Full embedding-only report (from `run_eval`) |
| `benchmark_summary.csv` | One row per embedding strategy |
| `benchmark_per_query.csv` | Per-query breakdown |

## Strategies compared

**Lexical / symbolic baselines**
1. BM25 (lexical)  
2. TF-IDF cosine (lexical)  
3. Exact skill overlap  

**Embedding-based** (same as before)
4. Semantic cosine  
5. Semantic euclidean-derived  
6. Skills Jaccard  
7. Soft skill embedding  
8. Multimodal weighted blend  
9. RRF ensemble  

## Metrics

Precision@K, Recall@K, MRR, nDCG@K, MAP — plus **latency_ms** (average per query).

Labels: `data/eval_pairs.json` (graded 0–2; binary relevant = relevance > 0 for P/R/MRR/MAP).

**Note:** Offline research only. Production portal matching stays on `strategy: composite`. Cross-encoder rerank is opt-in via `ENABLE_CROSS_ENCODER_RERANK=true` + `use_cross_encoder` on match API (admin console only by default).

### Cross-encoder two-stage report

```bash
ENABLE_CROSS_ENCODER_RERANK=true python -m benchmarks.run_cross_encoder_report
# → cross_encoder_table.csv (quality, latency, rank changes)
```

### Ablation study (composite components)

```bash
python -m benchmarks.run_ablation
# → ablation_summary.md, ablation_table.csv, ablation_report.json
```

### Bootstrap significance (paired nDCG@K & MRR)

```bash
python -m benchmarks.run_significance
# → significance_summary.md, significance_report.json, significance_comparisons.csv
```

Options:

```bash
python -m benchmarks.run_significance --source comparison --baseline semantic_cosine
python -m benchmarks.run_significance --source ablation --baseline semantic_only
python -m benchmarks.run_significance --per-query-csv benchmark_per_query.csv
```

### Fairness & bias audit (synthetic profiles)

```bash
python -m benchmarks.run_fairness_audit
# → fairness_audit_summary.md, fairness_audit_report.json, fairness_audit_flagged.csv
```

Uses `data/fairness_audit_profiles.json` — **fabricated counterfactuals only**; never infers protected attributes from real users.

### Explainability evaluation

```bash
python -m benchmarks.run_explainability_eval
# → explainability_summary.md, explainability_flagged.csv, explainability_consistency.csv
```

Checks: skill mention coverage, hallucination detection, score-component alignment, cross-profile consistency.

### Paper tables (manuscript copy-paste)

```bash
python -m benchmarks.run_paper_tables
# → docs/research/evaluation/paper_tables/*.md, *.csv, *.tex
```
