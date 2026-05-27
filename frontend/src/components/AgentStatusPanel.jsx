import { useEffect, useState } from "react";
import { fetchAgentStatus } from "../api/client.js";
import { IconAgents } from "./icons.jsx";

const CARD_CLASS = {
  candidates: "kpi-card--candidates",
  employer: "kpi-card--employer",
  matchmaking: "kpi-card--matchmaking",
};

const LABELS = {
  candidates: "Candidate Agent",
  employer: "Employer Agent",
  matchmaking: "Matchmaking Agent",
};

const UNITS = {
  candidates: "profiles",
  employer: "jobs",
  matchmaking: "sessions",
};

export default function AgentStatusPanel({ onConnectionChange }) {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;
    const load = async () => {
      try {
        const data = await fetchAgentStatus();
        if (active) {
          setStatus(data);
          setError(null);
          onConnectionChange?.(true);
        }
      } catch (err) {
        if (active) {
          const code = err.response?.status;
          if (code === 404) {
            setError("Start the API on port 8001 (see README).");
          } else {
            setError(err.message || "Connection failed");
          }
          onConnectionChange?.(false);
        }
      }
    };
    load();
    const id = setInterval(load, 5000);
    return () => {
      active = false;
      clearInterval(id);
    };
  }, [onConnectionChange]);

  if (error) {
    return (
      <div className="span-12">
        <div className="alert-banner critical">
          <span>Backend offline</span>
          <span>{error}</span>
        </div>
      </div>
    );
  }

  if (!status) {
    return (
      <div className="span-12 kpi-grid">
        {[1, 2, 3].map((i) => (
          <div key={i} className="skeleton" />
        ))}
      </div>
    );
  }

  return (
    <div className="span-12">
      <div className="panel-header">
        <IconAgents size={18} />
        <h2>Agent Status</h2>
      </div>
      <div className="kpi-grid">
        {Object.entries(status).map(([key, agent]) => (
          <article key={key} className={`kpi-card ${CARD_CLASS[key] || ""}`}>
            <div className="kpi-card-head">
              <span className="kpi-label">{LABELS[key] || agent.display_name}</span>
              <span
                className={`status-dot ${agent.healthy ? "healthy" : "critical"}`}
                title={agent.healthy ? "Healthy" : "Degraded"}
              />
            </div>
            <div className="kpi-value">
              {agent.entity_count}
              <span className="kpi-unit">{UNITS[key] || "items"}</span>
            </div>
            <dl className="kpi-meta">
              <div>
                <dt>Store ver.</dt>
                <dd>{agent.store_version}</dd>
              </div>
              <div>
                <dt>Vector store</dt>
                <dd>{agent.vector_store_backend}</dd>
              </div>
              <div style={{ gridColumn: "1 / -1" }}>
                <dt>Last event</dt>
                <dd>{agent.last_event || "—"}</dd>
              </div>
            </dl>
          </article>
        ))}
      </div>
    </div>
  );
}
