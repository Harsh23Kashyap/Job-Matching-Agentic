import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import Button from "../../components/Button.jsx";
import { fetchMyApplications, fetchSavedJobs, updateSavedJob } from "../../api/client.js";

export default function CandidateSaved() {
  const [saved, setSaved] = useState([]);
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const [savedRows, appRows] = await Promise.all([fetchSavedJobs(), fetchMyApplications()]);
      setSaved(savedRows);
      setApplications(appRows);
    } catch (err) {
      setError(err.response?.data?.detail?.error || err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleUnsave = async (row) => {
    await updateSavedJob(row.job_id, row.job_title, false);
    setSaved((prev) => prev.filter((s) => s.job_id !== row.job_id));
  };

  return (
    <>
      <PageHeader
        eyebrow="Candidate"
        title="Saved & applied"
        subtitle="Your shortlist and applications are stored in your account."
        inlineAction={
          <Link to="/candidate/matches" className="btn-secondary">
            Back to matches
          </Link>
        }
      />
      <section className="portal-panel portal-panel--elevated">
        {error && <p className="notice-warning">{error}</p>}
        {loading ? (
          <p className="auth-sub">Loading…</p>
        ) : (
          <>
            <div className="portal-section-block">
              <h2 className="portal-section-title">Saved jobs ({saved.length})</h2>
              {saved.length === 0 ? (
                <p className="auth-sub">No saved jobs yet. Save roles from your match results.</p>
              ) : (
                <ul className="activity-list">
                  {saved.map((row) => (
                    <li key={row.id} className="activity-row">
                      <span>{row.job_title}</span>
                      <button type="button" className="row-action-btn" onClick={() => handleUnsave(row)}>
                        Remove
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>
            <div className="portal-section-block" style={{ marginTop: 24 }}>
              <h2 className="portal-section-title">Applications ({applications.length})</h2>
              {applications.length === 0 ? (
                <p className="auth-sub">No applications yet.</p>
              ) : (
                <ul className="activity-list">
                  {applications.map((row) => (
                    <li key={row.id} className="activity-row">
                      <span>
                        {row.job_title}
                        {row.match_score != null && (
                          <span className="signal-chip signal-chip--match" style={{ marginLeft: 8 }}>
                            {Math.round(row.match_score * 100)}% match
                          </span>
                        )}
                      </span>
                      <span className="auth-sub">{new Date(row.created_at).toLocaleDateString()}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
            <div style={{ marginTop: 16 }}>
              <Button onClick={load}>Refresh</Button>
            </div>
          </>
        )}
      </section>
    </>
  );
}
