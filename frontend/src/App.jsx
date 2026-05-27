import { useEffect, useState } from "react";
import AgentStatusPanel from "./components/AgentStatusPanel.jsx";
import MatchControls from "./components/MatchControls.jsx";
import ResultsPanel from "./components/ResultsPanel.jsx";
import { runDailyBatch, runMatch } from "./api/client.js";

const RECENT_KEY = "jm_recent_runs";
const THEME_KEY = "jm_theme";

function loadRecent() {
  try {
    return JSON.parse(localStorage.getItem(RECENT_KEY) || "[]");
  } catch {
    return [];
  }
}

export default function App() {
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [recentRuns, setRecentRuns] = useState(loadRecent);
  const [theme, setTheme] = useState(() => localStorage.getItem(THEME_KEY) || "dark");

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem(THEME_KEY, theme);
  }, [theme]);

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
      setError(null);
      setResponse({
        query_label: "Daily batch",
        direction: "candidate_to_jobs",
        strategy_used: "batch",
        evaluated_count: data.users_processed,
        corpus_size: data.users_processed,
        results: [
          {
            target_id: "batch",
            target_label: `Wrote ${data.output_file}`,
            rank: 1,
            similarity: 1,
            semantic_score: 1,
            why_ranked: [`Processed ${data.users_processed} users at ${data.generated_at_utc}`],
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
    <div className="app">
      <header className="app-header">
        <div>
          <h1>Job Matching</h1>
          <p>Three-agent resume ↔ job matching (v1)</p>
        </div>
        <button type="button" className="theme-toggle" onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>
          {theme === "dark" ? "Light" : "Dark"}
        </button>
      </header>

      <main className="layout">
        <AgentStatusPanel />
        <MatchControls onRun={handleRun} onDailyBatch={handleDailyBatch} loading={loading} />
        <ResultsPanel response={response} error={error} recentRuns={recentRuns} />
      </main>
    </div>
  );
}
