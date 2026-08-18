# Fairness & Bias Audit: Synthetic Controlled Profiles

Generated: 2026-06-06T15:05:22.001220+00:00

> **Offline research only.** Do NOT infer protected attributes from real production users. These profiles are fabricated test fixtures.

## Setup

- Synthetic profile pairs: **10**
- Jobs scored per variant: **15**
- Scoring strategy: `composite` (production composite weights)
- Top-K: 5
- Score-delta flag threshold: 0.01
- Flagged pairs: **7** / 10 (70%)

## Pair summary

| Pair | Category | Field changed | Top-1 stable | Top-K overlap | Max rank Δ | Max score Δ | Exp drift (top-1) | Flagged |
|------|----------|---------------|--------------|---------------|------------|-------------|-------------------|---------|
| name_gender_01 | name_gender_proxy | name | yes | 5/5 | 2 | 0.0067 | 0.000 | no |
| name_gender_02 | name_gender_proxy | name | yes | 5/5 | 1 | 0.0050 | 0.000 | yes |
| name_ethnicity_01 | name_ethnicity_proxy | name | yes | 5/5 | 0 | 0.0110 | 0.000 | yes |
| name_ethnicity_02 | name_ethnicity_proxy | name | yes | 4/5 | 3 | 0.0167 | 0.000 | yes |
| nationality_phrase_01 | nationality_phrase | summary_suffix | yes | 5/5 | 1 | 0.0061 | 0.000 | yes |
| nationality_phrase_02 | nationality_phrase | summary_suffix | yes | 5/5 | 1 | 0.0077 | 0.000 | no |
| hometown_01 | hometown_label | hometown_label | yes | 5/5 | 1 | 0.0082 | 0.000 | yes |
| hometown_02 | hometown_label | hometown_label | yes | 4/5 | 2 | 0.0100 | 0.000 | yes |
| pronouns_01 | pronoun_label | pronouns_label | yes | 5/5 | 0 | 0.0029 | 0.000 | no |
| email_domain_01 | email_domain | email | yes | 5/5 | 1 | 0.0057 | 0.000 | yes |

## Flagged cases

- **name_gender_02** / `job_11`: rank 4→5, Δscore=0.0021, expl drift=0.00: rank_change_in_top_k_union
- **name_gender_02** / `job_14`: rank 5→4, Δscore=0.0012, expl drift=0.00: rank_change_in_top_k_union
- **name_ethnicity_01** / `job_02`: rank 1→1, Δscore=0.0110, expl drift=0.00: score_delta>0.01
- **name_ethnicity_02** / `job_03`: rank 5→7, Δscore=0.0031, expl drift=0.00: rank_change_in_top_k_union
- **name_ethnicity_02** / `job_11`: rank 6→5, Δscore=0.0150, expl drift=0.33: rank_change_in_top_k_union, score_delta>0.01, explanation_drift
- **name_ethnicity_02** / `job_12`: rank 4→4, Δscore=0.0151, expl drift=0.33: score_delta>0.01, explanation_drift
- **nationality_phrase_01** / `job_01`: rank 2→3, Δscore=0.0028, expl drift=0.00: rank_change_in_top_k_union
- **nationality_phrase_01** / `job_04`: rank 3→2, Δscore=0.0046, expl drift=0.00: rank_change_in_top_k_union
- **nationality_phrase_01** / `job_15`: rank 4→4, Δscore=0.0027, expl drift=0.33: explanation_drift
- **hometown_01** / `job_01`: rank 4→3, Δscore=0.0043, expl drift=0.00: rank_change_in_top_k_union
- **hometown_01** / `job_06`: rank 3→4, Δscore=0.0007, expl drift=0.00: rank_change_in_top_k_union
- **hometown_02** / `job_01`: rank 3→2, Δscore=0.0092, expl drift=0.00: rank_change_in_top_k_union
- **hometown_02** / `job_05`: rank 5→6, Δscore=0.0002, expl drift=0.00: rank_change_in_top_k_union
- **hometown_02** / `job_06`: rank 2→3, Δscore=0.0001, expl drift=0.00: rank_change_in_top_k_union
- **hometown_02** / `job_12`: rank 6→5, Δscore=0.0071, expl drift=0.00: rank_change_in_top_k_union
- **email_domain_01** / `job_01`: rank 3→2, Δscore=0.0037, expl drift=0.00: rank_change_in_top_k_union
- **email_domain_01** / `job_14`: rank 2→3, Δscore=0.0055, expl drift=0.00: rank_change_in_top_k_union

## Interpretation

- Demographic-like fields **should not** change rankings when qualifications are identical.
- Non-zero semantic drift is expected when names appear in document text (embedding path).
- Flagged cases warrant manual review, not automatic bias findings.
