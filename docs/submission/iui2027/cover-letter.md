# Cover Letter — IUI 2027 Submission

**To:** IUI 2027 Program Chairs
**From:** Anonymous Authors
**Re:** Submission of *"Understanding, Controlling, and Trusting Agentic AI: An Interactive, Explainable Job-Matching System"* to the 32nd ACM Conference on Intelligent User Interfaces (IUI 2027)
**Date:** 2026-08-13

---

Dear IUI 2027 Program Chairs,

We are pleased to submit our manuscript for consideration at IUI 2027.
The paper presents **\JobMatch**, a research prototype for interactive, explainable agentic career recommendation, and is positioned at the intersection of human–AI interaction, explainable AI, and LLM-based agentic systems.

## Contribution

The contribution of the paper is a **design artifact and an evaluation methodology** for interactive agentic career recommendation, not a deployment study.
The system organizes a job–candidate matching workflow as three cooperating interaction components, each described by the user need it addresses, the information it returns, and the control it preserves.
Four design principles—**transparency of state, faithful component-level explanations, user control at consequential points, and multi-perspective decision support**—anchor the design.
An evaluation methodology maps each principle to a measurable property: recommendation quality (nDCG@5), explanation faithfulness, confidence calibration (ECE), counterfactual probe, and adversarial robustness.

## Why IUI

IUI is the natural home for this work for three reasons.
First, the contribution is an interaction surface, not a model: the system exists to support transparent, controllable decisions, and the design choices are visible in the user-facing surface.
Second, the agentic framing aligns with the IUI 2027 call's stated interest in "user interactions with LLMs, workplace applications, bias, and user control" — all four are present in the prototype.
Third, the evaluation methodology treats each metric as a user-facing property, which is the orientation the IUI community has consistently argued for in explainability and trust-calibration research.

## What the paper is not

The paper is not a deployment study.
The prototype is a research artifact, the evaluation is on a fixed demo corpus of 30 resumes and 15 jobs, and the user-facing claims are about the design and the methodology, not about production-scale hiring outcomes.
The paper is not a comparative study against deployed hiring tools; we discuss this as future work.
The paper is not an LLM-architecture paper; the LLM is currently used for parsing and explanation generation, and the agentic component separation is the contribution, not the LLM capability.

## Anonymization and conflicts of interest

The submission is anonymized for double-blind review.
All author names, affiliations, and acknowledgments have been removed from the manuscript.
Self-citations to the authors' prior work have been replaced with `[Anonymous, year]` placeholders.
The artifact (code, data, benchmarks) is available at an anonymized URL: `https://anonymous.4open.science/r/jobmatch-iui2027`.
The authors declare no conflict of interest with the IUI 2023, 2024, 2025, 2026, or 2027 program committees.

## Suggested reviewers

The following researchers work in adjacent areas and may be well-positioned to evaluate the submission (suggestions only; the program committee retains discretion):

- (HCI / XAI) — see IUI 2026 program committee for current candidates
- (Recommender systems / calibration) — see RecSys 2026 senior PC
- (LLM-based agents) — see IUI 2026/2027 program committee

We respectfully ask that the following individuals not review this submission due to recent collaboration (none in this case, but the program committee may have other reasons).

## Supplementary material

A separate supplementary PDF is uploaded with the submission, containing the full method-comparison table, the calibration curves, the hard-negatives table, the full explainability table, the full fairness table, the full latency table, and the implementation detail.
The supplementary material is reference, not extension; the main paper is self-contained.

## Reproducibility

The artifact at the anonymized URL includes the prototype, the frozen demo corpus, the explanation generator, the calibration layer, and the regression benchmark.
A clean-clone run of the test suite (302 Python + 39 Node = 341 tests) is the documented reproducibility check.
The committed benchmark JSONs match the numbers reported in the manuscript.

Thank you for considering this submission.
We look forward to the reviewer's feedback.

Sincerely,

Anonymous Authors
on behalf of the JobMatch research team
