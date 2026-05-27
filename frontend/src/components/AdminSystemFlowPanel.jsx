import { useReducedMotion } from "../hooks/useReducedMotion.js";

const STEPS = [
  { id: "candidate", label: "Candidate ingest", key: "candidates", unit: "profiles" },
  { id: "employer", label: "Job indexing", key: "employer", unit: "jobs" },
  { id: "vector", label: "Vector store", key: "employer", unit: "embedded" },
  { id: "match", label: "Matchmaking", key: "matchmaking", unit: "sessions" },
  { id: "results", label: "Ranked output", key: null, unit: "top-K" },
];

export default function AdminSystemFlowPanel({ status }) {
  const reducedMotion = useReducedMotion();

  return (
    <aside className="admin-system-flow panel" aria-label="System flow">
      <div className="admin-system-flow__head">
        <h3>System flow</h3>
        <p>Candidate → embed → vector store → match</p>
      </div>

      <svg className="admin-system-flow__svg" viewBox="0 0 240 360" fill="none" aria-hidden="true">
        <defs>
          <linearGradient id="adminFlowLine" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="rgba(148,163,184,0.08)" />
            <stop offset="100%" stopColor="rgba(132,170,145,0.18)" />
          </linearGradient>
        </defs>
        <line x1="120" y1="36" x2="120" y2="324" stroke="url(#adminFlowLine)" strokeWidth="1.5" />
        {[36, 108, 180, 252, 324].map((y, i) => (
          <g key={y}>
            <circle cx="120" cy={y} r="14" stroke="rgba(255,255,255,0.08)" strokeWidth="1" fill="#1b222b" />
            <circle cx="120" cy={y} r="4" fill="rgba(132,170,145,0.55)" />
            {i < 4 && !reducedMotion && (
              <circle r="2.5" fill="rgba(132,170,145,0.22)">
                <animateMotion dur={`${3.2 + i * 0.4}s`} repeatCount="indefinite" path={`M120,${y + 18} L120,${[36, 108, 180, 252, 324][i + 1] - 18}`} />
              </circle>
            )}
          </g>
        ))}
      </svg>

      <ol className="admin-system-flow__steps">
        {STEPS.map((step, index) => {
          const agent = step.key ? status?.[step.key] : null;
          const metric = agent ? agent.entity_count : step.id === "results" ? "Top-K" : "—";
          const detail = agent
            ? `${metric} ${step.unit}`
            : step.id === "vector"
              ? status?.employer?.vector_store_backend || "Chroma"
              : "Explain + rank";

          return (
            <li key={step.id} className="admin-system-flow__step">
              <span className="admin-system-flow__index">{index + 1}</span>
              <span className="admin-system-flow__copy">
                <strong>{step.label}</strong>
                <span>{detail}</span>
              </span>
            </li>
          );
        })}
      </ol>

      <p className="admin-system-flow__footnote">
        Read-only matchmaking over versioned snapshots. Humans approve save, apply, and shortlist.
      </p>
    </aside>
  );
}
