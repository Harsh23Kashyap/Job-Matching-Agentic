> **STALE — pre-numbers-pass planning notes.** Numbers below are superseded. Canonical values: composite nDCG@5 0.949, strongest single 0.924, semantic 0.878, RRF 0.913; held-out ECE 0.019 (low discrimination); ranking parity — not significant (two-sided p=0.10, fails Holm); counterfactual = 50-pair recourse-null; artifact DOI upon acceptance. See research/reports/FINAL_NUMERICAL_AUDIT.md.

# ESWA Fit Assessment — JobMatch Manuscript

> **Audit date:** 2026-07-29
> **Source paper:** JAAAMAS submission (desk-rejected 2026-07-29)
> **Target venue:** Expert Systems with Applications (Elsevier), IF 9.4, Q1
> **Reviewer lens:** Associate editor + AI methodology reviewer + applied-AI reviewer
> **Conclusion:** As currently framed, acceptance is **30–40%**. After the reframing described in `POSITIONING.md`, acceptance rises to **55–65%**.

---

## Scorecard (as submitted to JAAAMAS)

| Dimension | Score | Reasoning |
|---|---|---|
| **AI novelty** | **6/10** | The architecture is not novel in MAS literature; the individual components (BM25, sentence-BERT, RRF, Platt scaling) are textbook. The novelty is in the *integration* (calibrated confidence bound to component-level explanations on a ranking output), which is a defensible contribution but not a new algorithm. |
| **Engineering application relevance** | **7/10** | HR / recruitment is in ESWA's scope (human resources management is explicitly named). The 30/15/47 demo corpus is too small for a real engineering deployment claim; the paper is a *prototype*, not a *system*. |
| **Methodological depth** | **6/10** | The methodology is sufficient but not deep. The composite ranking with six channels is described but not deeply analyzed; the calibration is one paragraph; the counterfactual probe is a 10-pair sanity check; the faithfulness metric is described but the specific scoring function is underspecified. |
| **Experimental strength** | **5/10** | 30 resumes and 15 jobs is a benchmark that ESWA reviewers will dismiss as a "demo." Baselines are limited to BM25, TF–IDF, semantic cosine, and a few hybrids — no RAG, no LLM-as-judge, no production baselines (LinkedIn, Indeed-style ranking). The 0.949 nDCG is a strong number on a tiny corpus, but it does not transfer. |
| **ESWA acceptance likelihood (as-is)** | **30–40%** | High desk-reject risk on (a) Figure 1 = architecture diagram (the single most common ESWA desk-reject signal), (b) "we applied known methods to HR" without a new methodology, (c) the LLM being decorative rather than central. |

## What an ESWA reviewer will say (predicted)

A typical ESWA reviewer, reading the JAAAMAS manuscript as submitted, will produce a report along these lines:

> *"The paper presents a multi-agent system for job–candidate matching with explanation and calibration features. The engineering is solid, the results are reported honestly, and the prototype is reproducible. However, I have concerns:
> (1) The novelty is incremental: every component is well-known (BM25, sentence-BERT, RRF, Platt scaling). The integration is plausible but not a methodological contribution.
> (2) The corpus (30 resumes, 15 jobs) is too small to support claims of engineering relevance. A reviewer cannot tell if the system would work at production scale.
> (3) The LLM is decorative: it is used only for parsing and explanation generation, not for ranking. The 'agentic AI' framing is not earned by the LLM's actual role.
> (4) The fairness audit is narrow (10 pairs); the disparate-impact ratios (0.82, 0.75) are not contextualized against any baseline.
> (5) Figure 1 is an architecture diagram; ESWA's editorial guidance asks for the application context to be established in Figure 1.
> Recommendation: Major revision. The authors should (a) articulate a single, specific AI methodology contribution; (b) expand the corpus or contextualize the small corpus as a controlled evaluation; (c) integrate the LLM more substantively or de-emphasize the 'agentic' framing; (d) replace Figure 1 with an application context figure; (e) expand the baselines to include LLM-based methods (RAG, LLM-as-judge, prompt-based ranking)."*

## What is publishable (preserve)

These parts of the JAAAMAS manuscript survive the ESWA reframe:

1. **Composite ranking with six explicit channels** (semantic 0.28, skill 0.27, title 0.10, experience 0.15, compensation 0.10, remote 0.10). The channel decomposition is a clean methodological choice.
2. **nDCG@5 = 0.949 (composite) / 0.969 (best single) / 0.968 (learned fusion)** with statistical significance (p=0.048 vs semantic-only). The hybrid-gains result is defensible.
3. **Platt-scaled composite score with ECE 0.40 → 0.032** and Brier 0.093. The application of Platt scaling to a ranking composite is a clean contribution.
4. **Counterfactual probe methodology** (10 pairs, 7 flagged, top-1 stable, max shift 0.017). The probe is small but methodologically sound.
5. **Component-level faithfulness evaluation** (rule-based: faithfulness 0.745, specificity 0.627, consistency 1.000, skill mention 0.253). The metric suite is reasonable.
6. **Adversarial fairness probe** (10 controlled profile pairs, DIR 0.82 / 0.75). The probe is narrow but the engineering is honest.
7. **Hard-negative mining** (150 high-scoring negatives, 0 conflicts with declared relevant set). The result is publishable as a label-consistency check.
8. **Latency profile** (composite bi-encoder 0.4 ms, cross-encoder 141.7 ms). The numbers are honest.
9. **Test suite** (302 Python + 39 Node = 341 tests, ±0.04 nDCG tolerance). The engineering surface is reproducible.

## What needs redesign (transform)

These parts of the JAAAMAS manuscript must change for ESWA:

1. **The contribution statement.** Currently "we built a multi-agent system." For ESWA, the contribution must be: "a multi-agent recommendation architecture with component-level explanations and calibrated confidence, validated on a real engineering domain (recruitment) with reproducible offline evidence."
2. **Figure 1.** Currently the role-separated architecture diagram. For ESWA, Figure 1 must be an *application context* figure: a recruiter or job-seeker using the system, with the system as a black box from their perspective.
3. **The introduction.** Currently leads with "users struggle with opaque recommendations." For ESWA, the introduction must lead with the *HR engineering problem* (recruitment at scale, ATS limitations, time-to-hire, recruiter overload), not the HCI design gap.
4. **The related work.** Currently 4 streams (interactive recsys, XAI, human–AI decision, LLM agents). For ESWA, the related work should be 5 streams: AI-based recommendation, semantic matching, knowledge-driven AI, LLM agents, XAI for recommendation, trustworthy AI.
5. **The methodology section.** Currently 943 words with metric definitions. For ESWA, the methodology must be the longest section (~2,200 words) with detailed architecture, knowledge representation, retrieval strategy, ranking algorithm, explanation generation, calibration, and implementation.
6. **The results section.** Currently 1,206 words, strong on numbers. For ESWA, the results must add: (a) RAG baseline, (b) LLM-as-judge baseline, (c) sensitivity analysis on Platt parameters, (d) reliability diagram, (e) cross-method significance tests.
7. **The discussion section.** Currently 764 words on design implications. For ESWA, the discussion must focus on *engineering implications* (deployment cost, scaling, latency at 100K-job scale, integration with existing ATS) not on design implications.
8. **The user-facing design content.** Currently §3 Design Principles (G1–G4) and §5 Interactive Interface (8 portal screenshots). For ESWA, these become a single paragraph in §3.3 (System Architecture) and a figure in supplementary. ESWA is not the home for design-walkthroughs.
9. **The reference list.** Currently weighted toward HCI / XAI / human–AI interaction. For ESWA, the references should be re-balanced toward AI / recsys / HR / trustworthy AI.
10. **The title.** Currently "Understanding, Controlling, and Trusting Agentic AI: An Interactive, Explainable Job-Matching System." For ESWA, the title must be: "An Explainable and Trustworthy Multi-Agent Architecture for Job-Candidate Recommendation with Calibrated Confidence" (or a similar applied-AI title — see `POSITIONING.md`).

## What is honest to keep

The paper must remain honest. Specifically:

- The 30/15/47 corpus is small. The paper must say so, and must contextualize the small corpus as a controlled evaluation, not as a production claim.
- The LLM is decorative. The paper must say so, and must de-emphasize "agentic" if the LLM is not central.
- The fairness probe is narrow. The paper must say so, and must not claim demographic-fairness audit.
- The user study is missing. The paper must say so, and must list the planned study in future work.

These honest statements are *strengths* for ESWA reviewers, who reward transparent limitation acknowledgment.

## Specific reviewer concerns to pre-empt in the reframe

| Concern | Reframe strategy |
|---|---|
| "Figure 1 is an architecture diagram" | Replace with application context figure (recruiter + system) |
| "Architecture is standard" | Lead with the *integrated pipeline* (calibration + counterfactual + faithfulness) as the contribution, not the architecture per se |
| "Corpus is small" | Frame the small corpus as a *controlled evaluation*; report the 341-test regression gate as the engineering surface; describe the planned larger-corpus study |
| "LLM is decorative" | Either integrate the LLM more substantively (e.g., LLM-as-judge for explanation quality) or de-emphasize "agentic" in the title and abstract |
| "Baselines are limited" | Add RAG baseline, LLM-as-judge baseline, prompt-based ranking baseline |
| "Calibration is well-known" | Frame the contribution as the *integration* of calibration with component-level explanations, not the calibration itself |
| "No deployment evidence" | Report latency, throughput, and engineering surface; describe the planned deployment study in future work |
| "Counterfactual probe is small (10 pairs)" | Run a larger probe (50–100 pairs) before ESWA submission |

## Bottom line

The JAAAMAS paper is **not** a desk-reject candidate for ESWA if reframed. The numbers are strong, the engineering is honest, the limitations are stated. The reframing work is real but bounded: ~2 weeks of writing + 2–4 weeks of additional experiments (per `SUBMISSION-PLAN.md`).

After the reframing, ESWA acceptance likelihood is **55–65%** based on the fit assessment, with the principal remaining risk being the small corpus (a single, well-known limitation that can be partially addressed by adding a public baseline comparison and a sensitivity analysis).
