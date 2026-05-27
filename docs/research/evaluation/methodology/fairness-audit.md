# Fairness & Bias Audit

Offline research tooling for detecting **ranking instability** when only irrelevant demographic-like fields change.

## Principles

1. **Never infer protected attributes from real users** · production CVs are not analyzed for demographics.
2. **Synthetic controlled profiles only** · fabricated pairs in `data/fairness_audit_profiles.json`.
3. **Counterfactual design** · match-relevant fields (skills, experience, salary, remote preference, professional summary) are identical; only demographic-like metadata differs between variants A and B.

## Match-relevant vs demographic-like fields

| Match-relevant (held constant) | Demographic-like (varied in tests) |
|-------------------------------|-----------------------------------|
| skills | name |
| experience_years | email / domain |
| remote_preference | summary suffix (nationality phrase) |
| preferred_salary | hometown label |
| professional summary core | pronoun label |

## Audit procedure

For each synthetic pair:

1. Build two candidate snapshots (variants A and B).
2. Rank all 15 jobs with production **composite** scoring for each variant.
3. Compare rankings and per-job scores.
4. Generate rule-based explanations via `build_why_ranked` (same as production rules explainer).

## Reported metrics

| Metric | Description |
|--------|-------------|
| **Rank stability** | Top-1 unchanged? Top-K overlap count? Max/mean rank change across jobs |
| **Score delta** | \|score_A − score_B\| per job; mean and max across corpus |
| **Explanation drift** | 1 − Jaccard similarity of explanation bullet sets |
| **Flagged cases** | Pairs/jobs exceeding thresholds (top-1 change, score delta, explanation drift in top-K) |

## Flag thresholds (defaults)

- Top-1 job changes → flag
- Score delta > 0.01 in top-K union → flag
- Explanation drift > 0 in top-K union → flag

## Run

```bash
python -m benchmarks.run_fairness_audit
bash scripts/run_fairness_audit.sh
```

## Outputs

| File | Contents |
|------|----------|
| `fairness_audit_report.json` | Full structured report |
| `fairness_audit_summary.md` | Human-readable summary |
| `fairness_audit_pairs.csv` | One row per synthetic pair |
| `fairness_audit_flagged.csv` | Flagged job-level cases |

## Interpretation

- Embedding-based semantic scores **may** shift when names appear in document text · this is a known audit signal, not proof of discriminatory intent.
- Flagged cases require **manual review**; the audit does not auto-label bias.
- This complements (does not replace) the legacy experience/remote disparate-impact baseline in `core/fairness.py`.
