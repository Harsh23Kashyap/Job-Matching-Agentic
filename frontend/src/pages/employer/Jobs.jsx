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

export default function EmployerJobs() {
  const { showToast } = useToast();
  const [jobs, setJobs] = useState([]);
  const [fields, setFields] = useState(EMPTY_JOB_FIELDS);
  const [fieldErrors, setFieldErrors] = useState({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [closingId, setClosingId] = useState("");
  const [uploading, setUploading] = useState(false);
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
  };

  const handleUpload = async (file) => {
    if (!file) return;
    setUploading(true);
    setError("");
    try {
      const data = await uploadJobDescription(file);
      setFields((prev) => ({ ...prev, ...jobFieldsFromExtracted(data.extracted_fields || {}) }));
      showToast("Job description parsed — review the fields below.");
      scrollToForm();
    } catch (err) {
      setError(apiErrorMessage(err, "Upload failed. Try a PDF, DOCX, or TXT under 5MB."));
    } finally {
      setUploading(false);
      if (fileRef.current) fileRef.current.value = "";
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
          <div className="jd-upload-bar">
            <div className="jd-upload-bar-text">
              <h4 className="jd-upload-bar-title">Upload job description</h4>
              <p className="form-helper">PDF, DOCX, or TXT — fields below will pre-fill when parsing succeeds.</p>
            </div>
            <input
              ref={fileRef}
              type="file"
              accept=".pdf,.docx,.txt"
              className="visually-hidden"
              id="jd-upload"
              onChange={(e) => handleUpload(e.target.files?.[0])}
            />
            <Button loading={uploading} loadingLabel="Parsing…" onClick={() => fileRef.current?.click()}>
              Upload JD
            </Button>
          </div>

          <form className="employer-job-form" onSubmit={handleSubmit}>
            <JobPostingForm
              fields={fields}
              errors={fieldErrors}
              onChange={setFields}
              footer={
                <div className="form-actions form-actions--sticky profile-form-footer">
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
          {error && <p className="auth-error">{error}</p>}
        </PortalSection>
      </div>
    </>
  );
}
