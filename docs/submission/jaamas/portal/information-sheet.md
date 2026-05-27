# Springer Nature Information Sheet — JAAMAS

**Manuscript title:** JobMatch: An Agentic Multi-Role Platform for Explainable Job–Candidate Matching

**Article type:** Original research (regular paper)

**Corresponding author:** First Author (author@example.edu)

---

## Q1. What is the main contribution?

This paper presents **JobMatch**, an integrated research prototype for **explainable job–candidate matching** built as a **role-aware multi-agent platform**. The contribution is architectural, algorithmic, and evaluative—not a claim of production hiring effectiveness.

**1. Agentic platform design.** We describe a three-agent pattern in which Candidate and Employer agents own profile ingestion, normalization, and embedding, while a read-only Matchmaking agent scores and explains candidate–job pairs. Agents coordinate through a shared in-process event bus; role-separated web portals enforce authenticated ownership and keep hiring actions (save, apply, contact) under explicit human control.

**2. Hybrid matching with structured explainability.** We specify a composite ranker that fuses semantic similarity, skill overlap, title overlap, experience compatibility, compensation compatibility, and remote-preference signals. The default portal configuration uses a fixed **composite** strategy with **topK = 10** and documented weights **28/27/10/15/10/10**. Each ranked pair can carry a structured explanation object (matched/missing skills, constraint fit rows, score breakdown) rather than a single opaque score.

**3. Reproducible offline evaluation tied to deployed code.** We document an evaluation protocol on a labeled demo corpus of **30 resumes**, **15 job postings**, and **47 graded relevance pairs** (grades 0/1/2), with macro-averaged **P@5**, **R@5**, and **nDCG@5** at **K = 5**, hard-negative mining, regression gates, and a synthetic counterfactual fairness audit. All headline numbers are taken from committed benchmark artifacts, not re-estimated for this sheet.

**Headline offline results (exhaustive resume→jobs ranking, K = 5):**

| Result | Source | nDCG@5 |
|--------|--------|--------|
| Multimodal soft embed (α = 0.7) | `paper_progression_summary.json` | **0.969** |
| Learned fusion (logistic regression) | `table11_fusion.json` | **0.968** |
| Full composite ablation | `ablation_summary.json` (weights 40/30/15/10/5) | **0.942** |
| TF–IDF / BM25 lexical baselines | progression benchmark | **0.905 / 0.901** |

**Additional measured findings:**

- **Cross-encoder reranking** (pool = 20): **ΔnDCG@5 = −0.108** vs composite bi-encoder, **~141.7 ms/query**; disabled in the default portal configuration.
- **Hard-negative mining** (multimodal top-10 pool, 5 negatives/query): **30 queries**, **150 pairs**, **0** label conflicts with declared relevant jobs.
- **Synthetic fairness audit** (10 fabricated profile pairs, composite ranking): **6/10** pairs flagged for rank or score instability; treated as an engineering sanity check, **not** demographic fairness validation in live hiring.

**Scope and limits.** We position JobMatch as a traceable research artifact with benchmark drivers and regression tests that map offline metrics to implemented code paths. We **do not** claim generalization beyond the demo corpus, validated recruiter outcomes, or operational fairness guarantees.

---

## Q2. Why is it relevant to JAAMAS?

*Journal of Autonomous Agents and Multi-Agent Systems* publishes research on **agent architectures, coordination, and deployed agent systems**. JobMatch fits this scope in four ways:

**Multi-agent decomposition with clear responsibilities.** Profile mutation (Candidate and Employer agents) is separated from matchmaking (read-only Matchmaking agent). This modular design supports independent failure diagnosis, cache invalidation on profile updates, and role-specific workflows—core MAS concerns rather than a monolithic recommender service.

**Coordination without autonomous hiring decisions.** Agents exchange events (e.g., profile updates) and expose HTTP endpoints consumed by role-aware interfaces. Users review parsed profiles, inspect explanations, and explicitly act on matches. The system **orchestrates** retrieval and scoring; it does **not** autonomously hire, reject, or negotiate on behalf of users.

**Human-in-the-loop agentic workflows.** Candidate and employer portals implement distinct agent-mediated workflows (resume/JD ingestion, match discovery, explainability consumption, admin inspection). These workflows illustrate how MAS patterns apply to a high-stakes domain while preserving human oversight.

**Empirical study of agent-supported ranking choices.** The paper compares lexical baselines, dense retrieval, reciprocal rank fusion, learned fusion, composite scoring, and cross-encoder reranking on a fixed labeled corpus, and reports when higher offline nDCG does **not** justify deployment (e.g., cross-encoder latency/quality trade-off; portal preference for interpretable composite weights over the highest offline nDCG in research drivers).

In summary, the paper contributes an **agentic, explainable matching platform** with **reproducible evaluation**, aligned with JAAMAS interest in multi-agent systems that are designed, measured, and deployed with explicit human roles—not fully autonomous labor-market agents.

---

## Q3. How does it relate to prior work?

JobMatch sits at the intersection of **information retrieval**, **multi-agent systems**, and **explainable ranking** for hiring workflows.

**Information retrieval and hybrid ranking.** Job–candidate matching is fundamentally a retrieval-and-ranking problem over semi-structured documents. Our evaluation compares standard IR baselines (TF–IDF, BM25), dense bi-encoder similarity (`all-MiniLM-L6-v2`, 384-dimensional embeddings), multimodal combinations of semantic and skill signals, reciprocal rank fusion (RRF), learned fusion, and cross-encoder reranking. These components build on established IR practice (Manning et al.; Robertson & Zaragoza on BM25; Reimers & Gurevych on sentence embeddings; Cormack et al. on RRF). **Our novelty is not a new single retrieval formula** but the **integration** of these signals in a composite, explainable ranker within an agentic platform, with metrics reported only from reproducible drivers.

**Multi-agent systems.** We adopt a role-specialized agent decomposition (Wooldridge) in which agents own domain state and communicate via events. Unlike generic MAS tutorials or abstract coordination models, we document **concrete portal workflows**, gateway endpoints, and the read-only boundary of the Matchmaking agent—connecting MAS design to an implemented hiring support system.

**Explainability and calibration.** Structured explanations are attached at scoring time (skill alignment, constraint fit, component weights). Optional Platt scaling and LIME-style rationale hooks exist in the codebase; calibration and feedback boost are **off** in the default portal configuration. We do not claim LIME- or calibration-driven improvements without held-out numbers in the manuscript.

**Gap relative to typical deployed matchers.** Many production systems expose opaque scores or hide ranking logic from candidates and employers. JobMatch instead (i) separates profile ownership from scoring, (ii) exposes structured explanations in the UI, and (iii) pairs the deployed composite default with an offline benchmark suite (negative mining, regression tests, synthetic fairness audit). Prior ATS and job-matching products are not reproduced here; our comparison is against **implemented baselines on the same labeled corpus**.

**What we do not claim.** We do not assert state-of-the-art hiring accuracy, large-scale web evaluation, or demographic fairness certification. The labeled set is small (30 queries, 15 documents); learned fusion shares structural overlap with evaluation queries; hard negatives are high-scoring **unlabeled** jobs, not confirmed irrelevant documents.

---

## Q4. What is the relationship to prior publications, GitHub, or technical reports?

**Prior publication.** This manuscript has **not been published previously** and is **not under consideration elsewhere**. No portion of the text has appeared as a colored-layout preprint. This submission is **original research** submitted as a **regular paper**.

**Technical reports and overlapping write-ups.** There is **no separate technical report** or conference version whose results are reused without disclosure. Benchmark JSON/CSV artifacts and evaluation tables in the repository support the manuscript but are **supporting research outputs**, not standalone prior publications.

**Code availability (per manuscript declarations).** Source code for the platform, benchmark drivers, and regression tests is available in the **JobMatch project repository at the submission tag**. Key entry points: `backend/gateway/`, `backend/agents/`, `frontend/src/`, and `tests/benchmarks/test_eval_regression.py`.

**Data availability (per manuscript declarations).** The demo corpus (`data/cvs.json`, `data/jobs.json`, `data/eval_pairs.json`) and benchmark outputs under `backend/benchmark_outputs/` and `docs/research/evaluation/` are included in the project repository. Metrics can be regenerated with `python backend/scripts/run_research_pipeline.py` and `python -m benchmarks.paper_progression`.

**Relationship between repository and paper.** The repository implements the architecture, matching core, portals, and evaluation pipeline described in the manuscript. Reported numbers (e.g., nDCG@5 **0.969**, **0.968**, **0.942**; cross-encoder **ΔnDCG@5 = −0.108**; hard negatives **150** pairs with **0** conflicts; fairness audit **6/10** flagged) are drawn from named artifacts cited in the paper tables, not from unaudited runs.

**Author note.** Author names, affiliations, and CRediT roles in the manuscript remain placeholders pending final submission metadata; this information sheet will be updated accordingly before upload.

---

*Document version: aligned with `docs/submission/jaamas/manuscript/main.tex` (May 2026).*
