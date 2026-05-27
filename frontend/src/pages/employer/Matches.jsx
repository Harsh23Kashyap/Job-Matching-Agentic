import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import EmployerCandidateResults, { EmployerNoJobsEmpty } from "../../components/EmployerCandidateResults.jsx";
import { EmployerAllClosedEmpty } from "../../components/EmptyState.jsx";
import EmptyStatePanel from "../../components/EmptyStatePanel.jsx";
import Button from "../../components/Button.jsx";
import { useToast } from "../../components/Toast.jsx";
import { apiErrorMessage, fetchMyJobs, runMatch, DEFAULT_EMPLOYER_MATCH } from "../../api/client.js";
import { matchPercent, countStrongMatches } from "../../utils/format.js";

export default function EmployerMatches() {
  const { showToast } = useToast();
  const [searchParams] = useSearchParams();
  const [jobs, setJobs] = useState([]);
  const [jobsLoading, setJobsLoading] = useState(true);
  const [selected, setSelected] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [refreshedAt, setRefreshedAt] = useState(null);

  useEffect(() => {
    setJobsLoading(true);
    fetchMyJobs()
      .then(setJobs)
      .catch(() => setJobs([]))
      .finally(() => setJobsLoading(false));
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
          ? "Refresh finished. No candidates matched this role yet."
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

  const heroStats = useMemo(() => {
    if (!response?.results?.length) return [];
    const strong = countStrongMatches(response.results);
    const top = response.results[0]?.similarity ?? 0;
    return [
      { label: "Candidates reviewed", value: response.evaluated_count ?? response.results.length },
      { label: "Strong matches", value: strong },
      { label: "Top match", value: matchPercent(top) },
    ];
  }, [response]);

  if (jobsLoading) {
    return (
      <>
        <PageHeader eyebrow="Employer" title="Candidate matches" />
        <section className="portal-panel portal-panel--form">
          <div className="loading-shimmer" aria-hidden="true">
            <span className="skeleton-block skeleton-block--lg" />
            <span className="skeleton-block skeleton-block--md" />
          </div>
        </section>
      </>
    );
  }

  if (jobs.length === 0) {
    return (
      <>
        <PageHeader
          eyebrow="Employer"
          title="Candidate matches"
          subtitle="Candidates ranked by fit for your open roles."
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

  if (openJobs.length === 0) {
    return (
      <>
        <PageHeader
          eyebrow="Employer"
          title="Candidate matches"
          subtitle="Reopen a role or post a new one to search for candidates."
          inlineAction={
            <Link to="/employer/jobs" className="btn-primary">
              Manage roles
            </Link>
          }
        />
        <EmptyStatePanel>
          <EmployerAllClosedEmpty
            action={
              <Link to="/employer/jobs" className="btn-primary">
                Manage roles
              </Link>
            }
          />
        </EmptyStatePanel>
      </>
    );
  }

  const matchCount = response?.results?.length || 0;
  const subtitle = response
    ? `${matchCount} candidate${matchCount === 1 ? "" : "s"} ranked for ${selectedJob?.title || selected}.`
    : selectedJob?.title
      ? `Ranked candidates for ${selectedJob.title}.`
      : "Candidates ranked by fit for your open roles.";

  return (
    <>
      <PageHeader
        eyebrow="Employer"
        title="Candidate matches"
        subtitle={subtitle}
        stats={heroStats}
        inlineAction={
          <div className="hero-toolbar employer-matches-toolbar">
            <label className="hero-toolbar-field">
              <span className="field-label">Select role</span>
              <select className="portal-select" value={selected} onChange={(e) => handleRoleChange(e.target.value)}>
                {openJobs.map((job) => (
                  <option key={job.id} value={job.title}>
                    {job.title}
                  </option>
                ))}
              </select>
            </label>
            <Button loading={loading} loadingLabel="Refreshing…" onClick={handleRefresh} disabled={!selected}>
              {response ? "Refresh matches" : "Find candidates"}
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
