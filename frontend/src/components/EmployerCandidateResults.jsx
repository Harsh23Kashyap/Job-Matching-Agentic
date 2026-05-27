import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { deriveWhyMatch, humanizeStrategy, matchPercent, matchSkills, matchTier, pluralGoodMatches } from "../utils/format.js";
import { ResultsDecor } from "./PortalBackground.jsx";
import MatchDetailsDrawer from "./MatchDetailsDrawer.jsx";
import EmptyState from "./EmptyState.jsx";
import { IconAlert } from "./icons.jsx";

function CandidateMatchCard({ row, onViewDetails }) {
  const tier = matchTier(row.similarity);
  const { matched } = matchSkills(row);
  const whyLine = deriveWhyMatch(row);

  return (
    <article className="job-match-card job-match-row">
      <div className="job-match-col job-match-col--role">
        <span className="col-label">Candidate</span>
        <h3>{row.target_label}</h3>
      </div>
      <div className="job-match-col job-match-col--match">
        <span className="col-label">Match</span>
        <span className={`match-badge match-badge--pill ${tier.className}`}>{matchPercent(row.similarity)} match</span>
      </div>
      <div className="job-match-col job-match-col--why">
        <span className="col-label">Why they match</span>
        <p>{whyLine}</p>
      </div>
      <div className="job-match-col job-match-col--skills">
        <span className="col-label">Skills</span>
        {matched.length > 0 ? (
          <div className="signal-chips">
            {matched.slice(0, 4).map((s) => (
              <span key={s} className="signal-chip signal-chip--match">{s}</span>
            ))}
          </div>
        ) : (
          <span className="signal-chip signal-chip--empty">No direct overlap</span>
        )}
      </div>
      <div className="job-match-col job-match-col--actions">
        <span className="col-label">Actions</span>
        <div className="row-actions">
          <button type="button" className="row-action-btn" onClick={() => onViewDetails(row, whyLine)}>
            View details
          </button>
        </div>
      </div>
    </article>
  );
}

export default function EmployerCandidateResults({ response, error, jobTitle }) {
  const [search, setSearch] = useState("");
  const [minMatch, setMinMatch] = useState("0");
  const [drawer, setDrawer] = useState(null);

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
      <section className="portal-panel portal-panel--elevated portal-panel--empty">
        <EmptyState
          title="No candidates yet"
          description="Select a job and run a search to see ranked candidate matches."
          checklist={["Post a job with required skills", "Choose the role to match against", "Review ranked profiles"]}
          action={<Link to="/employer/jobs" className="btn-primary">Create a job</Link>}
          helperText="Matches rank profiles by skills overlap and experience fit."
        />
      </section>
    );
  }

  const good = (response.results || []).filter((r) => r.similarity >= 0.6).length;
  const top = response.results[0]?.similarity ?? 0;

  return (
    <>
      <section className="portal-panel portal-panel--elevated candidate-results">
        <ResultsDecor />
        <p className="auth-sub">
          Matches for <strong>{jobTitle || response.query_label}</strong> · {humanizeStrategy(response.strategy_used)}
        </p>
        <div className="match-summary-cards">
          <div className="summary-card">
            <span className="summary-value">{response.evaluated_count ?? response.results.length}</span>
            <span className="summary-label">Profiles reviewed</span>
          </div>
          <div className="summary-card summary-card--accent">
            <span className="summary-value">{good}</span>
            <span className="summary-label">{pluralGoodMatches(good)}</span>
          </div>
          <div className="summary-card">
            <span className="summary-value">{matchPercent(top)}</span>
            <span className="summary-label">Top match</span>
          </div>
        </div>
        <div className="results-filters">
          <input
            type="search"
            className="filter-search"
            placeholder="Search candidates…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <select className="filter-select" value={minMatch} onChange={(e) => setMinMatch(e.target.value)}>
            <option value="0">Any match</option>
            <option value="60">60%+ match</option>
            <option value="80">80%+ match</option>
          </select>
        </div>
        <div className="job-match-list">
          <div className="job-match-list-head" aria-hidden="true">
            <span>Candidate</span>
            <span>Match</span>
            <span>Why they match</span>
            <span>Skills</span>
            <span>Actions</span>
          </div>
          {filtered.length === 0 ? (
            <p className="auth-sub">No candidates match your current filters.</p>
          ) : (
            filtered.map((row) => (
              <CandidateMatchCard
                key={row.target_id}
                row={row}
                onViewDetails={(r, why) => setDrawer({ row: r, whyLine: why })}
              />
            ))
          )}
        </div>
      </section>
      {drawer && (
        <MatchDetailsDrawer
          row={drawer.row}
          whyLine={drawer.whyLine}
          subtitle="Candidate match details"
          onClose={() => setDrawer(null)}
        />
      )}
    </>
  );
}

export function EmployerNoJobsEmpty() {
  return (
    <section className="portal-panel portal-panel--elevated portal-panel--empty">
      <EmptyState
        title="No jobs posted yet"
        description="Create a job posting first, then we'll rank matching candidates."
        action={<Link to="/employer/jobs" className="btn-primary">Create a job</Link>}
        helperText="Add required skills and experience to improve match quality."
      />
    </section>
  );
}
