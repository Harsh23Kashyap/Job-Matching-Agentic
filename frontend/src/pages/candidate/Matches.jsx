import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import ResultsPanel from "../../components/ResultsPanel.jsx";
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
      <section className="portal-panel span-12">
        <h2>Find jobs</h2>
        <p>{bootError}</p>
        <Link to="/candidate/onboarding" className="btn-primary">Set up profile</Link>
      </section>
    );
  }

  return (
    <>
      <section className="portal-panel span-12">
        <h2>Find jobs</h2>
        <p className="auth-sub">
          Matching jobs for <strong>{profile?.name}</strong> using semantic search and skill overlap.
        </p>
        <button type="button" className="btn-primary" onClick={handleFindJobs} disabled={loading || !profile}>
          {loading ? "Searching…" : "Find matching jobs"}
        </button>
      </section>
      <ResultsPanel response={response} error={error} recentRuns={[]} />
    </>
  );
}
