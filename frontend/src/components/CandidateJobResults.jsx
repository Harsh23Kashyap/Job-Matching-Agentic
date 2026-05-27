import { useEffect, useMemo, useState } from "react";
import { deriveWhyMatch, matchPercent, matchSkills, matchTier, pluralGoodMatches } from "../utils/format.js";
import { recordFeedback } from "../api/client.js";
import { IconAlert } from "./icons.jsx";
import { JobsResultsDecor } from "./PortalBackground.jsx";
import MatchDetailsDrawer from "./MatchDetailsDrawer.jsx";
import { useToast } from "./Toast.jsx";

const SAVED_JOBS_KEY = "jm_saved_jobs";

function loadSavedJobIds() {
  try {
    return new Set(JSON.parse(localStorage.getItem(SAVED_JOBS_KEY) || "[]"));
  } catch {
    return new Set();
  }
}

function formatRefreshedAt(iso) {
  if (!iso) return "Just now";
  const diff = Date.now() - new Date(iso).getTime();
  if (diff < 60000) return "Just now";
  const mins = Math.floor(diff / 60000);
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  return `${hrs}h ago`;
}

function MatchSummaryCards({ response, updatedAt }) {
  const results = response.results || [];
  const good = results.filter((r) => r.similarity >= 0.6).length;
  const top = results[0]?.similarity ?? 0;
  const reviewed = response.evaluated_count ?? results.length;

  return (
    <div className="match-summary-cards">
      <div className="summary-card">
        <span className="summary-value">{reviewed}</span>
        <span className="summary-label">Roles reviewed</span>
      </div>
      <div className="summary-card summary-card--accent">
        <span className="summary-value">{good}</span>
        <span className="summary-label">{pluralGoodMatches(good)}</span>
      </div>
      <div className="summary-card">
        <span className="summary-value">{matchPercent(top)}</span>
        <span className="summary-label">Top match</span>
      </div>
      <div className="summary-card">
        <span className="summary-value summary-value--text">{formatRefreshedAt(updatedAt)}</span>
        <span className="summary-label">Last updated</span>
      </div>
    </div>
  );
}

function MatchSkeletonRows() {
  return (
    <div className="match-skeleton-list" aria-hidden="true">
      {[1, 2, 3].map((i) => (
        <div key={i} className="match-skeleton-row">
          <span className="skeleton-block skeleton-block--lg" />
          <span className="skeleton-block skeleton-block--sm" />
          <span className="skeleton-block skeleton-block--md" />
        </div>
      ))}
    </div>
  );
}

function JobMatchCard({ row, onViewDetails, saved, onSave, onApply }) {
  const { showToast } = useToast();
  const tier = matchTier(row.similarity);
  const { matched } = matchSkills(row);
  const whyLine = deriveWhyMatch(row);

  const handleSave = () => {
    onSave(row);
    showToast(saved ? `Removed ${row.target_label} from saved.` : `Saved ${row.target_label} to your list.`);
  };

  const handleApply = () => {
    onApply(row);
    showToast(`Applied to ${row.target_label} — recorded for ranking feedback.`);
  };

  return (
    <article className="job-match-card job-match-row">
      <div className="job-match-col job-match-col--role">
        <span className="col-label">Role</span>
        <h3>{row.target_label}</h3>
      </div>
      <div className="job-match-col job-match-col--match">
        <span className="col-label">Match</span>
        <span className={`match-badge match-badge--pill ${tier.className}`}>{matchPercent(row.similarity)} match</span>
      </div>
      <div className="job-match-col job-match-col--why">
        <span className="col-label">Why it matches</span>
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
          <button type="button" className="row-action-btn" onClick={handleSave}>
            {saved ? "Unsave" : "Save"}
          </button>
          <button type="button" className="row-action-btn row-action-btn--muted" onClick={handleApply}>
            Apply
          </button>
        </div>
      </div>
    </article>
  );
}

export default function CandidateJobResults({ response, error, onRefresh, loading, updatedAt, candidateId }) {
  const [search, setSearch] = useState("");
  const [minMatch, setMinMatch] = useState("0");
  const [remoteOnly, setRemoteOnly] = useState(false);
  const [sort, setSort] = useState("best");
  const [drawer, setDrawer] = useState(null);
  const [savedIds, setSavedIds] = useState(loadSavedJobIds);

  useEffect(() => {
    localStorage.setItem(SAVED_JOBS_KEY, JSON.stringify([...savedIds]));
  }, [savedIds]);

  const toggleSave = (row) => {
    const saving = !savedIds.has(row.target_id);
    setSavedIds((prev) => {
      const next = new Set(prev);
      if (next.has(row.target_id)) next.delete(row.target_id);
      else next.add(row.target_id);
      return next;
    });
    if (candidateId && saving) {
      recordFeedback(candidateId, row.target_id, "save").catch(() => {});
    }
  };

  const handleApply = (row) => {
    if (candidateId) {
      recordFeedback(candidateId, row.target_id, "apply").catch(() => {});
    }
  };

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
      rows = rows.filter((r) => (r.why_ranked || []).some((line) => /remote/i.test(line)));
    }
    if (sort === "best") rows.sort((a, b) => b.similarity - a.similarity);
    if (sort === "title") rows.sort((a, b) => a.target_label.localeCompare(b.target_label));
    return rows;
  }, [response, search, minMatch, remoteOnly, sort]);

  if (error) {
    return (
      <section className="portal-panel portal-panel--elevated">
        <div className="notice-warning">
          <IconAlert />
          <span>{error}</span>
        </div>
      </section>
    );
  }

  if (!response) return null;

  return (
    <>
      <section className="portal-panel portal-panel--elevated candidate-results">
        <JobsResultsDecor />
        <MatchSummaryCards response={response} updatedAt={updatedAt} />
        <div className="results-filters">
          <input
            type="search"
            className="filter-search"
            placeholder="Search roles…"
            aria-label="Search roles"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <label className="filter-pill">
            <input type="checkbox" checked={remoteOnly} onChange={(e) => setRemoteOnly(e.target.checked)} />
            Remote only
          </label>
          <select className="filter-select" value={minMatch} onChange={(e) => setMinMatch(e.target.value)} aria-label="Minimum match">
            <option value="0">Any match</option>
            <option value="40">40%+ match</option>
            <option value="60">60%+ match</option>
            <option value="80">80%+ match</option>
          </select>
          <select className="filter-select" value={sort} onChange={(e) => setSort(e.target.value)} aria-label="Sort results">
            <option value="best">Best match</option>
            <option value="title">Role title</option>
          </select>
          <button type="button" className="btn-secondary filter-refresh" onClick={onRefresh} disabled={loading}>
            {loading ? "Refreshing matches…" : "Refresh"}
          </button>
        </div>
        <div className="job-match-list">
          <div className="job-match-list-head" aria-hidden="true">
            <span>Role</span>
            <span>Match</span>
            <span>Why it matches</span>
            <span>Skills</span>
            <span>Actions</span>
          </div>
          {loading ? (
            <MatchSkeletonRows />
          ) : filtered.length === 0 ? (
            <p className="auth-sub">No roles match your current filters.</p>
          ) : (
            filtered.map((row) => (
              <JobMatchCard
                key={row.target_id}
                row={row}
                saved={savedIds.has(row.target_id)}
                onSave={toggleSave}
                onApply={handleApply}
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
          onClose={() => setDrawer(null)}
        />
      )}
    </>
  );
}
