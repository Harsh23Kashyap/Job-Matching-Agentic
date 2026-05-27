# Study 2 — Lexical vs Embedding Baselines

## Protocol

- Same corpus and labels as Study 1 (K=5)
- Lexical: BM25, TF-IDF cosine, exact skill overlap
- Embedding: semantic, skills, soft embed, multimodal, RRF
- Latency measured as mean ms per query (exhaustive scan)

## Lexical baselines

| method | P@K | R@K | MRR | nDCG@K | MAP | latency_ms |
| --- | --- | --- | --- | --- | --- | --- |
| BM25 (lexical) | 0.307 | 0.983 | 0.912 | 0.894 | 0.838 | 0.112 |
| TF-IDF cosine (lexical) | 0.293 | 0.950 | 0.918 | 0.898 | 0.842 | 0.072 |
| Exact skill overlap | 0.233 | 0.733 | 0.816 | 0.748 | 0.681 | 0.026 |

## Embedding strategies

| method | P@K | R@K | MRR | nDCG@K | MAP | latency_ms |
| --- | --- | --- | --- | --- | --- | --- |
| Semantic cosine | 0.267 | 0.867 | 0.931 | 0.878 | 0.810 | 0.226 |
| Semantic euclidean-derived | 0.267 | 0.867 | 0.931 | 0.878 | 0.810 | 0.210 |
| Skills Jaccard | 0.233 | 0.733 | 0.816 | 0.748 | 0.681 | 0.034 |
| Soft skill embedding | 0.280 | 0.900 | 0.911 | 0.869 | 0.829 | 15.531 |
| Multimodal weighted blend | 0.287 | 0.933 | 0.961 | 0.924 | 0.867 | 0.258 |
| RRF ensemble | 0.293 | 0.950 | 0.944 | 0.913 | 0.845 | 0.953 |

## Observations

- Best lexical: **TF-IDF cosine (lexical)** (nDCG=0.898, 0.07 ms/query)
- Best embedding: **Multimodal weighted blend** (nDCG=0.924, 0.26 ms/query)
