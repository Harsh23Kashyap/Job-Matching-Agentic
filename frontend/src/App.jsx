import { useEffect, useState } from "react";
import AgentStatusPanel from "./components/AgentStatusPanel.jsx";
import MatchControls from "./components/MatchControls.jsx";
import ResultsPanel from "./components/ResultsPanel.jsx";
import { IconMoon, IconSun, SystemDiagram } from "./components/icons.jsx";
import { runDailyBatch, runMatch } from "./api/client.js";
import "./App.css";

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
  const [theme, setTheme] = useState(() => localStorage.getItem(THEME_KEY) || "light");
  const [apiOnline, setApiOnline] = useState(null);

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
    <div className="app">
      <header className="app-header">
        <div className="header-brand">
          <div>
            <h1>Job Matching</h1>
            <p>Multi-agent talent intelligence</p>
          </div>
          <SystemDiagram />
        </div>
        <div className="header-actions">
          <span className={`api-pill ${apiOnline === true ? "online" : apiOnline === false ? "offline" : ""}`}>
            {apiOnline !== null && (
              <span className={`status-dot ${apiOnline ? "healthy" : "critical"}`} style={{ width: 6, height: 6 }} />
            )}
            {apiOnline === null ? "Connecting…" : apiOnline ? "API online" : "API offline"}
          </span>
          <button
            type="button"
            className="theme-toggle"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            aria-label={theme === "light" ? "Switch to dark mode" : "Switch to light mode"}
          >
            {theme === "light" ? <IconMoon /> : <IconSun />}
          </button>
        </div>
      </header>

      <main className="dashboard">
        <section className="page-intro span-12">
          <h2>Match Console</h2>
          <p>
            Monitor agent health, configure matching strategies, and review ranked results across the
            candidate and employer corpus.
          </p>
        </section>
        <AgentStatusPanel onConnectionChange={setApiOnline} />
        <MatchControls onRun={handleRun} onDailyBatch={handleDailyBatch} loading={loading} />
        <ResultsPanel response={response} error={error} recentRuns={recentRuns} />
      </main>
    </div>
  );
}
