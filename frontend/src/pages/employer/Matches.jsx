import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import EmployerCandidateResults, { EmployerNoJobsEmpty } from "../../components/EmployerCandidateResults.jsx";
import Button from "../../components/Button.jsx";
import { useToast } from "../../components/Toast.jsx";
import { apiErrorMessage, fetchMyJobs, runMatch, DEFAULT_EMPLOYER_MATCH } from "../../api/client.js";

export default function EmployerMatches() {
  const { showToast } = useToast();
  const [searchParams] = useSearchParams();
  const [jobs, setJobs] = useState([]);
  const [selected, setSelected] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [refreshedAt, setRefreshedAt] = useState(null);

  useEffect(() => {
    fetchMyJobs().then(setJobs).catch(() => setJobs([]));
  }, []);

  const openJobs = useMemo(
    () => jobs.filter((job) => (job.status || "open") === "open"),
    [jobs],
  );

  const selectedJob = useMemo(
    () => openJobs.find((job) => job.title === selected) || null,
    [openJobs, selected],
  );

  useEffect(() => {
    if (!openJobs.length) return;
    const fromQuery = searchParams.get("job");
    if (fromQuery && openJobs.some((job) => job.title === fromQuery)) {
      setSelected(fromQuery);
      return;
    }
    if (!selected || !openJobs.some((job) => job.title === selected)) {
      setSelected(openJobs[0].title);
    }
  }, [openJobs, searchParams, selected]);

  const handleRefresh = async () => {
    if (!selected) return;
    setLoading(true);
    setError(null);
    try {
      const data = await runMatch({
        ...DEFAULT_EMPLOYER_MATCH,
        queryKey: selected,
      });
      setResponse(data);
      setRefreshedAt(new Date().toISOString());
      const count = data.results?.length ?? 0;
      showToast(
        count === 0
          ? "Refresh complete — no candidates matched this role yet."
          : `Found ${count} candidate${count === 1 ? "" : "s"} ranked for ${selected}.`,
      );
    } catch (err) {
      setError(apiErrorMessage(err, "Could not load candidate matches. Try again."));
    } finally {
      setLoading(false);
    }
  };

  const handleRoleChange = (title) => {
    setSelected(title);
    setResponse(null);
    setRefreshedAt(null);
    setError(null);
  };

  if (openJobs.length === 0) {
    return (
      <>
        <PageHeader
          eyebrow="Employer"
          title="Candidate matches"
          subtitle="Review candidates ranked by fit for your open roles."
          inlineAction={
            <Link to="/employer/jobs" className="btn-primary">
              Post a role
            </Link>
          }
        />
        <EmployerNoJobsEmpty />
      </>
    );
  }

  return (
    <>
      <PageHeader
        eyebrow="Employer"
        title="Candidate matches"
        subtitle="Review candidates ranked by fit for your open roles."
        inlineAction={
          <div className="hero-toolbar">
            <label className="hero-toolbar-field">
              <span className="field-label">Select role</span>
              <select value={selected} onChange={(e) => handleRoleChange(e.target.value)}>
                {openJobs.map((job) => (
                  <option key={job.id} value={job.title}>
                    {job.title}
                  </option>
                ))}
              </select>
            </label>
            <Button loading={loading} loadingLabel="Refreshing…" onClick={handleRefresh} disabled={!selected}>
              Refresh matches
            </Button>
          </div>
        }
      />
      <EmployerCandidateResults
        response={response}
        error={error}
        jobTitle={selectedJob?.title}
        jobId={selectedJob?.id}
        loading={loading}
        refreshedAt={refreshedAt}
        onRefresh={handleRefresh}
        onClearError={() => setError(null)}
      />
    </>
  );
}
