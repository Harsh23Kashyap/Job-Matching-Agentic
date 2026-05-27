import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import PortalSection from "../../components/PortalSection.jsx";
import FormField from "../../components/FormField.jsx";
import CustomCheckbox from "../../components/CustomCheckbox.jsx";
import Button from "../../components/Button.jsx";
import EmptyState from "../../components/EmptyState.jsx";
import { fetchMyJobs, saveJobPosting, uploadJobDescription } from "../../api/client.js";
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
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const fileRef = useRef(null);

  const load = () => {
    fetchMyJobs()
      .then(setJobs)
      .catch(() => setJobs([]))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const applyExtracted = (data) => {
    const x = data.extracted_fields || {};
    setFields((prev) => ({
      ...prev,
      title: x.title || prev.title,
      required_skills: Array.isArray(x.required_skills) ? x.required_skills.join(", ") : prev.required_skills,
      required_experience: x.required_experience ?? prev.required_experience,
      description: x.description || prev.description,
      company: x.company || prev.company,
      location: x.location || prev.location,
      remote_policy: Boolean(x.remote_policy),
    }));
  };

  const handleUpload = async (file) => {
    if (!file) return;
    setUploading(true);
    setError("");
    try {
      const data = await uploadJobDescription(file);
      applyExtracted(data);
    } catch (err) {
      setError(err.response?.data?.detail?.error || err.message || "Upload failed");
    } finally {
      setUploading(false);
      if (fileRef.current) fileRef.current.value = "";
    }
  };

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
      <PageHeader
        eyebrow="Employer"
        title="My jobs"
        subtitle="Manage postings and attract the right candidates."
        stats={
          !loading
            ? [
                { label: "Active postings", value: jobs.length },
                { label: "Remote-friendly", value: jobs.filter((j) => j.remote_policy).length },
              ]
            : []
        }
      />

      <div className="employer-jobs-grid">
        <PortalSection
          span={6}
          title="Active postings"
          description="Roles you've created — use them when finding candidates."
        >
          {loading ? (
            <div className="loading-shimmer" aria-hidden="true">
              <span className="skeleton-block skeleton-block--lg" />
              <span className="skeleton-block skeleton-block--md" />
            </div>
          ) : jobs.length === 0 ? (
            <EmptyState
              title="No jobs yet"
              description="Create your first posting or upload a job description to get started."
              helperText="Include required skills so we can rank the best profiles."
            />
          ) : (
            <div className="job-card-list">
              {jobs.map((j) => (
                <article key={j.id} className="job-card job-card--employer">
                  <div className="job-card-head">
                    <h3>{j.title}</h3>
                    {j.remote_policy && <span className="job-card-badge">Remote</span>}
                  </div>
                  {j.company && <p className="job-card-meta">{j.company}{j.location ? ` · ${j.location}` : ""}</p>}
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
                  <Link to="/employer/matches" className="job-card-link">
                    Find candidates →
                  </Link>
                </article>
              ))}
            </div>
          )}
        </PortalSection>

        <PortalSection
          span={6}
          title="New job posting"
          description="Paste details manually or upload a job description file."
        >
          <div className="jd-upload-bar">
            <input
              ref={fileRef}
              type="file"
              accept=".pdf,.docx,.txt"
              className="visually-hidden"
              id="jd-upload"
              onChange={(e) => handleUpload(e.target.files?.[0])}
            />
            <Button loading={uploading} loadingLabel="Parsing…" onClick={() => fileRef.current?.click()}>
              Upload JD
            </Button>
            <p className="form-helper">PDF, DOCX, or TXT — fields below will pre-fill when parsing succeeds.</p>
          </div>

          <form className="employer-job-form" onSubmit={handleCreate}>
            <FormField label="Title" htmlFor="ej-title">
              <input
                id="ej-title"
                value={fields.title}
                onChange={(e) => setFields({ ...fields, title: e.target.value })}
                required
              />
            </FormField>
            <FormField label="Required skills" helper="Comma-separated" htmlFor="ej-skills">
              <input
                id="ej-skills"
                value={fields.required_skills}
                onChange={(e) => setFields({ ...fields, required_skills: e.target.value })}
              />
            </FormField>
            <div className="form-row-2">
              <FormField label="Experience (years)" htmlFor="ej-exp">
                <input
                  id="ej-exp"
                  type="number"
                  min="0"
                  step="0.5"
                  value={fields.required_experience}
                  onChange={(e) => setFields({ ...fields, required_experience: e.target.value })}
                />
              </FormField>
              <FormField label="Budget (INR)" htmlFor="ej-budget">
                <input
                  id="ej-budget"
                  type="number"
                  value={fields.budget}
                  onChange={(e) => setFields({ ...fields, budget: e.target.value })}
                />
              </FormField>
            </div>
            <div className="form-row-2">
              <FormField label="Company" htmlFor="ej-company">
                <input
                  id="ej-company"
                  value={fields.company}
                  onChange={(e) => setFields({ ...fields, company: e.target.value })}
                />
              </FormField>
              <FormField label="Location" htmlFor="ej-location">
                <input
                  id="ej-location"
                  value={fields.location}
                  onChange={(e) => setFields({ ...fields, location: e.target.value })}
                />
              </FormField>
            </div>
            <CustomCheckbox
              id="ej-remote"
              label="Remote allowed"
              checked={fields.remote_policy}
              onChange={(checked) => setFields({ ...fields, remote_policy: checked })}
            />
            <FormField label="Description" htmlFor="ej-desc">
              <textarea
                id="ej-desc"
                rows={4}
                value={fields.description}
                onChange={(e) => setFields({ ...fields, description: e.target.value })}
              />
            </FormField>
            <div className="form-actions">
              <Button loading={saving} loadingLabel="Creating…" type="submit">
                Create job
              </Button>
            </div>
          </form>
          {error && <p className="auth-error">{error}</p>}
        </PortalSection>
      </div>
    </>
  );
}
