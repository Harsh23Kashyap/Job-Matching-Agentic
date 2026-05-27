import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import Button from "../../components/Button.jsx";
import { useToast } from "../../components/Toast.jsx";
import {
  apiErrorMessage,
  fetchMyApplications,
  fetchSavedJobs,
  recordFeedbackAction,
} from "../../api/client.js";
import { PROFILE_UPDATED_EVENT } from "../../utils/profileEvents.js";

export default function CandidateSaved() {
  const { showToast } = useToast();
  const [saved, setSaved] = useState([]);
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [unsavingId, setUnsavingId] = useState("");
  const [error, setError] = useState(null);

  const load = async ({ refresh = false } = {}) => {
    if (refresh) setRefreshing(true);
    else setLoading(true);
    setError(null);
    try {
      const [savedRows, appRows] = await Promise.all([fetchSavedJobs(), fetchMyApplications()]);
      setSaved(savedRows);
      setApplications(appRows);
    } catch (err) {
      setError(apiErrorMessage(err, "Could not load saved jobs and applications."));
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  useEffect(() => {
    const onProfileUpdated = () => load({ refresh: true });
    window.addEventListener(PROFILE_UPDATED_EVENT, onProfileUpdated);
    return () => window.removeEventListener(PROFILE_UPDATED_EVENT, onProfileUpdated);
  }, []);

  const handleUnsave = async (row) => {
    if (unsavingId) return;
    setUnsavingId(row.job_id);
    const previous = saved;
    setSaved((prev) => prev.filter((s) => s.job_id !== row.job_id));
    try {
      await recordFeedbackAction({
        targetId: row.job_id,
        action: "unsave",
        targetLabel: row.job_title,
      });
      showToast(`Removed ${row.job_title} from saved.`);
    } catch (err) {
      setSaved(previous);
      showToast(apiErrorMessage(err, "Could not remove saved job. Try again."), "error");
    } finally {
      setUnsavingId("");
    }
  };

  return (
    <>
      <PageHeader
        eyebrow="Candidate"
        title="Saved & applied"
        subtitle="Jobs you saved and roles you applied to."
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
                <p className="auth-sub">Nothing saved yet. Save roles from your job matches.</p>
              ) : (
                <ul className="activity-list">
                  {saved.map((row) => (
                    <li key={row.id} className="activity-row">
                      <span>{row.job_title}</span>
                      <button
                        type="button"
                        className="row-action-btn"
                        disabled={unsavingId === row.job_id}
                        onClick={() => handleUnsave(row)}
                      >
                        {unsavingId === row.job_id ? "Removing…" : "Remove"}
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
              <Button loading={refreshing} loadingLabel="Refreshing…" onClick={() => load({ refresh: true })}>
                Refresh
              </Button>
            </div>
          </>
        )}
      </section>
    </>
  );
}
