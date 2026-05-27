import { useEffect, useMemo, useRef, useState } from "react";
import { Link } from "react-router-dom";
import {
  candidateHasContact,
  countStrongMatches,
  formatCandidateMatchScore,
  formatRefreshedAt,
  matchTier,
  matchDisplayScore,
  matchScoreValue,
  pluralStrongMatches,
} from "../utils/format.js";
import { apiErrorMessage, fetchMyFeedback, recordFeedbackAction } from "../api/client.js";
import { buildFeedbackMaps } from "../utils/feedbackState.js";
import {
  collectSkillOptions,
  createMatchFilters,
  filterAndSortMatchRows,
} from "../utils/matchFilters.js";
import ResultsPanel from "./ResultsPanel.jsx";
import EmptyStatePanel from "./EmptyStatePanel.jsx";
import MatchExplainability from "./MatchExplainability.jsx";
import MatchResultsFilters from "./MatchResultsFilters.jsx";
import MatchDetailsDrawer from "./MatchDetailsDrawer.jsx";
import EmptyState, { EmployerNoCandidatesEmpty, EmployerCandidatesReadyEmpty } from "./EmptyState.jsx";
import { useToast } from "./Toast.jsx";
import { IconAlert } from "./icons.jsx";

function MatchSummaryCards({ response, refreshedAt }) {
  const results = response.results || [];
  const reviewed = response.evaluated_count ?? results.length;
  const strong = countStrongMatches(results);
  const top = results[0]?.similarity ?? 0;

  return (
    <div className="match-summary-cards">
      <div className="summary-card">
        <span className="summary-value">{reviewed}</span>
        <span className="summary-label">Candidates reviewed</span>
      </div>
      <div className="summary-card summary-card--accent">
        <span className="summary-value">{strong}</span>
        <span className="summary-label">{pluralStrongMatches(strong)}</span>
      </div>
      <div className="summary-card">
        <span className="summary-value">{formatCandidateMatchScore(top)}</span>
        <span className="summary-label">Top match</span>
      </div>
      <div className="summary-card">
        <span className="summary-value summary-value--text">{formatRefreshedAt(refreshedAt)}</span>
        <span className="summary-label">Last refreshed</span>
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

function EmployerCandidateCard({ row, saved, rejected, contacted, onViewProfile, onSave, onReject, onContact, pendingAction }) {
  const tier = matchTier(matchScoreValue(row));
  const busy = Boolean(pendingAction);

  return (
    <article className={`portal-card employer-candidate-card${rejected ? " employer-candidate-card--muted" : ""}`}>
      <div className="employer-candidate-card__head">
        <div className="employer-candidate-card__identity">
          <h3>{row.target_label}</h3>
          <div className="match-pill-stack">
            <span className={`match-badge match-badge--pill ${tier.className}`}>
              {matchDisplayScore(row)} match
            </span>
            <span className={`match-tier-pill ${tier.className}`}>{tier.label}</span>
          </div>
        </div>
      </div>

      <MatchExplainability row={row} variant="compact" className="employer-candidate-card__explain" />

      <div className="employer-candidate-card__actions">
        <button type="button" className="row-action-btn" onClick={() => onViewProfile(row)}>
          View profile
        </button>
        <button type="button" className="row-action-btn" onClick={() => onSave(row)} disabled={busy}>
          {saved ? "Saved" : "Save"}
        </button>
        {rejected ? (
          <span className="row-action-status row-action-status--muted">Rejected</span>
        ) : (
          <button type="button" className="row-action-btn row-action-btn--ghost" onClick={() => onReject(row)} disabled={busy}>
            Reject
          </button>
        )}
        <button type="button" className="row-action-btn" onClick={() => onContact(row)} disabled={busy}>
          {contacted ? "Contacted" : "Contact"}
        </button>
      </div>
    </article>
  );
}

export default function EmployerCandidateResults({
  response,
  error,
  jobTitle,
  jobId,
  loading,
  refreshedAt,
  onRefresh,
  onClearError,
}) {
  const { showToast } = useToast();
  const [filters, setFilters] = useState(createMatchFilters);
  const [drawer, setDrawer] = useState(null);
  const [savedIds, setSavedIds] = useState(new Set());
  const [rejectedIds, setRejectedIds] = useState(new Set());
  const [contactedIds, setContactedIds] = useState(new Set());
  const [pendingAction, setPendingAction] = useState("");
  const filtersRef = useRef(null);

  const runRowAction = async (key, fn) => {
    if (pendingAction) return;
    setPendingAction(key);
    try {
      await fn();
    } finally {
      setPendingAction("");
    }
  };

  useEffect(() => {
    setFilters(createMatchFilters());
  }, [response?.session_id, jobId]);

  useEffect(() => {
    if (!jobId) {
      setSavedIds(new Set());
      setRejectedIds(new Set());
      setContactedIds(new Set());
      return;
    }
    fetchMyFeedback(jobId)
      .then((rows) => {
        const maps = buildFeedbackMaps(rows, { contextId: jobId });
        setSavedIds(maps.saved);
        setRejectedIds(maps.rejected);
        setContactedIds(maps.contacted);
      })
      .catch(() => {});
  }, [response?.session_id, jobId]);

  const handleSave = async (row) => {
    if (!jobId) return;
    const saving = !savedIds.has(row.target_id);
    await runRowAction(`save:${row.target_id}`, async () => {
      try {
        await recordFeedbackAction({
          targetId: row.target_id,
          action: saving ? "save" : "unsave",
          contextId: jobId,
          targetLabel: row.target_label,
        });
        setSavedIds((prev) => {
          const next = new Set(prev);
          if (saving) next.add(row.target_id);
          else next.delete(row.target_id);
          return next;
        });
        showToast(saving ? `${row.target_label} saved to your shortlist.` : `${row.target_label} removed from saved.`);
      } catch (err) {
        showToast(apiErrorMessage(err, "Could not update saved candidates."), "error");
      }
    });
  };

  const handleReject = async (row) => {
    if (!jobId || rejectedIds.has(row.target_id)) return;
    await runRowAction(`reject:${row.target_id}`, async () => {
      try {
        await recordFeedbackAction({
          targetId: row.target_id,
          action: "reject",
          contextId: jobId,
          targetLabel: row.target_label,
        });
        setRejectedIds((prev) => new Set(prev).add(row.target_id));
        showToast(`${row.target_label} marked as rejected for this role.`);
      } catch (err) {
        showToast(apiErrorMessage(err, "Could not save your feedback. Try again."), "error");
      }
    });
  };

  const handleContact = async (row) => {
    if (!jobId) return;
    await runRowAction(`contact:${row.target_id}`, async () => {
      try {
        await recordFeedbackAction({
          targetId: row.target_id,
          action: "contact",
          contextId: jobId,
          targetLabel: row.target_label,
        });
        setContactedIds((prev) => new Set(prev).add(row.target_id));
      } catch (err) {
        showToast(apiErrorMessage(err, "Could not record contact feedback."), "error");
        return;
      }

      if (row.contact_email) {
        window.location.href = `mailto:${row.contact_email}`;
        return;
      }
      if (row.contact_phone) {
        window.location.href = `tel:${row.contact_phone}`;
        return;
      }
      if (candidateHasContact(row)) {
        setDrawer({ row });
        return;
      }
      showToast("No contact details on file. Open the profile for more context.", "info");
      setDrawer({ row });
    });
  };

  const skillOptions = useMemo(
    () => collectSkillOptions(response?.results || []),
    [response?.results],
  );

  const filtered = useMemo(
    () => filterAndSortMatchRows(response?.results || [], filters, "employer-candidates"),
    [response?.results, filters],
  );

  const handleClearFilters = () => {
    setFilters(createMatchFilters());
    filtersRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    filtersRef.current?.querySelector(".filter-search")?.focus();
  };

  if (error && !response) {
    return (
      <section className="portal-panel portal-panel--elevated">
        <div className="notice-warning match-error-banner">
          <IconAlert />
          <span>{error}</span>
        </div>
        <div className="empty-state-action" style={{ marginTop: 16 }}>
          <ButtonRefresh disabled={!jobTitle || loading} loading={loading} onRefresh={onRefresh} />
        </div>
      </section>
    );
  }

  if (!response) {
    return (
      <EmptyStatePanel>
        <EmployerCandidatesReadyEmpty
          jobTitle={jobTitle}
          action={
            <ButtonRefresh disabled={!jobTitle || loading} loading={loading} onRefresh={onRefresh} />
          }
        />
      </EmptyStatePanel>
    );
  }

  const refreshing = loading && (response.results?.length ?? 0) > 0;
  const showSkeleton = loading && !response.results?.length;

  return (
    <>
      <ResultsPanel
        backgroundVariant="employer-candidates"
        className={`candidate-results employer-candidate-results matches-card scroll-content${refreshing ? " results-panel--refreshing" : ""}`}
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
        <MatchSummaryCards response={response} refreshedAt={refreshedAt} />
        <div ref={filtersRef} className="matches-toolbar">
          <MatchResultsFilters
            variant="employer-candidates"
            filters={filters}
            onChange={setFilters}
            onClear={handleClearFilters}
            skillOptions={skillOptions}
            onRefresh={onRefresh}
            loading={loading}
            refreshLabel={response ? "Refresh matches" : "Find candidates"}
          />
        </div>
        <div className="employer-candidate-list scroll-content">
          {showSkeleton ? (
            <MatchSkeletonRows />
          ) : filtered.length === 0 ? (
            response.results?.length === 0 ? (
              <EmployerNoCandidatesEmpty
                action={
                  <button type="button" className="btn-secondary" onClick={onRefresh} disabled={loading}>
                    Refresh matches
                  </button>
                }
              />
            ) : (
              <EmployerNoCandidatesEmpty
                action={
                  <button type="button" className="btn-secondary" onClick={handleClearFilters}>
                    Clear all filters
                  </button>
                }
              />
            )
          ) : (
            filtered.map((row) => (
              <EmployerCandidateCard
                key={row.target_id}
                row={row}
                saved={savedIds.has(row.target_id)}
                rejected={rejectedIds.has(row.target_id)}
                contacted={contactedIds.has(row.target_id)}
                onViewProfile={(r) => setDrawer({ row: r })}
                onSave={handleSave}
                onReject={handleReject}
                onContact={handleContact}
                pendingAction={
                  pendingAction.startsWith(`save:${row.target_id}`)
                  || pendingAction.startsWith(`reject:${row.target_id}`)
                  || pendingAction.startsWith(`contact:${row.target_id}`)
                }
              />
            ))
          )}
        </div>
      </ResultsPanel>
      {drawer && (
        <MatchDetailsDrawer
          row={drawer.row}
          subtitle="Candidate match details"
          variant="employer"
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

function ButtonRefresh({ disabled, loading, onRefresh }) {
  return (
    <button type="button" className="btn-primary" onClick={onRefresh} disabled={disabled || loading}>
      {loading ? "Refreshing…" : "Refresh matches"}
    </button>
  );
}

export function EmployerNoJobsEmpty() {
  return (
    <EmptyStatePanel>
      <EmptyState
        title="No roles posted"
        description="Post a role first, then refresh matches to see ranked candidates."
        illustrationVariant="employer-jobs"
        checklist={["Post a role with required skills", "Set compensation and location", "Refresh matches for that role"]}
        checklistStyle="todo"
        action={<Link to="/employer/jobs" className="btn-primary">Post a role</Link>}
        helperText="Skills and experience on the posting drive match quality."
      />
    </EmptyStatePanel>
  );
}
