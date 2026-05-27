import { useEffect, useState } from "react";
import { fetchSystemConfig, setVectorStore } from "../api/client.js";

export default function SystemConfigPanel() {
  const [config, setConfig] = useState(null);
  const [error, setError] = useState("");
  const [switching, setSwitching] = useState(false);

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

  if (!config) {
    return (
      <div className="span-12 panel">
        <p>{error || "Loading system config…"}</p>
      </div>
    );
  }

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
      {error && <p className="auth-error">{error}</p>}
    </section>
  );
}
