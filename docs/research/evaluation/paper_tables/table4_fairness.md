**Fairness audit under synthetic demographic counterfactuals.**

*Label: `tab:fairness`*

| Pair | Field changed | Top-1 stable | Top-5 overlap | Max rank Δ | Max score Δ | Flagged |
| --- | --- | --- | --- | --- | --- | --- |
| name_gender_01 | name | Yes | 5/5 | 1 | 0.0096 | No |
| name_gender_02 | name | Yes | 5/5 | 0 | 0.0072 | No |
| name_ethnicity_01 | name | Yes | 5/5 | 2 | 0.0157 | Yes |
| name_ethnicity_02 | name | Yes | 5/5 | 3 | 0.0238 | Yes |
| nationality_phrase_01 | summary_suffix | No | 5/5 | 1 | 0.0087 | Yes |
| nationality_phrase_02 | summary_suffix | Yes | 5/5 | 1 | 0.0110 | No |
| hometown_01 | hometown_label | Yes | 4/5 | 2 | 0.0117 | Yes |
| hometown_02 | hometown_label | Yes | 5/5 | 2 | 0.0143 | Yes |
| pronouns_01 | pronouns_label | Yes | 5/5 | 1 | 0.0042 | No |
| email_domain_01 | email | Yes | 4/5 | 1 | 0.0082 | Yes |

*Note: Synthetic counterfactual pairs only (10 pairs). 6 flagged under score-delta and rank-stability thresholds. No protected attributes inferred from real users.*
