/** Composite match weights — keep in sync with backend/core/scoring.py COMPOSITE_WEIGHTS */

export const COMPOSITE_WEIGHTS = {
  semantic: 0.28,
  skills: 0.27,
  title: 0.1,
  experience: 0.15,
  compensation: 0.1,
  remote: 0.1,
};

export const COMPOSITE_SCORE_FIELDS = [
  { key: "semantic", field: "semantic_score", label: "Semantic fit" },
  { key: "skills", field: "skills_score", label: "Skills overlap" },
  { key: "title", field: "title_score", label: "Role title fit" },
  { key: "experience", field: "experience_score", label: "Experience" },
  { key: "compensation", field: "compensation_score", label: "Compensation" },
  { key: "remote", field: "remote_score", label: "Remote preference" },
];

export function resolveScoreComponents(row) {
  if (Array.isArray(row?.score_components) && row.score_components.length) {
    return row.score_components;
  }

  const remoteScore = row?.remote_score ?? row?.location_score;
  const fallback = COMPOSITE_SCORE_FIELDS.map(({ key, field, label }) => {
    const score = field === "remote_score" ? remoteScore : row?.[field];
    if (score == null || Number.isNaN(Number(score))) return null;
    const weight = COMPOSITE_WEIGHTS[key];
    const numeric = Number(score);
    return {
      key,
      label,
      weight,
      score: numeric,
      contribution: weight * numeric,
    };
  }).filter(Boolean);

  return fallback.length ? fallback : [];
}

export function formatWeightPct(weight) {
  return `${Math.round(Number(weight) * 100)}%`;
}

export function formatContributionPts(contribution) {
  return `${Math.round(Number(contribution) * 100)} pts`;
}

export function describeMatchDrivers(row) {
  const components = resolveScoreComponents(row);
  if (!components.length) return null;

  const sorted = [...components].sort((a, b) => b.contribution - a.contribution);
  const top = sorted[0];
  const weak = [...components].sort((a, b) => a.score - b.score)[0];
  const topPct = Math.round(top.score * 100);
  const weakPct = Math.round(weak.score * 100);

  if (top.score >= 0.7 && weak.score < 0.45 && top.key !== weak.key) {
    return `Strong ${top.label.toLowerCase()} (${topPct}%) drives the rank; ${weak.label.toLowerCase()} (${weakPct}%) is the main drag.`;
  }
  if (top.score >= 0.65) {
    return `${top.label} is the strongest signal (${topPct}%).`;
  }
  if (weak.score < 0.4) {
    return `${weak.label} is limiting the match (${weakPct}%).`;
  }
  return `Balanced across signals; ${top.label} contributes most.`;
}
