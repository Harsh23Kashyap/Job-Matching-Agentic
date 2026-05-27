import { useEffect, useMemo, useRef, useState } from "react";
import { Link } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import ProfileForm from "../../components/ProfileForm.jsx";
import ProfileStrength from "../../components/ProfileStrength.jsx";
import Button from "../../components/Button.jsx";
import { useToast } from "../../components/Toast.jsx";
import { fetchMyProfile, uploadResume, upsertCandidateProfile } from "../../api/client.js";
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
  const fileRef = useRef(null);

  const strength = useMemo(() => profileStrength(fields), [fields]);

  useEffect(() => {
    fetchMyProfile()
      .then((p) => {
        setHasProfile(true);
        setFields(profileFromApi(p));
      })
      .catch(() => setError("No profile yet."))
      .finally(() => setLoading(false));
  }, []);

  const handleReupload = async (file) => {
    if (!file) return;
    setReuploading(true);
    setError("");
    try {
      const data = await uploadResume(file);
      setFields((prev) => ({ ...prev, ...fieldsFromExtracted(data.extracted_fields || {}) }));
      showToast("Resume parsed — review updated fields and save.");
    } catch (err) {
      setError(err.response?.data?.detail?.error || err.message || "Upload failed");
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
      await upsertCandidateProfile(profileToPayload(fields));
      setHasProfile(true);
      showToast(
        "Profile updated. You can refresh matches now.",
        <Link to="/candidate/matches" className="btn-secondary btn-sm">
          Find jobs
        </Link>,
      );
    } catch (err) {
      setError(err.response?.data?.detail?.error || err.message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <>
        <PageHeader eyebrow="Candidate" title="Your profile" />
        <section className="portal-panel portal-panel--form"><p>Loading…</p></section>
      </>
    );
  }

  if (error && !fields.name) {
    return (
      <>
        <PageHeader eyebrow="Candidate" title="Your profile" subtitle="Create your candidate profile to start matching." />
        <section className="portal-panel portal-panel--form">
          <p>{error}</p>
          <Link to="/candidate/onboarding" className="btn-primary">Upload resume</Link>
        </section>
      </>
    );
  }

  return (
    <>
      <PageHeader
        eyebrow="Candidate"
        title="Your profile"
        subtitle="Keep your skills and preferences up to date for better matches."
      />
      <section className="portal-panel portal-panel--form">
        <div className="profile-reupload-bar">
          <div>
            <h3 className="profile-form-section-title">Update from resume</h3>
            <p className="profile-form-section-helper">Upload a new PDF, DOCX, or TXT to refresh skills and contact fields.</p>
          </div>
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
        </div>
        <ProfileStrength percent={strength.percent} hint={strength.hint} />
        <ProfileForm
          fields={fields}
          errors={fieldErrors}
          onChange={setFields}
          footer={
            <div className="form-actions form-actions--sticky">
              <Button loading={saving} loadingLabel="Saving…" onClick={handleSave}>
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
