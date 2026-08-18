# Bootstrap Significance · Benchmark Results

Generated: 2026-06-06T15:05:17.609008+00:00

## Setup

- Task: resume_to_jobs
- Baseline: **Semantic cosine** (`semantic_cosine`)
- Metrics: ndcg_at_k, mrr
- Resamples: 5,000 (seed=42)
- p-value: one-sided: fraction of bootstrap mean-diffs <= 0 (H1: compare > baseline)
- Top-K: 5

## Method means with 95% bootstrap CI

| Method | Metric | Mean | 95% CI |
|--------|--------|------|--------|
| BM25 (lexical) | nDCG@5 | 0.9023 | [0.8254, 0.9651] |
| BM25 (lexical) | MRR | 0.9178 | [0.8311, 0.9833] |
| Exact skill overlap | nDCG@5 | 0.7481 | [0.6218, 0.8613] |
| Exact skill overlap | MRR | 0.8158 | [0.6853, 0.9303] |
| Multimodal weighted blend | nDCG@5 | 0.9237 | [0.8698, 0.9710] |
| Multimodal weighted blend | MRR | 0.9611 | [0.9000, 1.0000] |
| RRF ensemble | nDCG@5 | 0.9131 | [0.8568, 0.9621] |
| RRF ensemble | MRR | 0.9444 | [0.8722, 1.0000] |
| Semantic cosine | nDCG@5 | 0.8782 | [0.7941, 0.9451] |
| Semantic cosine | MRR | 0.9315 | [0.8481, 1.0000] |
| Semantic euclidean-derived | nDCG@5 | 0.8782 | [0.7942, 0.9474] |
| Semantic euclidean-derived | MRR | 0.9315 | [0.8481, 1.0000] |
| Skills Jaccard | nDCG@5 | 0.7481 | [0.6220, 0.8590] |
| Skills Jaccard | MRR | 0.8158 | [0.6875, 0.9303] |
| Soft skill embedding | nDCG@5 | 0.8689 | [0.7829, 0.9366] |
| Soft skill embedding | MRR | 0.9107 | [0.8214, 0.9833] |
| TF-IDF cosine (lexical) | nDCG@5 | 0.9052 | [0.8387, 0.9604] |
| TF-IDF cosine (lexical) | MRR | 0.9178 | [0.8356, 0.9833] |

## Paired comparisons vs Semantic cosine

| Compare | Metric | Δ mean | 95% CI | p-value | sig@0.05 | W/L/T |
|---------|--------|--------|--------|---------|----------|-------|
| BM25 (lexical) | nDCG@5 | +0.0242 | [-0.0571, +0.0987] | 0.2612 | no | 13/4/13 |
| BM25 (lexical) | MRR | -0.0137 | [-0.0833, +0.0474] | 0.6496 | no | 3/2/25 |
| Exact skill overlap | nDCG@5 | -0.1301 | [-0.2640, +0.0005] | 0.9746 | no | 5/16/9 |
| Exact skill overlap | MRR | -0.1157 | [-0.2435, +0.0127] | 0.9632 | no | 1/7/22 |
| Multimodal weighted blend | nDCG@5 | +0.0456 | [+0.0024, +0.1208] | 0.0104 | yes | 6/1/23 |
| Multimodal weighted blend | MRR | +0.0296 | [+0.0000, +0.0889] | 0.3672 | no | 1/0/29 |
| RRF ensemble | nDCG@5 | +0.0350 | [+0.0033, +0.0835] | 0.0088 | yes | 8/3/19 |
| RRF ensemble | MRR | +0.0130 | [+0.0000, +0.0389] | 0.3512 | no | 1/0/29 |
| Semantic euclidean-derived | nDCG@5 | +0.0000 | [+0.0000, +0.0000] | 1.0000 | no | 0/0/30 |
| Semantic euclidean-derived | MRR | +0.0000 | [+0.0000, +0.0000] | 1.0000 | no | 0/0/30 |
| Skills Jaccard | nDCG@5 | -0.1301 | [-0.2636, -0.0011] | 0.9764 | no | 5/16/9 |
| Skills Jaccard | MRR | -0.1157 | [-0.2428, +0.0066] | 0.9688 | no | 1/7/22 |
| Soft skill embedding | nDCG@5 | -0.0093 | [-0.1105, +0.0980] | 0.5868 | no | 10/11/9 |
| Soft skill embedding | MRR | -0.0208 | [-0.1202, +0.0870] | 0.6602 | no | 2/4/24 |
| TF-IDF cosine (lexical) | nDCG@5 | +0.0270 | [-0.0526, +0.1047] | 0.2510 | no | 11/8/11 |
| TF-IDF cosine (lexical) | MRR | -0.0137 | [-0.1000, +0.0667] | 0.6250 | no | 3/3/24 |

## Significant improvements (p < 0.05)

- **Multimodal weighted blend** vs Semantic cosine on nDCG@5: Δ=+0.0456, p=0.0104, W/L/T=6/1/23
- **RRF ensemble** vs Semantic cosine on nDCG@5: Δ=+0.0350, p=0.0088, W/L/T=8/3/19
