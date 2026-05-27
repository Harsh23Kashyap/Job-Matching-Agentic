import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import EmployerCandidateResults, { EmployerNoJobsEmpty } from "../../components/EmployerCandidateResults.jsx";
import Button from "../../components/Button.jsx";
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
      <>
        <PageHeader title="Find candidates" subtitle="Post a job first, then we'll rank matching profiles." />
        <EmployerNoJobsEmpty />
      </>
    );
  }

  const jobTitle = jobs.find((j) => j.title === selected)?.title;

  return (
    <>
      <PageHeader
        title="Find candidates"
        subtitle="Select a role and discover top-matching profiles."
        inlineAction={
          <Button loading={loading} loadingLabel="Searching…" onClick={handleFind} disabled={!selected}>
            Find matching candidates
          </Button>
        }
      />
      <section className="portal-panel">
        <h2>Search by job</h2>
        <label className="form-field">
          <span className="field-label">Select job</span>
          <select value={selected} onChange={(e) => setSelected(e.target.value)}>
            <option value="">Choose a job…</option>
            {jobs.map((j) => (
              <option key={j.id} value={j.title}>
                {j.title}
              </option>
            ))}
          </select>
        </label>
      </section>
      <EmployerCandidateResults response={response} error={error} jobTitle={jobTitle} />
    </>
  );
}
