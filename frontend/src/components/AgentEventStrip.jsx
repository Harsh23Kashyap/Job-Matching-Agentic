import { useCallback, useEffect, useState } from "react";
import { fetchAgentEvents } from "../api/client.js";
import { formatRefreshAge, formatRelativeTime } from "../utils/formatRelativeTime.js";
import { IconRefresh } from "./icons.jsx";

const EVENT_COPY = {
  "candidate.profile.updated": {
    label: "Candidate agent updated a profile",
    role: "candidate",
    tone: "candidate",
  },
  "job.profile.updated": {
    label: "Employer agent indexed a job",
    role: "employer",
    tone: "employer",
  },
  "system.corpus.bootstrapped": {
    label: "System loaded demo corpus",
    role: "system",
    tone: "system",
  },
  "match.requested": {
    label: "Match requested",
    role: "matchmaking",
    tone: "matchmaking",
  },
  "match.completed": {
    label: "Match completed",
    role: "matchmaking",
    tone: "matchmaking",
  },
};

function eventMeta(event) {
  const mapped = EVENT_COPY[event.event_type];
  if (mapped) return mapped;
  const publisher = event.publisher_id || "system";
  let tone = "system";
  if (publisher.includes("candidate")) tone = "candidate";
  else if (publisher.includes("employer")) tone = "employer";
  else if (publisher.includes("match")) tone = "matchmaking";
  return {
    label: event.event_type?.replace(/\./g, " ") || "Event",
    role: publisher,
    tone,
  };
}

export default function AgentEventStrip() {
  const [events, setEvents] = useState([]);
  const [error, setError] = useState(null);
  const [lastRefreshed, setLastRefreshed] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const load = useCallback(async (manual = false) => {
    if (manual) setRefreshing(true);
    try {
      const data = await fetchAgentEvents();
      setEvents((data.events || []).slice(-12).reverse());
      setError(null);
      setLastRefreshed(new Date());
    } catch (err) {
      setError(err.message || "Could not load agent events");
    } finally {
      if (manual) setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, [load]);

  return (
    <section className="span-12 agent-event-strip panel" id="admin-section-activity">
      <div className="panel-head admin-event-head">
        <div>
          <h2>Agent activity</h2>
          <span className="panel-meta admin-event-refresh">
            {refreshing && <span className="admin-live-dot admin-live-dot--pulse" aria-hidden="true" />}
            Last refreshed {formatRefreshAge(lastRefreshed)} · live every 5s
          </span>
        </div>
        <button
          type="button"
          className="admin-refresh-btn"
          onClick={() => load(true)}
          disabled={refreshing}
          aria-label="Refresh activity"
        >
          <IconRefresh size={16} />
        </button>
      </div>
      {error ? (
        <p className="panel-error">{error}</p>
      ) : events.length === 0 ? (
        <p className="panel-muted">No recent events yet.</p>
      ) : (
        <ul className="agent-event-list">
          {events.map((event, index) => {
            const meta = eventMeta(event);
            return (
              <li key={`${event.timestamp}-${index}`} className="agent-event-item">
                <span className={`agent-event-dot agent-event-dot--${meta.tone}`} aria-hidden="true" />
                <span className="agent-event-time">{formatRelativeTime(event.timestamp)}</span>
                <span className="agent-event-type">{meta.label}</span>
                <span className={`agent-event-pill agent-event-pill--${meta.tone}`}>{meta.role}</span>
              </li>
            );
          })}
        </ul>
      )}
    </section>
  );
}
