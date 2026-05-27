import { useEffect, useMemo, useRef, useState } from "react";
import {
  formatCandidateMatchScore,
  formatRefreshedAt,
  isApplyAvailable,
  matchTier,
  matchDisplayScore,
  matchScoreValue,
  pluralGoodMatches,
} from "../utils/format.js";
import {
  collectSkillOptions,
  createMatchFilters,
  filterAndSortMatchRows,
} from "../utils/matchFilters.js";
import { fetchMyApplications, fetchMyFeedback, recordFeedbackAction, apiErrorMessage } from "../api/client.js";
import { buildFeedbackMaps } from "../utils/feedbackState.js";
import { IconAlert } from "./icons.jsx";
import ResultsPanel from "./ResultsPanel.jsx";
import MatchExplainability from "./MatchExplainability.jsx";
import MatchResultsFilters from "./MatchResultsFilters.jsx";
import { NoMatchingRolesEmpty } from "./EmptyState.jsx";
import MatchDetailsDrawer from "./MatchDetailsDrawer.jsx";
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

function ApplyAction({ row, applied, onApply, disabled = false }) {
  if (applied) {
    return <span className="row-action-status">Applied</span>;
  }
  if (!isApplyAvailable(row)) {
    return <span className="row-action-status">Apply unavailable</span>;
  }
  return (
    <button type="button" className="row-action-btn row-action-btn--pill row-action-btn--primary" onClick={onApply} disabled={disabled}>
      Apply
    </button>
  );
}

function JobMatchCard({ row, onViewDetails, saved, applied, notInterested, onSave, onDismiss, onApply, pendingAction }) {
  const tier = matchTier(matchScoreValue(row));
  const busy = Boolean(pendingAction);

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
            {matchDisplayScore(row)}
          </span>
          <span className={`match-tier-pill ${tier.className}`}>{tier.label}</span>
        </div>
      </div>
      <div className="job-match-col job-match-col--actions">
        <span className="col-label">Actions</span>
        <div className="row-actions row-actions--pills">
          <button type="button" className="row-action-btn row-action-btn--pill" onClick={() => onViewDetails(row)}>
            View details
          </button>
          <button type="button" className="row-action-btn row-action-btn--pill" onClick={() => onSave(row)} disabled={busy}>
            {saved ? "Unsave" : "Save"}
          </button>
          {notInterested ? (
            <span className="row-action-status row-action-status--muted">Not interested</span>
          ) : (
            <button
              type="button"
              className="row-action-btn row-action-btn--pill row-action-btn--ghost"
              onClick={() => onDismiss(row)}
              disabled={busy}
            >
              Not interested
            </button>
          )}
          <ApplyAction row={row} applied={applied} onApply={() => onApply(row)} disabled={busy} />
        </div>
      </div>
      <MatchExplainability row={row} variant="list" className="job-match-row__explain" />
    </article>
  );
}

export default function CandidateJobResults({ response, error, onRefresh, loading, updatedAt, onClearError }) {
  const { showToast } = useToast();
  const [filters, setFilters] = useState(createMatchFilters);
  const [drawer, setDrawer] = useState(null);
  const [savedIds, setSavedIds] = useState(new Set());
  const [appliedIds, setAppliedIds] = useState(new Set());
  const [dismissedIds, setDismissedIds] = useState(new Set());
  const [pendingAction, setPendingAction] = useState("");
  const filtersRef = useRef(null);
  const feedbackSessionRef = useRef(null);

  const runRowAction = async (key, fn) => {
    if (pendingAction) return;
    setPendingAction(key);
    try {
      await fn();
    } finally {
      setPendingAction("");
    }
  };

  const applyFeedbackState = (rows) => {
    const maps = buildFeedbackMaps(rows);
    setSavedIds(maps.saved);
    setAppliedIds(maps.applied);
    setDismissedIds(maps.notInterested);
  };

  useEffect(() => {
    setFilters(createMatchFilters());
  }, [response?.session_id]);

  useEffect(() => {
    const sessionId = response?.session_id;
    if (!sessionId) return undefined;
    feedbackSessionRef.current = sessionId;
    let cancelled = false;

    Promise.all([fetchMyFeedback(), fetchMyApplications()])
      .then(([feedback, apps]) => {
        if (cancelled || feedbackSessionRef.current !== sessionId) return;
        applyFeedbackState(feedback);
        setAppliedIds((prev) => {
          const next = new Set(prev);
          apps.forEach((a) => next.add(a.job_id));
          return next;
        });
      })
      .catch(() => {});

    return () => {
      cancelled = true;
    };
  }, [response?.session_id]);

  const skillOptions = useMemo(
    () => collectSkillOptions(response?.results || []),
    [response?.results],
  );

  const filtered = useMemo(
    () => filterAndSortMatchRows(response?.results || [], filters, "candidate-jobs"),
    [response?.results, filters],
  );

  const handleClearFilters = () => {
    setFilters(createMatchFilters());
    filtersRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    filtersRef.current?.querySelector(".filter-search")?.focus();
  };

  const toggleSave = async (row) => {
    const saving = !savedIds.has(row.target_id);
    const key = `save:${row.target_id}`;
    await runRowAction(key, async () => {
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
    });
  };

  const handleDismiss = async (row) => {
    if (dismissedIds.has(row.target_id)) return;
    const key = `dismiss:${row.target_id}`;
    await runRowAction(key, async () => {
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
    });
  };

  const handleApply = async (row) => {
    if (appliedIds.has(row.target_id) || !isApplyAvailable(row)) return;
    const key = `apply:${row.target_id}`;
    await runRowAction(key, async () => {
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
    });
  };

  if (!response) return null;

  const refreshing = loading && (response.results?.length ?? 0) > 0;
  const showSkeleton = loading && !response.results?.length;

  return (
    <>
      <ResultsPanel
        backgroundVariant="jobs"
        className={`candidate-results matches-card scroll-content${refreshing ? " results-panel--refreshing" : ""}`}
      >
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
        <div ref={filtersRef} className="matches-toolbar">
          <MatchResultsFilters
            variant="candidate-jobs"
            filters={filters}
            onChange={setFilters}
            onClear={handleClearFilters}
            skillOptions={skillOptions}
            onRefresh={onRefresh}
            loading={loading}
            refreshLabel="Refresh matches"
          />
        </div>
        <div className="job-match-list scroll-content">
          <div className="job-match-list-head" aria-hidden="true">
            <span>Role</span>
            <span>Match</span>
            <span>Actions</span>
          </div>
          {showSkeleton ? (
            <MatchSkeletonRows />
          ) : filtered.length === 0 ? (
            <NoMatchingRolesEmpty
              filteredOut={(response.results?.length ?? 0) > 0}
              action={
                <button type="button" className="btn-secondary" onClick={handleClearFilters}>
                  Clear all filters
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
                pendingAction={pendingAction.startsWith(`save:${row.target_id}`)
                  || pendingAction.startsWith(`dismiss:${row.target_id}`)
                  || pendingAction.startsWith(`apply:${row.target_id}`)}
                onViewDetails={(r) => setDrawer({ row: r })}
              />
            ))
          )}
        </div>
      </ResultsPanel>
      {drawer && (
        <MatchDetailsDrawer
          row={drawer.row}
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
