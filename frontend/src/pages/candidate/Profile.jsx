import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import ProfileForm from "../../components/ProfileForm.jsx";
import ProfileFormFooter from "../../components/ProfileFormFooter.jsx";
import ProfileHelperPanel from "../../components/ProfileHelperPanel.jsx";
import FormSection from "../../components/FormSection.jsx";
import CandidateProfileSummary from "../../components/CandidateProfileSummary.jsx";
import ExtractedSectionsPanel from "../../components/ExtractedSectionsPanel.jsx";
import ResumeUploadZone from "../../components/ResumeUploadZone.jsx";
import ResumePreview from "../../components/ResumePreview.jsx";
import Button from "../../components/Button.jsx";
import EmptyStatePanel from "../../components/EmptyStatePanel.jsx";
import { ProfileNeededEmpty, ProfileIncompleteEmpty, ProfileStaleEmpty } from "../../components/EmptyState.jsx";
import { useToast } from "../../components/Toast.jsx";
import {
  apiErrorMessage,
  checkProfileQuality,
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
import { profileFieldsDirty } from "../../utils/profileDirty.js";
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

function ProfileEditShell({
  title,
  subtitle,
  inlineAction,
  fields,
  setFields,
  baselineFields,
  fieldErrors,
  setFieldErrors,
  error,
  errorRef,
  saving,
  onSave,
  onBack,
  backLabel = "Cancel",
  saveLabel = "Update profile",
  reuploading,
  uploadProgress,
  file,
  onFileChange,
  resumePreview,
  extractedSections,
  quality,
  qualityLoading,
  suggestedSkills,
  onAddSuggestedSkill,
  addingSkill,
  showIncompleteEmpty = false,
  allowCleanSave = false,
}) {
  const dirty = profileFieldsDirty(fields, baselineFields);
  const canSave = !saving && !reuploading && (dirty || allowCleanSave);

  return (
    <>
      <PageHeader eyebrow="Candidate" title={title} subtitle={subtitle} inlineAction={inlineAction} />
      {showIncompleteEmpty && (
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
      <div className="candidate-form-shell">
        <section className="portal-panel portal-panel--form candidate-profile-edit-panel">
          <FormSection
            title="Update from resume"
            helper="Upload a new PDF, DOCX, or TXT to refresh skills and contact fields."
            className="profile-reupload-bar"
          >
            <ResumeUploadZone
              file={file}
              onFileChange={onFileChange}
              uploading={reuploading}
              progress={uploadProgress}
            />
          </FormSection>
          {resumePreview && <ResumePreview text={resumePreview} defaultCollapsed />}
          <ExtractedSectionsPanel extracted={extractedSections || {}} />
          <ProfileForm
            fields={fields}
            errors={fieldErrors}
            onChange={setFields}
            suggestedSkills={suggestedSkills}
            onAddSuggestedSkill={onAddSuggestedSkill}
            addingSkill={addingSkill}
            footer={
              <ProfileFormFooter dirty={dirty}>
                {onBack && (
                  <button type="button" className="btn-secondary" onClick={onBack}>
                    {backLabel}
                  </button>
                )}
                <Button loading={saving} loadingLabel="Updating…" onClick={onSave} disabled={!canSave}>
                  {saveLabel}
                </Button>
              </ProfileFormFooter>
            }
          />
          {error && (
            <p ref={errorRef} className="auth-error" role="alert">
              {error}
            </p>
          )}
        </section>
        <ProfileHelperPanel
          fields={fields}
          quality={quality}
          loading={qualityLoading}
          extractedSections={extractedSections}
        />
      </div>
    </>
  );
}

export default function Profile() {
  const navigate = useNavigate();
  const { showToast } = useToast();
  const [fields, setFields] = useState({ ...EMPTY_PROFILE_FIELDS, id: "" });
  const [baselineFields, setBaselineFields] = useState(null);
  const [fieldErrors, setFieldErrors] = useState({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [profileRecord, setProfileRecord] = useState(null);
  const [editing, setEditing] = useState(false);
  const [reuploading, setReuploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [reuploadFile, setReuploadFile] = useState(null);
  const [resumePreview, setResumePreview] = useState("");
  const [extractedSections, setExtractedSections] = useState(null);
  const [parseStatus, setParseStatus] = useState(null);
  const [quality, setQuality] = useState(null);
  const [qualityLoading, setQualityLoading] = useState(false);
  const [addingSkill, setAddingSkill] = useState("");
  const errorRef = useRef(null);

  const profileReady = Boolean(profileRecord && isCandidateProfileReady(profileRecord));
  const hasQualityInput = Boolean(fields.name?.trim() || fields.skills?.trim() || fields.summary?.trim());
  const showQualityPanel = (editing || profileReady) && hasQualityInput;

  useEffect(() => {
    if (!showQualityPanel) {
      if (!editing && !profileReady) {
        setQuality(null);
        setQualityLoading(false);
      }
      return undefined;
    }
    let cancelled = false;
    const delay = editing ? 450 : 0;
    const timer = window.setTimeout(async () => {
      setQualityLoading(true);
      try {
        const report = await checkProfileQuality(profileToPayload(fields), {
          llmStatus: editing ? parseStatus : null,
        });
        if (!cancelled) setQuality(report);
      } catch {
        if (!cancelled) setQuality(null);
      } finally {
        if (!cancelled) setQualityLoading(false);
      }
    }, delay);
    return () => {
      cancelled = true;
      window.clearTimeout(timer);
    };
  }, [fields, editing, profileReady, showQualityPanel, parseStatus]);

  useEffect(() => {
    if (!reuploading) {
      setUploadProgress(0);
      return undefined;
    }
    setUploadProgress(12);
    const id = window.setInterval(() => {
      setUploadProgress((p) => (p >= 88 ? p : p + 9));
    }, 280);
    return () => window.clearInterval(id);
  }, [reuploading]);

  const handleReuploadFileChange = (file) => {
    setReuploadFile(file);
    if (file) handleReupload(file);
  };

  const handleAddSuggestedSkill = (skill) => {
    if (!editing) setEditing(true);
    setAddingSkill(skill);
    setFields((prev) => ({
      ...prev,
      skills: mergeSkills(prev.skills, [skill]).join(", "),
    }));
    setAddingSkill("");
    showToast(`Added ${skill} to your skills.`);
  };

  useEffect(() => {
    fetchMyProfileOrNull()
      .then((profile) => {
        if (!hasCandidateProfile(profile)) {
          setProfileRecord(null);
          return;
        }
        setProfileRecord(profile);
        const mapped = profileFromApi(profile);
        setFields(mapped);
        setBaselineFields(mapped);
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
      setExtractedSections(data.extracted_fields || null);
      setParseStatus(data.llm_status || null);
      setQuality(data.quality || null);
      setFields((prev) => mergeExtractedIntoFields(prev, data.extracted_fields || {}));
      setResumePreview(resumePreviewFromUpload(data));
      setUploadProgress(100);
      showToast("Resume parsed. Review quality tips and updates, then save.");
    } catch (err) {
      setError(apiErrorMessage(err, "Upload failed. Try a PDF, DOCX, or TXT under 5MB."));
      errorRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    } finally {
      setReuploading(false);
      setReuploadFile(null);
    }
  };

  const handleCancelEdit = () => {
    if (profileRecord) {
      const mapped = profileFromApi(profileRecord);
      setFields(mapped);
      setBaselineFields(mapped);
    }
    setFieldErrors({});
    setResumePreview("");
    setExtractedSections(null);
    setParseStatus(null);
    setReuploadFile(null);
    setEditing(false);
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
    const wasFirstSave = !profileRecord;
    try {
      const saved = await upsertCandidateProfile(profileToPayload(fields));
      const mapped = profileFromApi(saved);
      setFields(mapped);
      setBaselineFields(mapped);
      setProfileRecord(saved);
      setEditing(false);
      notifyProfileUpdated();
      if (wasFirstSave) {
        navigate("/candidate/matches", { state: { searchAfterSave: true } });
        return;
      }
      showToast(
        "Profile updated.",
        <Link to="/candidate/matches" className="btn-secondary btn-sm">
          Find matching jobs
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
        <EmptyStatePanel>
          <ProfileStaleEmpty />
        </EmptyStatePanel>
        <ProfileEditShell
          title="Restore your profile"
          subtitle="Re-save your details to reload your profile and run job search again."
          fields={fields}
          setFields={setFields}
          baselineFields={baselineFields}
          fieldErrors={fieldErrors}
          setFieldErrors={setFieldErrors}
          error={error}
          errorRef={errorRef}
          saving={saving}
          onSave={handleSave}
          reuploading={reuploading}
          uploadProgress={uploadProgress}
          file={reuploadFile}
          onFileChange={handleReuploadFileChange}
          resumePreview={resumePreview}
          extractedSections={extractedSections}
          quality={quality}
          qualityLoading={qualityLoading}
          suggestedSkills={quality?.skill_suggestions || []}
          onAddSuggestedSkill={handleAddSuggestedSkill}
          addingSkill={addingSkill}
          saveLabel="Save profile"
          allowCleanSave
        />
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
      <ProfileEditShell
        title={isCandidateProfileReady(profileRecord) ? "Edit profile" : "Finish your profile"}
        subtitle={
          isCandidateProfileReady(profileRecord)
            ? "Update skills and preferences so matches stay accurate."
            : "Your account already has profile data. Add a name and save to enable job search."
        }
        inlineAction={
          isCandidateProfileReady(profileRecord) ? (
            <button type="button" className="btn-ghost btn-ghost--sm" onClick={handleCancelEdit}>
              Cancel
            </button>
          ) : (
            <Link to="/candidate/matches" className="btn-secondary">
              Find matching jobs
            </Link>
          )
        }
        fields={fields}
        setFields={setFields}
        baselineFields={baselineFields}
        fieldErrors={fieldErrors}
        setFieldErrors={setFieldErrors}
        error={error}
        errorRef={errorRef}
        saving={saving}
        onSave={handleSave}
        onBack={isCandidateProfileReady(profileRecord) ? handleCancelEdit : undefined}
        backLabel="Cancel"
        reuploading={reuploading}
        uploadProgress={uploadProgress}
        file={reuploadFile}
        onFileChange={handleReuploadFileChange}
        resumePreview={resumePreview}
        extractedSections={extractedSections}
        quality={quality}
        qualityLoading={qualityLoading}
        suggestedSkills={quality?.skill_suggestions || []}
        onAddSuggestedSkill={handleAddSuggestedSkill}
        addingSkill={addingSkill}
        showIncompleteEmpty={!isCandidateProfileReady(profileRecord)}
        allowCleanSave={!isCandidateProfileReady(profileRecord)}
      />
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
            Find matching jobs
          </Link>
        }
      />
      <div className="candidate-form-shell">
        <section className="portal-panel portal-panel--elevated candidate-profile-panel">
          <CandidateProfileSummary
            fields={fields}
            quality={quality}
            qualityLoading={qualityLoading}
            onEdit={() => setEditing(true)}
            footer={
              <div className="candidate-profile-summary__footer-actions">
                <Link to="/candidate/matches" className="btn-primary">
                  Find matching jobs
                </Link>
                <Link to="/candidate/onboarding" className="btn-ghost btn-ghost--sm">
                  Re-upload resume
                </Link>
              </div>
            }
          />
        </section>
        <ProfileHelperPanel
          fields={fields}
          quality={quality}
          loading={qualityLoading}
          extractedSections={extractedSections}
          hideScore
        />
      </div>
    </>
  );
}
