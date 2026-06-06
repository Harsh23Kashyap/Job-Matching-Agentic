# Explainability Evaluation: Match Explanations

Generated: 2026-06-06T15:05:23.188481+00:00

> Offline research only. Evaluates rule-based and template-grounded explainers.

## Setup

- Instances: 300 (30 candidates × top-5 jobs × 2 modes)
- Scoring: `composite`
- Explain modes: rules, template
- Consistency pairs (synthetic): 20

## Automated checks

1. Must mention at least one matched or missing skill
2. Must not mention skills absent from both candidate and job
3. Textual claims must align with score components
4. Specificity: concrete skill references vs generic-only bullets

## Results by explainer mode

| Mode | Flagged | Avg faithfulness | Avg specificity | Pass skill mention | Pass no hallucination | Pass component align |
|------|---------|------------------|-----------------|--------------------|-----------------------|----------------------|
| rules | 115/150 (77%) | 0.745 | 0.627 | 25% | 98% | 100% |
| template | 114/150 (76%) | 0.747 | 0.633 | 27% | 97% | 100% |

## Consistency (synthetic similar profiles)

- **template:** 10/10 pairs consistent (avg Jaccard=1.000)
- **rules:** 10/10 pairs consistent (avg Jaccard=1.000)

## Sample flagged instances

- `cv_01` × `job_10` (rules, rank 4): missing_skill_reference, too_generic
- `cv_02` × `job_02` (rules, rank 1): hallucinated_skills
- `cv_02` × `job_08` (rules, rank 2): missing_skill_reference, too_generic
- `cv_02` × `job_13` (rules, rank 3): missing_skill_reference, too_generic
- `cv_02` × `job_01` (rules, rank 4): missing_skill_reference, too_generic
- `cv_02` × `job_04` (rules, rank 5): missing_skill_reference, too_generic
- `cv_03` × `job_14` (rules, rank 2): missing_skill_reference, too_generic
- `cv_03` × `job_10` (rules, rank 3): missing_skill_reference, too_generic
- `cv_03` × `job_05` (rules, rank 4): missing_skill_reference, too_generic
- `cv_03` × `job_12` (rules, rank 5): missing_skill_reference, too_generic
- `cv_04` × `job_15` (rules, rank 3): missing_skill_reference, too_generic
- `cv_04` × `job_02` (rules, rank 5): missing_skill_reference, too_generic
- `cv_05` × `job_10` (rules, rank 2): missing_skill_reference, too_generic
- `cv_05` × `job_14` (rules, rank 3): missing_skill_reference, too_generic
- `cv_05` × `job_03` (rules, rank 4): missing_skill_reference, too_generic
