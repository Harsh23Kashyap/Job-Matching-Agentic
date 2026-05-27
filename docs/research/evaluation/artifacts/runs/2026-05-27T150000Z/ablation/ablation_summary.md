# Ablation Study — Composite Matching Components

Generated: 2026-05-27T14:56:36.574536+00:00

## Setup

- Task: resume_to_jobs
- Corpus: 30 candidates, 15 jobs
- Labeled queries: 30
- Top-K: 5
- Skills mode: jaccard
- Embedding model: `all-MiniLM-L6-v2`

Production composite weights (full model):

| Component | Weight |
|-----------|--------|
| Semantic | 40% |
| Skills | 30% |
| Experience | 15% |
| Compensation | 10% |
| Location | 5% |

## Summary (macro-averaged)

| Variant | Category | P@K | R@K | MRR | nDCG@K | MAP | Latency (ms) |
|---------|----------|-----|-----|-----|--------|-----|--------------|
| Semantic only | single | 0.267 | 0.867 | 0.931 | 0.878 | 0.810 | 0.22 |
| Skills only | single | 0.233 | 0.733 | 0.816 | 0.748 | 0.681 | 0.04 |
| Experience only | single | 0.160 | 0.467 | 0.384 | 0.326 | 0.314 | 0.02 |
| Compensation only | single | 0.187 | 0.567 | 0.457 | 0.393 | 0.387 | 0.02 |
| Location only | single | 0.167 | 0.467 | 0.388 | 0.335 | 0.328 | 0.02 |
| Semantic + skills | partial | 0.287 | 0.933 | 0.961 | 0.917 | 0.867 | 0.28 |
| Semantic + skills + experience | partial | 0.287 | 0.933 | 0.961 | 0.917 | 0.866 | 0.27 |
| Full composite | full | 0.307 | 0.983 | 0.944 | 0.942 | 0.896 | 0.26 |
| RRF ensemble | ensemble | 0.233 | 0.717 | 0.570 | 0.564 | 0.497 | 0.32 |

## Findings

- Best nDCG@5: **Full composite** (0.942)
- Full composite nDCG@5: 0.942
- Full composite vs best delta: +0.000

## Table-ready long format

See `ablation_table.csv` for columns: `variant`, `metric`, `top_k`, `score`, `latency_ms`.

| Variant | Metric | top_k | Score | latency_ms |
|---------|--------|-------|-------|------------|
| Semantic only | Precision@K | 5 | 0.2667 | 0.22 |
| Semantic only | Recall@K | 5 | 0.8667 | 0.22 |
| Semantic only | MRR | 5 | 0.9315 | 0.22 |
| Semantic only | nDCG@K | 5 | 0.8782 | 0.22 |
| Semantic only | MAP | 5 | 0.8099 | 0.22 |
| Skills only | Precision@K | 5 | 0.2333 | 0.04 |
| Skills only | Recall@K | 5 | 0.7333 | 0.04 |
| Skills only | MRR | 5 | 0.8158 | 0.04 |
| Skills only | nDCG@K | 5 | 0.7481 | 0.04 |
| Skills only | MAP | 5 | 0.6809 | 0.04 |
| Experience only | Precision@K | 5 | 0.1600 | 0.02 |
| Experience only | Recall@K | 5 | 0.4667 | 0.02 |
| Experience only | MRR | 5 | 0.3838 | 0.02 |
| Experience only | nDCG@K | 5 | 0.3256 | 0.02 |
| Experience only | MAP | 5 | 0.3136 | 0.02 |
| Compensation only | Precision@K | 5 | 0.1867 | 0.02 |
| Compensation only | Recall@K | 5 | 0.5667 | 0.02 |
| Compensation only | MRR | 5 | 0.4573 | 0.02 |
| Compensation only | nDCG@K | 5 | 0.3929 | 0.02 |
| Compensation only | MAP | 5 | 0.3872 | 0.02 |
| Location only | Precision@K | 5 | 0.1667 | 0.02 |
| Location only | Recall@K | 5 | 0.4667 | 0.02 |
| Location only | MRR | 5 | 0.3878 | 0.02 |
| Location only | nDCG@K | 5 | 0.3354 | 0.02 |
| Location only | MAP | 5 | 0.3276 | 0.02 |
| Semantic + skills | Precision@K | 5 | 0.2867 | 0.28 |
| Semantic + skills | Recall@K | 5 | 0.9333 | 0.28 |
| Semantic + skills | MRR | 5 | 0.9611 | 0.28 |
| Semantic + skills | nDCG@K | 5 | 0.9170 | 0.28 |
| Semantic + skills | MAP | 5 | 0.8670 | 0.28 |
| Semantic + skills + experience | Precision@K | 5 | 0.2867 | 0.27 |
| Semantic + skills + experience | Recall@K | 5 | 0.9333 | 0.27 |
| Semantic + skills + experience | MRR | 5 | 0.9611 | 0.27 |
| Semantic + skills + experience | nDCG@K | 5 | 0.9167 | 0.27 |
| Semantic + skills + experience | MAP | 5 | 0.8664 | 0.27 |
| Full composite | Precision@K | 5 | 0.3067 | 0.26 |
| Full composite | Recall@K | 5 | 0.9833 | 0.26 |
| Full composite | MRR | 5 | 0.9444 | 0.26 |
| Full composite | nDCG@K | 5 | 0.9417 | 0.26 |
| Full composite | MAP | 5 | 0.8959 | 0.26 |
| RRF ensemble | Precision@K | 5 | 0.2333 | 0.32 |
| RRF ensemble | Recall@K | 5 | 0.7167 | 0.32 |
| RRF ensemble | MRR | 5 | 0.5703 | 0.32 |
| RRF ensemble | nDCG@K | 5 | 0.5643 | 0.32 |
| RRF ensemble | MAP | 5 | 0.4973 | 0.32 |
