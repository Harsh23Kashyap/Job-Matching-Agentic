# FINAL_DOCUMENT_AUDIT (2026-08-18)

Cross-document + hygiene audit of the ESWA submission package.

## Manuscript hygiene — PASS
- No forbidden leftovers in `sections/*.tex` or `tables/*.tex`: grep for TODO/TBD/FIXME/PRE-SUBMISSION/
  placeholder/"to be added"/"reviewer 1|2"/XXX/??? returns **nothing**.
- ORCID: handled via "provided in the Editorial Manager submission system" (no dangling "ORCID: to be added").
- The main manuscript is intentionally ANONYMIZED (`Anonymous Authors`/`Anonymous Institution`, funding
  removed for blind review) with a SEPARATE unblinded `title-page.tex` carrying the real identity — a valid
  ESWA setup. The "pre-submission review" phrases remaining are blind-review acknowledgment placeholders,
  standard for a blinded manuscript.
- AI-use declaration present (Elsevier mandatory). CRediT + competing-interest + funding sections present.

## PII / anonymity — FIXED
- Author absolute home path (`/Users/harshkashyap/.../Job-Matching-Agentic-main/...`) was hardcoded in ~28
  tracked artifact JSONs + docs → **scrubbed to repo-relative** (numbers untouched); no remaining hits in
  source/text (only regenerable `.pyc`/`.sqlite` caches).
- Author's real GitHub/LeetCode handle used as a test fixture in 3 test files → **anonymized to `janedoe`**
  (tests still pass).

## Funding — KEPT per user (RD-008)
- Title page retains: "NVIDIA Academic Grant Program ... 32,000 NVIDIA A100 GPU-hours on the Brev cloud
  platform." Retained verbatim (unblinded doc); removed from the blinded main manuscript (correct).

## Cross-document consistency
- Manuscript ↔ artifacts: all headline numbers match `MANUSCRIPT_NUMBERS.json` (see FINAL_NUMERICAL_AUDIT);
  verifier passes.
- **DOCX sync (fixed):** `cover-letter.docx` and `highlights.docx` were STALE (still carried the phantom
  0.969 / p=0.048 / in-sample 0.032 / dead DOI / "7 of 10" / 0.745) after the `.md` fixes; both were
  **regenerated from the corrected `.md` via pandoc and re-scanned clean** (canonical 0.949/0.924/0.019/
  parity present, zero stale numbers).
- **`manuscript/main.docx` is STALE** (Aug-17 export, predates the numbers-pass + Stage-2 rewrite). It was
  NOT auto-regenerated: a pandoc conversion of the full LaTeX would degrade tables/figures/cross-refs. The
  authoritative manuscript is the current `main.pdf` (39pp, verifier-gated). If a Word manuscript is
  required at submission, the author should regenerate it from their own Word workflow — flagged below.
- **Full-tree phantom-number sweep (fixed):** a sweep of every ESWA text/docx found the disavowed numbers
  (0.969 / p=0.048 / dead DOI / "7 of 10" / 12.3 skills) lingering in several non-manuscript files. Fixed the
  submission/editor-facing ones: `title-page.tex` (dead DOI → "upon acceptance"; PDF regenerated),
  `strategy/pre-submission-inquiry.md` (an EDITOR-facing email that asserted 0.969/p=0.048 → corrected to
  0.924/parity), `SUBMISSION-FORM-GUIDE.md` (DOI → "upon acceptance"). Internal-only planning/QA docs
  (`strategy/POSITIONING.md`, `REVIEWER-SIM.md`, `ESWA-FIT-ASSESSMENT.md`, `highlights-eswa.md`,
  `highlights-check.txt`) were given a STALE banner pointing to the canonical values rather than rewritten.
  Only benign residual references remain: the execution-plan's instruction text ("revisit p=0.048") and the
  known-stale `main.docx`.
- Title kept: "An Explainable and Trustworthy Multi-Agent Architecture ..." (user decision); body softened
  "trustworthy"→"calibrated"; abstract/discussion frame the contribution as calibrated/explainable
  methodology, not superiority — consistent with the evidence.

## Flags for the author (NOT auto-fixed — require author knowledge)
1. **Author list mismatch:** `title-page.tex` names one author (Harsh Kashyap, corresponding) while the
   anonymized `main.tex` CRediT + line "ORCID identifiers for all three authors" imply THREE authors.
   Reconcile the true author list/roles before submission.
2. **Data availability / DOI:** per RD-008, assert "artifact will be deposited upon acceptance" + an
   anonymized artifact link for review; do NOT assert a live DOI (author to confirm the repository).
3. **Institutional emails / ORCID iDs:** provided via Editorial Manager; ensure they are entered there.
4. **README (§37):** DONE — the root `README.md` now has an "ESWA submission — one-command reproduction"
   section; the reproduction path is also in `scripts/reproduce_all.sh` + FINAL_REPRODUCTION.md.
5. **`manuscript/main.docx`:** stale Word export; submit the current `main.pdf` as the authoritative
   manuscript, or regenerate the DOCX from your own Word workflow before submitting a Word version.
   (`cover-letter.docx` and `highlights.docx` have already been regenerated clean.)
