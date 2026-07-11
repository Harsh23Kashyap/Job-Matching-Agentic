import { useEffect, useState } from "react";
import { fetchSystemConfig, resetDemoData, setVectorStore } from "../api/client.js";
import { copyToClipboard } from "../utils/copyToClipboard.js";
import Button from "./Button.jsx";
import FriendlyError from "./FriendlyError.jsx";
import { IconCopy } from "./icons.jsx";

function CopyRow({ label, value }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    const ok = await copyToClipboard(value);
    if (ok) {
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1500);
    }
  };

  return (
    <div className="admin-demo-copy-row">
      <span className="admin-demo-copy-row__label">{label}</span>
      <code className="admin-demo-copy-row__value">{value}</code>
      <button type="button" className="admin-copy-btn" onClick={handleCopy} aria-label={`Copy ${label}`}>
        <IconCopy size={14} />
        {copied ? "Copied" : "Copy"}
      </button>
    </div>
  );
}

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
        `Demo reset complete, ${result.candidates_loaded} candidates, ${result.jobs_loaded} jobs, `
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
      <div className="span-12 panel" id="admin-section-system">
        <p>{error ? <FriendlyError message={error} /> : "Loading system config…"}</p>
      </div>
    );
  }

  const demo = config.demo_accounts;
  const snapshot = config.demo_snapshot;

  const rows = [
    { label: "Vector store", value: config.vector_store },
    { label: "Embedding model", value: config.embedding_model },
    { label: "Read-only", value: config.read_only ? "Yes" : "No" },
    { label: "Demo mode", value: config.demo_mode ? "On" : "Off" },
  ];

  return (
    <section className="panel span-12 system-config-panel admin-system-panel" id="admin-section-system">
      <div className="panel-header">
        <h2>System configuration</h2>
      </div>
      <dl className="admin-kv-list">
        {rows.map((row) => (
          <div key={row.label} className="admin-kv-row">
            <dt>{row.label}</dt>
            <dd>{row.value}</dd>
          </div>
        ))}
      </dl>
      {config.read_only_note && (
        <p className="admin-system-note">{config.read_only_note}</p>
      )}
      {!config.read_only && (
        <div className="pill-group admin-vector-switch" style={{ marginTop: 12 }}>
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
        <div className="admin-demo-access-card">
          <h3>Demo access</h3>
          <p className="admin-demo-access-card__intro">
            Sample corpus and pre-seeded activity for live demos. Credentials are for localhost only.
          </p>
          {snapshot && (
            <p className="admin-demo-access-card__snapshot">
              Corpus: {snapshot.candidates_in_corpus} candidates · {snapshot.jobs_in_corpus} jobs ·{" "}
              {snapshot.saved_jobs} saved · {snapshot.applications} applied · {snapshot.employer_shortlist} shortlist
            </p>
          )}
          <div className="admin-demo-copy-list">
            <CopyRow label="Candidate" value={demo.candidate_email} />
            <CopyRow label="Employer" value={demo.employer_email} />
            <CopyRow label="Admin" value={demo.admin_email} />
            <CopyRow label="Password" value={demo.password} />
          </div>
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

      {error && <FriendlyError message={error} />}
    </section>
  );
}
