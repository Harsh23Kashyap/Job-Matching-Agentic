import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import Stepper from "../../components/Stepper.jsx";
import ProfileForm from "../../components/ProfileForm.jsx";
import ResumePreview from "../../components/ResumePreview.jsx";
import Button from "../../components/Button.jsx";
import { useToast } from "../../components/Toast.jsx";
import { IconAlert } from "../../components/icons.jsx";
import {
  apiErrorMessage,
  fetchMyProfileOrNull,
  upsertCandidateProfile,
  uploadResume,
} from "../../api/client.js";
import { notifyProfileUpdated } from "../../utils/profileEvents.js";
import { resumePreviewFromUpload } from "../../utils/resumeClean.js";
import {
  EMPTY_PROFILE_FIELDS,
  profileFromApi,
  profileToPayload,
} from "../../utils/profileFields.js";
import { mergeExtractedIntoFields } from "../../utils/profileNormalize.js";
import { validateProfileFields } from "../../utils/validation.js";

function scrollToFirstFieldError() {
  requestAnimationFrame(() => {
    const target =
      document.querySelector(".form-field .field-error") ||
      document.querySelector(".form-field.has-error") ||
      document.querySelector(".skills-chips-input.has-error") ||
      document.querySelector(".compensation-input.has-error");
    target?.scrollIntoView({ behavior: "smooth", block: "center" });
  });
}

export default function Onboarding() {
  const navigate = useNavigate();
  const { showToast } = useToast();
  const errorRef = useRef(null);
  const [step, setStep] = useState(1);
  const [file, setFile] = useState(null);
  const [fields, setFields] = useState(EMPTY_PROFILE_FIELDS);
  const [preview, setPreview] = useState("");
  const [fieldErrors, setFieldErrors] = useState({});
  const [error, setError] = useState("");
  const [showFallbackNotice, setShowFallbackNotice] = useState(false);
  const [loading, setLoading] = useState(false);
  const [hasExistingProfile, setHasExistingProfile] = useState(false);
  const [profileLoaded, setProfileLoaded] = useState(false);

  useEffect(() => {
    fetchMyProfileOrNull()
      .then((profile) => {
        if (profile) {
          setHasExistingProfile(true);
          setFields(profileFromApi(profile));
        }
      })
      .finally(() => setProfileLoaded(true));
  }, []);

  const goToReview = (data) => {
    setFields((prev) => mergeExtractedIntoFields(prev, data.extracted_fields || {}));
    setPreview(resumePreviewFromUpload(data));
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
      showToast("Resume parsed — review your details before saving.");
    } catch (err) {
      setError(apiErrorMessage(err, "Upload failed. Try a PDF, DOCX, or TXT under 5MB."));
      errorRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    const errors = validateProfileFields(fields, { requireSkills: true });
    if (Object.keys(errors).length) {
      setFieldErrors(errors);
      scrollToFirstFieldError();
      return;
    }
    setLoading(true);
    setError("");
    setFieldErrors({});
    try {
      const saved = await upsertCandidateProfile(profileToPayload(fields));
      setFields(profileFromApi(saved));
      setHasExistingProfile(true);
      notifyProfileUpdated();
      showToast(
        hasExistingProfile
          ? "Profile updated. You're ready to browse matches."
          : "Profile saved. You're ready to browse matches.",
      );
      navigate("/candidate/matches");
    } catch (err) {
      const message = apiErrorMessage(err, "Save failed. Check your details and try again.");
      setError(message);
      errorRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
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
        subtitle={
          hasExistingProfile
            ? "Update your details or upload a fresh resume — we'll keep your existing profile."
            : "Upload your resume or enter details manually. We'll use this to rank job matches."
        }
      />
      <section className="portal-panel portal-panel--form onboarding-panel">
        <Stepper steps={["Upload resume", "Review profile"]} current={step} />

        {step === 1 && (
          <div className="onboarding-upload">
            <h2>Upload resume</h2>
            <p className="form-helper onboarding-upload__intro">
              PDF, DOCX, or TXT up to 5MB. We extract your name, contact details, skills, and experience — you review everything before it's saved.
            </p>
            {!profileLoaded && (
              <p className="form-helper onboarding-upload__status">Checking for an existing profile…</p>
            )}
            {hasExistingProfile && profileLoaded && (
              <p className="form-helper onboarding-upload__status">
                You already have a profile on file. Uploading again will merge new details into the form — nothing is saved until you click Save.
              </p>
            )}
            <label className="dropzone">
              <input
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
              />
              {file ? file.name : "Choose a file or drag it here"}
            </label>
            <div className="onboarding-upload__actions">
              <Button loading={loading} loadingLabel="Parsing resume…" onClick={handleUpload} disabled={!file}>
                Upload and parse
              </Button>
              <button
                type="button"
                className="btn-secondary"
                onClick={() => {
                  setError("");
                  setShowFallbackNotice(false);
                  setFieldErrors({});
                  setStep(2);
                }}
              >
                Skip — enter manually
              </button>
            </div>
          </div>
        )}

        {step === 2 && (
          <>
            <h2>Review profile</h2>
            <p className="form-helper onboarding-review__intro">
              Confirm your details below. Skills appear as editable chips — add, remove, or paste a comma-separated list.
            </p>
            {showFallbackNotice && (
              <div className="notice-warning">
                <IconAlert />
                <span>
                  We couldn't auto-fill every field from your resume. The cleaned text is below — complete anything that's missing.
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
                  <Button loading={loading} loadingLabel={hasExistingProfile ? "Updating…" : "Saving…"} onClick={handleSave}>
                    {hasExistingProfile ? "Update profile" : "Save profile"}
                  </Button>
                </div>
              }
            />
          </>
        )}

        {error && (
          <p className="auth-error" ref={errorRef} role="alert">
            {error}
          </p>
        )}
      </section>
    </>
  );
}
