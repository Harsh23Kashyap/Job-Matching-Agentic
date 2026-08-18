# JobMatch — Status & Feedback Request (for Prof. review)

*Prepared 2026-08-18. One honest snapshot of where the work stands and where your feedback would help most before we submit. Governing principle throughout: **maximum scientific credibility, not maximum metric** — where a stronger-looking number and a more defensible one conflicted, we chose the defensible one and report negatives honestly.*

---

## 1. Overview
JobMatch is an **auditable, calibrated, and explainable** job–candidate recommendation system: a six-channel composite score (semantic, skills, title, experience, compensation, remote) that decomposes into a per-decision explanation, with a calibrated confidence display. It is implemented as a small multi-agent system (candidate / employer / matchmaking).

We are preparing **two venue-specific framings of the same underlying science**:
- **ESWA** (Expert Systems with Applications): foregrounds the *auditable / calibrated / explainable methodology*; multi-agent demoted to an implementation detail.
- **JAAMAS** (Autonomous Agents & Multi-Agent Systems): foregrounds the *multi-agent architecture* (the venue's focus).
The numbers and honest findings are identical across both; only the framing differs.

## 2. Headline results (honest)
- **Corpus:** 30 resumes × 15 jobs, **47 human-labeled pairs** (single author-annotator; a second LLM-assisted pass, κ = 0.69, used only as corroboration). Labels are **positive-only** (grades 1–2); 2.97 skills/resume; no preferred-skill field.
- **Ranking:** portal-default composite **nDCG@5 = 0.949**; strongest single configuration 0.924; pure-semantic baseline 0.878; RRF 0.913; BM25 0.902; TF-IDF 0.905; cross-encoder 0.939 (does *not* beat the composite, at ~340× the latency).
- **The key honest finding — ranking PARITY, not superiority:** the composite's gain over semantic is **not statistically significant** (Δ+0.071, two-sided **p = 0.10**, 95% CI crosses zero, and **no method survives Holm correction** at n = 30). A protocol-gated search over 25 configurations finds no better ranker. So we frame the contribution as *methodology* (auditability, calibration, explanation, reproducibility), **not** a ranking-superiority claim.

## 3. New contributions & findings (this cycle)
1. **Relation-aware graded skill matcher** (partial credit for related skills: exact 1.0 / same-taxonomy 0.5 / else 0). We were careful to **isolate** the novelty by decomposing its effect into (a) a coverage-form change and (b) the relation-aware credit:
   - On a high-power **synthetic** corpus (n = 500) the *coverage form* drives the gain (0.917 → 0.949, p < 0.001), while the relation-aware credit does **not** help there — because that generator has no related-skill structure.
   - On the **real human** corpus the reverse holds: the relation-aware credit is the driver (improves **6 of 30 queries, worsens none**, sign-test **p = 0.03**). We report this as a **directional signal only** (one query dominates the mean; effective n ≈ 6), not a broad effect.
   - *Interpretation:* the relation-aware matcher captures partial-credit structure that **human** judgment rewards but a synthetic exact-coverage generator cannot — which is why synthetic can't validate it and we don't claim it does.
2. **Beta calibration resolves a stated limitation.** Platt scaling reaches ECE 0.019 but with near-zero discrimination (and an *adaptive/equal-mass* ECE of 0.084 reveals equal-width bins were hiding miscalibration). **Beta calibration attains ECE 0.009 under both binnings *and* preserves discrimination (Brier skill 0.67, AUC 0.96)** — breaking the calibration-vs-discrimination trade-off. We keep Platt as the deployed default and recommend beta.
3. **Integrity audits (self-imposed).** We showed the synthetic "learned-fusion" gain was largely **by construction** (the derived features correlate 1.00 with the generator's own latent factors) and discounted it; a non-additive-latent control (recovery 0.891) refutes the "recovery is circular" objection.

## 4. Current state per venue
- **ESWA:** essentially submission-ready. PDF compiles clean (0 undefined refs/overfull), all numbers auto-generated from committed artifacts and **verifier-gated**, one-command reproduction runs end-to-end (byte-identical), and an independent hostile-review pass found **no realistically-fixable blocker/serious issue**. Realistic disposition: **Major → Minor Revision** (the honest ceiling is corpus size / novelty, disclosed).
- **JAAMAS:** the original manuscript carried some now-corrected problems (an over-optimistic best-single number and an over-stated significance claim); these are **fixed and reconciled** to the honest parity story, and the graded matcher + beta calibration were added. **Remaining: compile the PDF on Overleaf** (its Springer class needs a toolchain we couldn't run locally).

## 5. What we can share for your review
- Both manuscripts (ESWA: source + fresh PDF; JAAMAS: corrected source, PDF pending Overleaf).
- Cover letters, highlights, a related-work positioning table, and an editorial-risk matrix.
- **Reproducible artifact:** one-command `reproduce_all.sh`, per-experiment JSON results, a verifier that gates every headline number, and 184 unit + 12 scientific-claim + 29 integration + 10 frontend tests (all green).
- **Ready-to-run protocols** for the two additions below (larger benchmark; human study), plus an **annotation toolchain** that already generates a blank grading sheet for the corpus's 403 unjudged pairs.

## 6. Honest limitations (stated, not hidden)
Tiny, single-annotator corpus; **positive-only labels** (no explicit negatives yet); no human explanation/usefulness study; fairness is a proxy-only sensitivity probe; temporal/scale evidence is simulated/synthetic; the relation-aware skill benefit is real-corpus but underpowered (directional).

## 7. Questions where your feedback would most help
1. **Framing call:** is reporting honest ranking **parity** (not superiority) the right scientific choice, or would you push differently given the small corpus?
2. **Novelty for JAAMAS:** is the relation-aware graded skill matcher (+ the multi-agent auditability story) a strong-enough core contribution for JAAMAS, or should we reposition?
3. **Submit now vs strengthen first:** should we run the **larger explicit-negatives benchmark** (and/or a human explanation study) *before* submitting, or submit and add them in revision? This is the single biggest lever on the decision.
4. **Venue fit / order:** ESWA and JAAMAS in parallel, or one first? Any concern about dual submission of differently-framed versions of the same work?
5. **Title:** ESWA is now "An Auditable, Calibrated, and Explainable Multi-Agent System for Job-Candidate Recommendation" (we dropped "Trustworthy"). Comfortable with that, or prefer the original?
6. **Calibration:** adopt **beta** as the headline calibrator (it dominates), or keep Platt as primary and report beta as the recommendation?
7. **Author list & affiliations** for both venues — please confirm.

## 8. Proposed next steps (need your go-ahead / resources)
- **Larger 2-annotator, explicitly-negative-judged benchmark** — the annotation sheet + merge/re-eval tooling is already built and validated; we mainly need annotators. (Highest impact.)
- **Blinded human explanation/usefulness study** — protocol drafted; needs participants/ethics.
- **JAAMAS PDF** build on Overleaf; deposit a citable **DOI** on acceptance.
