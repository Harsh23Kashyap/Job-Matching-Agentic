import { useEffect, useState } from "react";
import PageHeader from "../../components/PageHeader.jsx";
import PortalSection from "../../components/PortalSection.jsx";
import { fetchEmployerApplications } from "../../api/client.js";

export default function EmployerApplications() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchEmployerApplications()
      .then(setApplications)
      .catch((err) => setError(err.response?.data?.detail?.error || err.message))
      .finally(() => setLoading(false));
  }, []);

  const byJob = applications.reduce((acc, row) => {
    if (!acc[row.job_title]) acc[row.job_title] = [];
    acc[row.job_title].push(row);
    return acc;
  }, {});

  return (
    <>
      <PageHeader
        eyebrow="Employer"
        title="Applicants"
        subtitle="Candidates who applied to your posted roles."
      />
      <PortalSection title="Application feed">
        {loading && <p className="auth-sub">Loading…</p>}
        {error && <p className="notice-warning">{error}</p>}
        {!loading && !error && applications.length === 0 && (
          <p className="auth-sub">No applications yet. Candidates can apply from their match results.</p>
        )}
        {Object.entries(byJob).map(([title, rows]) => (
          <div key={title} className="portal-section-block" style={{ marginBottom: 20 }}>
            <h3 className="portal-section-title">{title}</h3>
            <ul className="activity-list">
              {rows.map((row) => (
                <li key={row.id} className="activity-row">
                  <span>{row.candidate_name}</span>
                  <span className="auth-sub">
                    {row.match_score != null ? `${Math.round(row.match_score * 100)}% match · ` : ""}
                    {new Date(row.created_at).toLocaleDateString()}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </PortalSection>
    </>
  );
}
