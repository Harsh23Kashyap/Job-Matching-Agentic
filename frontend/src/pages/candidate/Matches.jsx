import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import CandidateJobResults from "../../components/CandidateJobResults.jsx";
import { ProfileNeededEmpty, JobsReadyEmpty } from "../../components/EmptyState.jsx";
import Button from "../../components/Button.jsx";
import { fetchMyProfile, runMatch } from "../../api/client.js";

export default function CandidateMatches() {
  const [profile, setProfile] = useState(null);
  const [profileLoading, setProfileLoading] = useState(true);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    fetchMyProfile()
      .then(setProfile)
      .catch(() => setProfile(null))
      .finally(() => setProfileLoading(false));
  }, []);

  const handleFindJobs = async () => {
    if (!profile) return;
    setLoading(true);
    setError(null);
    try {
      const data = await runMatch({
        mode: "candidate_to_jobs",
        queryKey: profile.name,
        topK: 10,
        strategy: "semantic",
        metric: "cosine",
        skillsMode: "jaccard",
        semanticWeight: 0.7,
        ensemble: false,
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

  if (profileLoading) {
    return (
      <>
        <PageHeader title="Jobs for you" />
        <section className="portal-panel portal-panel--form"><p>Loading…</p></section>
      </>
    );
  }

  if (!profile) {
    return (
      <>
        <PageHeader
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
        title="Jobs for you"
        subtitle={subtitle}
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
