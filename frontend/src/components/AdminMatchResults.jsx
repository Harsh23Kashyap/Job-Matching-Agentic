import FriendlyError from "./FriendlyError.jsx";
import { IconResults } from "./icons.jsx";

function formatStrategy(response) {
  if (!response) return "";
  const parts = [response.strategy_used, response.metric].filter(Boolean);
  return parts.join(" · ") || "Match";
}

export default function AdminMatchResults({ response, error, recentRuns = [], lastRun }) {
  const topResults = response?.results?.slice(0, 5) ?? [];

  return (
    <section className="panel admin-match-results" id="admin-section-results">
      <div className="panel-header">
        <IconResults size={18} />
        <h2>Match preview</h2>
      </div>

      {error && <FriendlyError message={error} />}

      {lastRun && !error && (
        <p className="admin-last-run">
          Last run: {lastRun.resultCount} results · {lastRun.ms}ms · {lastRun.label}
        </p>
      )}

      {response && !error && (
        <div className="admin-match-preview">
          <p className="admin-match-preview__query">
            <span className="admin-match-preview__label">Query</span>
            {response.query_label || "—"}
          </p>
          <p className="admin-match-preview__meta">
            {formatStrategy(response)} · {response.results?.length ?? 0} ranked · corpus {response.corpus_size ?? "—"}
          </p>
          {topResults.length > 0 ? (
            <ol className="admin-match-preview__list">
              {topResults.map((row) => (
                <li key={`${row.target_id}-${row.rank}`}>
                  <span className="admin-match-preview__rank">#{row.rank}</span>
                  <span className="admin-match-preview__title">{row.target_label || row.target_id}</span>
                  <span className="admin-match-preview__score">{(row.final_score ?? row.similarity)?.toFixed?.(3) ?? row.similarity}</span>
                </li>
              ))}
            </ol>
          ) : (
            <p className="panel-muted">No ranked results in this response.</p>
          )}
        </div>
      )}

      {!response && !error && (
        <p className="panel-muted">Run a match to preview ranked results here.</p>
      )}

      {recentRuns.length > 0 && (
        <div className="admin-recent-runs">
          <p className="control-section-title">Recent runs</p>
          <ul className="admin-recent-runs__list">
            {recentRuns.slice(0, 5).map((run, i) => (
              <li key={`${run.session_id || run.query_label}-${i}`}>
                <span>{run.query_label || "Match"}</span>
                <span className="admin-recent-runs__meta">
                  {run.results?.length ?? 0} results · {run.strategy_used || "—"}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}
