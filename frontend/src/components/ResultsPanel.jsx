export default function ResultsPanel({ response, error, recentRuns }) {
  if (error) {
    return (
      <section className="panel results-panel">
        <h2>Results</h2>
        <p className="error">{error}</p>
      </section>
    );
  }

  if (!response) {
    return (
      <section className="panel results-panel">
        <h2>Results</h2>
        <p>Select a query and run a match to see ranked results.</p>
        {recentRuns?.length > 0 && (
          <div className="recent-runs">
            <h3>Recent runs</h3>
            <ul>
              {recentRuns.map((run, i) => (
                <li key={i}>
                  {run.query_label} — {run.strategy_used} — {run.results?.length || 0} hits
                </li>
              ))}
            </ul>
          </div>
        )}
      </section>
    );
  }

  return (
    <section className="panel results-panel">
      <h2>Results</h2>
      <p className="meta">
        {response.query_label} · {response.direction.replace(/_/g, " ")} · {response.strategy_used} · evaluated{" "}
        {response.evaluated_count}/{response.corpus_size}
      </p>
      <ol className="results-list">
        {response.results.map((row) => (
          <li key={row.target_id} className="result-row">
            <div className="result-head">
              <span className="rank">#{row.rank}</span>
              <strong>{row.target_label}</strong>
              <span className="score">{row.similarity.toFixed(4)}</span>
            </div>
            <div className="sub-scores">
              semantic {row.semantic_score.toFixed(3)}
              {row.skills_score != null && <> · skills {row.skills_score.toFixed(3)}</>}
            </div>
            {row.why_ranked?.length > 0 && (
              <ul className="why">
                {row.why_ranked.map((line, i) => (
                  <li key={i}>{line}</li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ol>
    </section>
  );
}
