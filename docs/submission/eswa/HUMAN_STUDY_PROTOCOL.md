# Human Explanation Study — Protocol (author-executable)

> Purpose: convert JobMatch's explanation contribution from *automated* faithfulness (EXP-028) to
> *human-validated* usefulness — the single highest-leverage empirical addition for ESWA acceptance
> (EDITORIAL_RISK_MATRIX #7). This document is a ready-to-run protocol: hypotheses are pre-registered,
> materials point at the existing frozen corpus, and the analysis plan is fixed BEFORE data collection.
> Nothing here fabricates data; it specifies how to collect it. Run only after IRB/ethics clearance.

## 1. Research questions and pre-registered hypotheses
- **RQ-H1 (decision quality).** Do factor-grounded explanations improve recruiter shortlisting accuracy
  against the reference labels versus (a) score-only and (b) a generic template explanation?
  - H1: accuracy(factor-grounded) > accuracy(score-only). Directional, one-sided.
- **RQ-H2 (efficiency).** Do explanations reduce time-to-decision without hurting accuracy?
  - H2: time(factor-grounded) < time(score-only); accuracy not lower (non-inferiority margin 0.05).
- **RQ-H3 (appropriate reliance / trust calibration).** Do explanations improve *appropriate* reliance —
  agreeing with the system when it is right and overriding it when it is wrong — rather than blanket trust?
  - H3: the explanation condition shows higher agreement on correct recommendations AND higher override
    on injected-wrong recommendations (a trust-calibration interaction, not a main effect on raw trust).
- **RQ-H4 (perceived faithfulness).** Do recruiters judge the displayed top channel to be the reason the
  candidate ranked where they did, and does perceived faithfulness track the mechanistic faithfulness
  measured in EXP-028?
  - H4: perceived-faithfulness rating for the model-identified top channel > for a random channel.
- **RQ-H5 (usefulness/actionability).** Rated usefulness and, for the candidate view, actionability
  ("I know what would raise my rank") are higher with factor-grounded explanations.

State all five in the pre-registration BEFORE collecting data; report all five regardless of outcome
(including nulls). A null on H1 with a positive H2/H5 is still a publishable, honest result.

## 2. Design
- **Mixed design.** Between-subjects factor = EXPLANATION CONDITION {score-only, generic-template,
  factor-grounded (JobMatch)}; within-subjects factor = ITEM CORRECTNESS {system-correct, system-wrong}
  (see §5 for how "wrong" items are constructed honestly).
- **Task.** For each (job, shortlist-of-5-candidates) screen, the participant decides which candidates to
  advance and rates confidence; a subset asks the faithfulness and usefulness items.
- **Counterbalancing.** Latin-square over item order; each participant sees each job once; conditions are
  assigned at the participant level (between-subjects) to avoid learning transfer across explanation types.

## 3. Participants and power
- **Population.** Practising recruiters / technical hiring managers / HR screeners (>=1 year screening
  experience). Screen out non-recruiters. Target platform: a vetted panel (e.g., Prolific "recruitment"
  audience) or a partner talent-acquisition team.
- **Power analysis (fix before recruiting).** For H1 as a between-subjects comparison of two proportions
  at an expected medium effect (Cohen's h ~ 0.4, alpha 0.05, power 0.80, one-sided) => ~78 participants
  per arm; round to **n = 90 per arm, 270 total** to absorb exclusions (~15%) and support the mixed model.
  If a smaller sample is all that is feasible, PRE-REGISTER the achievable power and report the study as
  a pilot — do not run underpowered and then claim significance.
- **Exclusions (pre-specified).** Failed >1 of 2 attention checks; median item time < 3 s (satisficing);
  incomplete session. Report the exclusion count and re-run the analysis with and without exclusions.

## 4. Materials
- **Corpus.** Use the frozen real corpus (30 resumes x 15 jobs, `data/eval_pairs.json`) — the SAME items
  the paper reports, so the study is grounded in the published system. Select jobs with >=2 graded-positive
  candidates so shortlisting is non-trivial.
- **Three explanation renderings of the SAME ranking** (only the explanation differs; ranking identical):
  1. *Score-only:* the composite score and rank.
  2. *Generic template:* a fixed sentence ("This candidate is a strong overall match for the role.") — the
     control for "any text vs none".
  3. *Factor-grounded (JobMatch):* the six-channel breakdown with per-channel contributions and the
     matched/missing skills list, as produced by `build_composite_components` and the explanation generator.
- **UI.** A minimal web form (reuse the candidate/employer portal explanation component) or a static
  rendering exported per item. Keep visual complexity equal across arms (same layout; only text differs).

## 5. Constructing "system-wrong" items honestly
Trust calibration (H3) needs items where the system is wrong. Do NOT hand-pick or fabricate. Two honest
sources:
- Use the model's actual ranking errors on the frozen corpus: items where the top-ranked candidate is a
  graded-0/1 while a graded-3 sits lower. These are genuine system mistakes, not manufactured ones.
- If too few exist, apply a pre-registered perturbation (swap one required skill) that provably changes the
  ground-truth-optimal choice, and label the item by the reference labels — never by the model's own output.
Report the proportion of system-wrong items and how they were sourced.

## 6. Measures
| Construct | Measure | Type |
|---|---|---|
| Decision accuracy | agreement of advanced set with reference top-k (precision@k vs labels) | primary |
| Efficiency | time-to-decision per screen (ms), logged | primary |
| Appropriate reliance | agree-when-right rate; override-when-wrong rate; reliance interaction | primary |
| Perceived faithfulness | "Which factor most drove this candidate's rank?" match to model top channel + 5-pt agreement | secondary |
| Usefulness | 5-pt Likert (adapted ResQue explanation-usefulness items) | secondary |
| Actionability (candidate view) | 5-pt "I know what to change to rank higher" | secondary |
| Trust | single-item trust + a short trust scale (e.g., Cahour-Forzy 3 items) | secondary |
| Cognitive load | NASA-TLX short form (optional) | exploratory |

## 7. Procedure
1. Consent + demographics + screening (recruiting experience).
2. Instructions + 2 practice items (not analysed).
3. ~15-20 shortlisting screens (mix of system-correct and system-wrong), attention checks embedded.
4. Post-task: usefulness/trust scales, one open-ended "what would you change about the explanation?".
5. Debrief (disclose the system-wrong items were included by design).
Estimated 20-25 min/participant.

## 8. Analysis plan (fixed before data)
- **Primary (H1, H3):** mixed-effects logistic regression — outcome = correct-decision (per screen);
  fixed effects = condition, item-correctness, condition x item-correctness; random intercepts for
  participant and item. Report odds ratios + 95% CI. The H3 test is the condition x item-correctness
  interaction.
- **H2 (time):** linear mixed model on log(time); non-inferiority test on accuracy with margin 0.05.
- **H4 (faithfulness):** McNemar / mixed logistic on perceived-top-channel == model-top-channel vs chance;
  correlate participant-level perceived faithfulness with the item's EXP-028 mechanistic faithfulness.
- **H5 (usefulness/actionability):** ordinal mixed model on Likert responses by condition.
- **Multiplicity:** Holm-Bonferroni across the five pre-registered primary/secondary families.
- **Effect sizes + CIs always reported; nulls reported as nulls.** No optional stopping; fixed n.

## 9. Threats to validity (state in the paper)
- Panel recruiters != the paper's target enterprise recruiters (external validity) — report participant
  characteristics.
- Frozen 30x15 corpus is small and English/tech-skewed — the study inherits that limitation.
- Explanation rendering could confound layout with content — mitigated by equal-layout control (§4).
- Perceived faithfulness is subjective — triangulate with EXP-028 mechanistic faithfulness, do not conflate.

## 10. Deliverables back into the paper
- A new subsection in §5 (Explanation: human validation) + a row in the contributions/claims table moving
  "explanation faithfulness" from LIMITED (automated only) to SUPPORTED (human-validated), IF the data
  support it. If nulls: report honestly and keep the claim at LIMITED — that is still a stronger paper than
  no study.
- Pre-registration link + anonymized data + analysis code deposited with the artifact.

## 11. What the author must provide (cannot be automated here)
- IRB/ethics approval; participant recruitment + compensation; the actual responses.
- Everything else (items, renderings, instruments, analysis code skeleton) can be generated from the frozen
  corpus on request.
