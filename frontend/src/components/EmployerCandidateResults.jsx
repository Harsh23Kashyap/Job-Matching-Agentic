import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { humanizeStrategy, matchPercent, matchTier, parseWhySignals } from "../utils/format.js";
import { IconAlert } from "./icons.jsx";

function CandidateMatchCard({ row }) {
  const [open, setOpen] = useState(false);
  const tier = matchTier(row.similarity);
  const { matched, other } = parseWhySignals(row.why_ranked);

  return (
    <article className="job-match-card">
      <div className="job-match-card-head">
        <div>
          <h3>{row.target_label}</h3>
          <p>{tier.label} for this role.</p>
        </div>
        <span className={`match-badge ${tier.className}`}>{matchPercent(row.similarity)} match</span>
      </div>
      {matched.length > 0 && (
        <div className="signal-group">
          <span className="signal-label">Matched skills</span>
          <div className="signal-chips">
            {matched.slice(0, 5).map((s) => (
              <span key={s} className="signal-chip signal-chip--match">
                {s}
              </span>
            ))}
          </div>
        </div>
      )}
      {other.length > 0 && (
        <div className="signal-group">
          <span className="signal-label">Fit notes</span>
          <div className="signal-chips">
            {other.map((s) => (
              <span key={s} className="signal-chip">
                {s}
              </span>
            ))}
          </div>
        </div>
      )}
      <button type="button" className="btn-text" onClick={() => setOpen(!open)}>
        {open ? "Hide match details" : "View match details"}
      </button>
      {open && (
        <div className="match-details">
          <p>Skills overlap: {row.skills_score != null ? matchPercent(row.skills_score) : "—"}</p>
          <p>Profile alignment: {matchPercent(row.semantic_score)}</p>
          <p>Overall rank: #{row.rank}</p>
        </div>
      )}
    </article>
  );
}

export default function EmployerCandidateResults({ response, error, jobTitle }) {
  const [search, setSearch] = useState("");
  const [minMatch, setMinMatch] = useState("0");

  const filtered = useMemo(() => {
    if (!response?.results) return [];
    let rows = [...response.results];
    if (search.trim()) {
      const q = search.toLowerCase();
      rows = rows.filter((r) => r.target_label.toLowerCase().includes(q));
    }
    const min = Number(minMatch) / 100;
    rows = rows.filter((r) => r.similarity >= min);
    return rows.sort((a, b) => b.similarity - a.similarity);
  }, [response, search, minMatch]);

  if (error) {
    return (
      <section className="portal-panel">
        <div className="notice-warning">
          <IconAlert />
          <span>{error}</span>
        </div>
      </section>
    );
  }

  if (!response) {
    return (
      <section className="portal-panel">
        <div className="empty-state-product">
          <h3>No candidates yet</h3>
          <p>Select a job and run a search to see ranked candidate matches.</p>
          <ul className="empty-checklist">
            <li>Post a job with required skills</li>
            <li>Choose the role to match against</li>
            <li>Review ranked profiles</li>
          </ul>
        </div>
      </section>
    );
  }

  const good = (response.results || []).filter((r) => r.similarity >= 0.6).length;

  return (
    <section className="portal-panel candidate-results">
      <p className="auth-sub">
        Matches for <strong>{jobTitle || response.query_label}</strong> · {humanizeStrategy(response.strategy_used)}
      </p>
      <div className="match-summary-cards">
        <div className="summary-card">
          <span className="summary-value">{response.evaluated_count ?? response.results.length}</span>
          <span className="summary-label">Profiles reviewed</span>
        </div>
        <div className="summary-card">
          <span className="summary-value">{good}</span>
          <span className="summary-label">Strong fits</span>
        </div>
        <div className="summary-card">
          <span className="summary-value">{matchPercent(response.results[0]?.similarity ?? 0)}</span>
          <span className="summary-label">Top match</span>
        </div>
      </div>
      <div className="results-filters">
        <input type="search" placeholder="Search candidates…" value={search} onChange={(e) => setSearch(e.target.value)} />
        <select value={minMatch} onChange={(e) => setMinMatch(e.target.value)}>
          <option value="0">Min match: Any</option>
          <option value="60">Min match: 60%+</option>
          <option value="80">Min match: 80%+</option>
        </select>
      </div>
      <div className="job-match-list">
        {filtered.map((row) => (
          <CandidateMatchCard key={row.target_id} row={row} />
        ))}
      </div>
    </section>
  );
}

export function EmployerNoJobsEmpty() {
  return (
    <section className="portal-panel">
      <div className="empty-state-product">
        <h3>No jobs posted yet</h3>
        <p>Create a job posting first, then we'll rank matching candidates.</p>
        <Link to="/employer/jobs" className="btn-primary">
          Create a job
        </Link>
      </div>
    </section>
  );
}
