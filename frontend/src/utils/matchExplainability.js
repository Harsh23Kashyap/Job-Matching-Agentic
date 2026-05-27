import {
  formatContributionPts,
  formatWeightPct,
  resolveScoreComponents,
} from "./matchScoring.js";
import { matchPercent, matchSkills } from "./format.js";

export function fitLevelClass(label = "") {
  const normalized = label.toLowerCase();
  if (normalized.includes("strong")) return "match-fit--strong";
  if (normalized.includes("good")) return "match-fit--good";
  if (normalized.includes("moderate")) return "match-fit--moderate";
  if (normalized.includes("weak")) return "match-fit--weak";
  return "match-fit--neutral";
}

function fitLabelFromScore(score) {
  if (score == null || Number.isNaN(Number(score))) return "Not scored";
  const pct = Math.round(Number(score) * 100);
  if (pct >= 80) return "Strong";
  if (pct >= 60) return "Good";
  if (pct >= 40) return "Moderate";
  return "Weak";
}

function semanticReason(score) {
  const pct = matchPercent(score);
  const value = Number(score);
  if (value >= 0.75) return `Resume and job description align closely (${pct} semantic fit)`;
  if (value >= 0.55) return `Profile context partially matches the role (${pct} semantic fit)`;
  return `Limited profile-to-role text alignment (${pct} semantic fit)`;
}

function experienceReason(row, score) {
  const cand = row?.candidate_experience_years;
  if (score >= 0.8 && cand != null) {
    return `${cand} years experience aligns with role requirements`;
  }
  if (score >= 0.65) return "Experience is close to the role requirement";
  if (score < 0.45) return "Experience may be below what the role targets";
  return "Experience partially meets the role requirement";
}

function compensationReason(row, score) {
  if (score >= 0.85) return "Compensation expectations align with the role budget";
  if (score >= 0.65) return "Pay expectations are close to the posted range";
  if (score < 0.5) return "Expected pay may exceed or sit outside the role budget";
  return "Compensation fit is moderate — review the salary band";
}

function remoteReason(row, score) {
  const remote = row?.candidate_remote_preference ?? row?.remote_preference;
  if (remote == null) return "Remote preference not specified";
  if (remote && score >= 0.85) return "Remote-friendly role matches your preference";
  if (remote && score < 0.55) return "You prefer remote; role may require on-site work";
  if (!remote) return "On-site preference — remote policy has limited impact";
  return "Remote setup partially aligns";
}

function buildFitSignal(score, reason) {
  if (score == null || Number.isNaN(Number(score))) {
    return { score: null, label: "Not scored", reason };
  }
  return {
    score: Number(score),
    label: fitLabelFromScore(score),
    reason,
  };
}

/** Resolve structured explanation from API payload or legacy score fields. */
export function resolveMatchExplanation(row) {
  if (row?.explanation) {
    return {
      ...row.explanation,
      score_breakdown: row.explanation.score_breakdown?.length
        ? row.explanation.score_breakdown
        : resolveScoreComponents(row),
    };
  }

  const remoteScore = row?.remote_score ?? row?.location_score;
  const { matched, missing } = matchSkills(row);

  return {
    matched_skills: matched,
    missing_skills: missing,
    semantic: buildFitSignal(
      row?.semantic_score,
      row?.semantic_score != null ? semanticReason(row.semantic_score) : "Semantic fit not scored for this strategy",
    ),
    experience: buildFitSignal(
      row?.experience_score,
      row?.experience_score != null
        ? experienceReason(row, row.experience_score)
        : "Experience not scored for this strategy",
    ),
    compensation: buildFitSignal(
      row?.compensation_score,
      row?.compensation_score != null
        ? compensationReason(row, row.compensation_score)
        : "Compensation not scored for this strategy",
    ),
    remote: buildFitSignal(
      remoteScore,
      remoteScore != null ? remoteReason(row, remoteScore) : "Remote fit not scored for this strategy",
    ),
    score_breakdown: resolveScoreComponents(row),
    final_score: row?.final_score ?? row?.similarity ?? 0,
  };
}

export function formatFitScore(score) {
  if (score == null || Number.isNaN(Number(score))) return "—";
  return matchPercent(score);
}

export { formatContributionPts, formatWeightPct };
