import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import CandidateJobResults from "../../components/CandidateJobResults.jsx";
import EmptyState from "../../components/EmptyState.jsx";
import Button from "../../components/Button.jsx";
import { fetchMyProfile, runMatch } from "../../api/client.js";

export default function CandidateMatches() {
  const [profile, setProfile] = useState(null);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [bootError, setBootError] = useState("");

  useEffect(() => {
    fetchMyProfile()
      .then(setProfile)
      .catch(() => setBootError("Complete your profile before searching for jobs."));
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
    } catch (err) {
      setError(err.response?.data?.detail?.error || err.message);
      setResponse(null);
    } finally {
      setLoading(false);
    }
  };

  if (bootError) {
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
        <section className="portal-panel">
          <EmptyState
            title="Profile needed"
            description="Upload your resume or enter your skills so we can find roles that fit."
            checklist={["Upload or enter resume details", "Add skills", "Set salary and preferences"]}
            action={<Link to="/candidate/onboarding" className="btn-primary">Set up profile</Link>}
          />
        </section>
      </>
    );
  }

  const subtitle = response
    ? `Showing ${response.results?.length || 0} roles ranked for ${profile?.name}.`
    : `Ready to find roles for ${profile?.name}.`;

  return (
    <>
      <PageHeader
        title="Jobs for you"
        subtitle={subtitle}
        inlineAction={
          <Button loading={loading} loadingLabel="Searching…" onClick={handleFindJobs} disabled={!profile}>
            {response ? "Refresh matches" : "Find jobs"}
          </Button>
        }
      />
      {!response && !error ? (
        <section className="portal-panel">
          <EmptyState
            title="No matches yet"
            description="Run a search to see roles ranked by fit with your profile."
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
        />
      )}
    </>
  );
}
