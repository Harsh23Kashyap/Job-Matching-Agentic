import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import Stepper from "../../components/Stepper.jsx";
import ProfileForm from "../../components/ProfileForm.jsx";
import ResumePreview from "../../components/ResumePreview.jsx";
import Button from "../../components/Button.jsx";
import { IconAlert } from "../../components/icons.jsx";
import { fetchMyProfile, upsertCandidateProfile, uploadResume } from "../../api/client.js";
import { cleanResumeText } from "../../utils/resumeClean.js";
import {
  EMPTY_PROFILE_FIELDS,
  fieldsFromExtracted,
  profileFromApi,
  profileToPayload,
} from "../../utils/profileFields.js";
import { validateProfileFields } from "../../utils/validation.js";

export default function Onboarding() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [file, setFile] = useState(null);
  const [fields, setFields] = useState(EMPTY_PROFILE_FIELDS);
  const [preview, setPreview] = useState("");
  const [fieldErrors, setFieldErrors] = useState({});
  const [error, setError] = useState("");
  const [showFallbackNotice, setShowFallbackNotice] = useState(false);
  const [loading, setLoading] = useState(false);
  const [hasExistingProfile, setHasExistingProfile] = useState(false);

  useEffect(() => {
    fetchMyProfile()
      .then((p) => {
        setHasExistingProfile(true);
        setFields(profileFromApi(p));
      })
      .catch(() => {});
  }, []);

  const goToReview = (data) => {
    setFields((prev) => ({ ...prev, ...fieldsFromExtracted(data.extracted_fields || {}) }));
    setPreview(cleanResumeText(data.raw_text_preview || ""));
    setShowFallbackNotice(Boolean(data.llm_status && data.llm_status !== "ok"));
    setError("");
    setFieldErrors({});
    setStep(2);
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError("");
    setShowFallbackNotice(false);
    try {
      const data = await uploadResume(file);
      goToReview(data);
    } catch (err) {
      setError(err.response?.data?.detail?.error || err.message || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    const errors = validateProfileFields(fields, { requireSkills: true });
    if (Object.keys(errors).length) {
      setFieldErrors(errors);
      return;
    }
    setLoading(true);
    setError("");
    setFieldErrors({});
    try {
      const payload = profileToPayload(fields);
      if (fields.id) payload.id = fields.id;
      await upsertCandidateProfile(payload);
      navigate("/candidate/matches");
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(typeof detail === "object" ? detail.error : detail || err.message || "Save failed");
    } finally {
      setLoading(false);
    }
  };

  const fieldsFilled = Boolean(fields.name?.trim() && fields.skills?.trim());

  return (
    <>
      <PageHeader
        eyebrow="Candidate"
        title="Build your profile"
        subtitle="Upload your resume or enter details manually — we'll match you to the right jobs."
      />
      <section className="portal-panel portal-panel--form onboarding-panel">
        <Stepper steps={["Upload resume", "Review profile"]} current={step} />

        {step === 1 && (
          <div className="onboarding-upload">
            <h2>Upload resume</h2>
            <p className="auth-sub">
              We'll extract your name, contact details, skills, and experience from your resume. You can review and edit everything before saving.
            </p>
            <label className="dropzone">
              <input
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
              />
              {file ? file.name : "Drop PDF, DOCX, or TXT (max 5MB)"}
            </label>
            <Button loading={loading} loadingLabel="Parsing resume…" onClick={handleUpload} disabled={!file}>
              Upload and parse
            </Button>
            <button
              type="button"
              className="btn-secondary"
              onClick={() => {
                setError("");
                setShowFallbackNotice(false);
                setStep(2);
              }}
            >
              Skip — enter manually
            </button>
          </div>
        )}

        {step === 2 && (
          <>
            <h2>Review profile</h2>
            {showFallbackNotice && (
              <div className="notice-warning">
                <IconAlert />
                <span>
                  We couldn't auto-fill your profile. Your resume text was still imported — review it and complete any missing fields.
                </span>
              </div>
            )}
            {preview && <ResumePreview text={preview} defaultCollapsed={fieldsFilled} />}
            <ProfileForm
              fields={fields}
              errors={fieldErrors}
              onChange={setFields}
              requireSkills
              footer={
                <div className="form-actions form-actions--sticky">
                  <button type="button" className="btn-secondary" onClick={() => setStep(1)}>
                    Back
                  </button>
                  <Button loading={loading} loadingLabel="Saving…" onClick={handleSave}>
                    {hasExistingProfile ? "Update profile" : "Save profile"}
                  </Button>
                </div>
              }
            />
          </>
        )}

        {error && <p className="auth-error">{error}</p>}
      </section>
    </>
  );
}
