# Corpus and Labels

## Files

| File | Count | Description |
|------|-------|-------------|
| `data/cvs.json` | 30 | Structured candidate profiles with skills, experience, salary, remote preference, document text, embeddings |
| `data/jobs.json` | 15 | Structured job postings with required/preferred skills, experience, budget, remote policy, embeddings |
| `data/eval_pairs.json` | 47 pairs | Graded relevance judgments for candidate→job matching |

## Query construction

Each of the **30 candidates** is treated as one **query** in the resume→jobs task. For each query, all **15 jobs** are ranked and metrics are computed against the labeled relevant set for that candidate.

The eval file maps:

```
candidate_id → { job_id → relevance_grade }
```

## Relevance grades

| Grade | Meaning | Used as relevant? |
|-------|---------|-------------------|
| 0 | Not relevant | No |
| 1 | Partially relevant | Yes |
| 2 | Highly relevant | Yes |

Graded labels feed **nDCG@K** (full grade scale). **Precision@K**, **Recall@K**, **MRR**, and **MAP** treat relevance as binary (grade > 0).

## Embedding model

All snapshot embeddings are computed with **`all-MiniLM-L6-v2`** (384-d) unless a study explicitly swaps the model (e.g. paper progression alt-embedder).

Embeddings are precomputed at corpus load / snapshot creation time, not at query time in benchmarks.

## Demo linkage

The demo candidate account maps to **Rahul Sharma** (`cv_01`) in the corpus. See `backend/demo_seed.py`.

## Limitations

- Fixed small corpus · results do not generalize to open-domain job boards
- Labels are manually curated for thesis demo, not crowdsourced
- No temporal split or held-out employer/candidate groups in v1
