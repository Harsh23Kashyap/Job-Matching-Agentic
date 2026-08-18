# IUI 2027 — Review TODO

> Single source of truth for the open issues on the IUI manuscript.
> Items are organized by author pass (D4/D5, D11/D12) and by category (Critical / Important / Optional).
> Each item has an owner, an effort estimate, and a target date.

---

## Critical (must do before Aug 13 abstract deadline)

- [ ] **C1.** Strip all self-identifying citations. Use `\blindcite{key}` for `\cite{...}` of the authors' own prior work. Owner: Harsh. Effort: 30 min. Due: 2026-08-04.
- [ ] **C2.** Replace author/affiliation placeholders with "Anonymous Authors" / "Anonymous Institution". Owner: Harsh. Effort: 10 min. Due: 2026-08-04.
- [ ] **C3.** Move the implementation-detail section from main to supplementary. Owner: Harsh. Effort: 1 hr. Due: 2026-08-05.
- [ ] **C4.** Promote the portal screenshots to lead figure (Fig 1 in the IUI paper). Owner: Harsh. Effort: 1 hr. Due: 2026-08-05.
- [ ] **C5.** Add the GenAI Usage Disclosure paragraph to main.tex. Owner: Harsh. Effort: 10 min. Due: 2026-08-05.
- [ ] **C6.** Build the anonymized artifact at `anonymous.4open.science/r/jobmatch-iui2027`. Owner: Harsh. Effort: 30 min. Due: 2026-08-05.
- [ ] **C7.** Add ACM CCS classification. Owner: Harsh. Effort: 10 min. Due: 2026-08-05.
- [ ] **C8.** Verify the abstract is 200 ± 20 words. Owner: Harsh. Effort: 5 min. Due: 2026-08-04.
- [ ] **C9.** Verify the paper is 8,000 ± 500 words. Owner: Harsh. Effort: 5 min. Due: 2026-08-04.
- [ ] **C10.** Cross-check every number in the paper against the committed benchmark JSONs. Owner: Harsh. Effort: 30 min. Due: 2026-08-05.
- [ ] **C11.** Confirm the title is "Understanding, Controlling, and Trusting Agentic AI: An Interactive, Explainable Job-Matching System" (or a chosen alternate). Owner: Harsh + Parteek. Effort: 10 min. Due: 2026-08-03.
- [ ] **C12.** Confirm with Parteek that the HCI reframe direction is OK before sending to IUI. Owner: Harsh. Effort: 1 email. Due: 2026-08-02.
- [ ] **C13.** ~~CHI 2027 backup~~ — **CANCELLED 2026-07-29 by user instruction.** Sequential submission only; CHI is off the table. See `docs/submission/iui2027/strategy/VENUE-PLAN.md` for the locked IUI → ESWA → KBS → EAAI SI chain.

## Important (do before Aug 20 full-paper deadline)

- [ ] **I1.** Add the calibration reliability diagram (new Fig 8). Owner: Harsh. Effort: 1 hr. Due: 2026-08-08.
- [ ] **I2.** Add the component-level reason crop (new Fig 9). Owner: Harsh. Effort: 30 min. Due: 2026-08-08.
- [ ] **I3.** Compile the supplementary PDF. Owner: Harsh. Effort: 2 hr. Due: 2026-08-10.
- [ ] **I4.** Add a sensitivity table for the soft-embed weight (0.5, 0.6, 0.7, 0.8) to supplementary Table S2. Owner: Harsh. Effort: 30 min. Due: 2026-08-10.
- [ ] **I5.** Add a one-paragraph cross-encoder diagnosis to supplementary §S3. Owner: Harsh. Effort: 20 min. Due: 2026-08-10.
- [ ] **I6.** Soften the "agentic AI" framing in the title and abstract, or add a one-line clarification. Owner: Harsh. Effort: 10 min. Due: 2026-08-06.
- [ ] **I7.** Move the LLM-based explainer results from supplementary to §7.3. Owner: Harsh. Effort: 20 min. Due: 2026-08-09.
- [ ] **I8.** Add a sentence to the abstract acknowledging the absence of a user study and pointing to the planned one. Owner: Harsh. Effort: 5 min. Due: 2026-08-06.
- [ ] **I9.** Run `latex_lint.sh` and `latex_wordcount.sh`; resolve all errors. Owner: Harsh. Effort: 20 min. Due: 2026-08-10.
- [ ] **I10.** Pre-final PDF read-through (page count, line numbers, anonymization). Owner: Harsh. Effort: 1 hr. Due: 2026-08-11.
- [ ] **I11.** Final cover letter and information sheet. Owner: Harsh. Effort: 30 min. Due: 2026-08-12.
- [ ] **I12.** Register abstract in PCS 2.0. Owner: Harsh. Effort: 20 min. Due: 2026-08-11.
- [ ] **I13.** Submit abstract in PCS 2.0. Owner: Harsh. Effort: 30 min. Due: 2026-08-13.
- [ ] **I14.** Final paper pass. Owner: Harsh. Effort: 3 hr. Due: 2026-08-15.
- [ ] **I15.** Author end-to-end read of the PDF. Owner: Harsh. Effort: 1 hr. Due: 2026-08-17.
- [ ] **I16.** Upload supplementary to PCS. Owner: Harsh. Effort: 15 min. Due: 2026-08-18.
- [ ] **I17.** Verify the submission preview in PCS. Owner: Harsh. Effort: 30 min. Due: 2026-08-19.
- [ ] **I18.** **Submit full paper.** Owner: Harsh. Effort: 30 min. Due: 2026-08-20.

## Optional (do if time permits)

- [ ] **O1.** Add a "lessons learned" sub-section to §8 with three concrete design lessons. Effort: 30 min.
- [ ] **O2.** Add a related-work positioning paragraph that names 2–3 closest prior systems explicitly. Effort: 20 min.
- [ ] **O3.** Add a snapshot-evolution figure showing the snapshot history view. Effort: 1 hr.
- [ ] **O4.** Add a "what the prototype is not" callout at the end of §5. (Already drafted; verify it's the right tone.) Effort: 5 min.
- [ ] **O5.** Translate the design principles into a 4-row table at the top of §3. Effort: 10 min.
- [ ] **O6.** Add a "data-availability" footnote pointing to the anonymized artifact. Effort: 5 min.
- [ ] **O7.** Add a "code-availability" footnote pointing to the anonymized artifact. Effort: 5 min.
- [ ] **O8.** Add a "competing-interests" declaration: none. Effort: 5 min.
- [ ] **O9.** Re-check the references for self-citations one more time. Effort: 15 min.
- [ ] **O10.** Add a "future work: longitudinal behavior" concrete study design to §8. Effort: 20 min.

## R1 (HCI reviewer) — known issues to address

- The user study is missing. **I8** is the lowest-cost mitigation (5 min).
- The explanation specificity number (0.627) will draw "is that good enough?" Add a sentence in §7.3 explaining that 0.627 is reported because it is the honest number, not because it is the best number. Effort: 5 min.
- The interface walkthrough in §5 reads more like a tour than an analysis. Add a 1-paragraph framing at the top of §5: "we treat the screenshots as design artifacts, not as product screenshots." (Already drafted; verify the framing is in the section.) Effort: 2 min.

## R2 (AI/recommender reviewer) — known issues to address

- Cross-encoder nDCG drop not interrogated. **I5** addresses this.
- Soft-embed weight of 0.7 reported without sensitivity analysis. **I4** addresses this.
- Learned fusion fit on the same labeled pairs it is judged against. Add a sentence to §6.2 noting the overfitting concern. Effort: 5 min.

## R3 (LLM agent reviewer) — known issues to address

- "Agentic AI" in the title is a perception risk. **I6** addresses this.
- LLM-based explainer results in supplementary. **I7** addresses this.
- LLM is decorative, not central. Add a one-sentence clarification in §4: "the LLM is currently used for parsing and explanation generation; the agentic component separation is the contribution, not the LLM capability." Effort: 5 min.

## Open questions for Parteek (Sir)

1. **Title.** Confirm "Understanding, Controlling, and Trusting Agentic AI" or pick from the 14 alternates.
2. **Agentic framing.** Is the LLM-clarification sentence (R3 mitigation) acceptable, or should we de-emphasize "agentic" further?
3. **CHI 2027 backup.** If IUI gets a soft reject by Aug 22, do we pivot to CHI 2027 (Sept 10 deadline)?
4. **User study statement.** Is the "planned user study" sentence in §8 acceptable, or should we hold the paper until IRB + a pilot is done?
5. **Author order.** Confirm first-author / corresponding-author placement for the unblinded version.

## File map (current)

```
docs/submission/iui2027/
├── manuscript/
│   ├── main.tex                 # preamble + section includes
│   ├── iui-macros.tex           # \JFigure, \JFigPortrait, \JFigPair
│   ├── iui-style.tex            # typography, captions, float placement
│   ├── references.bib           # HCI/XAI/agents bibliography
│   └── sections/
│       ├── abstract.tex         # 200-word IUI abstract
│       ├── section-1-introduction.tex
│       ├── section-2-related-work.tex
│       ├── section-3-design-principles.tex   # NEW for IUI
│       ├── section-4-system-design.tex       # agents as interaction components
│       ├── section-5-interactive-interface.tex  # NEW for IUI
│       ├── section-6-methodology.tex
│       ├── section-7-results.tex
│       ├── section-8-discussion.tex
│       └── section-9-conclusion.tex
├── strategy/
│   ├── TRANSFORMATION-STRATEGY.md
│   ├── SUBMISSION-CHECKLIST.md
│   ├── FIGURE-PLAN.md
│   └── REVIEW-TODO.md           # (this file)
├── supplementary/               # (to be created)
├── anonymized-repo/             # (to be mirrored from /Users/.../anonymized.4open.science)
├── portal/                      # (to be created)
├── cover-letter.md              # (to be created)
└── information-sheet.md         # (to be created)
```

## Git workflow

- Branch: `iui2027-submission` (do not commit to main).
- One commit per Critical item (C1–C18) with a clear message: `iui: <item> — <description>`.
- Squash-merge to main only after the submission is uploaded and the submission ID is recorded.
- Do NOT push the anonymized repo's URL in any commit message; the URL is in the paper only.
