import { useEffect, useState } from "react";
import { fetchAgentEvents } from "../api/client.js";

const EVENT_LABELS = {
  "candidate.profile.updated": "Candidate updated",
  "job.profile.updated": "Job updated",
  "system.corpus.bootstrapped": "Corpus loaded",
  "match.requested": "Match requested",
  "match.completed": "Match completed",
};

function formatTime(iso) {
  if (!iso) return "";
  try {
    return new Date(iso).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  } catch {
    return iso;
  }
}

export default function AgentEventStrip() {
  const [events, setEvents] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;
    const load = async () => {
      try {
        const data = await fetchAgentEvents();
        if (active) {
          setEvents((data.events || []).slice(-8).reverse());
          setError(null);
        }
      } catch (err) {
        if (active) {
          setError(err.message || "Could not load agent events");
        }
      }
    };
    load();
    const id = setInterval(load, 5000);
    return () => {
      active = false;
      clearInterval(id);
    };
  }, []);

  return (
    <section className="span-12 agent-event-strip panel">
      <div className="panel-head">
        <h2>Agent activity</h2>
        <span className="panel-meta">Last 8 events · refreshes every 5s</span>
      </div>
      {error ? (
        <p className="panel-error">{error}</p>
      ) : events.length === 0 ? (
        <p className="panel-muted">No recent events yet.</p>
      ) : (
        <ul className="agent-event-list">
          {events.map((event, index) => (
            <li key={`${event.timestamp}-${index}`} className="agent-event-item">
              <span className="agent-event-time">{formatTime(event.timestamp)}</span>
              <span className="agent-event-type">
                {EVENT_LABELS[event.event_type] || event.event_type}
              </span>
              <span className="agent-event-publisher">{event.publisher_id}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
