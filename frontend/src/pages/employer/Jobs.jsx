import { useEffect, useState } from "react";
import PageHeader from "../../components/PageHeader.jsx";
import { fetchMyJobs, saveJobPosting } from "../../api/client.js";
import { formatInr } from "../../utils/format.js";

const EMPTY = {
  title: "",
  required_skills: "",
  required_experience: 0,
  budget: "",
  remote_policy: false,
  description: "",
  company: "",
  location: "",
};

export default function EmployerJobs() {
  const [jobs, setJobs] = useState([]);
  const [fields, setFields] = useState(EMPTY);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const load = () => {
    fetchMyJobs()
      .then(setJobs)
      .catch(() => setJobs([]))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError("");
    try {
      await saveJobPosting({
        title: fields.title,
        required_skills: fields.required_skills.split(",").map((s) => s.trim()).filter(Boolean),
        required_experience: Number(fields.required_experience) || 0,
        budget: fields.budget ? Number(fields.budget) : null,
        remote_policy: fields.remote_policy,
        description: fields.description,
        company: fields.company || null,
        location: fields.location || null,
      });
      setFields(EMPTY);
      load();
    } catch (err) {
      setError(err.response?.data?.detail?.error || err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <>
      <PageHeader title="My jobs" subtitle="Manage postings and attract the right candidates." />
      <section className="portal-panel">
        <h2>Active postings</h2>
        {loading ? (
          <p>Loading…</p>
        ) : jobs.length === 0 ? (
          <div className="empty-state-product">
            <h3>No jobs yet</h3>
            <p>Create your first posting below to start matching candidates.</p>
          </div>
        ) : (
          <div className="job-card-list">
            {jobs.map((j) => (
              <article key={j.id} className="job-card">
                <div className="job-card-head">
                  <h3>{j.title}</h3>
                  {j.company && <span className="job-card-meta">{j.company}</span>}
                </div>
                {j.location && <p className="job-card-location">{j.location}</p>}
                {j.required_skills?.length > 0 && (
                  <div className="signal-chips">
                    {j.required_skills.slice(0, 6).map((s) => (
                      <span key={s} className="signal-chip">
                        {s}
                      </span>
                    ))}
                  </div>
                )}
                {j.budget != null && (
                  <p className="job-card-budget">{formatInr(j.budget)} / year budget</p>
                )}
              </article>
            ))}
          </div>
        )}
      </section>

      <section className="portal-panel">
        <h2>New job posting</h2>
        <form className="profile-form" onSubmit={handleCreate}>
          <label>
            Title
            <input value={fields.title} onChange={(e) => setFields({ ...fields, title: e.target.value })} required />
          </label>
          <label>
            Required skills (comma-separated)
            <input
              value={fields.required_skills}
              onChange={(e) => setFields({ ...fields, required_skills: e.target.value })}
            />
          </label>
          <label>
            Required experience (years)
            <input
              type="number"
              min="0"
              step="0.5"
              value={fields.required_experience}
              onChange={(e) => setFields({ ...fields, required_experience: e.target.value })}
            />
          </label>
          <label>
            Budget (INR)
            <input type="number" value={fields.budget} onChange={(e) => setFields({ ...fields, budget: e.target.value })} />
          </label>
          <label>
            Company
            <input value={fields.company} onChange={(e) => setFields({ ...fields, company: e.target.value })} />
          </label>
          <label>
            Location
            <input value={fields.location} onChange={(e) => setFields({ ...fields, location: e.target.value })} />
          </label>
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={fields.remote_policy}
              onChange={(e) => setFields({ ...fields, remote_policy: e.target.checked })}
            />
            Remote allowed
          </label>
          <label>
            Description
            <textarea
              rows={4}
              value={fields.description}
              onChange={(e) => setFields({ ...fields, description: e.target.value })}
            />
          </label>
          <button type="submit" className="btn-primary" disabled={saving}>
            {saving ? "Creating…" : "Create job"}
          </button>
        </form>
        {error && <p className="auth-error">{error}</p>}
      </section>
    </>
  );
}
