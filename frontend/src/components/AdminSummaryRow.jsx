function systemStatusLabel(status, backendError) {
  if (backendError) return { label: "Offline", tone: "error" };
  if (!status) return { label: "Loading", tone: "idle" };
  const agents = Object.values(status);
  if (agents.every((a) => a.healthy)) return { label: "Healthy", tone: "healthy" };
  if (agents.some((a) => !a.healthy)) return { label: "Degraded", tone: "warning" };
  return { label: "Idle", tone: "idle" };
}

export default function AdminSummaryRow({ status, backendError }) {
  if (!status && !backendError) {
    return (
      <div className="admin-summary-row">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="admin-stat-card skeleton" />
        ))}
      </div>
    );
  }

  const profiles = status?.candidates?.entity_count ?? ": ";
  const jobs = status?.employer?.entity_count ?? ": ";
  const sessions = status?.matchmaking?.entity_count ?? ": ";
  const sys = systemStatusLabel(status, backendError);

  const cards = [
    { label: "Profiles indexed", value: profiles },
    { label: "Jobs indexed", value: jobs },
    { label: "Match sessions", value: sessions },
    { label: "System status", value: sys.label, tone: sys.tone, isStatus: true },
  ];

  return (
    <div className="admin-summary-row">
      {cards.map((card) => (
        <article
          key={card.label}
          className={`admin-stat-card${card.isStatus ? ` admin-stat-card--${card.tone}` : ""}`}
        >
          <p className="admin-stat-card__label">{card.label}</p>
          <p className="admin-stat-card__value">{card.value}</p>
        </article>
      ))}
    </div>
  );
}
