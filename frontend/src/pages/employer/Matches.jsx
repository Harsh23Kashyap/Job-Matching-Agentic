import { useEffect, useMemo, useState, useCallback, useRef } from "react";
import { Link, useSearchParams } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import EmployerCandidateResults, { EmployerNoJobsEmpty } from "../../components/EmployerCandidateResults.jsx";
import { EmployerAllClosedEmpty } from "../../components/EmptyState.jsx";
import EmptyStatePanel from "../../components/EmptyStatePanel.jsx";
import { useToast } from "../../components/Toast.jsx";
import { apiErrorMessage, fetchMyJobs, runMatch, DEFAULT_EMPLOYER_MATCH } from "../../api/client.js";
import { JOBS_UPDATED_EVENT } from "../../utils/profileEvents.js";

function resolveJobSelection(openJobs, queryValue) {
  if (!queryValue || !openJobs.length) return null;
  const byId = openJobs.find((job) => job.id === queryValue);
  if (byId) return byId.id;
  const byTitle = openJobs.find((job) => job.title === queryValue);
  return byTitle?.id ?? null;
}

export default function EmployerMatches() {
  const { showToast } = useToast();
  const [searchParams] = useSearchParams();
  const [jobs, setJobs] = useState([]);
  const [jobsLoading, setJobsLoading] = useState(true);
  const [selectedJobId, setSelectedJobId] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [refreshedAt, setRefreshedAt] = useState(null);
  const autoMatchDone = useRef(false);

  const loadJobs = useCallback(async ({ silent = false } = {}) => {
    if (!silent) setJobsLoading(true);
    try {
      const rows = await fetchMyJobs();
      setJobs(rows);
    } catch {
      setJobs([]);
    } finally {
      if (!silent) setJobsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadJobs();
  }, [loadJobs]);

  useEffect(() => {
    const onJobsUpdated = () => loadJobs({ silent: true });
    window.addEventListener(JOBS_UPDATED_EVENT, onJobsUpdated);
    return () => window.removeEventListener(JOBS_UPDATED_EVENT, onJobsUpdated);
  }, [loadJobs]);

  const openJobs = useMemo(
    () => jobs.filter((job) => (job.status || "open") === "open"),
    [jobs],
  );

  const selectedJob = useMemo(
    () => openJobs.find((job) => job.id === selectedJobId) || null,
    [openJobs, selectedJobId],
  );

  useEffect(() => {
    if (!openJobs.length) {
      setSelectedJobId("");
      return;
    }
    const fromQuery = resolveJobSelection(openJobs, searchParams.get("job"));
    if (fromQuery) {
      setSelectedJobId(fromQuery);
      return;
    }
    if (!selectedJobId || !openJobs.some((job) => job.id === selectedJobId)) {
      setSelectedJobId(openJobs[0].id);
    }
  }, [openJobs, searchParams, selectedJobId]);

  const handleRefresh = useCallback(async ({ silent = false } = {}) => {
    if (!selectedJob?.title) return;
    setLoading(true);
    if (!silent) setError(null);
    try {
      const data = await runMatch({
        ...DEFAULT_EMPLOYER_MATCH,
        queryKey: selectedJob.title,
      });
      setResponse(data);
      setRefreshedAt(new Date().toISOString());
      if (!silent) {
        const count = data.results?.length ?? 0;
        showToast(
          count === 0
            ? "Refresh finished. No candidates matched this role yet."
            : `Found ${count} candidate${count === 1 ? "" : "s"} ranked for ${selectedJob.title}.`,
        );
      }
    } catch (err) {
      setError(apiErrorMessage(err, "Could not load candidate matches. Try again."));
    } finally {
      setLoading(false);
    }
  }, [selectedJob, showToast]);

  useEffect(() => {
    const jobParam = searchParams.get("job");
    if (!jobParam) {
      autoMatchDone.current = false;
      return;
    }
    if (jobsLoading || !openJobs.length || !selectedJobId) return;
    const resolvedId = resolveJobSelection(openJobs, jobParam);
    if (!resolvedId || resolvedId !== selectedJobId || loading || response || autoMatchDone.current) return;
    autoMatchDone.current = true;
    handleRefresh({ silent: true });
  }, [
    searchParams,
    jobsLoading,
    openJobs,
    selectedJobId,
    loading,
    response,
    handleRefresh,
  ]);

  const handleRoleChange = (jobId) => {
    setSelectedJobId(jobId);
    setResponse(null);
    setRefreshedAt(null);
    setError(null);
  };

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
    ? `${matchCount} candidate${matchCount === 1 ? "" : "s"} ranked for ${selectedJob?.title || "this role"}.`
    : selectedJob?.title
      ? `Select a role and refresh matches to rank candidates.`
      : "Candidates ranked by fit for your open roles.";

  return (
    <>
      <PageHeader
        eyebrow="Employer"
        title="Candidate matches"
        subtitle={subtitle}
        inlineAction={
          <label className="hero-toolbar-field employer-matches-role-field">
            <span className="visually-hidden">Select role</span>
            <select
              className="portal-select"
              value={selectedJobId}
              onChange={(e) => handleRoleChange(e.target.value)}
              aria-label="Select role"
            >
              {openJobs.map((job) => (
                <option key={job.id} value={job.id}>
                  {job.title}
                </option>
              ))}
            </select>
          </label>
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
