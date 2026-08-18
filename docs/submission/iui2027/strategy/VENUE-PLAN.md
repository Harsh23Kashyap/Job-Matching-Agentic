# Venue Plan — JobMatch (lock rule: one venue at a time)

> **Lock rule (2026-07-29):** The JobMatch manuscript may be under submission at **exactly one venue at a time**. No parallel submission, no parallel hedging, no "shotgun." Sequential fallback only.
> **In-session confirmation:** Harsh confirmed the rule in chat on 2026-07-29 ("We can't submit at multiple places"). This file is the durable record of that decision.

## Submission chain (in order)

| Step | Venue | Type | When | Trigger to move to next step |
|---|---|---|---|---|
| 1 | **IUI 2027** | Conference | Now → 2026-08-20 (paper deadline) | Reject or withdraw |
| 2 | **ESWA** | Journal | After IUI rejection | Reject |
| 3 | **KBS** | Journal | After ESWA rejection | Reject |
| 4 | **EAAI Special Issue: Agentic AI for Intelligent Industrial Systems** | Journal SI | After KBS rejection (or in parallel with KBS if both Elsevier reject; check with editor first) | Reject |

**Why this order:**
- IUI 2027 has the highest acceptance probability for the reframed contribution. Feb 8–11, 2027 conference; notification Nov 23, 2026.
- ESWA is Prof. Kumar's direct suggestion, fastest desk screen in applied AI (5 days), and the cleanest fit for "interactive agentic career recommendation" once the HCI frame is dropped.
- KBS is the knowledge-engineering sibling, easier acceptance bar (~20–25%), 7-day first decision. Needs ORCID for corresponding author.
- EAAI SI is the agentic-AI special issue with Deng (KCL) + Bertino (Purdue) as guest editors; on-theme but the "industrial systems" framing is a stretch for hiring, so it goes last.

## Venues explicitly off the table

- **CHI 2027** — viable technically, but **off by user instruction 2026-07-29**. The IUI submission is the only conference target; CHI is not a parallel backup.
- **AAMAS 2027 main track** — same editor / scope as the prior JAAMAS submission; resubmitting in any form is wasted effort.
- **JAAMAS resubmit** — same editor (Winikoff), same contribution claim, same outcome. Skipped.
- **PRIMA 2026** — 5-day sprint, mid-tier MAS venue, not worth the cost.
- **RecSys 2027** — CFP not out; paper is not recsys-narrow enough.
- **UMUAI** — Q2, IF 3.5; weaker than ESWA and not the right editorial fit.
- **JAAAMAS special issue** — same scope as the rejected main submission.

## Sequential-only rule (rationale)

1. **No double submission.** ACM and Elsevier both explicitly prohibit simultaneous submission of the same manuscript to multiple venues. Violation is a ban-list offense in the worst case and a credibility loss in the typical case.
2. **No silent parallel.** Submitting to a journal while a conference submission is under review is a double submission by any reasonable reading of the rule.
3. **Withdraw on rejection.** When the conference rejects, withdraw the submission formally (some venues require this; PCS does) and then submit to the next venue in the chain.
4. **Withdraw on acceptance.** If the conference accepts (camera-ready stage), the journal chain is dead. The conference paper is the published version.

## What this changes in the workflow

- **No CHI formatting pass.** The IUI LaTeX does not need a CHI alternate.
- **No parallel journal submissions.** ESWA is submitted only after IUI rejects; KBS is submitted only after ESWA rejects; EAAI SI is submitted only after KBS rejects (or, with explicit editor confirmation, in parallel with KBS — both are Elsevier and the editor may want to coordinate).
- **HANDOFF.md update.** The project HANDOFF.md should reference this file under "venue plan" rather than carrying the rule inline.
- **Calendar entries.** Set one submission milestone at a time, not a fan-out of deadlines.

## What this does NOT change

- The IUI 2027 manuscript at `docs/submission/iui2027/` is the only paper in active development.
- The sequential journal fallbacks (ESWA, KBS, EAAI SI) reuse the IUI manuscript body with reformatting and a venue-specific cover letter. No new content is needed until the next venue is triggered.
- The deep-research top-5 venue analysis (2026-07-29) is the source of truth for the chain; this file is the executable version of that analysis under the one-venue-at-a-time rule.

## Open questions to confirm with Prof. Kumar (Sir)

1. Does Sir want to drive the IUI reframing, or leave it to Harsh? (Open since 2026-07-29.)
2. After IUI reject: is ESWA Sir's preferred journal, or should we lead with KBS? (Open since 2026-07-29.)
3. Does WSU have an existing IRB for the small user study that the journal will want? (Open since 2026-07-29.)

## File map

- This file: `docs/submission/iui2027/strategy/VENUE-PLAN.md`
- IUI manuscript: `docs/submission/iui2027/manuscript/`
- Deep-research top 5 venue analysis: chat history 2026-07-29 (not yet on disk; if needed, copy to `docs/submission/iui2027/strategy/VENUE-RESEARCH.md`).
- Project HANDOFF.md: `HANDOFF.md` (referenced from this file; the project-level HANDOFF should cross-reference this rule, not duplicate it).
