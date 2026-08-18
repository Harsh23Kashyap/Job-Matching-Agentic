> **STALE — pre-numbers-pass planning notes.** Numbers below are superseded. Canonical values: composite nDCG@5 0.949, strongest single 0.924, semantic 0.878, RRF 0.913; held-out ECE 0.019 (low discrimination); ranking parity — not significant (two-sided p=0.10, fails Holm); counterfactual = 50-pair recourse-null; artifact DOI upon acceptance. See research/reports/FINAL_NUMERICAL_AUDIT.md.

# ESWA Positioning — Direction Choice & Contribution

> **Goal:** Lock the single strongest ESWA positioning for the JobMatch manuscript.
> **Decision date:** 2026-07-29.
> **Decision:** **Direction C + E combined — Explainable + Trustworthy, with multi-agent as supporting detail.**

---

## The 5 candidate directions

| Direction | Hook | Strength for ESWA | Weakness for ESWA |
|---|---|---|---|
| **A. Agentic AI framework for intelligent decision support** | "agentic" is a 2024–2026 buzzword | ESWA has been publishing on multi-agent systems for 30 years; "agentic" is the new label for an old idea | The paper's agents are not LLM-driven in their core loops; the term invites the question "what is agentic about this?" |
| **B. Knowledge-driven multi-agent recommendation system** | KBS-friendly framing | Tight fit for the snapshot model, skill vocabulary, and rule-based explainer | This is a KBS positioning more than an ESWA positioning; KBS has a tighter knowledge-engineering identity |
| **C. Explainable AI recommendation architecture** | ESWA's #1 recurring theme | XAI is the strongest single thread at ESWA right now; the paper has explainability content (faithfulness, counterfactual, consistency) | The "recommendation architecture" framing is generic; needs a specific technical hook |
| **D. Hybrid LLM + retrieval-based intelligent matching system** | LLM+RAG is the 2024–2026 hot area | Aligns with the LLM-as-explainer use case | The LLM is decorative in the paper; this would invite the question "where is the LLM in the ranking?" |
| **E. Trustworthy AI system with calibrated recommendations** | ESWA's #2 recurring theme | Trust calibration is a clean engineering contribution; the Platt-scaled composite is novel in the recsys context | The "trustworthy AI" label is broad; needs a specific instantiation |

## Decision: C + E (Explainable + Trustworthy, with multi-agent as supporting detail)

The strongest single positioning is the **combination** of C and E, because:

1. **Both are top-3 themes at ESWA** (XAI and trustworthy AI are consistently the most-cited ESWA papers).
2. **The paper's actual content supports both** — faithfulness + counterfactual + consistency support C; Platt scaling + ECE + adversarial probe support E.
3. **The "multi-agent" detail is supporting**, not the headline. The agents are an implementation choice that supports the explainable + trustworthy properties, not the contribution itself.
4. **The technical hook is specific** — "calibrated confidence" is a concrete technical claim, not a vague label.

## Locked title (10 candidates, ranked)

| # | Title | Verdict |
|---|---|---|
| **1** | **An Explainable and Trustworthy Multi-Agent Architecture for Job-Candidate Recommendation with Calibrated Confidence** | **SELECTED** |
| 2 | A Knowledge-Driven Multi-Agent Recommendation System for Transparent Career Decision Support | Strong alternate (KBS-leaning) |
| 3 | Explainable AI for Recruitment: A Multi-Agent Approach with Calibrated Confidence and Knowledge-Driven Reasoning | Strong alternate (HCI-leaning) |
| 4 | A Trustworthy Multi-Agent Recommendation Framework with Faithful Explanations for Career Platforms | OK |
| 5 | Hybrid Semantic-Skill Matching with Component-Level Explanations and Calibrated Confidence for Recruitment | OK (technical) |
| 6 | An Intelligent Multi-Agent System for Explainable Job-Candidate Matching with Uncertainty Quantification | OK |
| 7 | A Multi-Agent Architecture for Job-Candidate Matching with Component-Level Explanations and Reliability-Aware Ranking | OK |
| 8 | Knowledge-Enhanced Multi-Agent Reasoning for Explainable Job-Candidate Recommendation | OK (KBS-leaning) |
| 9 | An Intelligent Recommendation System Combining Semantic Retrieval, Knowledge Grounding, and Calibrated Confidence for the Recruitment Domain | OK (long) |
| 10 | A Trustworthy AI Framework for Career Recommendation: Combining Hybrid Retrieval, Component Explanations, and Confidence Calibration | OK |

**Why #1 wins.** "Explainable" and "Trustworthy" are both top-3 ESWA themes; "Multi-Agent Architecture" is the implementation substrate without being the headline; "Job-Candidate Recommendation" is the application domain; "Calibrated Confidence" is the specific technical hook. The title is parseable in one read and pre-empts the "what is novel" question.

## Locked contribution statement (for the introduction)

The contribution of this paper is a multi-agent recommendation architecture for job–candidate matching that integrates four methodological contributions into a single, validated pipeline:

1. **A composite ranking with explicit channel decomposition.** We separate the ranking score into six channels (semantic, skill, title, experience, compensation, remote), each contributing a documented weight (0.28, 0.27, 0.10, 0.15, 0.10, 0.10), and report the contribution of each channel in the explanation panel. The decomposition enables component-level explanations without post-hoc attribution.

2. **A calibrated confidence display for ranking systems.** We apply Platt scaling to the composite ranking output and report a confidence value alongside the ranked list. The calibration reduces the expected calibration error from 0.40 to 0.032, a 12× improvement, and is evaluated on a held-out calibration set with 21 strong and 26 partial labels. To our knowledge, this is the first application of Platt-scaled confidence to a multi-channel recsys composite.

3. **A component-level faithfulness evaluation with counterfactual probe.** We introduce a faithfulness metric suite (faithfulness, specificity, consistency, skill-mention coverage) that evaluates whether explanation bullets correspond to the channels that produced the score, and a counterfactual probe that tests whether single-field edits predicted by the explanation move the rank. The probe finds 7 of 10 pairs are flagged, top-1 stable in all cases, with a maximum score shift of 0.017.

4. **A reproducible engineering surface.** The prototype, the frozen demo corpus (30 resumes, 15 jobs, 47 labeled pairs), the explanation generator, the calibration layer, and a 341-test regression-gated benchmark are released as an open-source artifact. A clean-clone run of the test suite reproduces the reported numbers within a ±0.04 nDCG tolerance.

These four contributions are integrated into a multi-agent system with role-separated ownership (candidate-side, employer-side, read-only matchmaking) and validated on the recruitment domain. The application consequence is a transparent, calibrated decision-support tool for the recruitment workflow; the methodological consequence is a reusable pipeline for explainable, trustworthy recommendation in any domain with structured documents and labeled pairs.

## Locked application framing (for §1)

> "Online hiring platforms process millions of resume–job pairs annually, yet the systems that rank them typically return a single opaque score with no breakdown of which resume fields or job requirements drove the ranking. This opacity creates a documented accountability gap: recruiters cannot justify shortlist decisions, candidates cannot act on what would change their rank, and neither side can detect when a model's behavior shifts under small input perturbations. We address this gap with an applied AI system for the recruitment domain that integrates hybrid retrieval, component-level explanations, and a calibrated confidence display into a single, validated pipeline."

This framing leads with the *engineering problem* (recruitment at scale, accountability gap), not the *design problem* (opaque recommendations from the user's perspective). The shift is small but consequential for ESWA reviewers.

## Locked methodology framing (for §3)

The methodology section is the longest in the paper (~2,200 words) and is structured to support the four contributions:

- **§3.1 Problem Formulation and Notation.** Resume–job pair scoring as a learning-to-rank problem with explanation and confidence requirements.
- **§3.2 Multi-Agent System Architecture.** The role-separated layout (candidate-side, employer-side, read-only matchmaking), justified as a *design-for-accountability* choice rather than as a contribution per se.
- **§3.3 Knowledge Representation and Retrieval.** The skill vocabulary, snapshot model, and hybrid retrieval (BM25 + sentence-BERT + Jaccard skill overlap + soft-embed skill fusion).
- **§3.4 Composite Ranking with Component Decomposition.** The six-channel composite, the weight selection, the learned fusion alternative, and the comparison to the single-channel baselines.
- **§3.5 Component-Level Explanation Generation.** The rule-based explainer bound to channels, the LLM-based explainer as a comparison, the explanation scoring function.
- **§3.6 Confidence Calibration.** The Platt scaling, the calibration set, the reliability diagram, the Brier score.
- **§3.7 Implementation Details.** The technology stack, the test surface, the latency profile.

## Locked experiments (for §4–§5)

The experiments section adds three new baselines to the existing benchmarks:

- **RAG baseline** (retrieval-augmented generation using sentence-BERT embeddings + GPT-class LLM as a reranker). This is the strongest 2024–2026 baseline for any retrieval task and is the one ESWA reviewers will ask about.
- **LLM-as-judge baseline** (zero-shot GPT-class prompting for ranking with chain-of-thought). This is the strongest prompt-based baseline.
- **Production-style baseline** (a simple learned-to-rank model: logistic regression on the six channel scores). This is the strongest "if you only had one number per pair" baseline.

The existing benchmarks (BM25, TF–IDF, semantic cosine, hybrid multimodal, RRF, cross-encoder) are preserved with the JAAMAS numbers.

A **sensitivity analysis** on the Platt parameters (a, b) is added to §5 to support the calibration contribution.

A **larger counterfactual probe** (50–100 pairs, not 10) is added to §5 to address the small-probe concern.

## Locked discussion framing (for §6)

The discussion section is rewritten to focus on *engineering implications*:

- **Deployment cost** (latency at 100K-job scale, throughput, integration with existing ATS).
- **Trust calibration in production** (the 12× ECE reduction is a strong claim; discuss what would change at scale).
- **Explanation specificity trade-off** (the rule-based explainer has 0.627 specificity; the LLM-based explainer has higher specificity but lower faithfulness; discuss the trade-off).
- **Fairness probe limitations** (the 10-pair probe is narrow; discuss what would be required for a production deployment).
- **Path to deployment** (what an industrial partner would need to validate before deploying).

The IUI-style design-implications content (G1–G4) is reduced to a single paragraph in §3.2 and moved to supplementary.

## Locked limitations (for §6.5)

The limitations section is explicit and unhedged:

- Corpus is small (30/15/47). A larger-corpus study is in progress.
- No live user study. A pilot study with n=10–15 is planned.
- Fairness probe is narrow (10 pairs). A larger probe with controlled demographic attributes is planned.
- Cross-encoder is disabled by default (141.7 ms latency, 0.108 nDCG drop). The diagnosis is in supplementary.
- LLM is decorative (used for parsing and explanation, not ranking). The integration of the LLM into the ranking loop is future work.

These limitations are *strengths* for ESWA reviewers, who reward transparent limitation acknowledgment.
