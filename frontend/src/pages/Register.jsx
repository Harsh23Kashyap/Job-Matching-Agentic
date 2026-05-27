import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiErrorMessage } from "../api/client.js";
import { useAuth, ROLE_HOME } from "../context/AuthContext.jsx";
import { IconCheck, IconBriefcase, IconConsole, IconProfile } from "../components/icons.jsx";
import AuthLayout from "../layouts/AuthLayout.jsx";

const ROLES = [
  { value: "candidate", label: "Candidate", hint: "Upload a resume and browse matched roles", icon: IconProfile },
  { value: "employer", label: "Employer", hint: "Post openings and review ranked applicants", icon: IconBriefcase },
  { value: "admin", label: "Admin", hint: "Run matching experiments and system checks", icon: IconConsole },
];

export default function Register() {
  const { register, user } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("candidate");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  if (user) {
    navigate(ROLE_HOME[user.role] || "/", { replace: true });
    return null;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const me = await register(email, password, role);
      if (me.role === "candidate") {
        navigate("/candidate/onboarding");
      } else {
        navigate(ROLE_HOME[me.role] || "/");
      }
    } catch (err) {
      setError(apiErrorMessage(err, "Registration failed"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout variant="register" title="Create your account" subtitle="Choose your workspace — we'll send you to the right place.">
      <form onSubmit={handleSubmit} className="auth-form auth-form--register">
        <label>
          Email
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoComplete="email"
            placeholder="you@example.com"
          />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            minLength={6}
            required
            autoComplete="new-password"
            placeholder="••••••••"
          />
        </label>
        <fieldset className="role-picker">
          <legend>I'm joining as a…</legend>
          {ROLES.map((r) => {
            const RoleIcon = r.icon;
            return (
            <label key={r.value} className={`role-option ${role === r.value ? "selected" : ""}`}>
              <input
                type="radio"
                name="role"
                value={r.value}
                checked={role === r.value}
                onChange={() => setRole(r.value)}
              />
              <span className="role-card-inner">
                <span className="role-card-icon" aria-hidden="true">
                  <RoleIcon size={18} />
                </span>
                <span className="role-card-text">
                  <strong>{r.label}</strong>
                  <small>{r.hint}</small>
                </span>
                <span className="role-card-check" aria-hidden="true">
                  {role === r.value && <IconCheck size={12} />}
                </span>
              </span>
            </label>
            );
          })}
        </fieldset>
        {error && <p className="auth-error">{error}</p>}
        <button type="submit" className="btn-primary btn-block" disabled={loading}>
          {loading ? "Creating account…" : "Create account"}
        </button>
        <p className="auth-hint">Most people choose Candidate or Employer. You can update your profile after sign-up.</p>
      </form>
      <p className="auth-footer">
        Already registered? <Link to="/login">Sign in</Link>
      </p>
    </AuthLayout>
  );
}
