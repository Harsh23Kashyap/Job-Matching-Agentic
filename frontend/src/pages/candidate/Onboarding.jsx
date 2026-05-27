import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { saveCandidateProfile, uploadResume } from "../../api/client.js";

const EMPTY = {
  name: "",
  skills: "",
  experience_years: 0,
  preferred_salary: "",
  remote_preference: false,
  summary: "",
};

export default function Onboarding() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [file, setFile] = useState(null);
  const [fields, setFields] = useState(EMPTY);
  const [preview, setPreview] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError("");
    try {
      const data = await uploadResume(file);
      const ext = data.extracted_fields;
      setFields({
        name: ext.name || "",
        skills: (ext.skills || []).join(", "),
        experience_years: ext.experience_years ?? 0,
        preferred_salary: ext.preferred_salary ?? "",
        remote_preference: ext.remote_preference ?? false,
        summary: ext.summary || "",
      });
      setPreview(data.raw_text_preview || "");
      setStep(2);
    } catch (err) {
      const code = err.response?.data?.detail?.code;
      if (code === "LLM_UNAVAILABLE" || code === "PARSE_FAILED") {
        setError(err.response?.data?.detail?.error || "Extraction failed. Fill in your details manually.");
        setStep(2);
      } else {
        setError(err.response?.data?.detail?.error || err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setLoading(true);
    setError("");
    try {
      const payload = {
        name: fields.name,
        skills: fields.skills.split(",").map((s) => s.trim()).filter(Boolean),
        experience_years: Number(fields.experience_years) || 0,
        preferred_salary: fields.preferred_salary ? Number(fields.preferred_salary) : null,
        remote_preference: fields.remote_preference,
        summary: fields.summary,
      };
      await saveCandidateProfile(payload);
      navigate("/candidate/matches");
    } catch (err) {
      setError(err.response?.data?.detail?.error || err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="portal-panel span-12">
      <h2>Resume onboarding</h2>
      <p className="auth-sub">Step {step} of 2 — upload your resume, review extracted details, then save.</p>

      {step === 1 && (
        <div className="onboarding-upload">
          <label className="dropzone">
            <input
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
            {file ? file.name : "Drop PDF, DOCX, or TXT (max 5MB)"}
          </label>
          <button type="button" className="btn-primary" onClick={handleUpload} disabled={!file || loading}>
            {loading ? "Extracting…" : "Extract with AI"}
          </button>
          <button type="button" className="btn-secondary" onClick={() => setStep(2)}>
            Skip — enter manually
          </button>
        </div>
      )}

      {step === 2 && (
        <form
          className="profile-form"
          onSubmit={(e) => {
            e.preventDefault();
            handleSave();
          }}
        >
          {preview && <p className="text-preview">{preview}</p>}
          <label>
            Name
            <input value={fields.name} onChange={(e) => setFields({ ...fields, name: e.target.value })} required />
          </label>
          <label>
            Skills (comma-separated)
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
            <textarea
              rows={4}
              value={fields.summary}
              onChange={(e) => setFields({ ...fields, summary: e.target.value })}
            />
          </label>
          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={() => setStep(1)}>
              Back
            </button>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? "Saving…" : "Save profile"}
            </button>
          </div>
        </form>
      )}

      {error && <p className="auth-error">{error}</p>}
    </section>
  );
}
