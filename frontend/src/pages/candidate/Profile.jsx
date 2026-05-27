import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import ProfileForm from "../../components/ProfileForm.jsx";
import ProfileStrength from "../../components/ProfileStrength.jsx";
import Button from "../../components/Button.jsx";
import { useToast } from "../../components/Toast.jsx";
import { fetchMyProfile, saveCandidateProfile } from "../../api/client.js";
import { parseInr } from "../../utils/format.js";
import { profileStrength, validateProfileFields } from "../../utils/validation.js";

const EMPTY = {
  name: "",
  skills: "",
  experience_years: 0,
  preferred_salary: "",
  remote_preference: false,
  summary: "",
};

export default function Profile() {
  const { showToast } = useToast();
  const [fields, setFields] = useState({ ...EMPTY, id: "" });
  const [fieldErrors, setFieldErrors] = useState({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const strength = useMemo(() => profileStrength(fields), [fields]);

  useEffect(() => {
    fetchMyProfile()
      .then((p) => {
        setFields({
          id: p.id,
          name: p.name || "",
          skills: (p.skills || []).join(", "),
          experience_years: p.experience_years ?? 0,
          preferred_salary: p.preferred_salary ?? "",
          remote_preference: p.remote_preference ?? false,
          summary: p.summary || "",
        });
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
      await saveCandidateProfile({
        id: fields.id,
        name: fields.name.trim(),
        skills: fields.skills.split(",").map((s) => s.trim()).filter(Boolean),
        experience_years: Number(fields.experience_years) || 0,
        preferred_salary: parseInr(fields.preferred_salary),
        remote_preference: fields.remote_preference,
        summary: fields.summary,
      });
      showToast(
        "Profile saved. Your matches are ready to refresh.",
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
        <section className="portal-panel"><p>Loading…</p></section>
      </>
    );
  }

  if (error && !fields.name) {
    return (
      <>
        <PageHeader title="Your profile" subtitle="Create your candidate profile to start matching." />
        <section className="portal-panel">
          <p>{error}</p>
          <Link to="/candidate/onboarding" className="btn-primary">Upload resume</Link>
        </section>
      </>
    );
  }

  return (
    <>
      <PageHeader title="Your profile" subtitle="Keep your skills and preferences up to date for better matches." />
      <section className="portal-panel">
        <ProfileStrength percent={strength.percent} hint={strength.hint} />
        <ProfileForm
          fields={fields}
          errors={fieldErrors}
          onChange={setFields}
          footer={
            <Button loading={saving} loadingLabel="Saving…" onClick={handleSave}>
              Save changes
            </Button>
          }
        />
        {error && <p className="auth-error">{error}</p>}
      </section>
    </>
  );
}
