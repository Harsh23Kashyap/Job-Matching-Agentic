# Explainability Evaluation

Offline audit of match explanations (`why_ranked` bullets) for faithfulness, consistency, specificity, and hallucination.

## Explainer modes evaluated

| Mode | Source | Notes |
|------|--------|-------|
| `rules` | `RuleExplainer` / `build_why_ranked` | Production default |
| `template` | `GroundedLlmExplainer._template_explain` | Template with matched + missing skills |

LLM mode is excluded by default (non-deterministic). Use template mode as the grounded upper bound.

## Evaluation instances

- **30 candidates × top-5 composite matches × explainer mode** = 300 instances (both modes)
- **10 synthetic similar-profile pairs** (from fairness audit fixtures) for consistency checks

## Automated checks

| Check | Rule |
|-------|------|
| **Skill mention** | Must reference ≥1 matched or missing skill (by name or structured list) |
| **No hallucination** | Must not mention skills absent from both candidate profile and job posting |
| **Component alignment** | Claims like "High semantic similarity" must match score thresholds |
| **Specificity** | Score 0–1: concrete skill names vs generic-only bullets |

## Dimensions

| Dimension | Metric |
|-----------|--------|
| **Faithfulness** | Pass rate on hard checks (skill mention, no hallucination, component align) |
| **Consistency** | Jaccard similarity of bullets across synthetic similar-profile pairs |
| **Specificity** | Mean specificity score per mode |
| **Hallucination** | Count of instances with phantom skill mentions |

## Flagged cases

An instance is flagged when any violation occurs:

- `missing_skill_reference`
- `hallucinated_skills`
- `component_mismatch:*`
- `too_generic` (skills exist but explanation is generic-only)

## Run

```bash
python -m benchmarks.run_explainability_eval
python -m benchmarks.run_explainability_eval --modes rules --top-k 3
```

## Outputs

| File | Contents |
|------|----------|
| `explainability_report.json` | Summary + flagged instances |
| `explainability_instances.csv` | All evaluated explanations |
| `explainability_flagged.csv` | Failed checks only |
| `explainability_consistency.csv` | Synthetic pair consistency |
| `explainability_summary.md` | Human-readable report |
