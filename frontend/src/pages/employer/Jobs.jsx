import { useEffect, useRef, useState } from "react";
import PageHeader from "../../components/PageHeader.jsx";
import PortalSection from "../../components/PortalSection.jsx";
import JobPostingForm from "../../components/JobPostingForm.jsx";
import EmployerJobList from "../../components/EmployerJobList.jsx";
import JdImportPanel from "../../components/JdImportPanel.jsx";
import JobQualityPanel from "../../components/JobQualityPanel.jsx";
import FormFeedback from "../../components/FormFeedback.jsx";
import Button from "../../components/Button.jsx";
import { useToast } from "../../components/Toast.jsx";
import {
  apiErrorMessage,
  checkJobQuality,
  fetchMyJobs,
  parseJobDescriptionText,
  saveJobPosting,
  updateEmployerJob,
  updateEmployerJobStatus,
  uploadJobDescription,
} from "../../api/client.js";
import {
  EMPTY_JOB_FIELDS,
  jobFieldsFromExtracted,
  jobFromApi,
  jobToPayload,
  validateJobFields,
} from "../../utils/jobFields.js";
import { mergeSkills } from "../../utils/skills.js";

const JD_PASTE_MIN = 40;

function scrollToFirstFieldError() {
  requestAnimationFrame(() => {
    const target =
      document.querySelector(".employer-job-form .form-field .field-error") ||
      document.querySelector(".employer-job-form .form-field.has-error") ||
      document.querySelector(".employer-job-form .skills-chips-input.has-error") ||
      document.querySelector(".employer-job-form .compensation-input.has-error");
    target?.scrollIntoView({ behavior: "smooth", block: "center" });
  });
}

function applyExtractionResponse(data, { setFields, setJdError, setQuality, showToast, scrollToForm }) {
  const extracted = data.extracted_fields || {};
  const hasExtracted = Boolean(
    extracted.title
      || (extracted.required_skills || []).length
      || extracted.description,
  );

  if (data.llm_status === "ok" || hasExtracted) {
    setFields((prev) => ({ ...prev, ...jobFieldsFromExtracted(extracted) }));
    setQuality(data.quality || null);
    setJdError("");
    if (data.llm_status === "ok") {
      showToast("Details extracted. Review the form and job quality tips below.");
    } else {
      showToast("Partial extraction applied. Review fields and quality tips below.");
    }
    scrollToForm?.();
    return;
  }

  if (data.quality) {
    setQuality(data.quality);
  }
  const message =
    data.message || "Extraction didn't work. Fill in the form yourself.";
  setJdError(message);
  showToast(message, "error");
}

export default function EmployerJobs() {
  const { showToast } = useToast();
  const [jobs, setJobs] = useState([]);
  const [fields, setFields] = useState(EMPTY_JOB_FIELDS);
  const [fieldErrors, setFieldErrors] = useState({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [closingId, setClosingId] = useState("");
  const [uploading, setUploading] = useState(false);
  const [extracting, setExtracting] = useState(false);
  const [jdPaste, setJdPaste] = useState("");
  const [editingJobId, setEditingJobId] = useState(null);
  const [jdError, setJdError] = useState("");
  const [formError, setFormError] = useState("");
  const [quality, setQuality] = useState(null);
  const [qualityLoading, setQualityLoading] = useState(false);
  const [addingSkill, setAddingSkill] = useState("");
  const fileRef = useRef(null);
  const formPanelRef = useRef(null);
  const formFeedbackRef = useRef(null);

  const load = () => {
    setLoading(true);
    return fetchMyJobs()
      .then(setJobs)
      .catch((err) => {
        showToast(apiErrorMessage(err, "Could not load your roles. Try again."), "error");
      })
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const openRoles = jobs.filter((job) => (job.status || "open") === "open");
  const editingJob = editingJobId ? jobs.find((j) => j.id === editingJobId) : null;

  const scrollToForm = () => {
    formPanelRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const resetForm = () => {
    setFields(EMPTY_JOB_FIELDS);
    setFieldErrors({});
    setEditingJobId(null);
    setFormError("");
    setJdError("");
    setJdPaste("");
    setQuality(null);
  };

  const hasQualityInput = Boolean(
    fields.title?.trim() || fields.required_skills?.trim() || fields.description?.trim(),
  );

  useEffect(() => {
    if (!hasQualityInput) {
      setQuality(null);
      setQualityLoading(false);
      return undefined;
    }
    let cancelled = false;
    const timer = window.setTimeout(async () => {
      setQualityLoading(true);
      try {
        const report = await checkJobQuality(jobToPayload(fields));
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
  }, [fields, hasQualityInput]);

  const handleAddSuggestedSkill = async (skill) => {
    setAddingSkill(skill);
    setFields((prev) => ({
      ...prev,
      required_skills: mergeSkills(prev.required_skills, [skill]).join(", "),
    }));
    setAddingSkill("");
    showToast(`Added ${skill} to required skills.`);
  };

  const handleExtraction = (data) => {
    applyExtractionResponse(data, { setFields, setJdError, setQuality, showToast, scrollToForm });
  };

  const handleUpload = async (file) => {
    if (!file) return;
    setUploading(true);
    setJdError("");
    try {
      const data = await uploadJobDescription(file);
      handleExtraction(data);
    } catch (err) {
      setJdError(apiErrorMessage(err, "Upload failed. Try a PDF, DOCX, or TXT under 5MB."));
    } finally {
      setUploading(false);
      if (fileRef.current) fileRef.current.value = "";
    }
  };

  const handleExtractPaste = async () => {
    const text = jdPaste.trim();
    if (text.length < JD_PASTE_MIN) {
      setJdError(`Paste at least ${JD_PASTE_MIN} characters of job description text to extract.`);
      return;
    }
    setExtracting(true);
    setJdError("");
    try {
      const data = await parseJobDescriptionText(text);
      handleExtraction(data);
    } catch (err) {
      setJdError(apiErrorMessage(err, "Extraction failed. Try again or fill in the form manually."));
    } finally {
      setExtracting(false);
    }
  };

  const handleEdit = (job) => {
    setFields(jobFromApi(job));
    setEditingJobId(job.id);
    setFieldErrors({});
    setFormError("");
    setJdError("");
    scrollToForm();
  };

  const handleClose = async (job) => {
    if (!window.confirm(`Close "${job.title}"? Candidates will no longer be able to apply.`)) return;
    setClosingId(job.id);
    setFormError("");
    try {
      await updateEmployerJobStatus(job.id, "closed");
      showToast("Role closed.");
      load();
    } catch (err) {
      showToast(apiErrorMessage(err, "Could not close role."), "error");
    } finally {
      setClosingId("");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const errors = validateJobFields(fields);
    if (Object.keys(errors).length) {
      setFieldErrors(errors);
      setFormError("Fix the highlighted fields below, then try again.");
      scrollToFirstFieldError();
      formFeedbackRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
      return;
    }
    setSaving(true);
    setFormError("");
    setFieldErrors({});
    try {
      if (editingJobId) {
        const updated = await updateEmployerJob(editingJobId, jobToPayload(fields, editingJobId));
        setJobs((prev) => prev.map((j) => (j.id === updated.id ? { ...j, ...updated } : j)));
        showToast("Role updated.");
      } else {
        const created = await saveJobPosting(jobToPayload(fields));
        setJobs((prev) => {
          const idx = prev.findIndex((j) => j.id === created.id);
          if (idx >= 0) {
            const next = [...prev];
            next[idx] = { ...next[idx], ...created };
            return next;
          }
          return [created, ...prev];
        });
        showToast("Role posted. Find candidates from your active postings.");
      }
      resetForm();
      load();
    } catch (err) {
      const message = apiErrorMessage(
        err,
        editingJobId ? "Could not update role." : "Could not post role. Check the form and try again.",
      );
      setFormError(message);
      formFeedbackRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    } finally {
      setSaving(false);
    }
  };

  const canExtractPaste = jdPaste.trim().length >= JD_PASTE_MIN;

  return (
    <>
      <PageHeader
        eyebrow="Employer"
        title="My jobs"
        subtitle="Manage postings and publish new roles."
        stats={
          !loading
            ? [
                { label: "Open roles", value: openRoles.length },
                { label: "Remote-friendly", value: jobs.filter((j) => j.remote_policy).length },
              ]
            : []
        }
      />

      <div className="employer-jobs-grid">
        <PortalSection
          span={5}
          className="employer-jobs-list-panel"
          title="Active postings"
          description="Search and manage open and closed roles."
        >
          <EmployerJobList
            jobs={jobs}
            openCount={openRoles.length}
            loading={loading}
            onEdit={handleEdit}
            onClose={handleClose}
            closingId={closingId}
            onPostRole={scrollToForm}
          />
        </PortalSection>

        <PortalSection
          span={7}
          className="employer-posting-panel"
          title={editingJobId ? "Edit role" : "Post a new role"}
          description={
            editingJobId
              ? "Updates apply to future candidate matches."
              : "Fill in the form or import a job description."
          }
        >
          <div id="employer-post-role" ref={formPanelRef} className="employer-post-role-anchor" />

          {editingJobId && editingJob && (
            <FormFeedback
              variant="info"
              title={`Editing: ${editingJob.title}`}
              message="Save changes when you're done, or cancel to discard."
            />
          )}

          <JdImportPanel
            paste={jdPaste}
            onPasteChange={setJdPaste}
            pasteMin={JD_PASTE_MIN}
            onExtractPaste={handleExtractPaste}
            extracting={extracting}
            canExtractPaste={canExtractPaste}
            onUploadClick={() => fileRef.current?.click()}
            uploading={uploading}
            error={jdError}
            fileInputRef={fileRef}
            onFileChange={handleUpload}
          />

          <div className="employer-form-divider">
            <span>Role details</span>
          </div>

          {(hasQualityInput || qualityLoading) && (
            <JobQualityPanel
              quality={quality}
              loading={qualityLoading}
              onAddSkill={handleAddSuggestedSkill}
              addingSkill={addingSkill}
            />
          )}

          <form className="employer-job-form" onSubmit={handleSubmit} noValidate>
            <div ref={formFeedbackRef}>
              {formError && (
                <FormFeedback variant="error" title="Could not save role" message={formError} />
              )}
            </div>

            <JobPostingForm
              fields={fields}
              errors={fieldErrors}
              onChange={setFields}
              footer={
                <div className="form-actions form-actions--sticky portal-form-footer employer-form-footer">
                  {editingJobId ? (
                    <Button className="btn-secondary" type="button" onClick={resetForm}>
                      Cancel
                    </Button>
                  ) : (
                    <span className="employer-form-footer__hint form-helper">
                      Job title required. Skills and pay range improve match quality.
                    </span>
                  )}
                  <Button
                    loading={saving}
                    loadingLabel={editingJobId ? "Saving…" : "Posting…"}
                    type="submit"
                  >
                    {editingJobId ? "Save changes" : "Post role"}
                  </Button>
                </div>
              }
            />
          </form>
        </PortalSection>
      </div>
    </>
  );
}
