# Study 1 · Embedding Retrieval Strategies

Generated from: `artifacts/.../embedding/benchmark_report.json`

## Protocol

- **Task:** resume → jobs (exhaustive ranking over 15 jobs per query)
- **Corpus:** 30 candidates, 15 jobs
- **Queries:** 30 labeled in `data/eval_pairs.json`
- **Top-K:** 5
- **Embedding model:** `all-MiniLM-L6-v2`
- **Multimodal semantic weight:** 0.7
- **RRF k:** 60

## Strategies

| Key | Method | Description |
|-----|--------|-------------|
| `semantic_cosine` | Semantic cosine | Bi-encoder cosine similarity on document embeddings. |
| `semantic_euclidean` | Semantic euclidean-derived | 1 / (1 + L2 distance) on document embeddings. |
| `skills_jaccard` | Skills Jaccard | Jaccard overlap on canonicalized required skills (skills-only signal). |
| `soft_skill_embed` | Soft skill embedding | Mean max cosine between required job skills and resume skill embeddings. |
| `multimodal_weighted` | Multimodal weighted blend | Weighted blend: semantic_weight=0.7, skills_mode=jaccard. |
| `rrf_ensemble` | RRF ensemble | Reciprocal rank fusion (k=60) over the five base rankers above. |

## Results (macro-averaged)

| method | P@K | R@K | MRR | nDCG@K | MAP |
| --- | --- | --- | --- | --- | --- |
| Semantic cosine | 0.267 | 0.867 | 0.931 | 0.878 | 0.810 |
| Semantic euclidean-derived | 0.267 | 0.867 | 0.931 | 0.878 | 0.810 |
| Skills Jaccard | 0.233 | 0.733 | 0.816 | 0.748 | 0.681 |
| Soft skill embedding | 0.280 | 0.900 | 0.911 | 0.869 | 0.829 |
| Multimodal weighted blend | 0.287 | 0.933 | 0.961 | 0.924 | 0.867 |
| RRF ensemble | 0.293 | 0.950 | 0.944 | 0.913 | 0.845 |

## Best method

**Multimodal weighted blend** · nDCG@5 = 0.924, MRR = 0.961
