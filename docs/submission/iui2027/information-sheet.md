# IUI 2027 — Author Information Sheet

> Required by the IUI 2027 submission system.
> Anonymized for double-blind review; the unblinded version is filled in after notification of acceptance.

---

## Paper

**Title:** Understanding, Controlling, and Trusting Agentic AI: An Interactive, Explainable Job-Matching System

**Track:** IUI 2027 Papers (main track)

**Keywords:** Agentic AI, Human-AI Interaction, Explainable AI, Trust Calibration, User Control, Job Recommendation, Interactive Recommender Systems, Career Decision Support, LLM Agents

**Abstract (matches the PDF exactly):**

> Job seekers and recruiters today interact with recommendation systems that produce ranked lists but rarely explain themselves, leaving users unable to judge whether a top match is worth their attention or how a profile change would move their ranking. We introduce \JobMatch, an interactive, explainable agentic system that supports transparent career decision-making by combining role-aware document analysis, hybrid semantic–skill matching, and structured natural-language explanations with a calibrated confidence display. Grounded in four design principles derived from prior human–AI interaction research—transparency, explainability, user control, and multi-perspective decision support—the system organizes the matching workflow as three cooperating interaction components: a candidate-side component that helps users understand and revise what the system knows about them, an employer-side component that helps recruiters understand which requirements drive a ranking, and a read-only matchmaking component that returns ranked lists with component-level reasons. We evaluated the system on a 30-resume, 15-job demo corpus with 47 manually labeled pairs. Hybrid ranking combining resume text and skills reached nDCG@5 = 0.969 and a portal-default composite reached 0.949, with explanations showing 0.745 faithfulness and confidence scores calibrated to an expected calibration error of 0.032. The contribution is a design artifact and an evaluation methodology for interactive, explainable agentic job recommendation, not a deployment study: every consequential outcome—apply, shortlist, contact—remains an explicit user action.

## Authors (anonymized)

| Position | Anonymized | Unblinded (to fill in) |
|---|---|---|
| First author | Anonymous Author 1 | (post-acceptance) |
| Second author | Anonymous Author 2 | (post-acceptance) |
| Third author | Anonymous Author 3 | (post-acceptance) |
| Corresponding | Anonymous Author 1 | (post-acceptance) |

**Affiliation (anonymized):** Anonymous Institution, Anytown, AnyState, AnyCountry

**Contact (anonymized):** anonymous@example.com

## Artifact

**Anonymized repository:** https://anonymous.4open.science/r/jobmatch-iui2027

**Contents:**
- Prototype source (Python backend, Node frontend)
- Frozen demo corpus: 30 resumes, 15 jobs, 47 labeled pairs
- Explanation generator (rule-based + LLM-based)
- Calibration layer (Platt scaling, ECE/Brier reporting)
- Benchmark JSONs (progression, fusion, hard-negatives, calibration, fairness, latency, explainability)
- Test suite: 302 Python + 39 Node = 341 tests
- README, LICENSE, requirements.txt, package.json

**License:** MIT (or as specified by the authors' institution)

## Supplementary material

**File:** `jobmatch-iui2027-supplementary.pdf`
**Length:** 8–10 pages
**Contents:**
- §S1 Detailed architecture (former Fig 5, 6, 7 from the JAAMAS submission)
- §S2 Matchmaking internals (former Fig 5)
- §S3 Cross-encoder diagnosis (one paragraph)
- §S4 Candidate workflow (former Fig 6)
- §S5 Employer workflow (former Fig 4)
- §S6 Full method-comparison table
- §S7 Full explainability table
- §S8 Full fairness table
- §S9 Full latency table
- §S10 Implementation detail (endpoints, default parameters, test surface)
- §S11 Snapshot/event model formal definition
- §S12 Sensitivity analysis: soft-embed weight (0.5, 0.6, 0.7, 0.8)
- §S13 Hard-negative mining details
- §S14 LLM-based explainer results (currently in supplementary; if moved to main per I7, this section is a reference)

## Conflict of interest

The authors declare no conflict of interest with the IUI 2027 program committee.

## Funding

Funding is not disclosed in the anonymized version. (To be added at the unblinded stage, post-acceptance.)

## GenAI usage disclosure

During preparation of this work, the author(s) used a large language model (GPT-4 class) to assist with copy-editing of selected paragraphs and to produce initial drafts of figure captions from a structured outline. All technical content, experimental results, and design decisions are the authors' own. After using this tool, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the publication.

## Reproducibility statement

The artifact at the anonymized URL is a complete snapshot of the prototype used to produce the reported numbers.
A clean-clone run of the test suite (302 Python + 39 Node = 341 tests) passes the regression benchmark with a ±0.04 nDCG tolerance.
The frozen demo corpus is committed; no evaluation run mutates it.
The benchmark JSONs are committed; the numbers in the manuscript match the JSONs byte-for-byte.

## Suggested reviewers (optional)

The program committee retains discretion over reviewer assignment. The authors suggest reviewers with expertise in:
- Human–AI interaction (HCI / IUI / CHI)
- Explainable AI
- Recommender systems (RecSys)
- LLM-based agents
- Trust calibration

## Suggested non-reviewers (optional)

None at this time. The authors will update this field if a conflict arises before the rebuttal window.
