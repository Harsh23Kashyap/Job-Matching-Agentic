# Bootstrap Significance · Benchmark Results

Generated: 2026-05-27T14:59:59.969107+00:00

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
| Compensation only | nDCG@5 | 0.3929 | [0.2699, 0.5191] |
| Compensation only | MRR | 0.4573 | [0.3285, 0.5939] |
| Experience only | nDCG@5 | 0.3256 | [0.2153, 0.4413] |
| Experience only | MRR | 0.3838 | [0.2717, 0.5048] |
| Full composite | nDCG@5 | 0.9417 | [0.8809, 0.9872] |
| Full composite | MRR | 0.9444 | [0.8778, 1.0000] |
| Location only | nDCG@5 | 0.3354 | [0.2228, 0.4581] |
| Location only | MRR | 0.3878 | [0.2773, 0.5177] |
| RRF ensemble | nDCG@5 | 0.5643 | [0.4423, 0.6873] |
| RRF ensemble | MRR | 0.5703 | [0.4510, 0.6969] |
| Semantic only | nDCG@5 | 0.8782 | [0.7955, 0.9456] |
| Semantic only | MRR | 0.9315 | [0.8463, 1.0000] |
| Semantic + skills | nDCG@5 | 0.9170 | [0.8632, 0.9629] |
| Semantic + skills | MRR | 0.9611 | [0.9000, 1.0000] |
| Semantic + skills + experience | nDCG@5 | 0.9167 | [0.8618, 0.9630] |
| Semantic + skills + experience | MRR | 0.9611 | [0.9000, 1.0000] |
| Skills only | nDCG@5 | 0.7481 | [0.6200, 0.8638] |
| Skills only | MRR | 0.8158 | [0.6878, 0.9302] |

## Paired comparisons vs Semantic only

| Compare | Metric | Δ mean | 95% CI | p-value | sig@0.05 | W/L/T |
|---------|--------|--------|--------|---------|----------|-------|
| Compensation only | nDCG@5 | -0.4852 | [-0.6269, -0.3371] | 1.0000 | no | 2/27/1 |
| Compensation only | MRR | -0.4742 | [-0.6128, -0.3314] | 1.0000 | no | 1/20/9 |
| Experience only | nDCG@5 | -0.5526 | [-0.6998, -0.3962] | 1.0000 | no | 3/25/2 |
| Experience only | MRR | -0.5477 | [-0.6755, -0.4128] | 1.0000 | no | 1/23/6 |
| Full composite | nDCG@5 | +0.0635 | [+0.0034, +0.1437] | 0.0204 | yes | 12/2/16 |
| Full composite | MRR | +0.0130 | [-0.0611, +0.0944] | 0.3832 | no | 2/1/27 |
| Location only | nDCG@5 | -0.5427 | [-0.6883, -0.3894] | 1.0000 | no | 5/25/0 |
| Location only | MRR | -0.5436 | [-0.6684, -0.4159] | 1.0000 | no | 1/23/6 |
| RRF ensemble | nDCG@5 | -0.3139 | [-0.4634, -0.1694] | 1.0000 | no | 6/21/3 |
| RRF ensemble | MRR | -0.3611 | [-0.4864, -0.2333] | 1.0000 | no | 1/18/11 |
| Semantic + skills | nDCG@5 | +0.0388 | [-0.0078, +0.1167] | 0.0936 | no | 5/2/23 |
| Semantic + skills | MRR | +0.0296 | [+0.0000, +0.0889] | 0.3616 | no | 1/0/29 |
| Semantic + skills + experience | nDCG@5 | +0.0385 | [-0.0082, +0.1135] | 0.1052 | no | 5/2/23 |
| Semantic + skills + experience | MRR | +0.0296 | [+0.0000, +0.0889] | 0.3540 | no | 1/0/29 |
| Skills only | nDCG@5 | -0.1301 | [-0.2640, +0.0027] | 0.9716 | no | 5/16/9 |
| Skills only | MRR | -0.1157 | [-0.2402, +0.0067] | 0.9692 | no | 1/7/22 |

## Significant improvements (p < 0.05)

- **Full composite** vs Semantic only on nDCG@5: Δ=+0.0635, p=0.0204, W/L/T=12/2/16
