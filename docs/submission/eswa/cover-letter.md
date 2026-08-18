# Cover Letter — ESWA Submission (Unblinded)

**To:** Professor Ling Wang, PhD, Editor-in-Chief, *Expert Systems with Applications*
**From:** Harsh Kashyap (corresponding author)
**Co-authors:** Taranumpreet Kaur Wasu, Parteek Kumar
**Re:** Submission of *"An Auditable, Calibrated, and Explainable Multi-Agent System for Job-Candidate Recommendation"* as a Research Article
**Date:** August 17, 2026

---

Dear Professor Wang,

We are pleased to submit our manuscript, **"An Auditable, Calibrated, and Explainable Multi-Agent System for Job-Candidate Recommendation"**, for consideration as a **Research Article** in *Expert Systems with Applications*.

**Authorship.** This work is joint-first-authored by Harsh Kashyap and Taranumpreet Kaur Wasu (Thapar Institute of Engineering and Technology, India), under the supervision of Parteek Kumar (Washington State University, USA). Harsh Kashyap is the corresponding author. All three authors have read and approved the submitted version and agree to its submission to *Expert Systems with Applications*.

**Real-world problem.** Online hiring platforms process millions of resume–job pairs annually, yet the systems that rank them typically return a single opaque score with no breakdown of which resume fields or job requirements drove the ranking. This opacity creates a documented accountability gap in the recruitment domain: recruiters cannot justify shortlist decisions, candidates cannot act on what would change their rank, and neither side can detect when a model's behavior shifts under small input perturbations.

**AI methodology contribution.** Our work presents a multi-agent AI system for the recruitment domain that integrates its methodological contributions into a single, evaluated pipeline:
1. A composite ranking score that decomposes into six explicit channels (semantic similarity, skill overlap, title fit, experience tier, compensation fit, remote policy), each contributing a documented weight, enabling per-decision factor decomposition without post-hoc attribution.
2. A calibrated confidence display that applies Platt scaling to the composite ranking output and reports a confidence value alongside the ranked list, reducing the held-out 5-fold expected calibration error from 0.40 (raw) to 0.019; we also report honestly that this calibrated confidence has limited discrimination (a stated limitation) and compare Platt against isotonic and temperature scaling.
3. A component-level faithfulness evaluation suite that quantifies whether explanation bullets correspond to the channels that produced the score, paired with a counterfactual probe that tests whether single-field edits predicted by the explanation move the rank.
4. A reproducible engineering surface: the prototype, the frozen demo corpus (30 resumes, 15 jobs, 47 labeled pairs), the explanation generator, the calibration layer, and a 341-test regression-gated benchmark are released as an open-source artifact.

**Application consequence.** The practical consequence for the recruitment domain is a transparent, calibrated decision-support tool: a recruiter who reads the per-decision factor decomposition can point to the specific job requirements that moved a candidate into or out of the shortlist, and a candidate who reads the calibrated confidence can act on what would change their rank. The composite reaches nDCG@5 = 0.949 on the portal-default configuration (strongest single configuration 0.924); on this small corpus its improvement over the baselines is positive but *not* statistically significant (two-sided $p = 0.10$, no comparison survives Holm correction), so we report ranking parity and frame the contribution as auditable, calibrated, explainable methodology rather than ranking superiority.

**Why this fits ESWA.** This work fits *Expert Systems with Applications* because it presents an intelligent system validated in a controlled application setting (the recruitment recommendation workflow) with substantive domain consequences (recommendation transparency, explanation faithfulness, and calibrated trust), not only an algorithmic result. The system is reproducible from a clean clone of the released artifact via a one-command script; the artifact will be deposited in a public repository with a citable DOI upon acceptance, and an anonymized copy (author identifiers removed from the code and test fixtures) is available to reviewers during review.

**Funding.** This work was supported by the NVIDIA Academic Grant Program through an unrestricted gift of 32,000 NVIDIA A100 GPU-hours on the Brev cloud platform. Institutional support was provided by Thapar Institute of Engineering and Technology and Washington State University. No external funding was received for the development of the ESWA manuscript.

**Originality and approvals.** We confirm that this manuscript is original, has not been published previously, and is not under consideration for publication elsewhere. All authors have read and approved the submitted version and agree to its submission to *Expert Systems with Applications*. We declare no competing interests.

**Institutional email.** Institutional email addresses for all three contributing authors are provided in the Editorial Manager submission system and the title page.

Thank you for considering our submission. We look forward to your response.

Sincerely,

**Harsh Kashyap** (corresponding author)
on behalf of Taranumpreet Kaur Wasu and Parteek Kumar
Department of Computer Science and Engineering
Thapar Institute of Engineering and Technology, Patiala, Punjab 147004, India
Email: hkashyap\_be19@thapar.edu
