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
import { ProfileNeededEmpty, ProfileIncompleteEmpty, ProfileStaleEmpty } from "../../components/EmptyState.jsx";
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
  hasCandidateProfile,
  isCandidateProfileReady,
  isProfileStale,
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
  const [profileRecord, setProfileRecord] = useState(null);
  const [editing, setEditing] = useState(false);
  const [reuploading, setReuploading] = useState(false);
  const [resumePreview, setResumePreview] = useState("");
  const fileRef = useRef(null);
  const errorRef = useRef(null);

  const strength = useMemo(() => profileStrength(fields), [fields]);

  useEffect(() => {
    fetchMyProfileOrNull()
      .then((profile) => {
        if (!hasCandidateProfile(profile)) {
          setProfileRecord(null);
          return;
        }
        setProfileRecord(profile);
        setFields(profileFromApi(profile));
        setError("");
        setEditing(isProfileStale(profile) || !isCandidateProfileReady(profile));
      })
      .catch(() => {
        setProfileRecord(null);
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
      showToast("Resume parsed. Review the updates, then save.");
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
      setProfileRecord(saved);
      setEditing(false);
      notifyProfileUpdated();
      showToast(
        profileRecord ? "Profile updated." : "Profile saved.",
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

  if (isProfileStale(profileRecord)) {
    return (
      <>
        <PageHeader
          eyebrow="Candidate"
          title="Restore your profile"
          subtitle="Re-save your details to reload your profile and run job search again."
        />
        <EmptyStatePanel>
          <ProfileStaleEmpty />
        </EmptyStatePanel>
        <section className="portal-panel portal-panel--form candidate-profile-edit-panel">
          <ProfileStrength percent={strength.percent} hint={strength.hint} />
          <ProfileForm
            fields={fields}
            errors={fieldErrors}
            onChange={setFields}
            footer={
              <div className="form-actions form-actions--sticky portal-form-footer">
                <Button loading={saving} loadingLabel="Saving…" onClick={handleSave}>
                  Save profile
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

  if (!profileRecord) {
    return (
      <>
        <PageHeader
          eyebrow="Candidate"
          title="Your profile"
          subtitle="Upload a resume to pull in skills, experience, and contact details."
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

  if (!isCandidateProfileReady(profileRecord) || editing) {
    return (
      <>
        <PageHeader
          eyebrow="Candidate"
          title={isCandidateProfileReady(profileRecord) ? "Edit profile" : "Finish your profile"}
          subtitle={
            isCandidateProfileReady(profileRecord)
              ? "Update skills and preferences so matches stay accurate."
              : "Your account already has profile data. Add a name and save to enable job search."
          }
          inlineAction={
            isCandidateProfileReady(profileRecord) ? (
              <button type="button" className="btn-ghost btn-ghost--sm" onClick={() => setEditing(false)}>
                Cancel
              </button>
            ) : (
              <Link to="/candidate/matches" className="btn-secondary">
                Jobs
              </Link>
            )
          }
        />
        {!isCandidateProfileReady(profileRecord) && (
          <EmptyStatePanel>
            <ProfileIncompleteEmpty
              action={
                <button type="button" className="btn-secondary" onClick={() => document.getElementById("pf-name")?.focus()}>
                  Add your name
                </button>
              }
            />
          </EmptyStatePanel>
        )}
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
                {isCandidateProfileReady(profileRecord) && (
                  <button type="button" className="btn-secondary" onClick={() => setEditing(false)}>
                    Cancel
                  </button>
                )}
                <Button loading={saving} loadingLabel="Saving…" onClick={handleSave}>
                  Save profile
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

  return (
    <>
      <PageHeader
        eyebrow="Candidate"
        title="Your profile"
        subtitle="What employers see when they review your matches."
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
