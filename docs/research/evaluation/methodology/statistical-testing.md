# Statistical Testing

## Method

We use **paired bootstrap resampling** on query-level scores to assess whether method B improves over baseline A beyond chance on this fixed corpus.

### Procedure

1. For each query *q*, compute score *s_A(q)* and *s_B(q)* for baseline and compare method.
2. Form paired differences *d(q) = s_B(q) − s_A(q)*.
3. Resample queries **with replacement** 5,000 times (seed=42).
4. For each resample, compute mean difference; sort to form **95% CI**.
5. **p-value (one-sided):** fraction of bootstrap mean-diffs ≤ 0, testing H₁: compare > baseline.

### Metrics tested

- **nDCG@K** (primary ranking quality metric)
- **MRR** (first-hit metric)

Precision, recall, and MAP are not bootstrap-tested in the default suite.

### Win / loss / tie

Per query, before bootstrap:

| Outcome | Condition |
|---------|-----------|
| Win | compare score > baseline + ε |
| Loss | compare score < baseline − ε |
| Tie | \|difference\| ≤ ε |

ε = 1e−12 (floating-point tie threshold).

## Baselines

| Study | Default baseline |
|-------|------------------|
| Embedding significance (4a) | Semantic cosine |
| Ablation significance (4b) | Semantic only |

## Interpretation caveats

- **n = 30 queries** — wide confidence intervals; non-significant ≠ no effect
- Bootstrap assumes queries are exchangeable; no multiple-comparison correction across methods
- One-sided p-values test improvement only; degradations require inspecting sign of Δ and CI
- Results are **corpus-specific**; do not extrapolate to production traffic

## Artifacts

| File | Contents |
|------|----------|
| `significance_report.json` | Full JSON (embedding study) |
| `significance_comparisons.csv` | Table-ready paired tests |
| `significance_methods.csv` | Per-method means + CI |
| `artifacts/tables/table_significance.csv` | Unified export |

## Implementation

- `backend/benchmarks/significance.py`
- CLI: `python -m benchmarks.run_significance`

## Example reading

```
Multimodal weighted blend | nDCG@5 | Δ=+0.046 | CI=[+0.002, +0.120] | p=0.014 | W/L/T=6/1/23
```

Multimodal blend beats semantic cosine on **6 of 30** queries outright, loses on **1**, ties on **23**. Bootstrap mean gain is positive with CI excluding zero at ~97.5%; one-sided p = 0.014 → significant at α=0.05.
