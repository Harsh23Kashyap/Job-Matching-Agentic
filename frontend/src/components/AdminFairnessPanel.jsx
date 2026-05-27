function diBadge(ratio) {
  if (ratio == null || Number.isNaN(ratio)) return { label: "n/a", tone: "muted" };
  if (ratio >= 0.8) return { label: "Acceptable", tone: "healthy" };
  if (ratio >= 0.7) return { label: "Review", tone: "warning" };
  return { label: "Concern", tone: "error" };
}

export default function AdminFairnessPanel({ fairness }) {
  if (!fairness) return null;

  const exp = diBadge(fairness.experience_disparate_impact);
  const remote = diBadge(fairness.remote_disparate_impact);

  return (
    <section className="panel admin-fairness-panel" id="admin-section-fairness">
      <div className="panel-header">
        <h2>Fairness baseline</h2>
      </div>
      <p className="admin-fairness-panel__help">
        Tracks whether matching results are balanced across configured proxy groups.
      </p>
      <div className="admin-fairness-metrics">
        <div className="admin-fairness-metric">
          <span className="admin-fairness-metric__label">Experience DI</span>
          <span className="admin-fairness-metric__value">
            {fairness.experience_disparate_impact?.toFixed(2) ?? "n/a"}
          </span>
          <span className={`admin-status-pill admin-status-pill--${exp.tone}`}>{exp.label}</span>
        </div>
        <div className="admin-fairness-metric">
          <span className="admin-fairness-metric__label">Remote DI</span>
          <span className="admin-fairness-metric__value">
            {fairness.remote_disparate_impact?.toFixed(2) ?? "n/a"}
          </span>
          <span className={`admin-status-pill admin-status-pill--${remote.tone}`}>{remote.label}</span>
        </div>
        <div className="admin-fairness-metric admin-fairness-metric--meta">
          <span className="admin-fairness-metric__label">Queries evaluated</span>
          <span className="admin-fairness-metric__value">{fairness.queries_evaluated ?? "—"}</span>
        </div>
      </div>
    </section>
  );
}
