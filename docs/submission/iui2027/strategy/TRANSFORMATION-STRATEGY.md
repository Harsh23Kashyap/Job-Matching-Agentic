# IUI 2027 Transformation Strategy

> **Status:** Paper sections 1–9 + abstract drafted in `manuscript/sections/`.
> **Deadline:** 2026-08-20 (full paper) · 2026-08-13 (abstract) · 22 days from today (2026-07-29).
> **Author pass needed:** Author identity, copyright, ACM TAPS formatting, GenAI disclosure, supplementary PDF, anonymized artifact URL.

This document is the strategic companion to the IUI 2027 manuscript.
It records (i) what the prior submission was, (ii) why it failed for IUI, (iii) what the new submission is, and (iv) the reviewer-simulation and day-by-day plan that justified the section-level changes.

---

## 1. What the prior submission was

The JAAMAS submission framed the contribution as **"a multi-agent architecture for explainable job–candidate matching."**
The contribution list was six architecture items: a Candidate Agent, an Employer Agent, a Matchmaking Agent, an event-driven communication model, a role-separated portal layer, and an offline evaluation.
The narrative was MAS-style: ownership, snapshots, event buses, read-only matchmaking, role boundaries.
The numbers were strong (nDCG@5 = 0.949, faithfulness = 0.745, ECE = 0.032), but the framing made them supporting evidence for an architecture paper, not a user-facing contribution.

The JAAMAS editor's reject was explicit: *"the present paper does not meet these criteria"* — meaning the contribution was not substantive enough as a multi-agent systems theory paper.
The editor did not reject the *system*; they rejected the *framing* for the venue.

## 2. Why the same paper would be rejected at IUI (independent analysis)

An IUI reviewer reading the JAAMAS submission would identify four structural problems that have nothing to do with the engineering quality of the system.

| # | Problem in the JAAMAS framing | IUI reviewer perception |
|---|---|---|
| 1 | The contribution is described as "we built three agents." | This is engineering work, not an HCI contribution. |
| 2 | The paper has no design principles section. | The system has no stated design commitments; reviewers cannot evaluate against them. |
| 3 | The paper has no interaction walkthrough. | The portal screenshots are referenced but not analyzed; reviewers cannot see what the user actually experiences. |
| 4 | The metrics are reported without a user-facing mapping. | nDCG is an offline IR metric; reviewers will ask "what does this mean for the user?" |

A fifth, smaller issue: the system description leads with the architecture diagram (Fig 1), not the user problem.
IUI reviewers will read the first figure and form an opinion about whether the contribution is HCI.
A multi-agent architecture diagram in Figure 1 immediately signals "this is an engineering paper."

## 3. What the new submission is

The IUI submission reframes the contribution as **"an interactive, explainable agentic system for transparent career decision-making."**
The narrative is HCI-style: a user problem, a design gap, four design principles, an instantiation, a methodology that maps each metric to a user-facing property, an honest discussion of limitations.

The agents are not the contribution; the *interaction patterns* the agents enable are.
The architecture diagram still exists (Fig 1), but it is no longer the lead figure — the lead is the user-facing interface (Fig 3 in the IUI submission, formerly Fig 10 in the JAAMAS submission).

## 4. The reframed research question (5 alternatives)

The user asked for 5 IUI-style research questions; the chosen one is marked.

> **Q1 (selected).** How should an interactive, explainable agentic AI system be designed so that job seekers and recruiters can understand, control, and act on the recommendations it produces?
>
> **Q2.** How can explanations of career recommendations be grounded in the components that produced them, so that users can act on the explanations as guides to revision?
>
> **Q3.** What design principles support trust calibration in agentic career recommendation, and how do they manifest as interaction patterns in a working prototype?
>
> **Q4.** How should a confidence display be calibrated and presented so that users can read a confidence value as a usable signal rather than as a decoration?
>
> **Q5.** How does a role-separated, agentic architecture enable or constrain user-facing design choices, and what design choices become available only because of the role separation?

**Why Q1 is strongest.** It is broad enough to encompass the design, the system, and the evaluation; it is narrow enough that a reviewer can recognize whether the paper answers it; and it has the three HCI verbs (understand, control, act) that signal the paper's commitments.

## 5. The 15 candidate titles

| # | Title | Verdict |
|---|---|---|
| 1 | Understanding, Controlling, and Trusting Agentic AI: An Interactive, Explainable Job-Matching System | **Selected** |
| 2 | Agentic AI for Career Decision Support: Designing Transparent and Controllable Job Recommendation | Strong alternate |
| 3 | Calibrated Confidence in Agentic Recommendations: Designing for Trust in Career AI | Strong alternate |
| 4 | Designing User Control and Explanation in Agentic Job Recommendation | Strong alternate |
| 5 | An Interactive System for Explainable, Trust-Calibrated Job–Candidate Matching | Strong alternate |
| 6 | Trust in Agentic Recommendations: A User-Centered Design for Explainable Job Matching | OK |
| 7 | Beyond the Ranking: Designing User Control and Explainability into Agentic Job Recommendation | OK |
| 8 | When AI Recommends Jobs: Designing Transparent Agentic Interfaces for Career Search | OK |
| 9 | User Trust and Control in Agentic Career Recommendation: A Design-Centered Study | OK |
| 10 | Toward Trustworthy Agentic AI: An Interactive Job-Matching Interface with Calibrated Explanations | OK |
| 11 | Multi-Perspective Explanations in Agentic AI: A User-Centered Approach to Job Recommendation | OK |
| 12 | From Black-Box Ranking to Interactive Career Decisions: Designing Explainable Agentic Job Matching | OK |
| 13 | How Users Engage with Agentic Job Recommendations: Interaction Design, Explanations, and Trust | OK |
| 14 | Agentic AI in the Hands of Users: An Interface for Transparent, Controllable Job Matching | OK |
| 15 | Designing for Trust Calibration in Agentic AI Job Matching | OK |

**Why #1 wins.** The three verbs (Understanding, Controlling, Trusting) telegraph the HCI contribution in the title alone. A reviewer scanning the program can place the paper without reading the abstract.

## 6. The four design principles (G1–G4)

| Principle | Statement | Operationalized by | Reported in |
|---|---|---|---|
| **G1 Transparency of state** | The user can see, before any recommendation is computed, what the system has parsed and what it will compare. | The parsed-fields review form in the candidate and employer portals; the snapshot confirmation gate. | §6.2 (recommendation quality), §7 (results) |
| **G2 Faithful, component-level explanations** | Every list item carries an explanation that names the input fields that contributed to its position. | The rule-based explainer bound to the composite channels; the LLM-based explainer as comparison. | §6.3 (faithfulness), §7.3 (results) |
| **G3 User control at consequential points** | Three actions (apply, shortlist, contact) require a user gesture and remain reversible. | The action menu in the match list; the snapshot revert view; the counterfactual view. | §6.4 (calibration), §6.5 (counterfactual), §7.4–7.5 (results) |
| **G4 Multi-perspective decision support** | The composite score is exposed as separable channels, not collapsed into a single value. | The component-level reason in the explanation drawer; the channel-weight display. | §6.2 (recommendation quality), §7.1 (results) |

## 7. Section-by-section rewrite plan (priority matrix)

| Current JAAMAS section | Problem for IUI | Required change | Priority |
|---|---|---|---|
| §1 Introduction | Leads with architecture (3 agents) instead of user problem. | Rewrite as user-problem-first, contribution-as-design, with three concrete challenges. | **Critical** |
| §2 Related Work | Reads as MAS literature review; no HCI grounding. | Rewrite as four streams (interactive recsys, XAI, human–AI decision, LLM agents) with HCI anchors. | **Critical** |
| §3 Architecture | Describes agents as engineering modules. | Add new §3 "Design Principles" (G1–G4). Move architecture to new §4 "System Design" and reframe agents as interaction components. | **Critical** |
| (new) | No design principles section. | Add G1–G4 with HCI grounding (Amershi, Shneiderman, Miller, Liao). | **Critical** |
| (new) | No interaction walkthrough. | Add new §5 "Interactive Interface" that walks through all 8 portal screenshots as design artifacts. | **Critical** |
| §4 Implementation | Heavy on internal libraries/APIs. | Cut most implementation detail; move to supplementary. | **Important if time** |
| §5 Quality Metrics | Metric definitions only. | Rewrite as §6 "Methodology" with metric-to-property mapping. | **Critical** |
| §6 Results | Strong numbers, weak user-facing interpretation. | Rewrite as §7 with each result mapped to a user-facing property. | **Critical** |
| §6 Strengths + Limitations | Combined, with no implications section. | Rewrite as §8 with separate Implications / Limitations / Future Work / Broader Perspective. | **Important if time** |
| §7 Conclusion | Short, technical. | Rewrite as §9 with HCI-style close, contributions restated, no claims of deployment. | **Important if time** |
| Tables | 11 tables, several with implementation detail. | Keep all 11 in supplementary. Promote only the progression table to main. | **Important if time** |
| Figures | 9 figures, 7 architecture diagrams. | Keep architecture diagrams. Promote portal screenshots to lead figure. | **Important if time** |

## 8. Reviewer simulation (3 reviewers)

### Reviewer R1 — HCI researcher (e.g., a CHI / IUI program committee member)

> **Overall score:** 6/10 → "borderline accept, lean accept after rebuttal"
>
> **Strengths.** The four principles give the paper a clear HCI spine; the principle-to-metric mapping is rare in IUI submissions and immediately answers "what does the system do for the user?"; the role-separated layout is a credible answer to the "where is the user in agentic AI" question; the calibration reporting is honest.
>
> **Weaknesses.** The user study is missing; the corpus is small; the explanation specificity number (0.627) will draw the question "is that good enough?"; the screenshot walkthrough, while useful, reads more like a tour than an analysis.
>
> **Reject reasons if pushed.** "This is a system paper with HCI language; the user-facing claims need a user study to back them."
>
> **Required fixes to clear the bar.** (a) Acknowledge the missing user study prominently and describe a concrete plan; (b) report at least one pilot with n ≥ 5 users or two think-aloud sessions; (c) soften the explanation coverage claim.

### Reviewer R2 — AI / recommender systems researcher

> **Overall score:** 7/10 → "accept, minor revision"
>
> **Strengths.** The baseline comparison is honest and complete (BM25, TF–IDF, semantic, hybrid, RRF, cross-encoder); the significance tests are reported; the calibration is reported with Platt parameters; the cross-encoder-disable decision is correctly documented.
>
> **Weaknesses.** The cross-encoder nDCG drop is interesting and is not interrogated; the soft-embed weight of 0.7 is reported without a sensitivity analysis; the learned fusion is fit on the same labeled pairs it is judged against.
>
> **Reject reasons if pushed.** "The numbers are good but the engineering details are in supplementary; I want to see why the cross-encoder underperforms."
>
> **Required fixes to clear the bar.** (a) Add a one-paragraph cross-encoder diagnosis in the supplementary; (b) add a sensitivity table for the soft-embed weight; (c) note the learned-fusion overfitting concern in the limitations.

### Reviewer R3 — LLM agent researcher

> **Overall score:** 5/10 → "borderline reject, weak accept"
>
> **Strengths.** The role-separation idea is a real contribution to the agent literature; the snapshot/event model is a clean way to formalize "the user is the boundary"; the read-only constraint is a strong design commitment.
>
> **Weaknesses.** The agents in the prototype are not LLM-driven in their core loops; the LLM is used only for parsing and explanation generation. The "agentic AI" framing in the title will draw the question "what is agentic about this?" The LLM-based explainer is in supplementary, not in the main results.
>
> **Reject reasons if pushed.** "This is a multi-component system, not an agentic system; the LLM is decorative."
>
> **Required fixes to clear the bar.** (a) Either de-emphasize "agentic" in the title and abstract, or strengthen the LLM-driven component; (b) move the LLM-based explainer results into the main paper; (c) explicitly state that the LLM is currently used for parsing and explanation and is the focus of future work, not the contribution.

**Composite read.** R1 and R2 will likely vote accept; R3 is the swing. The lowest-cost fix is to soften the "agentic" framing in the title and abstract — the LLM is genuinely used in the system, but the agentic-vs-component distinction is a reviewer-perception issue, not a correctness issue.

**Minimum changes to move from reject → borderline accept:**
1. Acknowledge the missing user study prominently in the abstract and §8.
2. Add a sensitivity table for the soft-embed weight to supplementary.
3. Add a one-paragraph cross-encoder diagnosis to supplementary.
4. Move the LLM-based explainer results into the main paper (one extra paragraph in §7).
5. Soften "agentic AI" in the title and abstract, or add a one-sentence clarification.

## 9. Day-by-day plan (3 weeks to Aug 20, 2026)

| Day | Date | Task | Output |
|---|---|---|---|
| D1 | Wed Jul 29 | Review this strategy doc; lock the title and principles; commit the IUI folder. | `main.tex`, `iui-macros.tex`, `iui-style.tex`, `references.bib`, all 9 sections + abstract committed. |
| D2 | Thu Jul 30 | Strip self-identifying citations (`\blindcite`); replace author/affiliation placeholders. | Anonymized main.tex. |
| D3 | Fri Jul 31 | Move implementation detail to supplementary; promote the portal screenshots to lead figure. | Re-organized figures and tables. |
| D4 | Sat Aug 1 | First author pass on the 9 sections; mark `TODO` items. | Marked-up tex. |
| D5 | Sun Aug 2 | Resolve `TODO` items; cross-check numbers against the committed benchmark artifacts. | Cleaned tex. |
| D6 | Mon Aug 3 | Dry-run compilation; fix LaTeX errors; run latex_lint. | Compiling PDF. |
| D7 | Tue Aug 4 | Pre-final PDF read-through; check page count, line numbers, anonymization. | Pre-final PDF. |
| D8 | Wed Aug 5 | Build the anonymized artifact at anonymous.4open.science. | Anonymized artifact URL. |
| D9 | Thu Aug 6 | Supplementary PDF; merge references. | Supplementary PDF. |
| D10 | Fri Aug 7 | Add GenAI Usage Disclosure paragraph to main.tex. | Disclosure added. |
| D11 | Sat Aug 8 | Add ACM CCS classification; verify keywords. | Classification done. |
| D12 | Sun Aug 9 | Author pass 2; cut to 8K words if over. | Tightened prose. |
| D13 | Mon Aug 10 | Final LaTeX pass; fix floats; check captions. | Submission-ready PDF. |
| D14 | Tue Aug 11 | **SUBMIT ABSTRACT (PCS 2.0, Aug 13 deadline)** — register the submission, enter title + abstract + authors. | Abstract submitted. |
| D15 | Wed Aug 12 | Reserve: final abstract edits in PCS. | Buffer. |
| D16 | Thu Aug 13 | **ABSTRACT HARD DEADLINE** | Abstract locked. |
| D17 | Fri Aug 14 | Final paper pass; check ACM TAPS compliance. | Final paper. |
| D18 | Sat Aug 15 | Author final review; read PDF end-to-end. | Final pass. |
| D19 | Sun Aug 16 | Reserve: cover-letter and information-sheet finalization. | Buffer. |
| D20 | Mon Aug 17 | Upload supplementary to PCS. | Supplementary attached. |
| D21 | Tue Aug 18 | **FINAL PRE-SUBMISSION CHECK** — verify PCS submission preview, anonymization, all required fields. | Submission verified. |
| D22 | Wed Aug 19 | **SUBMIT FULL PAPER** (Aug 20 AoE deadline). | Submitted. |
| D23 | Thu Aug 20 | **HARD DEADLINE (AoE)** | — |

The plan has explicit buffers on D15, D19, and D21.
LaTeX always surprises; the buffers are not optional.

## 10. Final reviewer assessment

If I received the current IUI submission as a reviewer, I would score it as follows.

> **Score:** 6.5/10 → borderline accept.
>
> **Strengths.** The reframing is clean; the principles are well grounded; the metric-to-property mapping is rare and useful; the calibration reporting is honest; the cross-encoder-disable decision is correctly documented; the limitations are stated without hand-waving.
>
> **Weaknesses.** The user study is the most likely rejection vector; the corpus is small; the LLM-based explainer results are in supplementary; "agentic" in the title is a perception risk.
>
> **Acceptance probability.** ~50% on first submission, ~75% after a minor revision that addresses the user-study and LLM-explainer issues.
>
> **Last-minute fixes that move the needle most.**
> 1. (5 min) Add a sentence to the abstract acknowledging the absence of a user study and pointing to the planned one. This pre-empts the most common reviewer objection.
> 2. (20 min) Move the LLM-based explainer paragraph from supplementary to §7.3. This addresses R3 directly.
> 3. (10 min) Soften "agentic" in the title to "interactive, explainable AI" or add a one-line clarification in the abstract. This is a perception fix, not a correctness fix.
> 4. (15 min) Add a sensitivity row for the soft-embed weight (0.5, 0.6, 0.7, 0.8) to supplementary Table S2. R2 will appreciate it.
> 5. (5 min) Add the cross-encoder diagnosis paragraph to supplementary §S3. R2 will appreciate it.

These five fixes take about an hour of author time and address 80% of the reviewer risk identified in §8.
