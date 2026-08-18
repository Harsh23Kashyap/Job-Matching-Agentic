# Numbers-pass worksheet — manuscript claim → honest value → source

> The staging sheet for the **user-led numbers pass** (Phases 31–36). Manuscript numbers are
> currently UNCHANGED (RD-010/11); this maps each claim to the verified/honest value from the
> experiments so the rewrite is fast and grounded. "Update to better/true, don't remove" (user).
> Every honest value below traces to a committed artifact under `backend/reports/` or `research/results/`.

| # | Manuscript claim (current) | Honest value (verified) | Source artifact | Recommended action |
|---|---|---|---|---|
| 1 | composite nDCG@5 **0.949** | 0.949 (held-out k-fold 0.949, CI [0.870,0.993]) | kfold_cv.json / composite_eval_report.json | **KEEP** — the anchor; cite held-out CI |
| 2 | best single **0.969 / R@5 1.000** | PHANTOM — no artifact; best committed = Multimodal **0.924** (R@5 0.933) | comparison_table.json | Regenerate the w=0.7 sweep & commit, OR replace with 0.924; drop dead file citations |
| 3 | learned fusion **0.968** | leaky; held-out pointwise-LR **0.917** [0.838,0.974] | pointwise_ltr.json | Replace with 0.917; note it doesn't beat composite |
| 4 | (new baseline) | **LambdaMART 0.963** [0.925,0.992] | lambdamart_baseline.json | ADD — genuine listwise LTR; CIs overlap composite |
| 5 | (new baseline) | **JobBERT 0.864** [0.779,0.934]; MiniLM two-tower 0.878 | jobbert_baseline.json | ADD — domain encoder does NOT beat MiniLM (honest negative) |
| 6 | cross-encoder **0.939 / −0.030 (ESWA) vs −0.108 (IUI)** | PHANTOM — CE never run; no artifact; inconsistent across papers | (none) | Run & commit CE report, OR remove specific CE numbers |
| 7 | significance **Δ=+0.071, p=0.048 ("statistically significant")** | REPRODUCIBLE re-run (fixed seed): Δ=+0.071, **CI [−0.014,+0.167] crosses 0**, one-sided **p=0.051 (>0.05)**, two-sided **p=0.102**, W/L/T 10/3/17; **NO comparison survives Holm** (family of 8) | significance_corrected.json (EXP-022) | **Withdraw "statistically significant"** → "positive but NOT significant (two-sided p=0.10, CI incl. 0, fails Holm)" |
| 8 | ECE **0.40 → 0.032 (held-out)** | leaky; held-out 5-fold **0.0192** [0.0097,0.0286] | calibration_binary.json | Replace 0.032 → 0.0192; recompute the "0.40" baseline held-out |
| 9 | Brier **0.093**; "0.9 ⇒ 9/10" | Brier 0.093 (= held-out); BUT **Brier skill-score 0.007**, AUC 0.758, confidence squashed [0.11,0.14] — never emits ~0.9 | calibration_discrimination.json | KEEP Brier; ADD BSS/AUC/range; **delete "0.9⇒9/10"** |
| 10 | faithfulness **0.745** (rule) / 0.747 (LLM-template) | lint-average of 3 checks (one 100% tautological); flag-rate 0.77; skill-mention 0.25; "LLM-template" invokes NO LLM | explainability_report.json | Rename metric; report flag-rate + skill-mention; fix "LLM-template" label |
| 11 | consistency **1.000** | trivial (deterministic template on inputs differing only in ignored fields) | explainability_report.json | Caveat as definitional, or replace with meaningful perturbation |
| 12 | counterfactual **7/10**, "10 pairs", top-1 stable all | 50-pair: recourse 12/25 (**all rank_delta=0** — recourse null), demographic 9/25, top1 stable 0.96 (one flip) | counterfactual_50.json | Adopt 50-pair; report recourse NULL honestly; separate recourse vs demographic; fix pronoun no-op |
| 13 | DIR **0.82 / 0.75** ("below 0.80–0.85 floor") | proxy groups on demo corpus, NOT demographic; 0.82 is ABOVE the 0.80 four-fifths threshold (only 0.75 fails); n=30, no CI | fairness_eval.json | Reframe as proxy sensitivity (not fairness audit); fix caption arithmetic |
| 14 | (RQ2 weights) semantic 0.28 > skills 0.27 > title 0.10 "maximize nDCG on held-out" | hand-set = **design PRIOR, not fitted**; bootstrap-fit near-reverses: title 0.30 > skills 0.238 > semantic 0.144 (all sign-stable) | weight_stability.json | Say "hand-set prior"; drop "maximize nDCG on held-out" (B11); report the divergence honestly |
| 15 | (RQ2 ablation) "six channels matter" | only **semantic** provably load-bearing (leave-one-out +0.080, CI excl 0); compensation marginal; title/skills/experience/remote not sig (n=30) | leave_one_out_ablation.json | Don't claim all six matter; report which are load-bearing |
| 16 | (RQ7 generalization) resume k-fold as generalization | vacuous for fixed weights; genuine **job-held-out (learned) 0.928** (strict 0.930) | job_heldout.json | ADD job-held-out as the real generalization; caveat fixed-composite k-fold |
| 17 | (RQ8) "multi-agent architecture" contribution | failure isolation REAL + hot path 0.045 ms/pair, but NO monolith-vs-agents benefit | architecture_value.json | **DEMOTE** multi-agent to implementation detail (RD-006) |
| 18 | corpus: 12.3 skills/resume, 8.7 req + 4.2 pref, ~5,000 vocab | true: **2.97** skills/resume, **2.13** req, **no preferred field**, **74** tokens | data/cvs.json, data/jobs.json | UPDATE to true values (deferred to numbers pass per user; don't remove) |
| 19 | Funding: 32,000 A100 GPU-hours (NVIDIA) | KEPT per user (RD-008 amend) | title-page.tex / cover-letter.md | KEEP as-is |
| 20 | DOI 10.7910/DVN/JOBMTCH-2026 + commit in blinded body | unverified; anonymity leak | main.tex | Numbers/anonymity pass: soften to "on acceptance" + anonymized artifact (currently left in place per "don't remove") |
| 21 | tests "302 pytest + 39 node = 341" | UNVERIFIED — re-count in Phase 24 | (pending) | Re-run pytest + node --test; record actual counts |

**One-line honest story for the rewrite:** *competitive* ranking (no method significantly beats another at n=30) + auditable, **semantic-dominant** decomposition + **honestly-characterized** calibration (low ECE but low discrimination) + genuine **unseen-job generalization**; multi-agent = implementation detail, not a contribution; "trustworthy" unsupported. Weaker than the current draft, defensible under hostile review.
