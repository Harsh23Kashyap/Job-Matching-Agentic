import { useEffect, useState } from "react";
import { fetchSystemConfig, resetDemoData, setVectorStore } from "../api/client.js";
import Button from "./Button.jsx";

export default function SystemConfigPanel() {
  const [config, setConfig] = useState(null);
  const [error, setError] = useState("");
  const [switching, setSwitching] = useState(false);
  const [resetting, setResetting] = useState(false);
  const [resetMessage, setResetMessage] = useState("");

  const load = () => {
    fetchSystemConfig()
      .then(setConfig)
      .catch((err) => setError(err.message || "Failed to load system config"));
  };

  useEffect(() => {
    load();
  }, []);

  const handleSwitch = async (backend) => {
    if (config?.read_only) return;
    setSwitching(true);
    setError("");
    try {
      await setVectorStore(backend);
      load();
    } catch (err) {
      setError(err.response?.data?.detail?.error || err.message);
    } finally {
      setSwitching(false);
    }
  };

  const handleResetDemo = async () => {
    if (!config?.demo_mode || config?.read_only) return;
    const confirmed = window.confirm(
      "Reset all demo data? This reloads sample candidates and jobs, clears demo activity, and re-seeds saved jobs and matches.",
    );
    if (!confirmed) return;
    setResetting(true);
    setError("");
    setResetMessage("");
    try {
      const result = await resetDemoData();
      setResetMessage(
        `Demo reset complete — ${result.candidates_loaded} candidates, ${result.jobs_loaded} jobs, `
        + `${result.saved_jobs} saved roles, ${result.applications} application(s), `
        + `${result.employer_shortlist} employer shortlist entries.`,
      );
      load();
    } catch (err) {
      setError(err.response?.data?.detail?.error || err.message);
    } finally {
      setResetting(false);
    }
  };

  if (!config) {
    return (
      <div className="span-12 panel">
        <p>{error || "Loading system config…"}</p>
      </div>
    );
  }

  const demo = config.demo_accounts;
  const snapshot = config.demo_snapshot;

  return (
    <section className="panel span-12 system-config-panel">
      <div className="panel-header">
        <h2>System</h2>
      </div>
      <dl className="system-config-grid">
        <div>
          <dt>Vector store</dt>
          <dd>{config.vector_store}</dd>
        </div>
        <div>
          <dt>Embedding model</dt>
          <dd>{config.embedding_model}</dd>
        </div>
        <div>
          <dt>Read-only</dt>
          <dd>{config.read_only ? "Yes" : "No"}</dd>
        </div>
        <div>
          <dt>Demo mode</dt>
          <dd>{config.demo_mode ? "On" : "Off"}</dd>
        </div>
        <div style={{ gridColumn: "1 / -1" }}>
          <dt>Note</dt>
          <dd>{config.read_only_note}</dd>
        </div>
      </dl>
      {!config.read_only && (
        <div className="pill-group" style={{ marginTop: 12 }}>
          {["chroma", "qdrant"].map((backend) => (
            <button
              key={backend}
              type="button"
              className={`pill-option ${config.vector_store === backend ? "active" : ""}`}
              disabled={switching || config.vector_store === backend}
              onClick={() => handleSwitch(backend)}
            >
              {backend}
            </button>
          ))}
        </div>
      )}

      {config.demo_mode && demo && (
        <div className="demo-data-panel">
          <h3>Demo data</h3>
          <p className="demo-data-panel__intro">
            Sample corpus, accounts, and pre-seeded activity for live demos. Log in with any demo account below.
          </p>
          <dl className="system-config-grid demo-data-grid">
            <div>
              <dt>Corpus</dt>
              <dd>
                {snapshot
                  ? `${snapshot.candidates_in_corpus} candidates · ${snapshot.jobs_in_corpus} jobs`
                  : "Loading…"}
              </dd>
            </div>
            <div>
              <dt>Sample activity</dt>
              <dd>
                {snapshot
                  ? `${snapshot.saved_jobs} saved · ${snapshot.applications} applied · ${snapshot.employer_shortlist} shortlist`
                  : "—"}
              </dd>
            </div>
            <div style={{ gridColumn: "1 / -1" }}>
              <dt>Accounts</dt>
              <dd className="demo-account-list">
                <span>Candidate: {demo.candidate_email}</span>
                <span>Employer: {demo.employer_email}</span>
                <span>Admin: {demo.admin_email}</span>
                <span>Password: {demo.password}</span>
              </dd>
            </div>
          </dl>
          {!config.read_only && (
            <div className="demo-data-panel__actions">
              <Button
                loading={resetting}
                loadingLabel="Resetting…"
                onClick={handleResetDemo}
                className="btn-secondary"
              >
                Reset demo data
              </Button>
            </div>
          )}
          {resetMessage && <p className="demo-data-panel__success">{resetMessage}</p>}
        </div>
      )}

      {error && <p className="auth-error">{error}</p>}
    </section>
  );
}
