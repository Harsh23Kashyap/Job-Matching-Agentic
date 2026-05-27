import { useEffect, useMemo, useRef, useState } from "react";
import { Link } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import ProfileForm from "../../components/ProfileForm.jsx";
import FormSection from "../../components/FormSection.jsx";
import ProfileStrength from "../../components/ProfileStrength.jsx";
import ResumePreview from "../../components/ResumePreview.jsx";
import Button from "../../components/Button.jsx";
import { useToast } from "../../components/Toast.jsx";
import { apiErrorMessage, fetchMyProfile, uploadResume, upsertCandidateProfile } from "../../api/client.js";
import { notifyProfileUpdated } from "../../utils/profileEvents.js";
import { resumePreviewFromUpload } from "../../utils/resumeClean.js";
import { EMPTY_PROFILE_FIELDS, fieldsFromExtracted, profileFromApi, profileToPayload } from "../../utils/profileFields.js";
import { profileStrength, validateProfileFields } from "../../utils/validation.js";

export default function Profile() {
  const { showToast } = useToast();
  const [fields, setFields] = useState({ ...EMPTY_PROFILE_FIELDS, id: "" });
  const [fieldErrors, setFieldErrors] = useState({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [hasProfile, setHasProfile] = useState(false);
  const [reuploading, setReuploading] = useState(false);
  const [resumePreview, setResumePreview] = useState("");
  const fileRef = useRef(null);

  const strength = useMemo(() => profileStrength(fields), [fields]);

  useEffect(() => {
    fetchMyProfile()
      .then((p) => {
        setHasProfile(true);
        setFields(profileFromApi(p));
        setError("");
      })
      .catch(() => {
        setHasProfile(false);
      })
      .finally(() => setLoading(false));
  }, []);

  const handleReupload = async (file) => {
    if (!file) return;
    setReuploading(true);
    setError("");
    try {
      const data = await uploadResume(file);
      setFields((prev) => ({ ...prev, ...fieldsFromExtracted(data.extracted_fields || {}) }));
      setResumePreview(resumePreviewFromUpload(data));
      showToast("Resume parsed — review updated fields and save.");
    } catch (err) {
      setError(apiErrorMessage(err, "Upload failed. Try a PDF, DOCX, or TXT under 5MB."));
    } finally {
      setReuploading(false);
      if (fileRef.current) fileRef.current.value = "";
    }
  };

  const handleSave = async () => {
    const errors = validateProfileFields(fields);
    if (Object.keys(errors).length) {
      setFieldErrors(errors);
      return;
    }
    setSaving(true);
    setError("");
    setFieldErrors({});
    try {
      const saved = await upsertCandidateProfile(profileToPayload(fields));
      setFields(profileFromApi(saved));
      setHasProfile(true);
      notifyProfileUpdated();
      showToast(
        hasProfile ? "Profile updated. You can refresh matches now." : "Profile saved.",
        <Link to="/candidate/matches" className="btn-secondary btn-sm">
          Find jobs
        </Link>,
      );
    } catch (err) {
      setError(apiErrorMessage(err, "Save failed. Check your details and try again."));
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <>
        <PageHeader eyebrow="Candidate" title="Your profile" />
        <section className="portal-panel portal-panel--form">
          <div className="loading-shimmer" aria-hidden="true">
            <span className="skeleton-block skeleton-block--lg" />
            <span className="skeleton-block skeleton-block--md" />
            <span className="skeleton-block skeleton-block--sm" />
          </div>
        </section>
      </>
    );
  }

  return (
    <>
      <PageHeader
        eyebrow="Candidate"
        title="Your profile"
        subtitle={
          hasProfile
            ? "Keep your skills and preferences up to date for better matches."
            : "Create your candidate profile to start matching."
        }
      />
      <section className="portal-panel portal-panel--form">
        {!hasProfile && (
          <div className="notice-warning profile-setup-notice">
            <span>No profile saved yet. Fill in your details below or upload a resume to get started.</span>
            <Link to="/candidate/onboarding" className="btn-secondary btn-sm">
              Upload resume
            </Link>
          </div>
        )}
        <FormSection
          title="Update from resume"
          helper="Upload a new PDF, DOCX, or TXT to refresh skills and contact fields."
          className="profile-reupload-bar"
        >
          <input
            ref={fileRef}
            type="file"
            accept=".pdf,.docx,.txt"
            className="visually-hidden"
            id="profile-reupload"
            onChange={(e) => handleReupload(e.target.files?.[0])}
          />
          <Button loading={reuploading} loadingLabel="Parsing…" onClick={() => fileRef.current?.click()}>
            Re-upload resume
          </Button>
        </FormSection>
        {resumePreview && <ResumePreview text={resumePreview} defaultCollapsed />}
        <ProfileStrength percent={strength.percent} hint={strength.hint} />
        <ProfileForm
          fields={fields}
          errors={fieldErrors}
          onChange={setFields}
          footer={
            <div className="form-actions form-actions--sticky portal-form-footer">
              <Link to="/candidate/matches" className="btn-secondary">
                Back to jobs
              </Link>
              <Button loading={saving} loadingLabel={hasProfile ? "Updating…" : "Saving…"} onClick={handleSave}>
                {hasProfile ? "Update profile" : "Save profile"}
              </Button>
            </div>
          }
        />
        {error && <p className="auth-error">{error}</p>}
      </section>
    </>
  );
}
