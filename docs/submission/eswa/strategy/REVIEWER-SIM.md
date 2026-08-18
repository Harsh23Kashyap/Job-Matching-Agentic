> **STALE — pre-numbers-pass planning notes.** Numbers below are superseded. Canonical values: composite nDCG@5 0.949, strongest single 0.924, semantic 0.878, RRF 0.913; held-out ECE 0.019 (low discrimination); ranking parity — not significant (two-sided p=0.10, fails Holm); counterfactual = 50-pair recourse-null; artifact DOI upon acceptance. See research/reports/FINAL_NUMERICAL_AUDIT.md.

# ESWA Reviewer Simulation

> Three simulated ESWA reviewers, one for each major ESWA reviewer archetype.
> Each review is written as if the reviewer had read the *reframed* ESWA paper (per `POSITIONING.md`), not the original JAAAMAS submission.
> Final composite read: **borderline accept to accept** (5.5–6.5 / 10) if the 12-week plan in `SUBMISSION-PLAN.md` is executed.

---

## Reviewer R1 — AI methodology expert

**Background:** Senior researcher in recommender systems and information retrieval. Has published at RecSys, SIGIR, and ESWA. Reviews for ESWA regularly. Cares about methodological rigor, baselines, and novelty.

**Overall score: 6.5/10 → Weak Accept**

> **Strengths.**
> The composite ranking with channel decomposition is a clean methodological choice; the ability to inspect per-channel contributions is a real engineering improvement over single-score ranking.
> The Platt-scaled confidence display is a small but legitimate contribution; the 12× ECE reduction is reported with the right diagnostics (reliability diagram, Brier, calibration parameters).
> The cross-encoder-disable decision is correctly documented and the 0.108 nDCG drop is an honest number.
> The 341-test regression gate is good engineering; reviewers will appreciate the reproducibility surface.
>
> **Weaknesses.**
> (1) The novelty is incremental. Every component is well-known: BM25, sentence-BERT, RRF, Platt scaling, rule-based explanation. The integration is plausible but not a methodological breakthrough.
> (2) The LLM is decorative. The paper acknowledges this, but the title and abstract suggest a more central role. Either integrate the LLM substantively (e.g., as a reranker, as a counterfactual generator, or as a judge for explanation quality) or de-emphasize "multi-agent" in the title.
> (3) The baselines are limited. ESWA reviewers in 2026 will expect at least one RAG baseline and one LLM-as-judge baseline. The current set (BM25, TF–IDF, semantic, hybrid, RRF, cross-encoder) is 2018–2022 vintage.
> (4) The counterfactual probe is small (10 pairs). Run a larger probe (50–100 pairs) before submission.
> (5) The learned fusion (nDCG 0.968) is fit on the same labeled pairs it is judged against; this is an overfitting risk that should be acknowledged explicitly.
>
> **Reject reasons if pushed.**
> "The novelty is in the integration, not the methodology. Without a stronger methodological contribution, this is a systems paper, not an AI paper."
>
> **Required fixes to clear the bar.**
> (a) Add an RAG baseline and an LLM-as-judge baseline.
> (b) Run a larger counterfactual probe (≥50 pairs).
> (c) Add a sensitivity analysis on the Platt parameters.
> (d) Acknowledge the learned-fusion overfitting risk in the limitations.
> (e) Either de-emphasize "multi-agent" in the title or integrate the LLM substantively in the ranking loop.

---

## Reviewer R2 — Recommendation systems expert

**Background:** Applied researcher in production recommendation. Cares about engineering relevance, dataset size, deployment evidence, and practical baselines (neural collaborative filtering, two-tower models, learned-to-rank).

**Overall score: 5.0/10 → Borderline**

> **Strengths.**
> The hybrid semantic–skill ranking is well-motivated and the nDCG@5 of 0.969 on the best configuration is a strong number. The p=0.048 significance test against the semantic-only baseline is correctly reported.
> The latency profile is honest: 0.4 ms per query for the bi-encoder composite, 141.7 ms for the cross-encoder. The 340× speed-up explains the cross-encoder-disable decision.
> The hard-negative mining (150 high-scoring negatives, 0 conflicts) is a useful label-consistency check.
>
> **Weaknesses.**
> (1) The corpus is too small. 30 resumes and 15 jobs is a benchmark that any senior reviewer will dismiss as a "demo." The 0.31 P@5 indicates the top-five is not very relevant; with 15 jobs total, the ceiling on ranking quality is low.
> (2) The baselines do not include any production-style learned-to-rank model. A two-tower neural model (e.g., Sentence-BERT bi-encoder with a learned head) would be the natural comparison and is missing.
> (3) No deployment evidence. The paper does not report latency at 100K-job scale, throughput, or integration with an existing ATS.
> (4) The fairness probe (10 pairs, DIR 0.82 / 0.75) is not contextualized. The "parity is 1.0" statement is correct but does not tell the reviewer whether 0.82 is acceptable for HR applications.
> (5) The 0.949 nDCG on the portal-default composite is a strong number, but the reviewer will suspect the 21+26 calibration set is too small to support the Platt parameters.
>
> **Reject reasons if pushed.**
> "The corpus is too small to support engineering claims. The 30-resume, 15-job dataset is a benchmark, not a deployment."
>
> **Required fixes to clear the bar.**
> (a) Contextualize the small corpus as a *controlled evaluation* and report the 341-test regression gate as the engineering surface.
> (b) Add a two-tower neural baseline.
> (c) Report latency at a larger scale (1K, 10K, 100K jobs) via simulation.
> (d) Contextualize the DIR numbers against published HR-fairness benchmarks.
> (e) Either expand the calibration set or acknowledge the small-set limitation.

---

## Reviewer R3 — Application / engineering expert

**Background:** Industrial AI researcher. Cares about practical deployment, integration with existing systems, cost-benefit, and engineering honesty. Reviews for ESWA from the "this should be deployable" perspective.

**Overall score: 6.0/10 → Weak Accept**

> **Strengths.**
> The role-separated agentic architecture is a clean engineering choice for an HR system. The ownership boundary (candidate-side owns candidate data, employer-side owns job data, matchmaking reads only) maps to a real privacy boundary in production HR systems.
> The fairness probe, while narrow, is the right kind of engineering probe for an HR system. The DIR 0.82 / 0.75 is honest; the paper does not over-claim.
> The 341-test regression gate is good engineering practice and is rare in academic submissions.
> The application framing (recruitment at scale, ATS limitations) is correct.
>
> **Weaknesses.**
> (1) The "agentic AI" framing is over-claimed. The agents are not LLM-driven in their core loops; the LLM is used only for parsing and explanation generation. The title "multi-agent architecture" is defensible; "agentic AI" in the abstract invites the question "what is agentic about this?"
> (2) The application consequence is not quantified. The paper reports accuracy metrics but does not report operational metrics (e.g., time-to-shortlist, recruiter workload reduction, candidate satisfaction).
> (3) The explanation specificity (0.627) is weak. A rule-based explainer that names a concrete skill in only a quarter of bullets is not a strong XAI artifact; the LLM-based explainer is reported in supplementary but not in the main results.
> (4) The cross-encoder is disabled, which is the right engineering decision, but the diagnosis (why does the cross-encoder underperform?) is not in the main paper.
> (5) No cost-benefit analysis. The paper does not estimate the engineering cost of deploying the system (engineering hours, infrastructure, ongoing maintenance).
>
> **Reject reasons if pushed.**
> "The application consequence is not demonstrated. The paper is a prototype, not a deployable system."
>
> **Required fixes to clear the bar.**
> (a) Either de-emphasize "agentic AI" in the title and abstract, or integrate the LLM substantively in the ranking loop.
> (b) Move the LLM-based explainer results from supplementary to §5.
> (c) Add a one-paragraph cross-encoder diagnosis to the main paper.
> (d) Add a deployment cost estimate in §6 (engineering hours, infrastructure, maintenance).
> (e) Acknowledge in §6 that the application consequence is not yet quantified and that operational metrics are future work.

---

## Composite read

| Reviewer | Score | Verdict |
|---|---|---|
| R1 (AI methodology) | 6.5/10 | Weak Accept |
| R2 (Recsys) | 5.0/10 | Borderline |
| R3 (Application) | 6.0/10 | Weak Accept |
| **Composite** | **5.8/10** | **Borderline Accept** |

**The swing reviewer is R2.** R2 is asking for engineering evidence (larger corpus, neural baseline, deployment metrics) that the small prototype cannot provide. R1 and R3 are likely to vote accept if the requested fixes are made; R2 is harder to satisfy.

**The minimum changes to move from borderline to accept:**

1. **Add an RAG baseline and an LLM-as-judge baseline** (R1 + R2). 1 week of work.
2. **Run a larger counterfactual probe (≥50 pairs)** (R1 + R2). 1 week of work.
3. **Add a sensitivity analysis on the Platt parameters** (R1). 2 days of work.
4. **Contextualize the small corpus as a controlled evaluation with the 341-test regression gate as the engineering surface** (R2 + R3). 1 paragraph in §4.
5. **Move the LLM-based explainer results from supplementary to §5** (R1 + R3). 1 day of work.
6. **Add a one-paragraph cross-encoder diagnosis to the main paper** (R3). 1 day of work.
7. **Soften "agentic AI" in the title and abstract, or add a one-line clarification in the abstract** (R3). 10 minutes of work.
8. **Add a deployment cost estimate in §6** (R3). 1 day of work.

These eight fixes take about 4 weeks of work and address 80% of the reviewer risk identified above. The 12-week plan in `SUBMISSION-PLAN.md` is calibrated to this fix list plus buffer.

## Acceptance probability (revised, after 12-week plan execution)

| Scenario | Probability |
|---|---|
| Submit as-is (JAAAMAS manuscript, no reframing) | 30–40% |
| Submit with reframe but no additional experiments | 40–50% |
| Submit with reframe + 8 fixes (per 12-week plan) | **55–65%** |
| Submit with reframe + 8 fixes + larger corpus (if achievable) | 70–80% |

The 12-week plan targets the 55–65% band. The larger corpus (which would push to 70–80%) is listed as future work in the plan, not as a hard requirement, because the small corpus is honest and well-contextualized.
