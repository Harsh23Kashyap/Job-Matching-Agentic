import { useMemo, useState } from "react";
import { humanizeStrategy, matchPercent, matchTier, parseWhySignals } from "../utils/format.js";
import { IconAlert } from "./icons.jsx";

function MatchSummaryCards({ response }) {
  const results = response.results || [];
  const good = results.filter((r) => r.similarity >= 0.6).length;
  const top = results[0]?.similarity ?? 0;

  return (
    <div className="match-summary-cards">
      <div className="summary-card">
        <span className="summary-value">{response.evaluated_count ?? results.length}</span>
        <span className="summary-label">Roles reviewed</span>
      </div>
      <div className="summary-card">
        <span className="summary-value">{good}</span>
        <span className="summary-label">Good matches</span>
      </div>
      <div className="summary-card">
        <span className="summary-value">{matchPercent(top)}</span>
        <span className="summary-label">Top match</span>
      </div>
      <div className="summary-card">
        <span className="summary-value summary-value--text">{humanizeStrategy(response.strategy_used)}</span>
        <span className="summary-label">Matching method</span>
      </div>
    </div>
  );
}

function JobMatchCard({ row }) {
  const [open, setOpen] = useState(false);
  const tier = matchTier(row.similarity);
  const { matched, other } = parseWhySignals(row.why_ranked);

  return (
    <article className="job-match-card">
      <div className="job-match-card-head">
        <div>
          <h3>{row.target_label}</h3>
          <p>{tier.label} based on your profile and skills.</p>
        </div>
        <span className={`match-badge ${tier.className}`}>{matchPercent(row.similarity)} match</span>
      </div>
      {matched.length > 0 && (
        <div className="signal-group">
          <span className="signal-label">Matched signals</span>
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
          <p>Resume alignment: {matchPercent(row.semantic_score)}</p>
          <p>Overall rank: #{row.rank}</p>
        </div>
      )}
    </article>
  );
}

export default function CandidateJobResults({ response, error, onRefresh, loading }) {
  const [search, setSearch] = useState("");
  const [minMatch, setMinMatch] = useState("0");
  const [remoteOnly, setRemoteOnly] = useState(false);
  const [sort, setSort] = useState("best");

  const filtered = useMemo(() => {
    if (!response?.results) return [];
    let rows = [...response.results];
    if (search.trim()) {
      const q = search.toLowerCase();
      rows = rows.filter((r) => r.target_label.toLowerCase().includes(q));
    }
    const min = Number(minMatch) / 100;
    rows = rows.filter((r) => r.similarity >= min);
    if (remoteOnly) {
      rows = rows.filter((r) =>
        (r.why_ranked || []).some((line) => /remote/i.test(line)),
      );
    }
    if (sort === "best") rows.sort((a, b) => b.similarity - a.similarity);
    if (sort === "title") rows.sort((a, b) => a.target_label.localeCompare(b.target_label));
    return rows;
  }, [response, search, minMatch, remoteOnly, sort]);

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
    return null;
  }

  return (
    <section className="portal-panel candidate-results">
      <MatchSummaryCards response={response} />
      <div className="results-filters">
        <input
          type="search"
          placeholder="Search roles…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select value={minMatch} onChange={(e) => setMinMatch(e.target.value)}>
          <option value="0">Min match: Any</option>
          <option value="40">Min match: 40%+</option>
          <option value="60">Min match: 60%+</option>
          <option value="80">Min match: 80%+</option>
        </select>
        <select value={sort} onChange={(e) => setSort(e.target.value)}>
          <option value="best">Sort: Best match</option>
          <option value="title">Sort: Role title</option>
        </select>
        <label className="filter-toggle">
          <input type="checkbox" checked={remoteOnly} onChange={(e) => setRemoteOnly(e.target.checked)} />
          Remote only
        </label>
        <button type="button" className="btn-secondary" onClick={onRefresh} disabled={loading}>
          {loading ? "Refreshing…" : "Refresh matches"}
        </button>
      </div>
      <div className="job-match-list">
        {filtered.length === 0 ? (
          <p className="auth-sub">No roles match your current filters.</p>
        ) : (
          filtered.map((row) => <JobMatchCard key={row.target_id} row={row} />)
        )}
      </div>
    </section>
  );
}
