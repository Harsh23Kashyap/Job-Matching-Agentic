# ESWA Submission Plan — 12 Weeks

> **Target:** Post-IUI-rejection submission to Expert Systems with Applications.
> **Trigger to start:** IUI 2027 final decision notification (2026-11-23).
> **Earliest ESWA submission:** 2027-01-15 (8 weeks after IUI notification, 2 weeks of buffer).
> **Acceptance probability at end of plan:** 55–65%.
> **Owner:** Harsh Kashyap + Parteek Kumar (Sir).

---

## Calendar

| Week | Dates (post-IUI) | Goal | Output |
|---|---|---|---|
| W1 | Nov 24 – Nov 30 | **Reframe the introduction and abstract.** New lead (HR engineering problem), new contribution statement, new title. | New §1 + new abstract. |
| W2 | Dec 1 – Dec 7 | **Replace Figure 1 + extend the methodology.** New lead figure (application context), new §3 methodology (2,200 words), new related work. | New §2, §3; new Figure 1. |
| W3 | Dec 8 – Dec 14 | **Add the missing experiments.** RAG baseline, LLM-as-judge baseline, sensitivity analysis on Platt parameters, larger counterfactual probe (50 pairs). | New §4 (extended) + new §5 (extended). |
| W4 | Dec 15 – Dec 21 | **Build the new figures.** Reliability diagram, application context figure, methodology flow figure, component contribution figure. | 4 new figures. |
| W5 | Dec 22 – Dec 28 | **Rewrite the discussion + limitations.** Engineering implications, deployment cost, cross-encoder diagnosis, larger counterfactual analysis. | New §6. |
| W6 | Dec 29 – Jan 4 | **Move LLM-based explainer to main paper.** Run the LLM-based explainer, report results, compare to rule-based. | New §5.3. |
| W7 | Jan 5 – Jan 11 | **Final pass on the manuscript.** Coherence, term consistency, claim–evidence check, word count (target 8,500–9,000). | Submission-ready draft. |
| W8 | Jan 12 – Jan 18 | **Internal review.** Send to Parteek + 1 external reviewer (HCI/recsys expert). | Reviewed draft + reviewer comments. |
| W9 | Jan 19 – Jan 25 | **Address reviewer comments.** Resolve each comment in a point-by-point response. | Final manuscript. |
| W10 | Jan 26 – Feb 1 | **Final polish.** Cover letter, highlights (3–5 × ≤85 chars), CRediT statement, data availability, GenAI disclosure, ORCID for corresponding author. | Submission package. |
| W11 | Feb 2 – Feb 8 | **Editorial Manager setup.** Author accounts, ORCID, institutional email, CRediT roles, conflict of interest, suggested reviewers. | EM submission prepared. |
| W12 | Feb 9 – Feb 15 | **Submit.** Upload main PDF, supplementary, highlights, cover letter, all required fields. | **Submitted.** |

**Buffer:** 2 weeks of buffer between W12 (submit) and the next critical date. The plan absorbs a 1-week delay without missing the target.

---

## Week-by-week detail

### Week 1 — Reframe the introduction and abstract

**Goal:** Replace the IUI-style framing with the ESWA applied-AI framing.

**Tasks:**
- [ ] Rewrite the abstract (250 words, ESWA structure: problem + limitation + AI methodology + application + validation + results).
- [ ] Rewrite §1 introduction (1,200 words, lead with HR engineering problem).
- [ ] Write the new contribution statement (4 bullets, per `POSITIONING.md`).
- [x] Lock the title: *"An Auditable, Calibrated, and Explainable Multi-Agent System for Job-Candidate Recommendation."* (changed 2026-08-18; dropped "Trustworthy"; reversible on author request)
- [ ] Update the keywords (6–8 terms, AI/recsys/HR weighted).

**Owner:** Harsh.

**Output:** New abstract.tex + new section-1-introduction.tex.

---

### Week 2 — Replace Figure 1 + extend the methodology

**Goal:** Make the paper look like an applied-AI paper, not a conference demo.

**Tasks:**
- [ ] Replace Figure 1 with an *application context* figure (a recruiter or job-seeker using the system, with the system as a black box).
- [ ] Rewrite §2 related work (5 streams: AI-based recommendation, semantic matching, knowledge-driven AI, LLM agents, XAI for recsys, trustworthy AI).
- [ ] Expand §3 methodology to 2,200 words with 7 subsections (per `POSITIONING.md`).
- [ ] Move the IUI-style G1–G4 design principles to a single paragraph in §3.2.
- [ ] Move the IUI-style interface walkthrough (§5 in IUI paper) to supplementary.

**Owner:** Harsh.

**Output:** New section-2-related-work.tex, new section-3-methodology.tex (2,200 words), new Figure 1.

---

### Week 3 — Add the missing experiments

**Goal:** Address R1 + R2 reviewer concerns about limited baselines.

**Tasks:**
- [ ] Implement and run an RAG baseline (retrieval-augmented generation with sentence-BERT + GPT-class LLM reranker). Target: 1 day.
- [ ] Implement and run an LLM-as-judge baseline (zero-shot GPT-class prompting for ranking with chain-of-thought). Target: 1 day.
- [ ] Run a sensitivity analysis on the Platt parameters (a, b) — vary a in {0.2, 0.298, 0.4} and b in {-1.5, -2.116, -2.5}, report ECE. Target: 1 day.
- [ ] Run a larger counterfactual probe (50 pairs, not 10). Target: 2 days.
- [ ] Update the calibration set: add 30 more pairs (51 strong + 56 partial total). Target: 2 days.

**Owner:** Harsh + Parteek (Sir provides compute access if needed).

**Output:** New §5.2 (extended baselines) + new §5.4 (sensitivity analysis) + new §5.5 (larger counterfactual probe).

---

### Week 4 — Build the new figures

**Goal:** Replace the architecture-diagram-heavy figure set with applied-AI figures.

**Tasks:**
- [ ] Build Figure 1 (application context figure): a recruiter or job-seeker using the system, with the system as a black box. Crop from existing portal screenshots or generate a new mockup.
- [ ] Build Figure 2 (reliability diagram): uncalibrated vs calibrated, 10 bins, sample counts. Use the calibration set (51 strong + 56 partial).
- [ ] Build Figure 3 (methodology flow): input → retrieval → ranking → explanation → calibration → output. One-page flowchart.
- [ ] Build Figure 4 (component contribution): bar chart of the six channel contributions to a sample ranking. Use the JAAMAS results.
- [ ] Build Figure 5 (architecture overview, now in supplementary): the role-separated layout, de-emphasized.

**Owner:** Harsh.

**Output:** 4 new figures + 1 demoted figure.

---

### Week 5 — Rewrite the discussion + limitations

**Goal:** Focus the discussion on engineering implications, not design implications.

**Tasks:**
- [ ] Rewrite §6 discussion: deployment cost, latency at scale, integration with ATS, trust calibration in production, explanation specificity trade-off, fairness probe limitations.
- [ ] Add a deployment cost estimate: engineering hours to deploy at 100K-job scale, infrastructure cost, ongoing maintenance.
- [ ] Add a one-paragraph cross-encoder diagnosis to the main paper.
- [ ] Add the larger counterfactual analysis (50 pairs).
- [ ] Move the IUI-style "lessons for interactive AI design" to a single paragraph in §3.2.

**Owner:** Harsh + Parteek (cost estimate).

**Output:** New section-6-discussion.tex (engineering-focused).

---

### Week 6 — Move LLM-based explainer to main paper

**Goal:** Address R1 + R3 reviewer concerns about the LLM being decorative.

**Tasks:**
- [ ] Run the LLM-based explainer on the 47 labeled pairs.
- [ ] Compare rule-based vs LLM-based on the metric suite (faithfulness, specificity, consistency, skill-mention coverage).
- [ ] Write §5.3: explanation methods comparison.
- [ ] Discuss the trade-off (rule-based is more faithful, LLM-based has higher skill-mention coverage).

**Owner:** Harsh.

**Output:** New §5.3.

---

### Week 7 — Final pass on the manuscript

**Goal:** Submission-ready draft.

**Tasks:**
- [ ] Read the manuscript end-to-end. Check for: claim–evidence alignment, term consistency, broken cross-references, broken sentences.
- [ ] Word count check (target 8,500–9,000).
- [ ] Run `latex_lint.sh` and `latex_wordcount.sh`.
- [ ] Run `latex_citation_extract.sh` to verify all `\cite{...}` resolve.
- [ ] Verify all numbers in §5 match the committed benchmark JSONs.

**Owner:** Harsh.

**Output:** Submission-ready draft.

---

### Week 8 — Internal review

**Goal:** External review before submission.

**Tasks:**
- [ ] Send the manuscript to Parteek (Sir).
- [ ] Send the manuscript to 1 external reviewer (HCI/recsys expert, ideally someone who has reviewed for ESWA).
- [ ] Wait 5–7 days for comments.
- [ ] Compile comments in a single document.

**Owner:** Harsh + Parteek.

**Output:** Reviewed draft + reviewer comments.

---

### Week 9 — Address reviewer comments

**Goal:** Final manuscript.

**Tasks:**
- [ ] Address each comment in a point-by-point response.
- [ ] Re-run any experiments that the reviewer requested.
- [ ] Update the manuscript with the response.

**Owner:** Harsh.

**Output:** Final manuscript.

---

### Week 10 — Final polish

**Goal:** Submission package.

**Tasks:**
- [ ] Write the cover letter (250–400 words, per ESWA cover letter structure).
- [ ] Write the highlights (3–5 bullets, ≤85 characters each, per `highlights.md`).
- [ ] Write the CRediT statement (14 standard roles).
- [ ] Write the data availability statement.
- [ ] Write the GenAI disclosure.
- [ ] Get ORCID for the corresponding author (Parteek if he's the corresponding, or Harsh if Parteek defers).
- [ ] Confirm institutional email for all authors.

**Owner:** Harsh.

**Output:** Submission package.

---

### Week 11 — Editorial Manager setup

**Goal:** EM submission prepared.

**Tasks:**
- [ ] Create author accounts on Editorial Manager (if not already).
- [ ] Enter the title, abstract, keywords.
- [ ] Enter the CRediT roles.
- [ ] Enter the conflict of interest declarations.
- [ ] Enter the funding source (NVIDIA Academic Grant or "no external funding").
- [ ] Suggest 2–4 preferred reviewers (HCI/recsys/ESWA experts).
- [ ] Identify 1–2 non-preferred reviewers (if any).

**Owner:** Harsh.

**Output:** EM submission prepared.

---

### Week 12 — Submit

**Goal:** Submitted to ESWA.

**Tasks:**
- [ ] Upload main PDF.
- [ ] Upload supplementary PDF.
- [ ] Upload highlights (separate file).
- [ ] Upload cover letter.
- [ ] Upload figures (separate files).
- [ ] Verify the submission preview in EM.
- [ ] **Submit.**
- [ ] Save the submission ID.
- [ ] Update HANDOFF.md and VENUE-PLAN.md.
- [ ] Send the pre-submission inquiry to the EiC (Prof. Ling Wang) if not already done in W10.

**Owner:** Harsh.

**Output:** Submitted.

---

## What to do in parallel (before IUI notification)

The following tasks can be started before the IUI notification, in parallel with the IUI submission:

- [ ] **Get ORCID for the corresponding author** (5 min at orcid.org).
- [ ] **Draft the ESWA cover letter** (per the template in `cover-letter.md`).
- [ ] **Draft the highlights** (per `highlights.md`).
- [ ] **Send the pre-submission inquiry to Prof. Ling Wang** (per `pre-submission-inquiry.md`).
- [ ] **Identify 2–4 preferred reviewers** (HCI/recsys/ESWA experts).
- [ ] **Run the RAG baseline** (if time permits; reduces W3 load).

These pre-IUI tasks reduce the W1–W12 timeline by 1–2 weeks.

## Risk register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| IUI notification slips past Nov 23 | Low (IUI on schedule) | High (delays ESWA) | Plan has 2 weeks of buffer; even with 1-week delay, the 12-week plan completes. |
| Parteek cannot review in W8 | Medium | Medium | Identify 1 external reviewer as backup. |
| Larger counterfactual probe (50 pairs) takes longer than 2 days | Medium | Low | 10-pair probe is the minimum; 50-pair is the target. Document both. |
| ORCID for corresponding author not available | Low | Low | ORCID is free; 5 min to create. |
| Editorial Manager institutional email requirement fails | Low | Medium | Explain in cover letter per ESWA rules. |
| LLM-based explainer results are poor | Medium | Medium | Report honestly; the rule-based explainer is the primary method. |
| RAG baseline outperforms our system | Low | High | Re-run with smaller corpus; contextualize. |
| Reviewer rejects on small corpus | High | Medium | Already in limitations; cannot fix without new data. |

## Bottom line

The 12-week plan is realistic, executable in parallel with the IUI notification, and targets a 55–65% acceptance probability. The 8 high-priority fixes in `REVIEWER-SIM.md` are the focus; the remaining tasks are polish and submission logistics.

The pre-IUI work (ORCID, cover letter draft, pre-submission inquiry) reduces the post-IUI workload and is the highest-leverage action to take this week.
