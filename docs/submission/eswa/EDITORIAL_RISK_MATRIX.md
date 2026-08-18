# EDITORIAL RISK MATRIX — JobMatch → ESWA (Stage-3 §28)
> Synthesized 2026-08-18 from three hostile-reviewer lenses (RecSys/ranking · XAI/calibration · applied-ESWA)
> across all review rounds: Iteration-0 9-agent audit, Iteration-5 5-reviewer panel, and the Stage-3 Kiro
> plan panel (gpt-5.6-sol, deepseek-3.2, claude-opus-5, glm-5). Probability = likelihood a reviewer raises it;
> Severity = impact on the decision. Sorted HIGH×HIGH first. "Evidence" = what already answers it; "Fix" = what
> remains. This is the prioritized action list for acceptance.

| # | Criticism | Prob | Sev | Current evidence (what answers it) | Remaining fix | Expected impact |
|---|-----------|------|-----|-----------------------------------|---------------|-----------------|
| 1 | **Novelty is thin** — a weighted 6-channel composite + Platt is not new | HIGH | HIGH | Reframed: contribution = auditable relation-aware skill matching (EXP-034/034b) + calibrated-with-discrimination confidence + factor-grounded explanation + reproducible protocol, as a *combination* | Finish P12 reframe so the ONE substantive method (relation-aware graded skill matching) leads the abstract/intro/title; add a related-work table showing this exact combination is underexplored | Largest single lever; converts "incremental" → "focused methodological contribution" |
| 2 | **Ranking parity, not superiority** (n=30, CIs overlap, fails Holm) | HIGH | HIGH | Disclosed everywhere; reframed as instrument limitation (labels all positive, 15-job pool at @5); synthetic headroom shown honestly (EXP-035/036: base6 nonlinear fusion 0.917→0.947/0.961; the +derived 0.99 jump is disclosed as by-construction, EXP-044) | Keep the honest "no statistically detectable difference" framing; present synthetic headroom as development-only + motivation for a larger benchmark | Neutralizes the biggest attack by owning it; prevents "overclaim" rejection |
| 3 | **Tiny, single-annotator corpus** (30×15/47) | HIGH | HIGH | Disclosed; LLM-assisted 2nd pass κ=0.69 (non-human); synthetic corpus for power | A larger, 2-annotator, explicitly-negative-judged benchmark (author-only; costly). Short of that: state as the headline limitation | Caps ceiling; honesty keeps it in "major revision" not "reject" |
| 4 | **"Untouched test" is indefensible** (corpus informed 33 experiments) | MED | HIGH | FIXED: PROTOCOL.md reframed real corpus as a secondary transfer check; only newly-frozen components get a one-shot prospective check | Ensure manuscript never calls the 47 labels a clean held-out test | Removes a credibility-killer a careful reviewer would catch |
| 5 | **Synthetic recovery is "by construction"** (additive latent mirrors composite) | MED | HIGH | FIXED with evidence: EXP-024b non-additive latent → recovery 0.891 vs additive 0.907 (Δ−0.016); framed as consistency check, not superiority | None (done) | Defuses a one-pass-kill manifest objection |
| 6 | **Calibration low discrimination** (Platt near base-rate) | HIGH | MED | EXP-026: reported ECE + BSS + AUC; isotonic keeps discrimination (BSS 0.64/AUC 0.95); honest trade-off | Optionally lead with isotonic as the probability head + adaptive ECE | Turns a caveat into a nuanced, honest calibration result |
| 7 | **Explanation faithfulness not human-validated** | HIGH | MED | EXP-028 mechanistic ranking-level faithfulness (non-tautological); disclosed no human study | A small blinded human study with recruiters (author-only; strongest remaining empirical add per panel) | Converts XAI contribution from automated → human-validated |
| 8 | **Skill benchmark circularity** (MiniLM labels graded by MiniLM) | MED | MED | FIXED: EXP-034b de-circularized (definitional labels, hard negatives, no MiniLM in exact/negative decisions); embedding tier marked exploratory | None (done) — keep the exploratory label on the SEMANTIC tier | Protects the headline contribution from a methodology attack |
| 9 | **Multi-agent / "trustworthy" overclaim in title** | HIGH | MED | Body demoted multi-agent to implementation; "trustworthy"→"calibrated" in body; EXP-019 shows no perf benefit | DONE (2026-08-18): title changed to *"An Auditable, Calibrated, and Explainable Multi-Agent System for Job-Candidate Recommendation"* — dropped "Trustworthy" (the flagged word), kept honest "Multi-Agent"; propagated to main.tex, title-page.tex, cover-letter.md, SUBMISSION-FORM-GUIDE.md | Reduces framing-mismatch irritation reviewers flagged 3× |
| 10 | **Fairness is proxy-only** | MED | MED | Disclosed as demographic-proxy sensitivity, not an audit; pronoun no-op disclosed | Keep as-is; do not overclaim | Already contained |
| 11 | **Weak/uncompetitive baselines** | MED | MED | BM25/TF-IDF/semantic/multimodal/RRF/LambdaMART/JobBERT all reported, identical protocol | Note CareerBERT unavailable offline (RD-007); optionally add if obtainable | Contained; honest |
| 12 | **Reproducibility** | LOW | HIGH | reproduce_all.sh one-command + verifier gate + pinned deps; validated end-to-end | Real DOI at acceptance (author-only) | Low prob (already strong), high sev if it failed |
| 13 | **Misspelling/formatting non-robustness** | MED | LOW | EXP-029 + EXP-034b report it honestly as a limitation | Optional: a normalization pre-pass | Minor |
| 14 | **Temporal/scalability are simulated/synthetic** | LOW | LOW | Labeled as simulation (EXP-030) / synthetic pool (EXP-031); not overclaimed | None | Contained |

## Priority actions (HIGH×HIGH, in order)
1. **P12 reframe** (#1, #2, #9): narrow the paper around auditable relation-aware skill matching; lead the abstract/intro/title with it; present ranking as honest non-difference + synthetic headroom; finalize the title decision.
2. **Own the corpus limitation** (#3): make small/single-annotator/positive-only the explicit headline caveat + the motivation section for a larger benchmark.
3. **(Author) human explanation study** (#7) and **larger 2-annotator benchmark** (#3) — the two additions that would most move the decision, both requiring resources/ethics.

## Residual honest ceiling
Even with all fixable items closed, the paper is a small-corpus methodological contribution whose real-world
ranking claim is "no detectable difference." The defensible target is **Major→Minor Revision** on the
strength of the auditable skill-matching method + calibration honesty + reproducibility; a clear **Accept**
realistically needs the larger judged benchmark and/or the human explanation study (author-gated).
