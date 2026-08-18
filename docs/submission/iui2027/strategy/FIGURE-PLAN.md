# IUI 2027 Figure Plan

> Goal: every figure answers a reviewer question, and the lead figure is a user-facing interaction surface, not an architecture diagram.

The IUI submission has 9 figures. The figure order and selection change meaningfully from the JAAMAS submission.

---

## Lead figure (Figure 1 in the IUI paper)

> **TODO: New figure to create** — *Concept sketch* of the user-facing design.
>
> Layout (4 panels):
> 1. Candidate on the parsed-fields review form (showing G1).
> 2. Candidate on the match list with explanation drawer open (showing G2 + G4).
> 3. Candidate on the counterfactual view (showing G3).
> 4. Recruiter on the shortlist panel (showing G3 + G4).
>
> Reviewer takeaway in 5 seconds: "this is a user-facing system, not an engineering artifact."

If a new concept sketch is not feasible in time, **fall back to the existing Fig 10 montage** (the 8 portal screenshots) and lead the paper with that.

## Figure-by-figure plan

| Fig # | Source (JAAMAS) | New role (IUI) | What the reviewer should understand in 5 sec | Caption focus |
|---|---|---|---|---|
| 1 | (new) **or** Fig 10 | Lead figure: user-facing design | The system is a working interface, not a paper architecture | "Interactive, explainable, agentic: the four interaction states a user encounters" |
| 2 | Fig 1 | Architecture overview | The role-separated layout: two owning components, one read-only broker | "Three cooperating interaction components; ownership boundaries match privacy boundaries" |
| 3 | Fig 7 | Architecture detail | The same layout expanded with portals; admin/eval sits below | "The role-separated architecture with portals and admin/evaluation console" |
| 4 | Fig 10 | Portal screenshots (8 states) | The user-facing surface is concrete, not aspirational | "Eight primary interaction states of the prototype, ordered as a user encounters them" |
| 5 | Fig 5 | Matchmaking internals (moved to supplementary) | The scoring internals are documented but not central | (supplementary) "Matchmaking component: composite scoring with six channels and component-level reasons" |
| 6 | Fig 6 | Candidate workflow (moved to supplementary) | The candidate lifecycle is documented but not central | (supplementary) "Candidate lifecycle: ingestion, snapshot, ranking, feedback" |
| 7 | Fig 4 | Employer workflow (moved to supplementary) | The employer lifecycle is documented but not central | (supplementary) "Employer workflow: JD ingestion, posting, reverse matching" |
| 8 | (new) | **Calibration plot** | The calibration is real and visualizable | (results) "Reliability diagram: uncalibrated ECE = 0.40, calibrated ECE = 0.032" |
| 9 | (new) | **Component-level reason screenshot** | A user reading the explanation panel sees the six channels | (results) "The component-level reason in the match list, with the six channels" |

## Figure 1 (new lead) — sketch details

Four panels, each a cropped screenshot with a short caption:

**Panel A — Parsed-fields review (G1)**
- Crop the candidate's parsed-fields review form (current Fig 10 panel a–b).
- Annotate: "1. The user sees what the system has parsed. 2. The user edits before confirming. 3. No ranking until confirmation."

**Panel B — Match list with explanation (G2 + G4)**
- Crop the candidate's match list with the explanation drawer open (current Fig 10 panel c).
- Annotate: "1. The list shows a ranked item. 2. The drawer names the components of the score. 3. The user can save, dismiss, or open the counterfactual view."

**Panel C — Counterfactual view (G3)**
- Crop the counterfactual view (current Fig 10 panel d).
- Annotate: "1. The user sees the predicted effect of a small edit. 2. The user can apply the edit (routes back to confirmation), copy as a note, or close."

**Panel D — Shortlist panel (G3 + G4)**
- Crop the recruiter's shortlist panel (current Fig 10 panel h).
- Annotate: "1. The recruiter sees the rationale that produced each shortlist. 2. The recruiter can remove an item, contact a candidate, or revisit the explanation."

## Figure 8 (calibration plot) — sketch details

A reliability diagram with two series:
- **Uncalibrated:** expected calibration error = 0.40. Ten bins, equal-width, plotted as confidence vs accuracy.
- **Calibrated:** expected calibration error = 0.032 after Platt scaling. Same bins, accuracy now tracks confidence.

Plotted on a 0–1 square, with the diagonal "perfect calibration" reference. Mark each bin with its sample count. The plot is the visual companion to §6.4 and §7.4.

The data is the calibration set: 21 strong + 26 partial labels, 10 equal-width confidence bins.

## Figure 9 (component-level reason) — sketch details

A clean crop of the explanation drawer showing:
- The rank position (e.g., "Rank 1 of 12").
- The composite score.
- Six component bars (semantic, skill, title, experience, compensation, remote).
- A short text rationale.
- The action menu (save, dismiss, counterfactual).

Annotated to point at: (i) the six channels, (ii) the calibrated confidence, (iii) the action menu. Caption emphasizes that the components are the same components the system uses to compute the score.

## Figures to demote to supplementary

- Fig 5 (Matchmaking internals) — supplementary §S2.
- Fig 6 (Candidate workflow) — supplementary §S3.
- Fig 4 (Employer workflow) — supplementary §S4.
- All algorithm pseudocode — supplementary §S5.
- All architecture-flow diagrams that overlap with Fig 2/3 — supplementary §S1.

## Figure 1 vs Fig 4 ordering

The IUI submission leads with **Figure 1 = the user-facing surface** (the new concept sketch OR the Fig 10 montage). The architecture diagram (former Fig 1 in JAAMAS) moves to **Figure 2** in IUI.

This ordering change is the single most important visual change in the submission; it signals "this is an HCI paper" before the reviewer reads a word.

## Figure file hygiene

- All figures in `figures/` directory, in PNG or PDF.
- All figures anonymized (no author names, no institution logos, no real user data).
- All captions self-contained (the figure + its caption is understandable without the body).
- All figures referenced in the body before they appear in the source order (LaTeX will auto-place them; this rule prevents "Figure X appears on page Y" from breaking).
- All figure-source files (e.g., .drawio, .svg) committed in `figures/source/` for reproducibility.
