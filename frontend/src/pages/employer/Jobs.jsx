import { useEffect, useRef, useState } from "react";
import PageHeader from "../../components/PageHeader.jsx";
import PortalSection from "../../components/PortalSection.jsx";
import JobPostingForm from "../../components/JobPostingForm.jsx";
import EmployerJobList from "../../components/EmployerJobList.jsx";
import Button from "../../components/Button.jsx";
import { useToast } from "../../components/Toast.jsx";
import {
  apiErrorMessage,
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

const JD_PASTE_MIN = 40;

function applyExtractionResponse(data, { setFields, setError, showToast, scrollToForm }) {
  if (data.llm_status === "ok") {
    setFields((prev) => ({ ...prev, ...jobFieldsFromExtracted(data.extracted_fields || {}) }));
    setError("");
    showToast("Details extracted — review the fields below.");
    scrollToForm?.();
    return;
  }
  const message =
    data.message || "Could not extract details automatically. Fill in the form manually.";
  setError(message);
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
  const [error, setError] = useState("");
  const fileRef = useRef(null);
  const formPanelRef = useRef(null);

  const load = () => {
    setLoading(true);
    fetchMyJobs()
      .then(setJobs)
      .catch(() => setJobs([]))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const openRoles = jobs.filter((job) => (job.status || "open") === "open");

  const scrollToForm = () => {
    formPanelRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const resetForm = () => {
    setFields(EMPTY_JOB_FIELDS);
    setFieldErrors({});
    setEditingJobId(null);
    setError("");
    setJdPaste("");
  };

  const handleExtraction = (data) => {
    applyExtractionResponse(data, { setFields, setError, showToast, scrollToForm });
  };

  const handleUpload = async (file) => {
    if (!file) return;
    setUploading(true);
    setError("");
    try {
      const data = await uploadJobDescription(file);
      handleExtraction(data);
    } catch (err) {
      setError(apiErrorMessage(err, "Upload failed. Try a PDF, DOCX, or TXT under 5MB."));
    } finally {
      setUploading(false);
      if (fileRef.current) fileRef.current.value = "";
    }
  };

  const handleExtractPaste = async () => {
    const text = jdPaste.trim();
    if (text.length < JD_PASTE_MIN) {
      setError(`Paste at least ${JD_PASTE_MIN} characters of job description text to extract.`);
      return;
    }
    setExtracting(true);
    setError("");
    try {
      const data = await parseJobDescriptionText(text);
      handleExtraction(data);
    } catch (err) {
      setError(apiErrorMessage(err, "Extraction failed. Try again or fill in the form manually."));
    } finally {
      setExtracting(false);
    }
  };

  const handleEdit = (job) => {
    setFields(jobFromApi(job));
    setEditingJobId(job.id);
    setFieldErrors({});
    setError("");
    scrollToForm();
  };

  const handleClose = async (job) => {
    if (!window.confirm(`Close "${job.title}"? Candidates will no longer be able to apply.`)) return;
    setClosingId(job.id);
    setError("");
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
      return;
    }
    setSaving(true);
    setError("");
    setFieldErrors({});
    try {
      if (editingJobId) {
        await updateEmployerJob(editingJobId, jobToPayload(fields, editingJobId));
        showToast("Role updated.");
      } else {
        await saveJobPosting(jobToPayload(fields));
        showToast("Role posted. You can find candidates from your active postings.");
      }
      resetForm();
      load();
    } catch (err) {
      setError(
        apiErrorMessage(err, editingJobId ? "Could not update role." : "Could not create job. Check the form and try again."),
      );
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
        subtitle="Manage postings and attract the right candidates."
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
        <PortalSection span={5} title="Your roles" description="Search, filter, and manage posted roles.">
          <EmployerJobList
            jobs={jobs}
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
              ? "Update role details — changes apply to future candidate matches."
              : "Add role details so candidates can be matched accurately."
          }
        >
          <div id="employer-post-role" ref={formPanelRef} className="employer-post-role-anchor" />

          <div className="jd-import-panel">
            <div className="jd-import-panel__head">
              <div className="jd-import-panel__intro">
                <h4 className="jd-import-panel__title">Import job description</h4>
                <p className="form-helper">
                  Paste a raw JD or upload a file — AI will pre-fill the form when extraction succeeds.
                </p>
              </div>
              <div className="jd-import-panel__upload">
                <input
                  ref={fileRef}
                  type="file"
                  accept=".pdf,.docx,.txt"
                  className="visually-hidden"
                  id="jd-upload"
                  onChange={(e) => handleUpload(e.target.files?.[0])}
                />
                <Button loading={uploading} loadingLabel="Parsing…" onClick={() => fileRef.current?.click()}>
                  Upload file
                </Button>
              </div>
            </div>

            <label className="jd-paste-field" htmlFor="jd-paste">
              <span className="jd-paste-field__label">Paste job description</span>
              <textarea
                id="jd-paste"
                className="jd-paste-field__textarea"
                rows={6}
                placeholder="Paste the full job description here — title, requirements, compensation, location, and responsibilities."
                value={jdPaste}
                onChange={(e) => setJdPaste(e.target.value)}
              />
              <span className="jd-paste-field__hint">
                {jdPaste.trim().length > 0
                  ? `${jdPaste.trim().length.toLocaleString()} characters`
                  : `At least ${JD_PASTE_MIN} characters needed`}
              </span>
            </label>

            <div className="jd-import-panel__actions">
              <Button
                loading={extracting}
                loadingLabel="Extracting…"
                onClick={handleExtractPaste}
                disabled={!canExtractPaste || uploading}
              >
                Extract details
              </Button>
            </div>
            {error && <p className="auth-error jd-import-error">{error}</p>}
          </div>

          <div className="employer-form-divider" aria-hidden="true" />

          <form className="employer-job-form" onSubmit={handleSubmit}>
            <JobPostingForm
              fields={fields}
              errors={fieldErrors}
              onChange={setFields}
              footer={
                <div className="form-actions form-actions--sticky portal-form-footer">
                  {editingJobId && (
                    <Button className="btn-secondary" type="button" onClick={resetForm}>
                      Cancel
                    </Button>
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
