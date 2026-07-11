import { IconBriefcase, IconMatch, IconProfile } from "./icons.jsx";
import FriendlyError from "./FriendlyError.jsx";

const CARD_META = {
  candidates: {
    label: "Candidate Agent",
    unit: "profiles indexed",
    icon: IconProfile,
  },
  employer: {
    label: "Employer Agent",
    unit: "jobs indexed",
    icon: IconBriefcase,
  },
  matchmaking: {
    label: "Matchmaking Agent",
    unit: "sessions",
    icon: IconMatch,
  },
};

function deriveHealth(agent, key) {
  if (!agent.healthy) return { tone: "error", label: "Error" };
  if (key === "matchmaking" && agent.entity_count === 0) return { tone: "idle", label: "Idle" };
  if ((key === "candidates" || key === "employer") && agent.entity_count === 0) {
    return { tone: "warning", label: "Warning" };
  }
  return { tone: "healthy", label: "Healthy" };
}

function formatLastEvent(raw) {
  if (!raw) return ": ";
  return raw.replace(/\./g, " · ");
}

export default function AgentStatusPanel({ status, error, loading }) {
  if (error) {
    return (
      <div className="span-12">
        <FriendlyError message={error} />
      </div>
    );
  }

  if (loading || !status) {
    return (
      <div className="span-12 kpi-grid">
        {[1, 2, 3].map((i) => (
          <div key={i} className="skeleton admin-agent-card-skeleton" />
        ))}
      </div>
    );
  }

  return (
    <div className="span-12 admin-agent-panel">
      <div className="admin-agent-panel__head">
        <div>
          <h2 className="admin-agent-panel__title">Agents</h2>
          <p className="admin-status-legend">
            <span className="admin-status-legend__item">
              <span className="admin-status-dot admin-status-dot--healthy" /> Healthy
            </span>
            <span className="admin-status-legend__item">
              <span className="admin-status-dot admin-status-dot--warning" /> Warning
            </span>
            <span className="admin-status-legend__item">
              <span className="admin-status-dot admin-status-dot--idle" /> Idle
            </span>
            <span className="admin-status-legend__item">
              <span className="admin-status-dot admin-status-dot--error" /> Error
            </span>
          </p>
        </div>
      </div>
      <div className="kpi-grid admin-agent-grid">
        {Object.entries(status).map(([key, agent]) => {
          const meta = CARD_META[key] || { label: agent.display_name, unit: "items", icon: IconMatch };
          const health = deriveHealth(agent, key);
          const Icon = meta.icon;
          return (
            <article key={key} className={`kpi-card admin-agent-card admin-agent-card--${health.tone}`}>
              <div className="admin-agent-card__head">
                <span className="admin-agent-card__icon" aria-hidden="true">
                  <Icon size={18} />
                </span>
                <div className="admin-agent-card__titles">
                  <span className="kpi-label">{meta.label}</span>
                  <span className={`admin-status-pill admin-status-pill--${health.tone}`}>{health.label}</span>
                </div>
              </div>
              <div className="admin-agent-card__metric">
                <span className="kpi-value">{agent.entity_count}</span>
                <span className="admin-agent-card__unit">{meta.unit}</span>
              </div>
              <dl className="kpi-meta admin-agent-card__meta">
                <div>
                  <dt>Store version</dt>
                  <dd>{agent.store_version}</dd>
                </div>
                <div>
                  <dt>Vector store</dt>
                  <dd>{agent.vector_store_backend}</dd>
                </div>
                <div style={{ gridColumn: "1 / -1" }}>
                  <dt>Last event</dt>
                  <dd>{formatLastEvent(agent.last_event)}</dd>
                </div>
              </dl>
            </article>
          );
        })}
      </div>
    </div>
  );
}
