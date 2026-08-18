# Explanation study — instrument (template; adjust per IRB/design)

Between-subjects factor = CONDITION {score_only, generic_template, factor_grounded}; each participant sees one condition across all screens (`*__<condition>.html`). Per screen, collect: advance decision (vs the reference labels), decision confidence (1-7), information usefulness (1-7), perceived top factor (free text -> compare to the model's top channel for faithfulness), trust (1-7); log time-to-decision. Analyse with a mixed-effects model (outcome ~ condition + (1|participant) + (1|screen)); Holm across the pre-registered families. See docs/submission/eswa/HUMAN_STUDY_PROTOCOL.md.

NOTE: valid *system-wrong* items (needed for the trust-calibration test) require the G2 explicit negatives; until then `shortlist_has_labeled_relevant` in manifest.csv is only a coarse proxy.
