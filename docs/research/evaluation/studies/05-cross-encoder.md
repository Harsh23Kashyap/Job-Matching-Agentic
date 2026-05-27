# Study 5 — Two-Stage Cross-Encoder Reranking

## Setup

- **Strategy:** composite
- **Top-K:** 5
- **Rerank pool:** 20
- **Queries:** 30

## Quality summary

| Metric | Bi-encoder | + Cross-encoder | Δ |
|--------|------------|-----------------|---|
| nDCG@K | 0.942 | 0.834 | -0.108 |
| MRR | — | — | -0.112 |

## Latency

- Bi-encoder avg: 0.41 ms/query
- With CE avg: 141.75 ms/query
- CE overhead: 141.37 ms/query

## Note

Cross-encoder is **not enabled in production UI by default**. Requires `ENABLE_CROSS_ENCODER_RERANK=true` and explicit `use_cross_encoder` on match API.
