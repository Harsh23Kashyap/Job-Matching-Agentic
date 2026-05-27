import { useEffect, useMemo, useState, useCallback } from "react";
import { Link, useLocation } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import CandidateJobResults from "../../components/CandidateJobResults.jsx";
import { ProfileNeededEmpty, JobsReadyEmpty } from "../../components/EmptyState.jsx";
import Button from "../../components/Button.jsx";
import { fetchMyProfile, runMatch, DEFAULT_CANDIDATE_MATCH } from "../../api/client.js";
import { matchPercent } from "../../utils/format.js";

export default function CandidateMatches() {
  const location = useLocation();
  const [profile, setProfile] = useState(null);
  const [profileLoading, setProfileLoading] = useState(true);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(null);

  const loadProfile = useCallback(() => {
    setProfileLoading(true);
    fetchMyProfile()
      .then(setProfile)
      .catch(() => setProfile(null))
      .finally(() => setProfileLoading(false));
  }, []);

  useEffect(() => {
    loadProfile();
  }, [loadProfile, location.pathname]);

  const handleFindJobs = async () => {
    if (!profile) return;
    setLoading(true);
    setError(null);
    try {
      const data = await runMatch({
        ...DEFAULT_CANDIDATE_MATCH,
        queryKey: profile.name,
      });
      setResponse(data);
      setLastUpdated(new Date().toISOString());
    } catch (err) {
      setError(err.response?.data?.detail?.error || err.message);
      setResponse(null);
    } finally {
      setLoading(false);
    }
  };

  const heroStats = useMemo(() => {
    if (!response?.results?.length) return [];
    const good = response.results.filter((r) => r.similarity >= 0.6).length;
    const top = response.results[0]?.similarity ?? 0;
    return [
      { label: "Roles reviewed", value: response.evaluated_count ?? response.results.length },
      { label: "Strong fits", value: good },
      { label: "Top match", value: matchPercent(top) },
    ];
  }, [response]);

  if (profileLoading) {
    return (
      <>
        <PageHeader eyebrow="Candidate" title="Jobs for you" />
        <section className="portal-panel portal-panel--form">
          <div className="loading-shimmer" aria-hidden="true">
            <span className="skeleton-block skeleton-block--lg" />
            <span className="skeleton-block skeleton-block--md" />
          </div>
        </section>
      </>
    );
  }

  if (!profile) {
    return (
      <>
        <PageHeader
          eyebrow="Candidate"
          title="Jobs for you"
          subtitle="Complete your profile to unlock personalized matches."
          inlineAction={
            <Link to="/candidate/onboarding" className="btn-primary">
              Set up profile
            </Link>
          }
        />
        <section className="portal-panel portal-panel--elevated portal-panel--empty">
          <ProfileNeededEmpty action={<Link to="/candidate/onboarding" className="btn-primary">Set up profile</Link>} />
        </section>
      </>
    );
  }

  const matchCount = response?.results?.length || 0;
  const subtitle = response
    ? `${matchCount} role${matchCount === 1 ? "" : "s"} matched for ${profile.name}.`
    : `Matching roles for ${profile.name} based on your profile.`;

  return (
    <>
      <PageHeader
        eyebrow="Candidate"
        title="Jobs for you"
        subtitle={subtitle}
        stats={heroStats}
        inlineAction={
          <Button loading={loading} loadingLabel="Searching…" onClick={handleFindJobs}>
            {response ? "Refresh matches" : "Find jobs"}
          </Button>
        }
      />
      {!response && !error ? (
        <section className="portal-panel portal-panel--elevated portal-panel--empty">
          <JobsReadyEmpty
            action={
              <Button loading={loading} loadingLabel="Searching…" onClick={handleFindJobs}>
                Find jobs
              </Button>
            }
          />
        </section>
      ) : (
        <CandidateJobResults
          response={response}
          error={error}
          onRefresh={handleFindJobs}
          loading={loading}
          updatedAt={lastUpdated}
        />
      )}
    </>
  );
}
