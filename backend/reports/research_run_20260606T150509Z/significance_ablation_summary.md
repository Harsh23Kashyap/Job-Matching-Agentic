# Bootstrap Significance · Benchmark Results

Generated: 2026-06-06T15:05:20.888092+00:00

## Setup

- Task: resume_to_jobs
- Baseline: **Semantic only** (`semantic_only`)
- Metrics: ndcg_at_k, mrr
- Resamples: 5,000 (seed=42)
- p-value: one-sided: fraction of bootstrap mean-diffs <= 0 (H1: compare > baseline)
- Top-K: 5

## Method means with 95% bootstrap CI

| Method | Metric | Mean | 95% CI |
|--------|--------|------|--------|
| Compensation only | nDCG@5 | 0.3929 | [0.2695, 0.5222] |
| Compensation only | MRR | 0.4573 | [0.3281, 0.5948] |
| Experience only | nDCG@5 | 0.3256 | [0.2148, 0.4477] |
| Experience only | MRR | 0.3838 | [0.2723, 0.5129] |
| Full composite | nDCG@5 | 0.9492 | [0.8720, 0.9931] |
| Full composite | MRR | 0.9722 | [0.9167, 1.0000] |
| Location only | nDCG@5 | 0.3354 | [0.2210, 0.4605] |
| Location only | MRR | 0.3878 | [0.2747, 0.5116] |
| RRF ensemble | nDCG@5 | 0.5643 | [0.4406, 0.6798] |
| RRF ensemble | MRR | 0.5703 | [0.4510, 0.6956] |
| Semantic only | nDCG@5 | 0.8782 | [0.7905, 0.9457] |
| Semantic only | MRR | 0.9315 | [0.8426, 1.0000] |
| Semantic + skills | nDCG@5 | 0.9170 | [0.8619, 0.9616] |
| Semantic + skills | MRR | 0.9611 | [0.9000, 1.0000] |
| Semantic + skills + experience | nDCG@5 | 0.9163 | [0.8618, 0.9626] |
| Semantic + skills + experience | MRR | 0.9611 | [0.9000, 1.0000] |
| Skills only | nDCG@5 | 0.7481 | [0.6184, 0.8587] |
| Skills only | MRR | 0.8158 | [0.6884, 0.9333] |

## Paired comparisons vs Semantic only

| Compare | Metric | Δ mean | 95% CI | p-value | sig@0.05 | W/L/T |
|---------|--------|--------|--------|---------|----------|-------|
| Compensation only | nDCG@5 | -0.4852 | [-0.6285, -0.3458] | 1.0000 | no | 2/27/1 |
| Compensation only | MRR | -0.4742 | [-0.6104, -0.3283] | 1.0000 | no | 1/20/9 |
| Experience only | nDCG@5 | -0.5526 | [-0.7028, -0.3902] | 1.0000 | no | 3/25/2 |
| Experience only | MRR | -0.5477 | [-0.6765, -0.4115] | 1.0000 | no | 1/23/6 |
| Full composite | nDCG@5 | +0.0711 | [-0.0158, +0.1673] | 0.0478 | yes | 10/3/17 |
| Full composite | MRR | +0.0407 | [-0.0222, +0.1259] | 0.1798 | no | 2/1/27 |
| Location only | nDCG@5 | -0.5427 | [-0.6830, -0.3887] | 1.0000 | no | 5/25/0 |
| Location only | MRR | -0.5436 | [-0.6633, -0.4089] | 1.0000 | no | 1/23/6 |
| RRF ensemble | nDCG@5 | -0.3139 | [-0.4596, -0.1753] | 1.0000 | no | 6/21/3 |
| RRF ensemble | MRR | -0.3611 | [-0.4824, -0.2308] | 1.0000 | no | 1/18/11 |
| Semantic + skills | nDCG@5 | +0.0388 | [-0.0078, +0.1199] | 0.0992 | no | 5/2/23 |
| Semantic + skills | MRR | +0.0296 | [+0.0000, +0.0889] | 0.3576 | no | 1/0/29 |
| Semantic + skills + experience | nDCG@5 | +0.0381 | [-0.0086, +0.1147] | 0.1054 | no | 5/3/22 |
| Semantic + skills + experience | MRR | +0.0296 | [+0.0000, +0.0889] | 0.3600 | no | 1/0/29 |
| Skills only | nDCG@5 | -0.1301 | [-0.2626, -0.0008] | 0.9760 | no | 5/16/9 |
| Skills only | MRR | -0.1157 | [-0.2477, +0.0091] | 0.9668 | no | 1/7/22 |

## Significant improvements (p < 0.05)

- **Full composite** vs Semantic only on nDCG@5: Δ=+0.0711, p=0.0478, W/L/T=10/3/17
