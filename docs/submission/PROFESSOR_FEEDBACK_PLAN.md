# JobMatch — Next-Phase Plan (governing, per supervisor feedback 2026-08-18)

The supervisor reviewed `PROFESSOR_STATUS.md` and gave decisions + an 8-goal program. This doc is now the
governing plan; it SUPERSEDES the prior "submit both venues in parallel" approach.

## Supervisor's decisions (on the 7 questions)
1. **Keep honest ranking PARITY** — do NOT hunt for p<0.05. The contribution is auditable/calibrated/
   decomposable methodology, not a proven ranking win. (Confirmed our stance.)
2. **Relation-aware matcher ≠ sole novelty** — frame it as part of the COMBINATION (multi-agent +
   auditable decomposition + relation-aware matching + calibration + explainability). Do not market the
   relation-aware benefit as broadly validated (it is directional/underpowered: 6/30, p=0.03, one query
   dominant, effective n≈6).
3. **Strengthen BEFORE submitting.** Priority: (1) larger explicit-negative, ≥2-annotator benchmark →
   (2) re-run ranking/ablation/calibration through the verifier-gated pipeline → (3) human explanation
   study if feasible → (4) submit. Ground truth is the foundational weakness.
4. **NO PARALLEL SUBMISSION.** Same dataset/experiments/results/figures/methodology = substantially
   overlapping even with different framing. Pick ONE primary venue → submit → await disposition → then
   decide the second on what remains genuinely non-overlapping. Do a line-by-line overlap comparison first.
5. **ESWA title:** keep "An Auditable, Calibrated, and Explainable Multi-Agent System for Job-Candidate
   Recommendation" (dropping "Trustworthy" was right). Consider whether "Multi-Agent System" should lead,
   given methodology/auditability is ESWA's strongest story (decide against the actual abstract).
6. **Beta vs Platt:** do NOT hide beta. Frame Platt = deployed baseline, beta = stronger post-hoc result +
   recommended upgrade. MUST give a concrete reason why Platt stays deployed if beta is better (reviewers
   will ask).
7. **Author list/affiliations:** resolve separately from contribution history (author-only).

**Primary venue (supervisor's instinct + ours): ESWA first** (broad applied-intelligent-systems scope).
JAAMAS is held pending (a) ESWA disposition and (b) a demonstrated, genuinely-distinct multi-agent
contribution (Goal 6). No parallel submission.

### OVERLAP VERDICT (line-by-line analysis, 2026-08-18) — DECISIVE
ESWA and JAAMAS are **two framings of ONE contribution, NOT two distinct contributions.** The empirical
core is byte-identical: same corpus (30×15/47), same method (six-channel composite + graded matcher +
Platt/beta), **every headline number matches**, same committed artifacts, same figures (redrawn), and the
entire empirical spine (§5 results, calibration trade-off, graded-matcher decomposition, significance,
limitations) is near-verbatim shared. Only intros/related-work/architecture prose diverge. JAAMAS's claimed
"three-agent architecture" novelty is **unmeasured** (it provides no experiment validating the agent
design; ESWA itself calls the multi-agent split "an engineering choice, not the scientific contribution").
=> Parallel/simultaneous submission would be redundant publication / self-plagiarism — NOT defensible.
**Action: submit ESWA ONLY. Hold JAAMAS.**

### What JAAMAS needs to become a genuinely separate paper
(a) A NEW empirical core that tests the agent claim — the Goal-6 **monolith-vs-multi-agent ablation** as its
    headline results section: staleness/invalidation correctness on profile edits, failure-isolation under
    injected parser/LLM/embedding faults, latency/consistency of event-driven refresh vs a monolith,
    cross-agent privacy-boundary enforcement. (Some raw material exists in EXP-019/EXP-033 but must be
    elevated to a headline architecture-specific results section, not inherited from ESWA's ranking bench.)
(b) An architecture-specific contribution ESWA does NOT measure.
(c) Explicit cross-citation of the ESWA paper.
Until (a)-(c) exist, JAAMAS is "the same paper in a different jacket" and must not be submitted.

## 8-goal next-phase research program (supervisor)
G1 Ranking improvement — learned/constrained weighting, nonlinear channel interactions, learning-to-rank,
   query-adaptive (job-family-specific) weighting. Success = ΔnDCG@5 ≥ 0.03–0.05 over the strongest
   baseline AND significant AND survives correction — on a POWERED dataset (not 47 labels).
G2 Ground truth (FOUNDATIONAL) — 50–100 resumes × 25–50 jobs, explicit human-judged negatives, ≥2
   annotators (3 on a subset), graded scale 0–4, report κ / α / agreement / adjudication.
G3 Relation-aware matching — multiple relation strengths (1.0/0.75/0.5/0.25/0), learned skill relatedness
   (embedding/ontology/co-occurrence/LLM-derived), optimize partial credit; test human-aligned gain.
G4 Calibration — Platt/beta/isotonic/temperature (+Dirichlet if applicable); SUBGROUP calibration
   (high/low confidence, sparse resumes/jobs, industries, experience levels).
G5 Explanation — blinded human study: usefulness, correctness, trust, decision time, error detection.
G6 Multi-agent contribution — monolithic vs multi-agent vs multi-agent+verification ablation (the JAAMAS
   empirical hook).
G7 Robustness — missing-data / synonym / title-paraphrase / noise perturbations; which components are
   brittle.
G8 Fairness — paired counterfactual resumes (one attribute changed), score/rank/top-k/explanation deltas.

## Autonomous vs author-gated split (what I can do without new data/people)
- **Autonomous NOW (high-power synthetic 500×75 + existing corpus):** G1 (nonlinear interactions,
  query-adaptive/family weighting, learning-to-rank) developed + validated under nested CV on synthetic;
  G3 (relation-strength tiers + learned-relatedness variants) on synthetic + the de-circularized benchmark;
  G4 subgroup calibration on the existing held-out data; G7 robustness (extend EXP-029); G8 counterfactuals
  (extend EXP-005). All reported as DEVELOPMENT evidence; real-corpus confirmation deferred to G2.
- **Autonomous ENABLEMENT for author-gated goals:** G2 — the explicit-negatives sheet for the 403
  unjudged existing pairs is built (upgrade to the 0–4 scale); G5 — build study renderings/instrument/
  analysis skeleton; G6 — build the monolithic-vs-agent harness.
- **Author-gated (need resources):** G2 new resumes/jobs + human annotators; G5 participants/ethics;
  author list; DOI; final venue submission.

## Guardrails (unchanged)
Maximum scientific credibility, not maximum metric. Do NOT over-optimize a ranker on 47 positive labels
(supervisor's explicit warning) — develop on synthetic power, validate on the powered benchmark once built.
If, after the larger benchmark, the composite still doesn't beat semantic, REPORT PARITY. Everything
verifier-gated; no fabrication; no parallel submission.

## Execution order (this cycle)
A. Framing fixes now (autonomous): relation-aware-as-combination; beta/Platt deployment rationale;
   ESWA/JAAMAS line-by-line overlap analysis; upgrade annotation scale to 0–4.
B. Autonomous experimental program on synthetic: G1 (nonlinear + query-adaptive + LTR) and G3
   (relation-strength tiers + learned relatedness), nested-CV, verifier-gated, negatives reported.
C. Author-gated enablement: G5 study materials, G6 monolith-vs-agent harness (build, don't run humans).
D. Hold submission until G2 (larger benchmark) is annotated and analyses re-run.
