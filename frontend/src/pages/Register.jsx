import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth, ROLE_HOME } from "../context/AuthContext.jsx";

const ROLES = [
  { value: "candidate", label: "Candidate", hint: "Upload resume and find jobs" },
  { value: "employer", label: "Employer", hint: "Post jobs and find candidates" },
  { value: "admin", label: "Admin", hint: "Full match console and eval tools" },
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
      setError(err.response?.data?.detail?.error || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card auth-card-wide">
        <h1>Create account</h1>
        <p className="auth-sub">Choose your role to get the right portal experience.</p>
        <form onSubmit={handleSubmit} className="auth-form">
          <label>
            Email
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </label>
          <label>
            Password
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              minLength={6}
              required
            />
          </label>
          <fieldset className="role-picker">
            <legend>Role</legend>
            {ROLES.map((r) => (
              <label key={r.value} className={`role-option ${role === r.value ? "selected" : ""}`}>
                <input
                  type="radio"
                  name="role"
                  value={r.value}
                  checked={role === r.value}
                  onChange={() => setRole(r.value)}
                />
                <span>
                  <strong>{r.label}</strong>
                  <small>{r.hint}</small>
                </span>
              </label>
            ))}
          </fieldset>
          {error && <p className="auth-error">{error}</p>}
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? "Creating…" : "Create account"}
          </button>
        </form>
        <p className="auth-footer">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
