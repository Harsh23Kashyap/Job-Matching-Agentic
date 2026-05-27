import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchMyProfile, saveCandidateProfile } from "../../api/client.js";

const EMPTY = {
  name: "",
  skills: "",
  experience_years: 0,
  preferred_salary: "",
  remote_preference: false,
  summary: "",
};

export default function Profile() {
  const [fields, setFields] = useState({ ...EMPTY, id: "" });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchMyProfile()
      .then((p) => {
        setFields({
          id: p.id,
          name: p.name || "",
          skills: (p.skills || []).join(", "),
          experience_years: p.experience_years ?? 0,
          preferred_salary: p.preferred_salary ?? "",
          remote_preference: p.remote_preference ?? false,
          summary: p.summary || "",
        });
      })
      .catch(() => setError("No profile yet."))
      .finally(() => setLoading(false));
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError("");
    setMessage("");
    try {
      await saveCandidateProfile({
        id: fields.id,
        name: fields.name,
        skills: fields.skills.split(",").map((s) => s.trim()).filter(Boolean),
        experience_years: Number(fields.experience_years) || 0,
        preferred_salary: fields.preferred_salary ? Number(fields.preferred_salary) : null,
        remote_preference: fields.remote_preference,
        summary: fields.summary,
      });
      setMessage("Profile updated.");
    } catch (err) {
      setError(err.response?.data?.detail?.error || err.message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <section className="portal-panel span-12"><p>Loading…</p></section>;

  if (error && !fields.name) {
    return (
      <section className="portal-panel span-12">
        <h2>Your profile</h2>
        <p>{error}</p>
        <Link to="/candidate/onboarding" className="btn-primary">Upload resume</Link>
      </section>
    );
  }

  return (
    <section className="portal-panel span-12">
      <h2>Your profile</h2>
      <form className="profile-form" onSubmit={handleSave}>
        <label>
          Name
          <input value={fields.name} onChange={(e) => setFields({ ...fields, name: e.target.value })} required />
        </label>
        <label>
          Skills
          <input value={fields.skills} onChange={(e) => setFields({ ...fields, skills: e.target.value })} />
        </label>
        <label>
          Years of experience
          <input
            type="number"
            min="0"
            value={fields.experience_years}
            onChange={(e) => setFields({ ...fields, experience_years: e.target.value })}
          />
        </label>
        <label>
          Preferred salary
          <input
            type="number"
            value={fields.preferred_salary}
            onChange={(e) => setFields({ ...fields, preferred_salary: e.target.value })}
          />
        </label>
        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={fields.remote_preference}
            onChange={(e) => setFields({ ...fields, remote_preference: e.target.checked })}
          />
          Open to remote work
        </label>
        <label>
          Summary
          <textarea rows={4} value={fields.summary} onChange={(e) => setFields({ ...fields, summary: e.target.value })} />
        </label>
        <button type="submit" className="btn-primary" disabled={saving}>
          {saving ? "Saving…" : "Save changes"}
        </button>
      </form>
      {message && <p className="auth-success">{message}</p>}
      {error && <p className="auth-error">{error}</p>}
    </section>
  );
}
