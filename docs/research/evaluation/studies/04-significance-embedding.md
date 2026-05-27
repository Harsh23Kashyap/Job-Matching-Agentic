# Study 4a — Bootstrap Significance (Embedding Strategies)

## Setup

- **Baseline:** Semantic cosine (`semantic_cosine`)
- **Metrics:** ndcg_at_k, mrr
- **Resamples:** 5,000 (seed=42)
- **p-value:** one-sided: fraction of bootstrap mean-diffs <= 0 (H1: compare > baseline)
- Compares embedding suite vs **Semantic cosine** baseline

## Method means with 95% bootstrap CI

| Method | Metric | Mean | 95% CI |
|--------|--------|------|--------|
| Multimodal weighted blend | nDCG@5 | 0.9237 | [0.8696, 0.9698] |
| Multimodal weighted blend | MRR | 0.9611 | [0.9000, 1.0000] |
| RRF ensemble | nDCG@5 | 0.9131 | [0.8564, 0.9623] |
| RRF ensemble | MRR | 0.9444 | [0.8778, 1.0000] |
| Semantic cosine | nDCG@5 | 0.8782 | [0.7908, 0.9440] |
| Semantic cosine | MRR | 0.9315 | [0.8463, 1.0000] |
| Semantic euclidean-derived | nDCG@5 | 0.8782 | [0.7955, 0.9454] |
| Semantic euclidean-derived | MRR | 0.9315 | [0.8481, 1.0000] |
| Skills Jaccard | nDCG@5 | 0.7481 | [0.6236, 0.8554] |
| Skills Jaccard | MRR | 0.8158 | [0.6837, 0.9300] |
| Soft skill embedding | nDCG@5 | 0.8689 | [0.7840, 0.9386] |
| Soft skill embedding | MRR | 0.9107 | [0.8190, 0.9833] |

## Paired comparisons vs Semantic cosine

| Compare | Metric | Δ mean | 95% CI | p-value | sig@0.05 | W/L/T |
|---------|--------|--------|--------|---------|----------|-------|
| Multimodal weighted blend | nDCG@5 | +0.0456 | [+0.0018, +0.1196] | 0.0142 | yes | 6/1/23 |
| Multimodal weighted blend | MRR | +0.0296 | [+0.0000, +0.0889] | 0.3430 | no | 1/0/29 |
| RRF ensemble | nDCG@5 | +0.0350 | [+0.0028, +0.0826] | 0.0080 | yes | 8/3/19 |
| RRF ensemble | MRR | +0.0130 | [+0.0000, +0.0389] | 0.3640 | no | 1/0/29 |
| Semantic euclidean-derived | nDCG@5 | +0.0000 | [+0.0000, +0.0000] | 1.0000 | no | 0/0/30 |
| Semantic euclidean-derived | MRR | +0.0000 | [+0.0000, +0.0000] | 1.0000 | no | 0/0/30 |
| Skills Jaccard | nDCG@5 | -0.1301 | [-0.2650, +0.0068] | 0.9696 | no | 5/16/9 |
| Skills Jaccard | MRR | -0.1157 | [-0.2458, +0.0085] | 0.9644 | no | 1/7/22 |
| Soft skill embedding | nDCG@5 | -0.0093 | [-0.1128, +0.1036] | 0.5766 | no | 10/11/9 |
| Soft skill embedding | MRR | -0.0208 | [-0.1202, +0.0848] | 0.6650 | no | 2/4/24 |
