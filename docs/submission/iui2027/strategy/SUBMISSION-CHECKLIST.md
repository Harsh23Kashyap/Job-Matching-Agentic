# IUI 2027 Submission Checklist

> **Target:** 32nd ACM Conference on Intelligent User Interfaces (IUI 2027)
> **Venue:** Helsinki, Finland · Feb 8–11, 2027
> **Abstract deadline:** 2026-08-13 (AoE)
> **Full paper deadline:** 2026-08-20 (AoE)
> **Submission system:** PCS 2.0 → Society: SIGCHI · Conference: IUI 2027 · Track: IUI 2027 Papers

---

## A. Manuscript deliverables

- [ ] **main.tex** compiles cleanly with `pdflatex + bibtex` (or `latexmk -pdf`).
- [ ] **iui-macros.tex** and **iui-style.tex** load without errors.
- [ ] **references.bib** resolves all `\cite{...}` keys (no `?` in the PDF).
- [ ] All 9 sections + abstract committed under `manuscript/sections/`.
- [ ] Word count: **8,000 ± 500 words** for the main paper body (excluding references).
- [ ] Page count target: **8–10 pages** in the ACM TAPS single-column layout.
- [ ] All figures render in the PDF; figure captions self-contained.
- [ ] All tables render; booktabs style; no vertical rules.
- [ ] All 8 portal screenshots in `figures/Fig10.png` (or split into Fig3(a)–(h) for clarity).
- [ ] Captions in the camera-ready tone (no "TODO", no "DRAFT" markers).

## B. Anonymization (double-blind)

- [ ] `documentclass` includes `[review, anonymous]` options.
- [ ] No author names, affiliations, or emails visible in the PDF.
- [ ] No acknowledgment of funding, NVIDIA grant, or institutional support.
- [ ] No self-citations that identify the authors. Use `\blindcite{key}` for any prior work by the same authors.
- [ ] All figures stripped of names, logos, or institution-specific UI.
- [ ] GitHub repository is the **anonymized fork** at `anonymous.4open.science/r/jobmatch-iui2027` (DO NOT link to the public repo with author names).
- [ ] Any reference to "NVIDIA A100 GPU-hours" or "Brev" removed from main paper.
- [ ] Reference list checked for self-citations; all converted to `[Anonymous, year]` form.

## C. Required ACM fields in main.tex

- [ ] `\title{...}` set to the selected title.
- [ ] `\author{Anonymous Authors}` (single placeholder for double-blind).
- [ ] `\affiliation{...}` uses `Anonymous Institution`, `Anytown`, `AnyState`, `AnyCountry`.
- [ ] `\email{anonymous@example.com}` (placeholder).
- [ ] **Abstract** present, 150–250 words, follows the IUI 6-part structure.
- [ ] **CCSXML** block with at least 3 concepts (HCI primary, UI design, Recommender systems).
- [ ] `\ccsdesc[500]{...}` for the primary concept.
- [ ] **Keywords** list with 5–9 terms.
- [ ] **GenAI Usage Disclosure** in the acknowledgments or in a footnote (required by IUI 2027).
- [ ] **Copyright line** stripped for the review version (added in the camera-ready).

## D. Supplementary material

- [ ] **supplementary.pdf** compiled separately, ≤ 10 pages.
- [ ] Contains: full method-comparison table, calibration curves, hard-negatives table, full explainability table, full fairness table, full latency table, implementation detail, screenshot index.
- [ ] No duplicate content with main paper; supplementary is reference, not extension.
- [ ] Anonymized; same author/affiliation policy as main.
- [ ] Uploaded to PCS as a separate file, not merged with the main paper.

## E. Anonymized artifact

- [ ] Repository at `https://anonymous.4open.science/r/jobmatch-iui2027` resolves.
- [ ] README is anonymized (no author names; use "the authors" or "this submission").
- [ ] `requirements.txt`, `package.json`, and any other dependency files committed.
- [ ] The frozen demo corpus (30 resumes, 15 jobs, 47 labels) committed and documented.
- [ ] The benchmark JSONs (`paper_progression_summary.json`, `fusion_eval.json`, etc.) committed.
- [ ] The test suite (302 Python + 39 Node = 341 tests) runs from a clean clone.
- [ ] No `git log` reveals author identities (consider `git filter-branch` or fresh repo if needed).
- [ ] The URL is added to the main paper's introduction (after acceptance, convert to a public URL).

## F. Cover letter and information sheet

- [ ] **cover-letter.md** present at `docs/submission/iui2027/cover-letter.md`.
- [ ] Identifies the contribution, the design principles, and the user-facing evaluation.
- [ ] Identifies the conflict-of-interest statement (none).
- [ ] Identifies any preferred reviewer suggestions (optional, but recommended for HCI-area reviewers).
- [ ] **information-sheet.md** present with the authors' anonymized contact, the artifact URL, and the supplementary file reference.

## G. Pre-submission verification

- [ ] `latex_lint.sh main.tex` passes with no errors (warnings OK).
- [ ] `latex_wordcount.sh main.tex` returns 8000 ± 500 words.
- [ ] `pdfinfo main.pdf` reports `Pages: 8-10`.
- [ ] `rg '\\todo' main.tex sections/` returns no matches.
- [ ] `rg 'TODO|XXX|FIXME' main.tex sections/` returns no matches.
- [ ] PDF read end-to-end; check for broken sentences, missing figures, dangling references.
- [ ] All `\ref{...}` resolve (no `??` in the PDF).
- [ ] `latex_citation_extract.sh main.tex --check` passes.

## H. Day-of-submission

- [ ] Log into PCS 2.0.
- [ ] Click "Submissions" → Society: SIGCHI → Conference: IUI 2027 → Track: IUI 2027 Papers.
- [ ] Enter title (matches `\title{...}` exactly).
- [ ] Enter author list (anonymized; replace with real authors at unblind time).
- [ ] Enter abstract (matches the abstract in the PDF exactly).
- [ ] Enter keywords.
- [ ] Upload main PDF.
- [ ] Upload supplementary PDF.
- [ ] Enter the anonymized artifact URL in the "supplementary material URL" field if PCS has one.
- [ ] Add GenAI Usage Disclosure to the "Acknowledgments" field.
- [ ] Add the conflict-of-interest statement.
- [ ] **Submit by 2026-08-20 AoE.** (Reserve the last 60 minutes for PCS upload surprises.)

## I. After submission

- [ ] Save the submission confirmation email and the submission ID.
- [ ] Add the submission ID to `HANDOFF.md`.
- [ ] Update the project's `STATUS.md` to mark IUI as "submitted, awaiting notification."
- [ ] Set a calendar reminder for 2026-10-29 (initial IUI notification).
- [ ] Set a calendar reminder for 2026-11-23 (final IUI decision).
- [ ] Begin planning for the rebuttal window (Nov 5, 2026) — the user study plan from §8 is the most likely rebuttal content.
