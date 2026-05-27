import { useEffect, useMemo, useRef, useState } from "react";
import {
  deriveWhyMatch,
  formatCandidateMatchScore,
  formatRefreshedAt,
  isApplyAvailable,
  matchSkills,
  matchTier,
  matchDisplayScore,
  matchScoreValue,
  pluralGoodMatches,
} from "../utils/format.js";
import { fetchMyApplications, fetchMyFeedback, recordFeedbackAction, apiErrorMessage } from "../api/client.js";
import { buildFeedbackMaps } from "../utils/feedbackState.js";
import { IconAlert } from "./icons.jsx";
import ResultsPanel from "./ResultsPanel.jsx";
import SkillChip, { SkillChipList } from "./SkillChip.jsx";
import { NoMatchingRolesEmpty } from "./EmptyState.jsx";
import MatchDetailsDrawer from "./MatchDetailsDrawer.jsx";
import Button from "./Button.jsx";
import { useToast } from "./Toast.jsx";

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
        <span className="summary-value">{formatCandidateMatchScore(top)}</span>
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

function ApplyAction({ row, applied, onApply }) {
  if (applied) {
    return <span className="row-action-status">Applied</span>;
  }
  if (!isApplyAvailable(row)) {
    return <span className="row-action-status">Apply unavailable</span>;
  }
  return (
    <button type="button" className="row-action-btn" onClick={onApply}>
      Apply
    </button>
  );
}

function JobMatchCard({ row, onViewDetails, saved, applied, notInterested, onSave, onDismiss, onApply }) {
  const tier = matchTier(matchScoreValue(row));
  const { matched } = matchSkills(row);
  const whyLine = deriveWhyMatch(row);

  return (
    <article className={`portal-card job-match-card job-match-row${notInterested ? " job-match-row--muted" : ""}`}>
      <div className="job-match-col job-match-col--role">
        <span className="col-label">Role</span>
        <h3>{row.target_label}</h3>
      </div>
      <div className="job-match-col job-match-col--match">
        <span className="col-label">Match</span>
        <div className="match-pill-stack">
          <span className={`match-badge match-badge--pill ${tier.className}`}>
            {matchDisplayScore(row)} match
          </span>
          <span className={`match-tier-pill ${tier.className}`}>{tier.label}</span>
        </div>
      </div>
      <div className="job-match-col job-match-col--why">
        <span className="col-label">Why it matches</span>
        <p className="job-match-why">{whyLine}</p>
      </div>
      <div className="job-match-col job-match-col--skills">
        <span className="col-label">Skills</span>
        {matched.length > 0 ? (
          <SkillChipList skills={matched} limit={4} />
        ) : (
          <SkillChip variant="empty">No direct overlap</SkillChip>
        )}
      </div>
      <div className="job-match-col job-match-col--actions">
        <span className="col-label">Actions</span>
        <div className="row-actions">
          <button type="button" className="row-action-btn" onClick={() => onViewDetails(row, whyLine)}>
            View details
          </button>
          <button type="button" className="row-action-btn" onClick={() => onSave(row)}>
            {saved ? "Unsave" : "Save"}
          </button>
          {notInterested ? (
            <span className="row-action-status row-action-status--muted">Not interested</span>
          ) : (
            <button type="button" className="row-action-btn row-action-btn--ghost" onClick={() => onDismiss(row)}>
              Not interested
            </button>
          )}
          <ApplyAction row={row} applied={applied} onApply={() => onApply(row)} />
        </div>
      </div>
    </article>
  );
}

export default function CandidateJobResults({ response, error, onRefresh, loading, updatedAt, onClearError }) {
  const { showToast } = useToast();
  const [search, setSearch] = useState("");
  const [minMatch, setMinMatch] = useState("0");
  const [remoteOnly, setRemoteOnly] = useState(false);
  const [sort, setSort] = useState("best");
  const [drawer, setDrawer] = useState(null);
  const [savedIds, setSavedIds] = useState(new Set());
  const [appliedIds, setAppliedIds] = useState(new Set());
  const [dismissedIds, setDismissedIds] = useState(new Set());
  const filtersRef = useRef(null);

  const applyFeedbackState = (rows) => {
    const maps = buildFeedbackMaps(rows);
    setSavedIds(maps.saved);
    setAppliedIds(maps.applied);
    setDismissedIds(maps.notInterested);
  };

  useEffect(() => {
    Promise.all([fetchMyFeedback(), fetchMyApplications()])
      .then(([feedback, apps]) => {
        applyFeedbackState(feedback);
        setAppliedIds((prev) => {
          const next = new Set(prev);
          apps.forEach((a) => next.add(a.job_id));
          return next;
        });
      })
      .catch(() => {});
  }, [response?.session_id]);

  const toggleSave = async (row) => {
    const saving = !savedIds.has(row.target_id);
    try {
      await recordFeedbackAction({
        targetId: row.target_id,
        action: saving ? "save" : "unsave",
        targetLabel: row.target_label,
      });
      setSavedIds((prev) => {
        const next = new Set(prev);
        if (saving) next.add(row.target_id);
        else next.delete(row.target_id);
        return next;
      });
      showToast(
        saving ? `Saved ${row.target_label} to your list.` : `Removed ${row.target_label} from saved.`,
      );
    } catch (err) {
      showToast(apiErrorMessage(err, "Could not update saved jobs. Try again."), "error");
    }
  };

  const handleDismiss = async (row) => {
    if (dismissedIds.has(row.target_id)) return;
    try {
      await recordFeedbackAction({
        targetId: row.target_id,
        action: "not_interested",
        targetLabel: row.target_label,
      });
      setDismissedIds((prev) => new Set(prev).add(row.target_id));
      showToast(`Marked ${row.target_label} as not interested.`);
    } catch (err) {
      showToast(apiErrorMessage(err, "Could not save your feedback. Try again."), "error");
    }
  };

  const handleApply = async (row) => {
    if (appliedIds.has(row.target_id) || !isApplyAvailable(row)) return;
    try {
      await recordFeedbackAction({
        targetId: row.target_id,
        action: "apply",
        targetLabel: row.target_label,
        matchScore: row.similarity,
      });
      setAppliedIds((prev) => new Set(prev).add(row.target_id));
      showToast(`Applied to ${row.target_label}.`);
    } catch (err) {
      showToast(apiErrorMessage(err, "Could not record your application. Try again."), "error");
    }
  };

  const handleAdjustFilters = () => {
    setSearch("");
    setMinMatch("0");
    setRemoteOnly(false);
    filtersRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    filtersRef.current?.querySelector(".filter-search")?.focus();
  };

  const filtered = useMemo(() => {
    if (!response?.results) return [];
    const listOrder = new Map(response.results.map((row, index) => [row.target_id, index]));
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
    if (sort === "best") {
      rows.sort((a, b) => b.similarity - a.similarity);
    } else if (sort === "title") {
      rows.sort((a, b) => a.target_label.localeCompare(b.target_label));
    } else if (sort === "recent") {
      rows.sort((a, b) => (listOrder.get(b.target_id) ?? 0) - (listOrder.get(a.target_id) ?? 0));
    }
    return rows;
  }, [response, search, minMatch, remoteOnly, sort]);

  if (!response) return null;

  return (
    <>
      <ResultsPanel backgroundVariant="jobs" className="candidate-results">
        {error && (
          <div className="notice-warning match-error-banner">
            <IconAlert />
            <span>{error}</span>
            {onClearError && (
              <button type="button" className="row-action-btn match-error-dismiss" onClick={onClearError}>
                Dismiss
              </button>
            )}
          </div>
        )}
        <MatchSummaryCards response={response} updatedAt={updatedAt} />
        <div className="results-filters" ref={filtersRef}>
          <input
            type="search"
            className="filter-search"
            placeholder="Search roles…"
            aria-label="Search roles"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <label className={`filter-pill${remoteOnly ? " filter-pill--active" : ""}`}>
            <input
              type="checkbox"
              className="visually-hidden"
              checked={remoteOnly}
              onChange={(e) => setRemoteOnly(e.target.checked)}
            />
            Remote only
          </label>
          <select className="filter-select" value={minMatch} onChange={(e) => setMinMatch(e.target.value)} aria-label="Minimum match">
            <option value="0">Any match</option>
            <option value="50">50%+</option>
            <option value="60">60%+</option>
            <option value="70">70%+</option>
            <option value="80">80%+</option>
          </select>
          <select className="filter-select" value={sort} onChange={(e) => setSort(e.target.value)} aria-label="Sort results">
            <option value="best">Best match</option>
            <option value="title">Role title</option>
            <option value="recent">Recently added</option>
          </select>
          <Button
            className="btn-secondary filter-refresh"
            loading={loading}
            loadingLabel="Refreshing…"
            onClick={onRefresh}
          >
            Refresh
          </Button>
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
            <NoMatchingRolesEmpty
              filteredOut={(response.results?.length ?? 0) > 0}
              action={
                <button type="button" className="btn-secondary" onClick={handleAdjustFilters}>
                  Adjust filters
                </button>
              }
            />
          ) : (
            filtered.map((row) => (
              <JobMatchCard
                key={row.target_id}
                row={row}
                saved={savedIds.has(row.target_id)}
                applied={appliedIds.has(row.target_id)}
                notInterested={dismissedIds.has(row.target_id)}
                onSave={toggleSave}
                onDismiss={handleDismiss}
                onApply={handleApply}
                onViewDetails={(r, why) => setDrawer({ row: r, whyLine: why })}
              />
            ))
          )}
        </div>
      </ResultsPanel>
      {drawer && (
        <MatchDetailsDrawer
          row={drawer.row}
          whyLine={drawer.whyLine}
          variant="candidate"
          matchContext={{
            evaluated_count: response.evaluated_count,
            corpus_size: response.corpus_size,
            strategy_used: response.strategy_used,
            fusion_mode: response.fusion_mode,
          }}
          onClose={() => setDrawer(null)}
        />
      )}
    </>
  );
}
