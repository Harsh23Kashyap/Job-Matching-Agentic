import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import ResultsPanel from "../../components/ResultsPanel.jsx";
import { fetchMyJobs, runMatch } from "../../api/client.js";

export default function EmployerMatches() {
  const [jobs, setJobs] = useState([]);
  const [selected, setSelected] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchMyJobs().then(setJobs).catch(() => setJobs([]));
  }, []);

  const handleFind = async () => {
    if (!selected) return;
    setLoading(true);
    setError(null);
    try {
      const data = await runMatch({
        mode: "job_to_candidates",
        queryKey: selected,
        topK: 10,
        strategy: "semantic",
        metric: "cosine",
        skillsMode: "jaccard",
        semanticWeight: 0.7,
        ensemble: false,
      });
      setResponse(data);
    } catch (err) {
      setError(err.response?.data?.detail?.error || err.message);
      setResponse(null);
    } finally {
      setLoading(false);
    }
  };

  if (jobs.length === 0) {
    return (
      <section className="portal-panel span-12">
        <h2>Find candidates</h2>
        <p>Create a job posting first.</p>
        <Link to="/employer/jobs" className="btn-primary">Go to My jobs</Link>
      </section>
    );
  }

  return (
    <>
      <section className="portal-panel span-12">
        <h2>Find candidates</h2>
        <label>
          Select job
          <select value={selected} onChange={(e) => setSelected(e.target.value)}>
            <option value="">Choose a job…</option>
            {jobs.map((j) => (
              <option key={j.id} value={j.title}>
                {j.title}
              </option>
            ))}
          </select>
        </label>
        <button type="button" className="btn-primary" onClick={handleFind} disabled={!selected || loading}>
          {loading ? "Searching…" : "Find matching candidates"}
        </button>
      </section>
      <ResultsPanel response={response} error={error} recentRuns={[]} />
    </>
  );
}
