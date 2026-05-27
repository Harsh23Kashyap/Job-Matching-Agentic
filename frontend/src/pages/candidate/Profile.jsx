import { useEffect, useMemo, useRef, useState } from "react";
import { Link } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import ProfileForm from "../../components/ProfileForm.jsx";
import FormSection from "../../components/FormSection.jsx";
import ProfileStrength from "../../components/ProfileStrength.jsx";
import CandidateProfileSummary from "../../components/CandidateProfileSummary.jsx";
import ResumePreview from "../../components/ResumePreview.jsx";
import Button from "../../components/Button.jsx";
import EmptyStatePanel from "../../components/EmptyStatePanel.jsx";
import { ProfileNeededEmpty } from "../../components/EmptyState.jsx";
import { useToast } from "../../components/Toast.jsx";
import {
  apiErrorMessage,
  fetchMyProfileOrNull,
  uploadResume,
  upsertCandidateProfile,
} from "../../api/client.js";
import { notifyProfileUpdated } from "../../utils/profileEvents.js";
import { resumePreviewFromUpload } from "../../utils/resumeClean.js";
import {
  EMPTY_PROFILE_FIELDS,
  isCandidateProfileReady,
  profileFromApi,
  profileToPayload,
} from "../../utils/profileFields.js";
import { mergeExtractedIntoFields } from "../../utils/profileNormalize.js";
import { profileStrength, validateProfileFields } from "../../utils/validation.js";

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

export default function Profile() {
  const { showToast } = useToast();
  const [fields, setFields] = useState({ ...EMPTY_PROFILE_FIELDS, id: "" });
  const [fieldErrors, setFieldErrors] = useState({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [hasProfile, setHasProfile] = useState(false);
  const [editing, setEditing] = useState(false);
  const [reuploading, setReuploading] = useState(false);
  const [resumePreview, setResumePreview] = useState("");
  const fileRef = useRef(null);
  const errorRef = useRef(null);

  const strength = useMemo(() => profileStrength(fields), [fields]);

  useEffect(() => {
    fetchMyProfileOrNull()
      .then((profile) => {
        if (isCandidateProfileReady(profile)) {
          setHasProfile(true);
          setFields(profileFromApi(profile));
          setError("");
        } else {
          setHasProfile(false);
        }
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
      setFields((prev) => mergeExtractedIntoFields(prev, data.extracted_fields || {}));
      setResumePreview(resumePreviewFromUpload(data));
      showToast("Resume parsed — review updated fields and save.");
    } catch (err) {
      setError(apiErrorMessage(err, "Upload failed. Try a PDF, DOCX, or TXT under 5MB."));
      errorRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    } finally {
      setReuploading(false);
      if (fileRef.current) fileRef.current.value = "";
    }
  };

  const handleSave = async () => {
    const errors = validateProfileFields(fields);
    if (Object.keys(errors).length) {
      setFieldErrors(errors);
      scrollToFirstFieldError();
      return;
    }
    setSaving(true);
    setError("");
    setFieldErrors({});
    try {
      const saved = await upsertCandidateProfile(profileToPayload(fields));
      setFields(profileFromApi(saved));
      setHasProfile(true);
      setEditing(false);
      notifyProfileUpdated();
      showToast(
        hasProfile ? "Profile updated. You can refresh matches now." : "Profile saved.",
        <Link to="/candidate/matches" className="btn-secondary btn-sm">
          Find jobs
        </Link>,
      );
    } catch (err) {
      setError(apiErrorMessage(err, "Save failed. Check your details and try again."));
      errorRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
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

  if (!hasProfile) {
    return (
      <>
        <PageHeader
          eyebrow="Candidate"
          title="Your profile"
          subtitle="Upload your resume once — we'll pull skills, experience, and contact details for you."
          inlineAction={
            <Link to="/candidate/onboarding" className="btn-primary">
              Set up profile
            </Link>
          }
        />
        <EmptyStatePanel>
          <ProfileNeededEmpty
            action={
              <Link to="/candidate/onboarding" className="btn-primary">
                Set up profile
              </Link>
            }
          />
        </EmptyStatePanel>
      </>
    );
  }

  if (!editing) {
    return (
      <>
        <PageHeader
          eyebrow="Candidate"
          title="Your profile"
          subtitle="This is what employers see when reviewing your matches."
          inlineAction={
            <Link to="/candidate/matches" className="btn-secondary">
              Find jobs
            </Link>
          }
        />
        <section className="portal-panel portal-panel--elevated candidate-profile-panel">
          <CandidateProfileSummary
            fields={fields}
            strength={strength}
            onEdit={() => setEditing(true)}
            footer={
              <div className="candidate-profile-summary__footer-actions">
                <Link to="/candidate/matches" className="btn-primary">
                  Find jobs
                </Link>
                <Link to="/candidate/onboarding" className="btn-ghost btn-ghost--sm">
                  Re-upload resume
                </Link>
              </div>
            }
          />
        </section>
      </>
    );
  }

  return (
    <>
      <PageHeader
        eyebrow="Candidate"
        title="Edit profile"
        subtitle="Keep your skills and preferences up to date for better matches."
        inlineAction={
          <button type="button" className="btn-ghost btn-ghost--sm" onClick={() => setEditing(false)}>
            Cancel
          </button>
        }
      />
      <section className="portal-panel portal-panel--form candidate-profile-edit-panel">
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
              <button type="button" className="btn-secondary" onClick={() => setEditing(false)}>
                Cancel
              </button>
              <Button loading={saving} loadingLabel="Updating…" onClick={handleSave}>
                Update profile
              </Button>
            </div>
          }
        />
        {error && (
          <p ref={errorRef} className="auth-error" role="alert">
            {error}
          </p>
        )}
      </section>
    </>
  );
}
