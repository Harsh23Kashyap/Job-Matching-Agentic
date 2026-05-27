import { useEffect, useState } from "react";
import {
  deriveWhyMatch,
  deriveEmployerWhyMatch,
  formatCandidateExperience,
  formatExpectedCompensation,
  formatRemotePreference,
  humanizeStrategy,
  matchPercent,
  matchScoreValue,
  matchSkills,
  matchTier,
} from "../utils/format.js";
import SkillChip, { SkillChipList } from "./SkillChip.jsx";
import ResumeImprovementPanel from "./ResumeImprovementPanel.jsx";
import SimilarRecommendations from "./SimilarRecommendations.jsx";

const SCORE_COMPONENTS = [
  { key: "semantic_score", label: "Semantic", weight: "40%" },
  { key: "skills_score", label: "Skills", weight: "30%" },
  { key: "experience_score", label: "Experience", weight: "15%" },
  { key: "compensation_score", label: "Compensation", weight: "10%" },
  { key: "location_score", label: "Location / remote", weight: "5%" },
];

const SCORING_NOTE =
  "Weighted blend: semantic 40%, skills 30%, experience 15%, compensation 10%, location/remote 5%.";

function ScoreBar({ label, weight, value }) {
  const numeric = value != null && !Number.isNaN(Number(value)) ? Number(value) : null;
  const pct = numeric != null ? Math.round(numeric * 100) : null;

  return (
    <div className="match-drawer-score-row">
      <div className="match-drawer-score-row__head">
        <span className="match-drawer-score-row__label">{label}</span>
        <span className="match-drawer-score-row__meta">
          <span className="match-drawer-score-row__weight">{weight}</span>
          <span className="match-drawer-score-row__value">{pct != null ? `${pct}%` : "—"}</span>
        </span>
      </div>
      <div
        className="match-drawer-score-bar"
        role="progressbar"
        aria-valuenow={pct ?? 0}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={`${label} score`}
      >
        <div
          className="match-drawer-score-bar__fill"
          style={{ width: pct != null ? `${Math.max(pct, 2)}%` : "0%" }}
        />
      </div>
    </div>
  );
}

function MatchDrawerCard({ title, children, className = "" }) {
  return (
    <section className={`match-drawer-card ${className}`.trim()}>
      {title && <h3 className="match-drawer-card__title">{title}</h3>}
      {children}
    </section>
  );
}

function buildMetaRows(row, matchContext, variant) {
  const rows = [{ label: "Rank in results", value: `#${row.rank}` }];

  if (matchContext.strategy_used) {
    rows.push({ label: "Matching approach", value: humanizeStrategy(matchContext.strategy_used) });
  }
  if (matchContext.evaluated_count != null) {
    rows.push({
      label: variant === "employer" ? "Candidates compared" : "Roles compared",
      value: String(matchContext.evaluated_count),
    });
  }
  if (matchContext.corpus_size != null) {
    rows.push({
      label: variant === "employer" ? "Candidates in pool" : "Open roles in pool",
      value: String(matchContext.corpus_size),
    });
  }
  if (row.routing_reason) {
    rows.push({ label: "Routing note", value: row.routing_reason });
  }
  if (row.constraint_notes?.length) {
    rows.push({ label: "Constraint notes", value: row.constraint_notes.join("; ") });
  }

  return rows;
}

export default function MatchDetailsDrawer({
  row,
  whyLine,
  onClose,
  subtitle = "Role details",
  variant = "candidate",
  matchContext = {},
}) {
  const [showResumeCoach, setShowResumeCoach] = useState(false);

  useEffect(() => {
    setShowResumeCoach(false);
  }, [row?.target_id]);

  useEffect(() => {
    const onKey = (e) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [onClose]);

  if (!row) return null;

  const tier = matchTier(matchScoreValue(row));
  const { matched, missing } = matchSkills(row);
  const explanation =
    whyLine || (variant === "employer" ? deriveEmployerWhyMatch(row) : deriveWhyMatch(row));
  const metaRows = buildMetaRows(row, matchContext, variant);
  const hasContact =
    row.contact_email || row.contact_phone || row.contact_linkedin || row.contact_portfolio;

  return (
    <div className="drawer-backdrop" onClick={onClose} role="presentation">
      <aside
        className="match-drawer"
        role="dialog"
        aria-labelledby="match-drawer-title"
        onClick={(e) => e.stopPropagation()}
      >
        <header className="match-drawer-head">
          <div>
            <p className="match-drawer-eyebrow">{subtitle}</p>
            <h2 id="match-drawer-title">{row.target_label}</h2>
          </div>
          <button type="button" className="icon-btn" onClick={onClose} aria-label="Close">
            ×
          </button>
        </header>

        <div className="match-drawer-body">
          <MatchDrawerCard className={`match-drawer-card--hero ${tier.className}`}>
            <p className="match-drawer-score-label">Overall match</p>
            <p className="match-drawer-score-display">{matchPercent(matchScoreValue(row))}</p>
            <span className={`match-tier-pill match-tier-pill--lg ${tier.className}`}>{tier.label}</span>
            <p className="match-drawer-explanation">{explanation}</p>
          </MatchDrawerCard>

          <MatchDrawerCard title="Score breakdown">
            <div className="match-drawer-score-list">
              {SCORE_COMPONENTS.map(({ key, label, weight }) => (
                <ScoreBar key={key} label={label} weight={weight} value={row[key]} />
              ))}
            </div>
            <p className="match-drawer-scoring-note">{SCORING_NOTE}</p>
          </MatchDrawerCard>

          <MatchDrawerCard title="Skills">
            <div className="match-drawer-skills-block">
              <p className="match-drawer-skills-label">Matched</p>
              {matched.length > 0 ? (
                <SkillChipList skills={matched} variant="match" />
              ) : (
                <SkillChip variant="empty">No direct overlap</SkillChip>
              )}
            </div>
            <div className="match-drawer-skills-block">
              <p className="match-drawer-skills-label">Missing</p>
              {missing.length > 0 ? (
                <SkillChipList skills={missing} variant="missing" />
              ) : (
                <SkillChip variant="empty">No major gaps flagged</SkillChip>
              )}
            </div>
          </MatchDrawerCard>

          {variant === "candidate" && row.target_id && (
            showResumeCoach ? (
              <ResumeImprovementPanel
                jobId={row.target_id}
                jobTitle={row.target_label}
                onClose={() => setShowResumeCoach(false)}
              />
            ) : (
              <MatchDrawerCard className="match-drawer-card--actions">
                <p className="match-drawer-coach-intro">
                  Tailor your resume for this role without changing your saved profile.
                </p>
                <button
                  type="button"
                  className="btn-primary match-drawer-coach-btn"
                  onClick={() => setShowResumeCoach(true)}
                >
                  Improve resume for this role
                </button>
              </MatchDrawerCard>
            )
          )}

          {variant === "candidate" && row.target_id && !showResumeCoach && (
            <SimilarRecommendations
              entityId={row.target_id}
              entityType="jobs"
              title="Similar jobs"
            />
          )}

          {variant === "employer" && row.target_id && (
            <SimilarRecommendations
              entityId={row.target_id}
              entityType="candidates"
              title="Similar candidates"
            />
          )}

          {variant === "employer" && (
            <MatchDrawerCard title="Profile summary">
              <ul className="match-drawer-meta-list">
                <li>
                  <span>Experience</span>
                  <strong>{formatCandidateExperience(row.candidate_experience_years) || "—"}</strong>
                </li>
                <li>
                  <span>Expected compensation</span>
                  <strong>{formatExpectedCompensation(row) || "—"}</strong>
                </li>
                <li>
                  <span>Remote preference</span>
                  <strong>{formatRemotePreference(row) || "—"}</strong>
                </li>
              </ul>
            </MatchDrawerCard>
          )}

          {variant === "employer" && hasContact && (
            <MatchDrawerCard title="Contact">
              <ul className="match-drawer-contact">
                {row.contact_email && (
                  <li>
                    <span>Email</span>
                    <a href={`mailto:${row.contact_email}`}>{row.contact_email}</a>
                  </li>
                )}
                {row.contact_phone && (
                  <li>
                    <span>Phone</span>
                    <a href={`tel:${row.contact_phone}`}>{row.contact_phone}</a>
                  </li>
                )}
                {row.contact_linkedin && (
                  <li>
                    <span>LinkedIn</span>
                    <a href={row.contact_linkedin} target="_blank" rel="noreferrer">
                      Profile
                    </a>
                  </li>
                )}
                {row.contact_portfolio && (
                  <li>
                    <span>Portfolio</span>
                    <a href={row.contact_portfolio} target="_blank" rel="noreferrer">
                      Site
                    </a>
                  </li>
                )}
              </ul>
            </MatchDrawerCard>
          )}

          {metaRows.length > 1 && (
            <details className="match-drawer-details">
              <summary>Session details</summary>
              <ul className="match-drawer-scores">
                {metaRows.map(({ label, value }) => (
                  <li key={label}>
                    <span>{label}</span>
                    <strong>{value}</strong>
                  </li>
                ))}
              </ul>
            </details>
          )}
        </div>
      </aside>
    </div>
  );
}
