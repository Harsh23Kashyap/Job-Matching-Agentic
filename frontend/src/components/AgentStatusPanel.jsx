import { useEffect, useState } from "react";
import { fetchAgentStatus } from "../api/client.js";

const LABELS = {
  candidates: "Candidate Agent",
  employer: "Employer Agent",
  matchmaking: "Matchmaking Agent",
};

export default function AgentStatusPanel() {
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
        }
      } catch (err) {
        if (active) setError(err.message);
      }
    };
    load();
    const id = setInterval(load, 5000);
    return () => {
      active = false;
      clearInterval(id);
    };
  }, []);

  if (error) {
    return (
      <section className="panel agent-panel">
        <h2>Agent Status</h2>
        <p className="error">Backend unreachable: {error}</p>
      </section>
    );
  }

  if (!status) {
    return (
      <section className="panel agent-panel">
        <h2>Agent Status</h2>
        <p>Loading agents…</p>
      </section>
    );
  }

  return (
    <section className="panel agent-panel">
      <h2>Agent Status</h2>
      <div className="agent-grid">
        {Object.entries(status).map(([key, agent]) => (
          <article key={key} className="agent-card">
            <header>
              <strong>{LABELS[key] || agent.display_name}</strong>
              <span className={agent.healthy ? "badge ok" : "badge bad"}>
                {agent.healthy ? "healthy" : "degraded"}
              </span>
            </header>
            <dl>
              <div>
                <dt>Entities</dt>
                <dd>{agent.entity_count}</dd>
              </div>
              <div>
                <dt>Store version</dt>
                <dd>{agent.store_version}</dd>
              </div>
              <div>
                <dt>Vector store</dt>
                <dd>{agent.vector_store_backend}</dd>
              </div>
              <div>
                <dt>Last event</dt>
                <dd>{agent.last_event || "—"}</dd>
              </div>
            </dl>
          </article>
        ))}
      </div>
    </section>
  );
}
