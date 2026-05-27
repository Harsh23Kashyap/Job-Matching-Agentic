import { useEffect, useMemo, useState, useCallback, useRef } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import CandidateJobResults from "../../components/CandidateJobResults.jsx";
import { ProfileNeededEmpty, ProfileIncompleteEmpty, ProfileStaleEmpty, JobsReadyEmpty } from "../../components/EmptyState.jsx";
import EmptyStatePanel from "../../components/EmptyStatePanel.jsx";
import Button from "../../components/Button.jsx";
import { useToast } from "../../components/Toast.jsx";
import { apiErrorMessage, fetchMyProfileOrNull, runMatch, DEFAULT_CANDIDATE_MATCH } from "../../api/client.js";
import { matchPercent } from "../../utils/format.js";
import { hasCandidateProfile, isCandidateProfileReady } from "../../utils/profileFields.js";
import { PROFILE_UPDATED_EVENT } from "../../utils/profileEvents.js";

export default function CandidateMatches() {
  const location = useLocation();
  const navigate = useNavigate();
  const { showToast } = useToast();
  const [profile, setProfile] = useState(null);
  const [profileLoading, setProfileLoading] = useState(true);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(null);
  const autoSearchDone = useRef(false);

  const profileReady = isCandidateProfileReady(profile);

  const loadProfile = useCallback(() => {
    setProfileLoading(true);
    fetchMyProfileOrNull()
      .then((data) => setProfile(data))
      .catch(() => setProfile(null))
      .finally(() => setProfileLoading(false));
  }, []);

  const handleFindJobs = useCallback(async () => {
    if (!profileReady || !profile?.name) return;
    setLoading(true);
    setError(null);
    try {
      const data = await runMatch({
        ...DEFAULT_CANDIDATE_MATCH,
        queryKey: profile.name,
      });
      setResponse(data);
      setLastUpdated(new Date().toISOString());
      const count = data.results?.length ?? 0;
      showToast(
        count === 0
          ? "Search finished. No roles matched your profile yet."
          : `Found ${count} role${count === 1 ? "" : "s"} matched to your profile.`,
      );
    } catch (err) {
      setError(apiErrorMessage(err, "Could not load job matches. Try again."));
    } finally {
      setLoading(false);
    }
  }, [profile, profileReady, showToast]);

  useEffect(() => {
    loadProfile();
  }, [loadProfile, location.pathname]);

  useEffect(() => {
    const onProfileUpdated = () => loadProfile();
    window.addEventListener(PROFILE_UPDATED_EVENT, onProfileUpdated);
    return () => window.removeEventListener(PROFILE_UPDATED_EVENT, onProfileUpdated);
  }, [loadProfile]);

  useEffect(() => {
    const onVisible = () => {
      if (document.visibilityState === "visible") loadProfile();
    };
    document.addEventListener("visibilitychange", onVisible);
    return () => document.removeEventListener("visibilitychange", onVisible);
  }, [loadProfile]);

  useEffect(() => {
    if (!location.state?.searchAfterSave) {
      autoSearchDone.current = false;
      return;
    }
    if (profileLoading || !profileReady || autoSearchDone.current) return;
    autoSearchDone.current = true;
    navigate(location.pathname, { replace: true, state: {} });
    handleFindJobs();
  }, [
    location.pathname,
    location.state?.searchAfterSave,
    profileLoading,
    profileReady,
    navigate,
    handleFindJobs,
  ]);

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

  if (isProfileStale(profile)) {
    return (
      <>
        <PageHeader
          eyebrow="Candidate"
          title="Jobs for you"
          subtitle="Restore your profile to search for roles again."
          inlineAction={
            <Link to="/candidate/profile" className="btn-primary">
              Restore profile
            </Link>
          }
        />
        <EmptyStatePanel>
          <ProfileStaleEmpty
            action={
              <Link to="/candidate/profile" className="btn-primary">
                Restore profile
              </Link>
            }
          />
        </EmptyStatePanel>
      </>
    );
  }

  if (!hasCandidateProfile(profile)) {
    return (
      <>
        <PageHeader
          eyebrow="Candidate"
          title="Jobs for you"
          subtitle="Set up your profile before searching for roles."
          inlineAction={
            <Link to="/candidate/onboarding" className="btn-primary">
              Set up profile
            </Link>
          }
        />
        <EmptyStatePanel>
          <ProfileNeededEmpty action={<Link to="/candidate/onboarding" className="btn-primary">Set up profile</Link>} />
        </EmptyStatePanel>
      </>
    );
  }

  if (!profileReady) {
    return (
      <>
        <PageHeader
          eyebrow="Candidate"
          title="Jobs for you"
          subtitle="Add your name on your profile to search for roles."
          inlineAction={
            <Link to="/candidate/profile" className="btn-primary">
              Finish profile
            </Link>
          }
        />
        <EmptyStatePanel>
          <ProfileIncompleteEmpty
            action={
              <Link to="/candidate/profile" className="btn-primary">
                Finish profile
              </Link>
            }
          />
        </EmptyStatePanel>
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
          response || error ? (
            <Button loading={loading} loadingLabel="Searching…" onClick={handleFindJobs}>
              Refresh matches
            </Button>
          ) : null
        }
      />
      {!response && !error ? (
        <EmptyStatePanel>
          <JobsReadyEmpty
            action={
              <Button loading={loading} loadingLabel="Searching…" onClick={handleFindJobs}>
                Find jobs
              </Button>
            }
          />
        </EmptyStatePanel>
      ) : error && !response ? (
        <section className="portal-panel portal-panel--elevated">
          <div className="notice-warning match-error-banner">
            <span>{error}</span>
          </div>
          <div className="empty-state-action" style={{ marginTop: 16 }}>
            <Button loading={loading} loadingLabel="Searching…" onClick={handleFindJobs}>
              Try again
            </Button>
          </div>
        </section>
      ) : (
        <CandidateJobResults
          response={response}
          error={error}
          onRefresh={handleFindJobs}
          loading={loading}
          updatedAt={lastUpdated}
          onClearError={() => setError(null)}
        />
      )}
    </>
  );
}
