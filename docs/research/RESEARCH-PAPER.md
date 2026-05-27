# JobMatch: A Multi-Agent Composite Matching System for Transparent Job–Candidate Ranking

**Status:** Draft · results synced from offline benchmark reports  
**Report source:** `backend/reports/research_run_smoke_test/` (pipeline run, 2026-05-27)  
**Cross-encoder source:** `backend/reports/cross_encoder_report.json` (separate run, 2026-05-27)  
**Paper tables:** `backend/reports/research_run_smoke_test/paper_tables/`

---

## Abstract

Recruiting systems must rank candidates against job requirements while remaining explainable and auditable. We present **JobMatch**, a three-agent event-driven system that combines semantic bi-encoder similarity, structured skill overlap, and auxiliary signals (experience, compensation, location) into a weighted composite score with rule-based explanations.

We evaluate on a fixed offline corpus of **30 candidate profiles**, **15 job postings**, and **47 graded relevance pairs** (scale 0–2). Under exhaustive resume→jobs ranking at **K=5**, production composite scoring achieves **nDCG@5 = 0.942**, **MRR = 0.944**, and **Recall@5 = 0.983** · the best result among nine ablation variants. Paired bootstrap testing (5,000 resamples, one-sided, α = 0.05) shows full composite significantly improves nDCG@5 over semantic-only scoring (**Δ = +0.064**, **p = 0.019**). Lexical baselines (best: BM25, nDCG@5 = 0.894) and single-signal rankers underperform the full composite.

A synthetic fairness audit flags **6/10** counterfactual profile pairs under demographic-like perturbations. Automated explainability checks find the rules explainer passes skill-mention checks on only **25.3%** of instances, while a grounded template explainer reaches **100%** skill mention at **96.2%** faithfulness. Optional cross-encoder reranking on composite matches **degrades** nDCG@5 by **0.108** while adding **~141 ms/query** latency; it is disabled in production by default.

**TODO:** Evaluate on the generated 100×50 research corpus (`data/research/`). **TODO:** Human-rated explanation quality study.

---

## 1. Introduction

Job–candidate matching is typically implemented as a single retrieval pipeline. JobMatch instead separates **profile ownership** (Candidate and Employer agents) from **read-only scoring** (Matchmaking agent), uses an in-process event bus for coordination, and exposes per-result explanations. This design supports human-in-the-loop hiring: the system ranks and explains; it does not automate hiring decisions.

This paper documents the implemented architecture, matching algorithms, and offline evaluation protocol. All quantitative claims below are drawn from generated reports under `backend/reports/`; missing studies are explicitly marked **TODO**.

---

## 2. Methodology

### 2.1 System overview

JobMatch is an **event-driven monolith** with three agents:

| Agent | Responsibility | Persistence |
|-------|----------------|-------------|
| **Candidate Agent** | CV ingest, validation, embedding, profile state | Chroma + in-memory index |
| **Employer Agent** | JD ingest, validation, embedding, job state | Chroma + in-memory index |
| **Matchmaking Agent** | Scoring, ranking, explanation (read-only) | Ephemeral match sessions |

Communication uses a synchronous in-process `AgentEventBus`. The FastAPI gateway delegates to `app.state.container`; agents never write to each other's stores during matching.

### 2.2 Design principles

- **Human-in-the-loop:** UI presents ranked lists and explanations; no automated hire/reject.
- **Transparency:** Each result includes `why_ranked` bullets derived from score components.
- **Offline evaluation isolation:** Benchmark runners in `backend/benchmarks/` do not alter production API defaults unless explicitly enabled.

### 2.3 Reproducibility

Full pipeline (nine stages):

```bash
python backend/scripts/run_research_pipeline.py
# → backend/reports/research_run_<timestamp>/
```

Stages: dataset validation → baseline comparison → composite scoring → ablation → cross-encoder (if enabled) → bootstrap significance → fairness audit → explainability evaluation → paper table generation.

Primary results in this draft come from run **`research_run_smoke_test`** (cross-encoder step skipped). Cross-encoder numbers come from a separate report at `backend/reports/cross_encoder_report.json`.

---

## 3. System Architecture

### 3.1 Agent boundaries

The Matchmaking agent computes scores and ranks but **does not** mutate candidate or job profiles or vector stores. Candidate and Employer agents publish `candidate.profile.updated` and `job.profile.updated` events after registration.

### 3.2 Data flow (match request)

1. Client sends match request (candidate → jobs or job → candidates).
2. Matchmaking agent loads snapshots (skills, experience, embeddings, salary, remote preference).
3. Scoring strategy selected (`composite`, `semantic`, `rrf`, etc.).
4. Optional two-stage rerank: bi-encoder shortlist → cross-encoder rescore (off by default).
5. Top-K results returned with score breakdown and `why_ranked` explanation.

### 3.3 Technology stack

| Layer | Choice |
|-------|--------|
| Backend | Python 3.11, FastAPI |
| Embeddings | `all-MiniLM-L6-v2` (384-d) |
| Vector store | Chroma (default); Qdrant optional |
| Frontend | React 19, Vite (role portals v1.1) |

**TODO:** Architecture diagram figure for paper submission (Mermaid/TikZ pipeline figure).

---

## 4. Matching Algorithms

### 4.1 Semantic similarity

Document text is built from resume/JD fields and embedded with MiniLM-L6-v2. Semantic score uses cosine similarity between candidate and job embeddings (euclidean-derived variant also evaluated offline).

### 4.2 Skill overlap

- **Jaccard** on required skill sets (production default for composite).
- **Soft skill embedding:** embedding-based skill similarity (higher latency offline: **12.07 ms/query** vs **0.25 ms/query** for composite).

### 4.3 Multimodal weighted blend (retrieval baseline)

Offline embedding baseline combining semantic and skill signals with default semantic weight **w = 0.7**:

\[
s_{\text{multimodal}} = w \cdot s_{\text{semantic}} + (1 - w) \cdot s_{\text{skills}}
\]

### 4.4 Production composite score

The production ranker (`compute_composite`) uses fixed weights:

| Component | Weight |
|-----------|--------|
| Semantic | 40% |
| Skills | 30% |
| Experience | 15% |
| Compensation | 10% |
| Location | 5% |

Experience, compensation, and location are normalized component scores in \([0, 1]\). Final score is the weighted sum, clamped to \([0, 1]\).

### 4.5 RRF ensemble

Reciprocal Rank Fusion (k = 60) merges ranked lists from multiple strategies. In the **comparison** benchmark, RRF over embedding strategies achieves nDCG@5 = **0.913**. In the **ablation** study, RRF over five single-component rankers achieves nDCG@5 = **0.564** · substantially below full composite on this corpus.

### 4.6 Lexical baselines (offline)

- **BM25** over tokenized documents  
- **TF-IDF cosine**  
- **Exact skill overlap** (binary set match count)

These are research baselines only; production portals default to `composite`.

### 4.7 Cross-encoder reranking (optional)

Two-stage pipeline: bi-encoder retrieves top-20, cross-encoder rescores, top-K returned. Controlled by `ENABLE_CROSS_ENCODER_RERANK` (default **false**). See §7.4 for measured trade-off.

---

## 5. Evaluation Setup

### 5.1 Corpus

From `dataset_validation.json`:

| Statistic | Value |
|-----------|-------|
| Candidates | 30 |
| Jobs | 15 |
| Labeled queries | 30 |
| Graded pairs | 47 |
| Relevance scale | 0–2 (2 = strong, 1 = partial) |
| Relevance distribution | rel=2: **21**, rel=1: **26** |
| Embedding model | `all-MiniLM-L6-v2` |

Binary relevance for P@K, R@K, MAP: grade **> 0**.

### 5.2 Task and protocol

- **Task:** resume → jobs (exhaustive ranking: all 15 jobs scored per query).
- **Cutoff:** K = 5 (default across all reports).
- **Aggregation:** macro-average over 30 queries.

Exhaustive evaluation removes approximate nearest-neighbor recall error so comparisons isolate **scoring quality**.

### 5.3 Baselines and variants evaluated

**Comparison study (9 methods):** BM25, TF-IDF, exact overlap, semantic cosine, semantic L2, skills Jaccard, soft skill embed, multimodal blend, RRF ensemble.

**Composite evaluation:** production `compute_composite` (single strategy).

**Ablation study (9 variants):** five single-component rankers, two partial composites (renormalized weights), full composite, RRF over single-component lists.

### 5.4 Statistical testing

Paired bootstrap on per-query nDCG@5 and MRR:

- **Resamples:** 5,000  
- **Seed:** 42  
- **Baseline (comparison):** semantic cosine  
- **Baseline (ablation):** semantic only  
- **p-value:** one-sided · fraction of bootstrap mean-diffs ≤ 0 (H₁: compare > baseline)

### 5.5 Fairness audit protocol

- **10 synthetic counterfactual pairs** (`fairness_audit_profiles.json`); fabricated profiles only · no real-user demographic inference.
- **Strategy:** production composite, K = 5.
- **Flags:** top-1 change, score delta > 0.01, explanation drift in top-K union.

### 5.6 Explainability evaluation

- **300 instances:** 30 candidates × top-5 composite matches × 2 explainers (`rules`, `template`).
- **Automated checks:** skill mention, no hallucinated skills, component alignment, specificity.
- **Consistency:** bullet Jaccard on 10 synthetic similar-profile pairs per explainer.

### 5.7 Not yet evaluated

| Study | Status |
|-------|--------|
| 100 candidate × 50 job research corpus (`data/research/`) | **TODO** · generator exists, full pipeline not run |
| ANN vs exhaustive (Chroma/Qdrant sweep) | **TODO** · `phase11.py` exists, not in pipeline run |
| Job → candidate reverse direction | **TODO** |
| Learned fusion / weight tuning | **TODO** |
| Human explanation ratings | **TODO** |

---

## 6. Metrics

| Metric | Definition | Graded? |
|--------|------------|---------|
| **Precision@K** | \|relevant ∩ top-K\| / K | Binary |
| **Recall@K** | \|relevant ∩ top-K\| / \|relevant\| | Binary |
| **MRR** | Mean of 1/rank(first relevant) | Binary |
| **nDCG@K** | DCG@K / IDCG@K | Grades 0–2 |
| **MAP** | Mean average precision | Binary |
| **Latency** | Mean ms per query (exhaustive) | · |

Copy-pasteable paper tables: `backend/reports/research_run_smoke_test/paper_tables/` (Markdown, CSV, LaTeX booktabs).

---

## 7. Results

### 7.1 Baseline comparison (lexical vs embedding)

Macro-averaged results at K=5 from `comparison_summary.json`:

| Method | Family | P@5 | R@5 | MRR | nDCG@5 | MAP | Latency (ms) |
|--------|--------|-----|-----|-----|--------|-----|--------------|
| Multimodal weighted blend | Embedding | 0.287 | 0.933 | 0.961 | **0.924** | 0.867 | 0.252 |
| RRF ensemble | Embedding | 0.293 | 0.950 | 0.944 | 0.913 | 0.845 | 0.959 |
| TF-IDF cosine | Lexical | 0.293 | 0.950 | 0.918 | 0.898 | 0.842 | 0.072 |
| BM25 | Lexical | 0.307 | 0.983 | 0.912 | 0.894 | 0.838 | 0.103 |
| Semantic cosine | Embedding | 0.267 | 0.867 | 0.931 | 0.878 | 0.810 | 0.211 |
| Soft skill embed | Embedding | 0.280 | 0.900 | 0.911 | 0.869 | 0.829 | 12.074 |
| Exact overlap | Lexical | 0.233 | 0.733 | 0.816 | 0.748 | 0.681 | 0.025 |
| Skills Jaccard | Embedding | 0.233 | 0.733 | 0.816 | 0.748 | 0.681 | 0.034 |

**Finding:** Best embedding-only baseline is multimodal blend (nDCG@5 = 0.924). Best lexical baseline is BM25 (nDCG@5 = 0.894). Semantic cosine alone (0.878) is below both.

### 7.2 Production composite scoring

From `composite_eval_report.json`:

| Method | P@5 | R@5 | MRR | nDCG@5 | MAP | Latency (ms) |
|--------|-----|-----|-----|--------|-----|--------------|
| Production composite | 0.307 | 0.983 | 0.944 | **0.942** | 0.896 | 0.264 |

Production composite exceeds all comparison baselines on nDCG@5 on this corpus (+0.018 vs multimodal blend).

### 7.3 Ablation study

From `ablation_summary.json` (K=5):

| Variant | Category | nDCG@5 | MRR | R@5 | Latency (ms) |
|---------|----------|--------|-----|-----|--------------|
| **Full composite** | full | **0.942** | 0.944 | 0.983 | 0.259 |
| Semantic + skills | partial | 0.917 | 0.961 | 0.933 | 0.281 |
| Semantic + skills + experience | partial | 0.917 | 0.961 | 0.933 | 0.279 |
| Semantic only | single | 0.878 | 0.931 | 0.867 | 0.246 |
| Skills only | single | 0.748 | 0.816 | 0.733 | 0.043 |
| Compensation only | single | 0.393 | 0.457 | 0.567 | 0.023 |
| Location only | single | 0.335 | 0.388 | 0.467 | 0.020 |
| Experience only | single | 0.326 | 0.384 | 0.467 | 0.021 |
| RRF (5 singles) | ensemble | 0.564 | 0.570 | 0.717 | 0.318 |

**Finding:** Structural signals alone (experience, compensation, location) rank poorly in isolation (nDCG@5 ≤ 0.393). Adding skills to semantic yields most of the gain (0.917 vs 0.878). Full five-component composite adds a further +0.025 nDCG@5. RRF over single-component lists underperforms weighted composite on this corpus.

### 7.4 Cross-encoder reranking

From `backend/reports/cross_encoder_report.json` (composite strategy, K=5, rerank pool=20):

| Configuration | nDCG@5 | MRR | Total latency (ms) |
|---------------|--------|-----|---------------------|
| Bi-encoder only | 0.942 | 0.944 | 0.408 |
| Bi-encoder + cross-encoder | 0.834 | 0.833 | 141.747 |
| **Delta** | **−0.108** | **−0.112** | **+141.3 ms** |

All 30 queries had top-5 rank changes after cross-encoder reranking. Cross-encoder is **not enabled in production** by default.

**TODO:** Include cross-encoder results in unified pipeline run (`--enable-cross-encoder`).

### 7.5 Statistical significance

#### Comparison vs semantic cosine (`significance_comparisons.csv`)

Significant at α = 0.05 (nDCG@5):

| Compare | Δ nDCG@5 | 95% CI | p-value | W/L/T |
|---------|----------|--------|---------|-------|
| Multimodal weighted blend | +0.046 | [0.002, 0.118] | 0.013 | 6/1/23 |
| RRF ensemble | +0.035 | [0.003, 0.086] | 0.009 | 8/3/19 |

Not significant: BM25 (p = 0.350), TF-IDF (p = 0.345), soft skill embed (p = 0.575).

#### Ablation vs semantic only (`significance_ablation_comparisons.csv`)

Significant at α = 0.05 (nDCG@5):

| Compare | Δ nDCG@5 | 95% CI | p-value | W/L/T |
|---------|----------|--------|---------|-------|
| Full composite | +0.064 | [0.002, 0.146] | 0.019 | 12/2/16 |

Not significant at α = 0.05: semantic + skills (p = 0.113), semantic + skills + experience (p = 0.100). Full composite MRR improvement vs semantic only (Δ = +0.013) is not significant (p = 0.385).

**TODO:** Bootstrap comparison of production composite vs multimodal blend directly.

---

## 8. Fairness Audit · Limitations

### 8.1 Scope

The audit uses **10 synthetic counterfactual pairs** only. It does **not** measure demographic parity on real applicants and must not be interpreted as production bias evidence.

Report summary (`fairness_audit_report.json`):

- **Flagged pairs:** 6 / 10 (**60%**)
- **Categories:** name/gender proxy (2), name/ethnicity proxy (2), nationality phrase (2), hometown label (2), pronouns (1), email domain (1)
- **Top-1 stable:** 9/10 pairs; **nationality_phrase_01** had top-1 change

### 8.2 Observed instability

Flagged cases cluster around:

- **Name/ethnicity proxy pairs:** score deltas up to **0.024**, rank changes in top-K, explanation drift on some jobs.
- **Hometown and email domain perturbations:** score deltas above 0.01 threshold on individual jobs.

Name/gender proxy pairs (identical qualifications, different first names) showed **stable top-1** and full top-5 overlap · but names still appear in embedded document text, so semantic paths can couple to surface tokens.

### 8.3 Limitations (must appear in paper)

1. **Synthetic fixtures only** · no protected-attribute labels on real users.  
2. **Small pair count (n=10)** · wide uncertainty; exploratory, not confirmatory.  
3. **Flags indicate review triggers**, not adjudicated discrimination.  
4. **Embedding path** may legitimately shift when counterfactual text changes (e.g., nationality phrase in summary).  
5. **No intersectional or subgroup power analysis.**  
6. **No legal/compliance certification.**

**TODO:** Expand counterfactual set; add permutation tests; evaluate debiasing or blinded document text.

---

## 9. Explainability Evaluation

### 9.1 Automated results

From `explainability_report.json` (300 instances, composite top-5):

| Explainer | Faithfulness | Specificity | Skill mention | No hallucination | Flagged rate | Consistency (Jaccard) |
|-----------|--------------|-------------|---------------|------------------|--------------|------------------------|
| Rules | 0.747 | 0.621 | 25.3% | 98.7% | **76.0%** | 1.000 |
| Template | 0.962 | 1.000 | 100.0% | 88.7% | **11.3%** | 1.000 |

- **Total flagged instances:** 131 / 300  
- **Hallucination count:** 19 (mostly template path · 11.3% fail no-hallucination check)  
- **Consistency** on synthetic similar-profile pairs: perfect (Jaccard = 1.0) for both explainers

### 9.2 Discussion

The **rules explainer** fails primarily on **skill mention** (only 25.3% pass) despite strong component alignment (100%). Explanations can be faithful to numeric components yet omit readable skill grounding · a usability gap for recruiters.

The **template explainer** achieves near-perfect specificity and skill mention by construction but shows higher hallucination flags (11.3%): templated text can reference skills not supported by the structured profile check.

Both explainers show perfect consistency on controlled pairs · explanation bullets are stable when qualifications match · but this does not imply fairness under demographic counterfactuals (see §8).

**TODO:** Human evaluation (recruiter comprehension, trust). **TODO:** LLM-generated explanations with citation grounding. **TODO:** Link explanation drift flags to fairness cases in a unified case study table.

---

## 10. Limitations (General)

1. **Small corpus:** 30 queries, 15 jobs · bootstrap CIs are wide; results may not generalize.  
2. **Exhaustive vs production ANN:** offline eval scores all jobs; live system uses vector retrieval.  
3. **Hand-tuned composite weights** (40/30/15/10/5) · not learned from data.  
4. **Synthetic/demo corpus** · not real labor-market distribution.  
5. **Cross-encoder evaluated separately** from main pipeline run.  
6. **No end-to-end user study** of portal workflows.

---

## 11. Future Work

| Direction | Rationale | Status |
|-----------|-----------|--------|
| **Large-scale eval** on 100×50 research corpus | Reduce small-n variance | Corpus generated; **TODO** run pipeline on `data/research/` |
| **Learned fusion weights** | Replace hand-tuned 40/30/15/10/5 | **TODO** |
| **ANN recall vs exhaustive gap** | Quantify production retrieval error | `phase11.py` exists; **TODO** export to paper |
| **Cross-encoder tuning** | CE hurt nDCG on demo corpus | **TODO** domain-adapted CE or larger rerank pool study |
| **Explanation human eval** | Automated checks ≠ user trust | **TODO** |
| **Fairness audit expansion** | n=10 synthetic pairs insufficient | **TODO** |
| **Significance vs strong baselines** | Composite vs multimodal not bootstrapped | **TODO** |
| **Reverse matching eval** | Job → candidate direction untested | **TODO** |
| **Multi-lingual / multi-sector corpora** | Demo corpus is English tech-focused | **TODO** |

---

## 12. Conclusion

JobMatch demonstrates that a multi-agent composite ranker · combining semantic, skill, and structural signals with transparent explanations · achieves the strongest offline ranking quality on the demo corpus (nDCG@5 = **0.942**), significantly beating semantic-only retrieval (p = **0.019**). Lexical and single-signal baselines are insufficient alone. Cross-encoder reranking trades large latency for worse nDCG on this setup. Synthetic fairness and explainability audits reveal review-worthy instability and explanation gaps that require larger studies before production fairness claims.

---

## Appendix A · Report file index

| Section | Primary report file |
|---------|---------------------|
| Corpus validation | `research_run_smoke_test/dataset_validation.json` |
| Baseline comparison | `research_run_smoke_test/comparison_summary.json` |
| Composite scoring | `research_run_smoke_test/composite_eval_report.json` |
| Ablation | `research_run_smoke_test/ablation_summary.json` |
| Significance (comparison) | `research_run_smoke_test/significance_report.json` |
| Significance (ablation) | `research_run_smoke_test/significance_ablation_report.json` |
| Cross-encoder | `cross_encoder_report.json` |
| Fairness | `research_run_smoke_test/fairness_audit_report.json` |
| Explainability | `research_run_smoke_test/explainability_report.json` |
| Paper tables | `research_run_smoke_test/paper_tables/` |

## Appendix B · LaTeX table inclusion

Copy `\input{}` or paste from:

- `table1_method_comparison.tex` · `\label{tab:method-comparison}`
- `table2_ablation.tex` · `\label{tab:ablation}`
- `table3_latency.tex` · `\label{tab:latency}`
- `table4_fairness.tex` · `\label{tab:fairness}`
- `table5_explanation_quality.tex` · `\label{tab:explanation-quality}`
- `table6_qualitative_examples.tex` · `\label{tab:qualitative}`

Requires `\usepackage{booktabs}` in LaTeX preamble.
