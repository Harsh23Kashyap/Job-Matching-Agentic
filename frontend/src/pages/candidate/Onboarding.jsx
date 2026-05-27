import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import Stepper from "../../components/Stepper.jsx";
import ProfileForm from "../../components/ProfileForm.jsx";
import ResumePreview from "../../components/ResumePreview.jsx";
import ExtractedSectionsPanel from "../../components/ExtractedSectionsPanel.jsx";
import ProfileQualityPanel from "../../components/ProfileQualityPanel.jsx";
import Button from "../../components/Button.jsx";
import { useToast } from "../../components/Toast.jsx";
import { IconAlert } from "../../components/icons.jsx";
import {
  apiErrorMessage,
  checkProfileQuality,
  fetchMyProfileOrNull,
  upsertCandidateProfile,
  uploadResume,
} from "../../api/client.js";
import { resumePreviewFromUpload } from "../../utils/resumeClean.js";
import {
  EMPTY_PROFILE_FIELDS,
  isCandidateProfileReady,
  isProfileStale,
  profileFromApi,
  profileToPayload,
} from "../../utils/profileFields.js";
import { mergeExtractedIntoFields } from "../../utils/profileNormalize.js";
import { mergeSkills } from "../../utils/skills.js";
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
  const [uploading, setUploading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [hasExistingProfile, setHasExistingProfile] = useState(false);
  const [profileReady, setProfileReady] = useState(false);
  const [profileLoaded, setProfileLoaded] = useState(false);
  const [extractedSections, setExtractedSections] = useState(null);
  const [parseStatus, setParseStatus] = useState(null);
  const [quality, setQuality] = useState(null);
  const [qualityLoading, setQualityLoading] = useState(false);
  const [addingSkill, setAddingSkill] = useState("");

  useEffect(() => {
    fetchMyProfileOrNull()
      .then((profile) => {
        if (profile && !isProfileStale(profile)) {
          setHasExistingProfile(true);
          setFields(profileFromApi(profile));
          setProfileReady(isCandidateProfileReady(profile));
        } else if (isProfileStale(profile)) {
          setHasExistingProfile(true);
          setFields(profileFromApi(profile));
        }
      })
      .finally(() => setProfileLoaded(true));
  }, []);

  const goToReview = (data) => {
    setExtractedSections(data.extracted_fields || null);
    setFields((prev) => mergeExtractedIntoFields(prev, data.extracted_fields || {}));
    setPreview(resumePreviewFromUpload(data));
    setParseStatus(data.llm_status || null);
    setQuality(data.quality || null);
    setShowFallbackNotice(Boolean(data.llm_status && data.llm_status !== "ok"));
    setError("");
    setFieldErrors({});
    setStep(2);
  };

  const hasQualityInput = Boolean(fields.name?.trim() || fields.skills?.trim() || fields.summary?.trim());

  useEffect(() => {
    if (step !== 2 || !hasQualityInput) {
      if (step !== 2) {
        setQuality(null);
        setQualityLoading(false);
      }
      return undefined;
    }
    let cancelled = false;
    const timer = window.setTimeout(async () => {
      setQualityLoading(true);
      try {
        const report = await checkProfileQuality(profileToPayload(fields), { llmStatus: parseStatus });
        if (!cancelled) setQuality(report);
      } catch {
        if (!cancelled) setQuality(null);
      } finally {
        if (!cancelled) setQualityLoading(false);
      }
    }, 450);
    return () => {
      cancelled = true;
      window.clearTimeout(timer);
    };
  }, [fields, step, hasQualityInput, parseStatus]);

  const handleAddSuggestedSkill = (skill) => {
    setAddingSkill(skill);
    setFields((prev) => ({
      ...prev,
      skills: mergeSkills(prev.skills, [skill]).join(", "),
    }));
    setAddingSkill("");
    showToast(`Added ${skill} to your skills.`);
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setError("");
    setShowFallbackNotice(false);
    try {
      const data = await uploadResume(file);
      goToReview(data);
      showToast("Resume parsed. Review your details, then save.");
    } catch (err) {
      setError(apiErrorMessage(err, "Upload failed. Try a PDF, DOCX, or TXT under 5MB."));
      errorRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    } finally {
      setUploading(false);
    }
  };

  const handleSave = async () => {
    const errors = validateProfileFields(fields, { requireSkills: true });
    if (Object.keys(errors).length) {
      setFieldErrors(errors);
      scrollToFirstFieldError();
      return;
    }
    const wasUpdate = hasExistingProfile;
    setSaving(true);
    setError("");
    setFieldErrors({});
    try {
      const saved = await upsertCandidateProfile(profileToPayload(fields));
      setFields(profileFromApi(saved));
      setHasExistingProfile(true);
      setProfileReady(isCandidateProfileReady(saved));
      showToast(wasUpdate ? "Profile updated." : "Profile saved.");
      navigate("/candidate/matches", { state: { searchAfterSave: true } });
    } catch (err) {
      const message = apiErrorMessage(err, "Save failed. Check your details and try again.");
      setError(message);
      errorRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    } finally {
      setSaving(false);
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
            ? "Update your details or upload a new resume."
            : "Upload a resume or enter details manually. Used to rank job matches."
        }
      />
      <section className="portal-panel portal-panel--form onboarding-panel">
        <Stepper steps={["Upload resume", "Review profile"]} current={step} />

        {step === 1 && (
          <div className="onboarding-upload">
            <h2>Upload resume</h2>
            <p className="form-helper onboarding-upload__intro">
              PDF, DOCX, or TXT, max 5 MB. We extract contact details, skills, experience, education, projects, and summary. Nothing saves until you confirm.
            </p>
            {!profileLoaded && (
              <p className="form-helper onboarding-upload__status">Checking for an existing profile…</p>
            )}
            {hasExistingProfile && profileLoaded && (
              <p className="form-helper onboarding-upload__status">
                You already have a profile. A new upload merges into the form. Save when you're done.
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
              <Button loading={uploading} loadingLabel="Parsing resume…" onClick={handleUpload} disabled={!file || saving}>
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
                Enter details manually
              </button>
              {profileReady && (
                <button
                  type="button"
                  className="btn-primary"
                  onClick={() => navigate("/candidate/matches", { state: { searchAfterSave: true } })}
                >
                  Continue to jobs
                </button>
              )}
            </div>
          </div>
        )}

        {step === 2 && (
          <>
            <h2>Review profile</h2>
            <p className="form-helper onboarding-review__intro">
              Check everything below. Edit skills as chips or paste a comma-separated list.
            </p>
            {showFallbackNotice && (
              <div className="notice-warning">
                <IconAlert />
                <span>
                  Some fields didn't parse from your resume. Use the text below and fill in what's missing.
                </span>
              </div>
            )}
            {preview && <ResumePreview text={preview} defaultCollapsed={fieldsFilled} />}
            <ExtractedSectionsPanel extracted={extractedSections || {}} />
            {(hasQualityInput || qualityLoading) && (
              <ProfileQualityPanel
                quality={quality}
                loading={qualityLoading}
                onAddSkill={handleAddSuggestedSkill}
                addingSkill={addingSkill}
              />
            )}
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
                  <Button loading={saving} loadingLabel={hasExistingProfile ? "Updating…" : "Saving…"} onClick={handleSave} disabled={uploading}>
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
