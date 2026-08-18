# Pre-Submission Inquiry — ESWA

> **Purpose:** Warm the journal before formal submission, confirm scope fit, and create a soft queue position.
> **Recipient:** Prof. Ling Wang, Editor-in-Chief, *Expert Systems with Applications* (Tsinghua University, Department of Automation, Beijing, China).
> **Channel:** Editorial Manager pre-submission inquiry form (preferred) OR email to the editorial office (eswa@elsevier.com).
> **When to send:** 2 weeks before formal submission (per `SUBMISSION-PLAN.md` Week 10).
> **Effort:** 2 minutes to send; expected response time 3–7 days.

---

## Email template (pre-submission inquiry)

**To:** eswa@elsevier.com (or Editorial Manager inquiry form)
**Cc:** (any senior editors listed on the ScienceDirect editorial board, optional)
**Subject:** Pre-submission inquiry — multi-agent architecture for explainable job-candidate recommendation

```
Dear Professor Wang,

We are preparing a manuscript for Expert Systems with Applications
on an auditable, calibrated, and explainable job-candidate recommendation
methodology (implemented as a multi-agent system), with a controlled
evaluation on a 30-resume, 15-job demo corpus (nDCG@5 = 0.949 for the
portal-default composite, strongest single configuration 0.924; on this
small corpus the differences are not statistically significant after
correction, so we frame the contribution as methodology, not ranking
superiority).

The contribution is fourfold: (i) a composite ranking with six
explicit channels and per-decision factor decomposition, (ii) a
Platt-scaled confidence display that reduces the expected
calibration error from 0.40 to 0.032, (iii) a component-level
faithfulness evaluation suite, and (iv) a reproducible engineering
surface (prototype + frozen demo corpus + 341-test regression-gated
benchmark) released as an open-source artifact.

Before formal submission, we would like to confirm scope fit. The
contribution is an applied AI system for the recruitment domain
(human resources management, which is in the journal's stated
scope) that integrates hybrid retrieval, component-level
explanations, and calibrated confidence. The system is
reproducible from a clean clone of the released artifact.

Would this work fit ESWA's applied-AI scope, or would a different
venue in the Elsevier portfolio (e.g., Knowledge-Based Systems,
Engineering Applications of Artificial Intelligence) be a better
match? We would be happy to share a one-page summary if useful.

Thank you for your time.

Best regards,
[Corresponding Author Name]
[Affiliation, email]
```

---

## Expected response patterns and how to handle each

### Response A: "Yes, this fits; please submit."

**What it means:** The EiC has confirmed scope fit. You have a soft queue position and the formal submission will go through the standard review process.

**What to do:**
1. Submit via Editorial Manager within 1–2 weeks (don't sit on it).
2. In the cover letter, reference the EiC's confirmation: "We are submitting per our pre-submission inquiry on [date], in which the EiC confirmed scope fit."
3. Continue with the 12-week plan.

### Response B: "Try Knowledge-Based Systems / EAAI instead."

**What it means:** The EiC has read the pitch and believes a sibling journal is a better fit. This is a valuable signal and saves you a desk-reject cycle.

**What to do:**
1. If KBS: proceed with the KBS submission (per the venue plan in `iui2027/strategy/VENUE-PLAN.md`).
2. If EAAI: proceed with the EAAI Special Issue on Agentic AI submission (Oct 10 deadline).
3. Thank the EiC for the redirect and acknowledge it in the new submission's cover letter.

### Response C: "Submit and let the handling editor decide."

**What it means:** The EiC has not made a scope judgment and is deferring to the handling editor. This is a neutral response and does not affect the formal submission.

**What to do:**
1. Submit via Editorial Manager as planned.
2. Expect a 5-day first decision (per the journal's published median).
3. If the handling editor's decision is a desk reject, address the editor's specific concern and re-submit if appropriate.

### Response D: No response within 7 days.

**What it means:** The EiC is busy (the journal receives many pre-submission inquiries) and the inquiry has been deprioritized.

**What to do:**
1. Submit via Editorial Manager as planned. The formal submission triggers an editorial decision that the pre-submission inquiry was meant to short-circuit.
2. Do not follow up on the pre-submission inquiry. The formal submission is the more important channel.

---

## Risks of pre-submission inquiry

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| EiC pre-rejects on scope | Low | Medium (saves a desk-reject cycle) | Treat as a free scoping check. |
| EiC suggests KBS / EAAI | Medium | Medium | The redirect is valuable; the venue plan accommodates it. |
| EiC ignores the inquiry | Medium | Low | Submit anyway. The formal review is the more important channel. |
| EiC commits to fast-track | Very low | High (good) | Don't expect this; treat as a bonus. |

The pre-submission inquiry is a low-cost, high-information move. Send it 2 weeks before formal submission; do not let the response delay the plan.

---

## What to attach (if the EiC requests a one-page summary)

If the EiC asks for a one-page summary (Response A or B), attach a 1-page document with:
- Title and author list (anonymized for pre-submission)
- 4-bullet contribution statement (from `POSITIONING.md`)
- 1 table: the progression table from `section-5-results.tex`
- 1 figure: the application-context figure (Fig 1 in the paper)
- 1 paragraph on the engineering surface (the 341-test regression gate)

Do not send the full manuscript at the pre-submission stage; the formal review is the more important channel.
