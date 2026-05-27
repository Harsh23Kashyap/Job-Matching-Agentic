import { useEffect } from "react";
import {
  deriveWhyMatch,
  deriveEmployerWhyMatch,
  formatCandidateExperience,
  formatCandidateMatchScore,
  formatExpectedCompensation,
  formatRemotePreference,
  humanizeStrategy,
  matchSkills,
  matchTier,
} from "../utils/format.js";

const CANDIDATE_MATCH_EXPLANATION =
  "We compare your profile with the role using skills, experience, and resume context.";

function buildTechnicalRows(row, matchContext = {}, variant = "candidate") {
  const rows = [
    { label: "Overall fit", value: formatCandidateMatchScore(row.similarity) },
    {
      label: "Skills overlap",
      value: row.skills_score != null ? formatCandidateMatchScore(row.skills_score) : "—",
    },
    {
      label: "Profile alignment",
      value: formatCandidateMatchScore(row.semantic_score),
    },
    { label: "Rank in results", value: `#${row.rank}` },
  ];

  if (matchContext.strategy_used) {
    rows.push({
      label: "Matching approach",
      value: humanizeStrategy(matchContext.strategy_used),
    });
  }
  if (matchContext.fusion_mode) {
    rows.push({ label: "Score blending", value: String(matchContext.fusion_mode) });
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
  if (row.calibrated_similarity != null) {
    rows.push({
      label: "Calibrated score",
      value: formatCandidateMatchScore(row.calibrated_similarity),
    });
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

  const tier = matchTier(row.similarity);
  const { matched, missing } = matchSkills(row);
  const why = whyLine || (variant === "employer" ? deriveEmployerWhyMatch(row) : deriveWhyMatch(row));
  const technicalRows = buildTechnicalRows(row, matchContext, variant);
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

        <div className="match-drawer-pills">
          <span className={`match-badge match-badge--pill ${tier.className}`}>
            {formatCandidateMatchScore(row.similarity)} match
          </span>
          <span className={`match-tier-pill ${tier.className}`}>{tier.label}</span>
        </div>

        <section className="match-drawer-section">
          <h3>Why this matched</h3>
          <p>{why}</p>
        </section>

        {variant === "employer" && (
          <section className="match-drawer-section">
            <h3>Profile summary</h3>
            <ul className="match-drawer-scores match-drawer-scores--plain">
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
          </section>
        )}

        <section className="match-drawer-section">
          <h3>Matched skills</h3>
          {matched.length > 0 ? (
            <div className="signal-chips">
              {matched.map((skill) => (
                <span key={skill} className="signal-chip signal-chip--match">
                  {skill}
                </span>
              ))}
            </div>
          ) : (
            <span className="signal-chip signal-chip--empty">No direct overlap</span>
          )}
        </section>

        <section className="match-drawer-section">
          <h3>Missing or weak signals</h3>
          {missing.length > 0 ? (
            <div className="signal-chips">
              {missing.map((skill) => (
                <span key={skill} className="signal-chip signal-chip--missing">
                  {skill}
                </span>
              ))}
            </div>
          ) : (
            <span className="signal-chip signal-chip--empty">No major gaps flagged</span>
          )}
        </section>

        <section className="match-drawer-section">
          <h3>How we score matches</h3>
          <p className="match-drawer-note match-drawer-note--lead">
            {variant === "candidate"
              ? CANDIDATE_MATCH_EXPLANATION
              : "We compare candidate profiles with your role using skills, experience, and resume context."}
          </p>
        </section>

        {variant === "employer" && hasContact && (
          <section className="match-drawer-section">
            <h3>Contact</h3>
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
          </section>
        )}

        <details className="match-drawer-details">
          <summary>Technical details</summary>
          <ul className="match-drawer-scores">
            {technicalRows.map(({ label, value }) => (
              <li key={label}>
                <span>{label}</span>
                <strong>{value}</strong>
              </li>
            ))}
          </ul>
        </details>
      </aside>
    </div>
  );
}
