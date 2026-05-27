import { useEffect } from "react";
import { deriveWhyMatch, explainMatchScore, matchPercent, matchSkills, matchTier } from "../utils/format.js";

export default function MatchDetailsDrawer({ row, whyLine, onClose, subtitle = "Match details" }) {
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
  const why = whyLine || deriveWhyMatch(row);

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
          <span className={`match-badge match-badge--pill ${tier.className}`}>{matchPercent(row.similarity)} match</span>
        </div>

        <section className="match-drawer-section">
          <h3>Why this matched</h3>
          <p>{why}</p>
        </section>

        <section className="match-drawer-section">
          <h3>Matched skills</h3>
          {matched.length > 0 ? (
            <div className="signal-chips">
              {matched.map((s) => (
                <span key={s} className="signal-chip signal-chip--match">{s}</span>
              ))}
            </div>
          ) : (
            <span className="signal-chip signal-chip--empty">No direct overlap</span>
          )}
        </section>

        <section className="match-drawer-section">
          <h3>Missing skills</h3>
          {missing.length > 0 ? (
            <div className="signal-chips">
              {missing.map((s) => (
                <span key={s} className="signal-chip signal-chip--missing">{s}</span>
              ))}
            </div>
          ) : (
            <span className="signal-chip signal-chip--empty">No gaps — all required skills covered</span>
          )}
        </section>

        {(row.contact_email || row.contact_phone || row.contact_linkedin || row.contact_portfolio) && (
          <section className="match-drawer-section">
            <h3>Contact</h3>
            <ul className="match-drawer-contact">
              {row.contact_email && (
                <li><span>Email</span><a href={`mailto:${row.contact_email}`}>{row.contact_email}</a></li>
              )}
              {row.contact_phone && (
                <li><span>Phone</span><a href={`tel:${row.contact_phone}`}>{row.contact_phone}</a></li>
              )}
              {row.contact_linkedin && (
                <li><span>LinkedIn</span><a href={row.contact_linkedin} target="_blank" rel="noreferrer">Profile</a></li>
              )}
              {row.contact_portfolio && (
                <li><span>Portfolio</span><a href={row.contact_portfolio} target="_blank" rel="noreferrer">Site</a></li>
              )}
            </ul>
          </section>
        )}

        <section className="match-drawer-section">
          <h3>Match score explanation</h3>
          <p className="match-drawer-note match-drawer-note--lead">{explainMatchScore(row)}</p>
          <ul className="match-drawer-scores">
            <li><span>Overall fit</span><strong>{matchPercent(row.similarity)}</strong></li>
            <li><span>Skills overlap</span><strong>{row.skills_score != null ? matchPercent(row.skills_score) : "—"}</strong></li>
            <li><span>Profile alignment</span><strong>{matchPercent(row.semantic_score)}</strong></li>
            <li><span>Rank</span><strong>#{row.rank}</strong></li>
          </ul>
        </section>
      </aside>
    </div>
  );
}
