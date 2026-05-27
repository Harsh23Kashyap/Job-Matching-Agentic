import { useEffect, useState } from "react";
import PageHeader from "../../components/PageHeader.jsx";
import SystemConfigPanel from "../../components/SystemConfigPanel.jsx";
import AgentEventStrip from "../../components/AgentEventStrip.jsx";
import AgentStatusPanel from "../../components/AgentStatusPanel.jsx";
import MatchControls from "../../components/MatchControls.jsx";
import ResultsPanel from "../../components/ResultsPanel.jsx";
import { runDailyBatch, runMatch, fetchFairnessReport } from "../../api/client.js";

const RECENT_KEY = "jm_recent_runs";

function loadRecent() {
  try {
    return JSON.parse(localStorage.getItem(RECENT_KEY) || "[]");
  } catch {
    return [];
  }
}

export default function AdminConsole() {
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [recentRuns, setRecentRuns] = useState(loadRecent);
  const [fairness, setFairness] = useState(null);

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
    try {
      const data = await runMatch(config);
      setResponse(data);
      saveRecent(data);
    } catch (err) {
      setError(err.response?.data?.detail?.error || err.message);
      setResponse(null);
    } finally {
      setLoading(false);
    }
  };

  const handleDailyBatch = async (config) => {
    setLoading(true);
    setError(null);
    try {
      const data = await runDailyBatch(config);
      setResponse({
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
      });
    } catch (err) {
      setError(err.response?.data?.detail?.error || err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="admin-workspace">
      <PageHeader
        eyebrow="Admin"
        title="Match console"
        subtitle="Agent status, match settings, and result inspection."
      />

      <section className="admin-workspace-block">
        <p className="admin-workspace-label">System health</p>
        <AgentStatusPanel onConnectionChange={() => {}} />
        <SystemConfigPanel />
        <AgentEventStrip />
        {fairness && (
          <div className="portal-panel portal-panel--compact" style={{ marginTop: 12 }}>
            <p className="admin-workspace-label">Fairness baseline (proxy groups)</p>
            <p className="auth-sub">
              Experience DI ratio: {fairness.experience_disparate_impact?.toFixed(2) ?? "n/a"} · Remote DI ratio:{" "}
              {fairness.remote_disparate_impact?.toFixed(2) ?? "n/a"} · {fairness.queries_evaluated} queries
            </p>
          </div>
        )}
      </section>

      <section className="admin-workspace-block admin-workspace-block--controls">
        <p className="admin-workspace-label">Matching</p>
        <div className="admin-console-grid">
          <MatchControls onRun={handleRun} onDailyBatch={handleDailyBatch} loading={loading} />
          <ResultsPanel response={response} error={error} recentRuns={recentRuns} />
        </div>
      </section>
    </div>
  );
}
