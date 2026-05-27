import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import ProfileForm from "../../components/ProfileForm.jsx";
import ProfileStrength from "../../components/ProfileStrength.jsx";
import Button from "../../components/Button.jsx";
import { useToast } from "../../components/Toast.jsx";
import { fetchMyProfile, upsertCandidateProfile } from "../../api/client.js";
import { EMPTY_PROFILE_FIELDS, profileFromApi, profileToPayload } from "../../utils/profileFields.js";
import { profileStrength, validateProfileFields } from "../../utils/validation.js";

export default function Profile() {
  const { showToast } = useToast();
  const [fields, setFields] = useState({ ...EMPTY_PROFILE_FIELDS, id: "" });
  const [fieldErrors, setFieldErrors] = useState({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [hasProfile, setHasProfile] = useState(false);

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
        <PageHeader title="Your profile" />
        <section className="portal-panel portal-panel--form"><p>Loading…</p></section>
      </>
    );
  }

  if (error && !fields.name) {
    return (
      <>
        <PageHeader title="Your profile" subtitle="Create your candidate profile to start matching." />
        <section className="portal-panel portal-panel--form">
          <p>{error}</p>
          <Link to="/candidate/onboarding" className="btn-primary">Upload resume</Link>
        </section>
      </>
    );
  }

  return (
    <>
      <PageHeader title="Your profile" subtitle="Keep your skills and preferences up to date for better matches." />
      <section className="portal-panel portal-panel--form">
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
