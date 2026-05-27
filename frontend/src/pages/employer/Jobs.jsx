import { useEffect, useState } from "react";
import { fetchMyJobs, saveJobPosting } from "../../api/client.js";

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
      <section className="portal-panel span-12">
        <h2>My job postings</h2>
        {loading ? (
          <p>Loading…</p>
        ) : jobs.length === 0 ? (
          <p className="auth-sub">No jobs yet. Create your first posting below.</p>
        ) : (
          <ul className="job-list">
            {jobs.map((j) => (
              <li key={j.id}>
                <strong>{j.title}</strong>
                {j.company && <span> — {j.company}</span>}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="portal-panel span-12">
        <h2>Create job posting</h2>
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
              value={fields.required_experience}
              onChange={(e) => setFields({ ...fields, required_experience: e.target.value })}
            />
          </label>
          <label>
            Budget
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
