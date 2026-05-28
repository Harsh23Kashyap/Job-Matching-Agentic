import { useEffect, useState } from "react";
import BackgroundOrnaments from "../../components/BackgroundOrnaments.jsx";
import PageHeader from "../../components/PageHeader.jsx";
import AdminSectionNav from "../../components/AdminSectionNav.jsx";
import AdminSummaryRow from "../../components/AdminSummaryRow.jsx";
import SystemConfigPanel from "../../components/SystemConfigPanel.jsx";
import AgentEventStrip from "../../components/AgentEventStrip.jsx";
import AgentStatusPanel from "../../components/AgentStatusPanel.jsx";
import MatchControls from "../../components/MatchControls.jsx";
import AdminMatchResults from "../../components/AdminMatchResults.jsx";
import AdminFairnessPanel from "../../components/AdminFairnessPanel.jsx";
import AdminLiveJobsPanel from "../../components/AdminLiveJobsPanel.jsx";
import AdminSystemFlowPanel from "../../components/AdminSystemFlowPanel.jsx";
import { runDailyBatch, runMatch, fetchFairnessReport } from "../../api/client.js";
import { useAgentStatus } from "../../hooks/useAgentStatus.js";

const RECENT_KEY = "jm_recent_runs";

function loadRecent() {
  try {
    return JSON.parse(localStorage.getItem(RECENT_KEY) || "[]");
  } catch {
    return [];
  }
}

function runLabel(config, response) {
  if (response?.strategy_used === "batch") return "Daily batch";
  const parts = [response?.strategy_used || config.strategy, config.metric].filter(Boolean);
  const title = parts.map((p) => p.charAt(0).toUpperCase() + p.slice(1)).join(" + ");
  return title || "Match";
}

export default function AdminConsole() {
  const { status, error: statusError, lastRefreshed, refreshing, refresh } = useAgentStatus();
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [recentRuns, setRecentRuns] = useState(loadRecent);
  const [fairness, setFairness] = useState(null);
  const [lastRun, setLastRun] = useState(null);

  useEffect(() => {
    fetchFairnessReport().then(setFairness).catch(() => setFairness(null));
  }, []);

  const saveRecent = (data) => {
    const next = [data, ...recentRuns].slice(0, 10);
    setRecentRuns(next);
    localStorage.setItem(RECENT_KEY, JSON.stringify(next));
  };

  const handleRun = async (config) => {
    setLoading(true);
    setError(null);
    const t0 = performance.now();
    try {
      const data = await runMatch(config);
      setResponse(data);
      saveRecent(data);
      setLastRun({
        resultCount: data.results?.length ?? 0,
        ms: Math.round(performance.now() - t0),
        label: runLabel(config, data),
      });
    } catch (err) {
      setError(err.response?.data?.detail?.error || err.message);
      setResponse(null);
      setLastRun(null);
    } finally {
      setLoading(false);
    }
  };

  const handleDailyBatch = async (config) => {
    setLoading(true);
    setError(null);
    const t0 = performance.now();
    try {
      const data = await runDailyBatch(config);
      const batchResponse = {
        query_label: "Daily batch",
        direction: "candidate_to_jobs",
        strategy_used: "batch",
        evaluated_count: data.users_processed,
        corpus_size: data.users_processed,
        results: [
          {
            target_id: "batch",
            target_label: data.output_file.split("/").pop(),
            rank: 1,
            similarity: 1,
            semantic_score: 1,
            skills_score: null,
            why_ranked: [`Processed ${data.users_processed} users`, data.generated_at_utc],
          },
        ],
      };
      setResponse(batchResponse);
      setLastRun({
        resultCount: data.users_processed,
        ms: Math.round(performance.now() - t0),
        label: "Daily batch",
      });
    } catch (err) {
      setError(err.response?.data?.detail?.error || err.message);
      setLastRun(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="admin-workspace admin-workspace--console">
      <BackgroundOrnaments variant="admin" scope="page" />
      <div className="admin-console-shell">
        <div className="admin-console-main">
          <PageHeader
            eyebrow="Admin"
            title="Operations console"
            subtitle="Health, configuration, matching controls, and result preview."
          />
          <AdminSectionNav />

          <section className="admin-workspace-block" id="admin-section-health">
            <div className="admin-block-head">
              <p className="admin-workspace-label">Dashboard</p>
              {lastRefreshed && (
                <span className="admin-event-refresh">
                  {refreshing && <span className="admin-live-dot admin-live-dot--pulse" aria-hidden="true" />}
                  Agents refreshed {Math.max(0, Math.round((Date.now() - lastRefreshed.getTime()) / 1000))}s ago
                  <button type="button" className="admin-inline-refresh" onClick={refresh}>
                    Refresh
                  </button>
                </span>
              )}
            </div>
            <AdminSummaryRow status={status} backendError={statusError} />
            <AgentStatusPanel status={status} error={statusError} loading={!status && !statusError} />
          </section>

          <section className="admin-workspace-block">
            <SystemConfigPanel />
            <AdminLiveJobsPanel onSynced={refresh} />
            <AgentEventStrip />
            <AdminFairnessPanel fairness={fairness} />
          </section>

          <section className="admin-workspace-block admin-workspace-block--controls" id="admin-section-matching">
            <p className="admin-workspace-label">Matching</p>
            <div className="admin-match-split">
              <MatchControls
                onRun={handleRun}
                onDailyBatch={handleDailyBatch}
                loading={loading}
                lastRun={lastRun}
              />
              <AdminMatchResults
                response={response}
                error={error}
                recentRuns={recentRuns}
                lastRun={lastRun}
              />
            </div>
          </section>
        </div>

        <AdminSystemFlowPanel status={status} />
      </div>
    </div>
  );
}
