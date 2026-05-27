import { IconAlert, IconEmpty, IconResults } from "./icons.jsx";

export default function ResultsPanel({ response, error, recentRuns }) {
  if (error) {
    return (
      <section className="panel span-7">
        <div className="panel-header">
          <IconResults size={18} />
          <h2>Match Results</h2>
        </div>
        <div className="alert-banner critical">
          <IconAlert />
          <span>{error}</span>
        </div>
      </section>
    );
  }

  if (!response) {
    return (
      <section className="panel span-7">
        <div className="panel-header">
          <IconResults size={18} />
          <h2>Match Results</h2>
        </div>
        <div className="empty-state">
          <IconEmpty />
          <h3>No results yet</h3>
          <p>Select a candidate or job and run a match to see ranked results.</p>
        </div>
        {recentRuns?.length > 0 && (
          <div className="recent-runs">
            <h3>Recent runs</h3>
            <ul className="recent-list">
              {recentRuns.map((run, i) => (
                <li key={i}>
                  <span>
                    {run.query_label} · {run.strategy_used}
                  </span>
                  <span>{run.results?.length || 0} hits</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </section>
    );
  }

  return (
    <section className="panel span-7">
      <div className="panel-header">
        <IconResults size={18} />
        <h2>Match Results</h2>
      </div>

      <div className="results-meta">
        <span>
          Query: <strong>{response.query_label}</strong>
        </span>
        <span>
          Direction: <strong>{response.direction.replace(/_/g, " ")}</strong>
        </span>
        <span>
          Strategy: <strong>{response.strategy_used}</strong>
        </span>
        <span>
          Evaluated: <strong>{response.evaluated_count}</strong> / {response.corpus_size}
        </span>
      </div>

      <div className="data-table-wrap">
        <table className="data-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Target</th>
              <th className="num">Score</th>
              <th className="num">Semantic</th>
              <th className="num">Skills</th>
              <th>Why ranked</th>
            </tr>
          </thead>
          <tbody>
            {response.results.map((row) => (
              <tr key={row.target_id}>
                <td className="rank-cell">{row.rank}</td>
                <td>
                  <strong>{row.target_label}</strong>
                  <div className="score-bar-wrap" style={{ marginTop: 6 }}>
                    <div className="score-bar-track">
                      <div className="score-bar-fill" style={{ width: `${Math.min(row.similarity * 100, 100)}%` }} />
                    </div>
                  </div>
                </td>
                <td className="num">{row.similarity.toFixed(4)}</td>
                <td className="num">{row.semantic_score.toFixed(3)}</td>
                <td className="num">{row.skills_score != null ? row.skills_score.toFixed(3) : "—"}</td>
                <td>
                  {row.why_ranked?.length > 0 ? (
                    <div className="why-tags">
                      {row.why_ranked.map((line, i) => (
                        <span key={i} className="why-tag">
                          {line}
                        </span>
                      ))}
                    </div>
                  ) : (
                    "—"
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
