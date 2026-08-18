# ESWA Submission Form — Step-by-Step Guide

**Manuscript:** *An Auditable, Calibrated, and Explainable Multi-Agent System for Job-Candidate Recommendation*
**Submission portal:** Elsevier Editorial Manager (`https://www.editorialmanager.com/eswa/`)
**Login:** Harsh Kashyap (`hkashyap_be19@thapar.edu`)
**Submission date:** August 17, 2026 (Monday)
**Expected handling editor assignment:** 1-3 business days from submission
**Expected first decision:** ~August 22, 2026 (5-day median)
**Expected reviewer decision (if sent out):** ~mid-October 2026 (62-day post-review median)

---

## Files to prepare (5 total)

| # | File | Where it is | Size |
|---|---|---|---|
| 1 | `main.pdf` (anonymized) | `~/Desktop/jobmatch-eswa-main.pdf` | 3.28 MB, 36 pp |
| 2 | `main.docx` (anonymized) | `~/Desktop/jobmatch-eswa-main.docx` | 3.34 MB |
| 3 | `title-page.pdf` (unblinded) | `~/Desktop/jobmatch-eswa-titlepage.pdf` | 100 KB, 2 pp |
| 4 | `highlights.docx` | `~/Desktop/jobmatch-eswa-highlights.docx` | 11 KB |
| 5 | `cover-letter.docx` (or PDF) | Convert `cover-letter.md` to docx | ~10 KB |

> **Step 0 — Replace placeholders first.** Before uploading, edit three files and replace the `[brackets]` placeholders with real values:
> - `title-page.tex`: `hkashyap\_be19@thapar.edu`, `twasu\_be20@thapar.edu`, `to be added (Harsh ORCID)`, `to be added (Taranum ORCID)`, `to be added (Parteek ORCID)`, `to be added (Harsh phone)`
> - `cover-letter.md`: `hkashyap\_be19@thapar.edu`
> - `SUBMISSION-FORM-GUIDE.md` (this file): all `[REPLACE]` markers below
>
> Then recompile `title-page.pdf` and re-convert `cover-letter.docx`.

---

## Step 1 — Article Type

| Field | Value |
|---|---|
| Article Type | **Research Article** (NOT Review Article) |
| Section/Category | Applications |
| Submission type | New submission |

---

## Step 2 — Title & Abstract

| Field | Value |
|---|---|
| Title | An Auditable, Calibrated, and Explainable Multi-Agent System for Job-Candidate Recommendation |
| Abstract | (paste from `sections/abstract.tex` — 184 body words) |
| Keywords | recommender systems; explainable AI; confidence calibration; skill matching; job-candidate matching; auditable ranking; recruitment |

---

## Step 3 — Author Information

Enter authors **in submission order** (matches title page):

### Author 1 (Corresponding)
| Field | Value |
|---|---|
| First name | Harsh |
| Last name | Kashyap |
| E-mail | hkashyap\_be19@thapar.edu |
| ORCID | Harsh to register at orcid.org/0000-0000-0000-0000 (5 min, free) before completing this field |
| Affiliation | Thapar Institute of Engineering and Technology, Department of Computer Science and Engineering, Patiala, Punjab 147004, India |
| Country | India |
| Is corresponding? | **Yes** |

### Author 2
| Field | Value |
|---|---|
| First name | Taranumpreet |
| Last name | Kaur Wasu |
| E-mail | twasu\_be20@thapar.edu |
| ORCID | Optional; if not registered, leave blank |
| Affiliation | Thapar Institute of Engineering and Technology, Department of Computer Science and Engineering, Patiala, Punjab 147004, India |
| Country | India |
| Is corresponding? | No |

### Author 3
| Field | Value |
|---|---|
| First name | Parteek |
| Last name | Kumar |
| E-mail | parteek.kumar@wsu.edu |
| ORCID | Optional; if not registered, leave blank |
| Affiliation | Washington State University, School of Electrical Engineering and Computer Science, Pullman, WA 99164, USA |
| Country | United States |
| Is corresponding? | No |

> **Note:** If Harsh has a current WSU or Apple email that he prefers for the corresponding-author field, use that. The DOI form only requires that an institutional email be on file.

---

## Step 4 — Files Upload (in this exact order)

| Order | File type | File |
|---|---|---|
| 1 | Manuscript | `jobmatch-eswa-main.pdf` (anonymized, double-blind) |
| 2 | Manuscript source (optional but recommended) | `jobmatch-eswa-main.docx` |
| 3 | Title page (separate, unblinded) | `jobmatch-eswa-titlepage.pdf` |
| 4 | Highlights | `jobmatch-eswa-highlights.docx` |
| 5 | Cover letter | `jobmatch-eswa-coverletter.docx` (or PDF) |
| 6 | Supplementary (optional) | `paper_progression_summary.json`, `calibration_summary.json`, `explainability_report.json`, `fairness_eval.json` (in a ZIP) |

**Item type order in Editorial Manager** (per Elsevier convention):
1. Manuscript (anonymized)
2. Title page (unblinded, separate file — Editorial Manager will keep this from the reviewers)
3. Highlights
4. Cover letter

---

## Step 5 — Declarations (per-author)

### Declaration of Interests (DOI)
Each of the 3 authors completes separately. All select:

- Research Support for This Reported Work: **YES** — disclose:
  - Organization: NVIDIA Academic Grant Program
  - Support type: Non-financial (32,000 A100 GPU-hours on Brev cloud)
  - Who received: Harsh Kashyap (and the project as a whole)
- Other Support: **None**
- Intellectual Property: **None**
- Other Activities: **None**

After all 3 complete, the merged statement (uploaded by the system) should read:
> "This work was supported by the NVIDIA Academic Grant Program through an unrestricted gift of 32,000 NVIDIA A100 GPU-hours on the Brev cloud platform. The authors declare no other competing financial interests or personal relationships."

### Authorship Confirmation
- All 3 authors will receive a confirmation link by email from ESWA's Editorial Manager
- Harsh needs to forward each author's link to them
- Each author clicks the link, reviews the PDF, and approves

### Ethics Statement
- Not applicable — the system uses synthetic and manually-curated demo profiles, no human subjects recruitment data were collected
- If asked: "Not applicable. Evaluation uses synthetic and manually curated demo profiles; no human subjects recruitment data were collected for this study."

---

## Step 6 — Suggested Reviewers

(Optional but recommended — 3-5 names, alphabetical)

Each requires: full name, affiliation, email. Examples (replace with real contacts):

1. **Dr. [Reviewer Name 1]** — [Affiliation], [email]
2. **Dr. [Reviewer Name 2]** — [Affiliation], [email]
3. **Dr. [Reviewer Name 3]** — [Affiliation], [email]

**Opposed reviewers:** (Optional) — anyone with a conflict of interest. For this paper, none required.

---

## Step 7 — Final Check Before "Approve Submission"

Run through this list:

- [ ] Article type = Research Article ✓
- [ ] Title (no abbreviations) ✓
- [ ] Abstract ≤250 words (currently 184) ✓
- [ ] Keywords = 7 ✓
- [ ] Authors in order: Harsh, Taranum, Parteek ✓
- [ ] Corresponding author = Harsh ✓
- [ ] Institutional email for every author ✓
- [ ] All 5 files uploaded in correct order ✓
- [ ] Main manuscript is anonymized (no author names anywhere) ✓
- [ ] Title page is unblinded (real names, NVIDIA funding) ✓
- [ ] Highlights ≤85 chars each, 5 bullets ✓
- [ ] Cover letter names real authors ✓
- [ ] Data availability: artifact deposited with a citable DOI UPON ACCEPTANCE; anonymized copy for reviewers (do NOT assert a live DOI before it resolves)
- [ ] Competing interest declared (NVIDIA funding + no other) ✓
- [ ] AI declaration (OpenAI ChatGPT GPT-4) ✓
- [ ] ORCID for corresponding author (Harsh) ✓
- [ ] NVIDIA funding disclosed in DOI form (not "no additional support") ✓
- [ ] All 3 authors will receive approval emails — forward them
- [ ] Conflicts of interest = none for editorial board

---

## Step 8 — Submit

1. Click **Build PDF for Approval** (Editorial Manager compiles everything)
2. **View Submission** to verify the merged PDF
3. **Approve Submission** to finalize

**Post-submission:**
- All 3 authors receive approval emails with links
- Each clicks link within 14 days to approve
- ESWA's handling editor is assigned within 1-3 business days
- 5-day first decision median
- If sent to reviewers: 62-day post-review, 147-day total median

---

## Quick Reference — All Exact Values to Copy

| Field | Exact value |
|---|---|
| Article Type | Research Article |
| Title | An Auditable, Calibrated, and Explainable Multi-Agent System for Job-Candidate Recommendation |
| # keywords | 7 |
| Keyword 1 | recommender systems |
| Keyword 2 | explainable AI |
| Keyword 3 | confidence calibration |
| Keyword 4 | skill matching |
| Keyword 5 | job-candidate matching |
| Keyword 6 | auditable ranking |
| Keyword 7 | recruitment |
| # pages | 36 |
| # figures | 13 |
| # tables | 6 |
| # words (body) | ~9,643 |
| # references | 41 |
| Corresponding author | Harsh Kashyap |
| Author 2 | Taranumpreet Kaur Wasu |
| Author 3 (supervisor) | Parteek Kumar |
| Affiliation 1 | Thapar Institute of Engineering and Technology, India |
| Affiliation 2 | Washington State University, USA |
| Data DOI | to be minted upon acceptance (anonymized artifact link for review) |
| Code commit | 02a700e |
| Funded by | NVIDIA Academic Grant Program (32,000 A100 GPU-hours, Brev) |
| AI tool used | OpenAI ChatGPT (GPT-4 model) |
| Editor | Ling Wang, PhD (EiC) |
| Submission portal | editorialmanager.com/eswa/ |
| Median first decision | 5 days |
| Acceptance rate | 12-15% |
| APC | $0 (subscription), $3,490 (gold OA), $698 (India GPOA) |
