# Metrics and Evaluation Protocols

## Task

**Resume → jobs:** given a candidate profile, rank all job postings by predicted match quality.

Direction is fixed for all studies in this archive. Job→candidate reverse matching uses the same scoring functions in production but is not the primary eval protocol here.

## Protocol variants

| Protocol | Ranking scope | Used in |
|----------|---------------|---------|
| **Exhaustive** | Score all 15 jobs per query | All studies in this archive |
| **ANN** | Approximate nearest neighbors in vector store | `phase11.py` (not exported here by default) |
| **Two-stage CE** | Bi-encoder top-20 → cross-encoder rerank → top-K | Study 5 |

Exhaustive evaluation removes ANN recall error so strategy comparisons isolate **scoring quality**.

## Metrics (K=5 default)

| Metric | Definition | Notes |
|--------|------------|-------|
| **Precision@K** | \|relevant ∩ top-K\| / K | Binary relevance |
| **Recall@K** | \|relevant ∩ top-K\| / \|relevant\| | Binary relevance |
| **MRR** | Mean of 1/rank of first relevant doc | Per query, then macro-averaged |
| **nDCG@K** | DCG@K / IDCG@K | Graded relevance 0–2 |
| **MAP** | Mean average precision | Binary relevant set |

All reported scores are **macro-averaged** over the 30 labeled queries unless noted.

## Latency

Comparison and ablation studies record **mean milliseconds per query** for exhaustive ranking on a single machine. Latency is for relative comparison only · not SLA benchmarks.

Cross-encoder study splits **bi-encoder ms**, **cross-encoder ms**, and **total ms**.

## Strategies reference

### Embedding suite (Study 1)

1. Semantic cosine  
2. Semantic euclidean-derived  
3. Skills Jaccard  
4. Soft skill embedding  
5. Multimodal weighted blend (default w=0.7 semantic)  
6. RRF ensemble (k=60)

### Lexical baselines (Study 2)

1. BM25  
2. TF-IDF cosine  
3. Exact skill overlap  

### Composite ablation (Study 3)

Production weights: semantic **40%**, skills **30%**, experience **15%**, compensation **10%**, location **5%**.

Variants: each single component, partial composites (renormalized weights), full composite, RRF over five single rankers.

## Implementation

- Metrics: `backend/benchmarks/metrics.py`
- Runners: `backend/benchmarks/*.py`
- Production composite: `backend/core/scoring.py` → `compute_composite()`
