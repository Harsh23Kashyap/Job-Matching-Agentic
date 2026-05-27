import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import PortalSection from "../../components/PortalSection.jsx";
import EmployerCandidateResults, { EmployerNoJobsEmpty } from "../../components/EmployerCandidateResults.jsx";
import Button from "../../components/Button.jsx";
import { fetchMyJobs, runMatch } from "../../api/client.js";
import { matchPercent } from "../../utils/format.js";

export default function EmployerMatches() {
  const [jobs, setJobs] = useState([]);
  const [selected, setSelected] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchMyJobs().then(setJobs).catch(() => setJobs([]));
  }, []);

  useEffect(() => {
    if (jobs.length && !selected) setSelected(jobs[0].title);
  }, [jobs, selected]);

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

  const heroStats = useMemo(() => {
    if (!response?.results?.length) return [];
    const top = response.results[0]?.similarity ?? 0;
    return [
      { label: "Profiles reviewed", value: response.evaluated_count ?? response.results.length },
      { label: "Shortlist", value: response.results.length },
      { label: "Top match", value: matchPercent(top) },
    ];
  }, [response]);

  if (jobs.length === 0) {
    return (
      <>
        <PageHeader
          eyebrow="Employer"
          title="Find candidates"
          subtitle="Post a job first, then we'll rank matching profiles."
          inlineAction={
            <Link to="/employer/jobs" className="btn-primary">
              Create a job
            </Link>
          }
        />
        <EmployerNoJobsEmpty />
      </>
    );
  }

  const jobTitle = jobs.find((j) => j.title === selected)?.title;

  return (
    <>
      <PageHeader
        eyebrow="Employer"
        title="Find candidates"
        subtitle={selected ? `Ranking profiles against ${selected}.` : "Select a role to discover top-matching profiles."}
        stats={heroStats}
        inlineAction={
          <div className="hero-toolbar">
            <label className="hero-toolbar-field">
              <span className="field-label">Job</span>
              <select value={selected} onChange={(e) => setSelected(e.target.value)}>
                {jobs.map((j) => (
                  <option key={j.id} value={j.title}>
                    {j.title}
                  </option>
                ))}
              </select>
            </label>
            <Button loading={loading} loadingLabel="Searching…" onClick={handleFind} disabled={!selected}>
              Find matches
            </Button>
          </div>
        }
      />
      <EmployerCandidateResults response={response} error={error} jobTitle={jobTitle} />
    </>
  );
}
