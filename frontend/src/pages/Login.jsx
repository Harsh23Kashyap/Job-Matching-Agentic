import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { apiErrorMessage } from "../api/client.js";
import { useAuth, ROLE_HOME } from "../context/AuthContext.jsx";
import { DEMO_ACCOUNTS } from "../constants/demoAccounts.js";
import AuthLayout from "../layouts/AuthLayout.jsx";

export default function Login() {
  const { login, user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from;
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
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
      const me = await login(email, password);
      navigate(from || ROLE_HOME[me.role] || "/");
    } catch (err) {
      setError(apiErrorMessage(err, "Login failed"));
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = async (account) => {
    setEmail(account.email);
    setPassword(account.password);
    setLoading(true);
    setError("");
    try {
      const me = await login(account.email, account.password);
      navigate(from || ROLE_HOME[me.role] || "/");
    } catch (err) {
      setError(apiErrorMessage(err, "Demo login failed — restart the backend to seed demo accounts."));
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout title="Sign in" subtitle="Use your account or try a demo login below.">
      <form onSubmit={handleSubmit} className="auth-form">
        <label>
          Email
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required autoComplete="email" placeholder="you@example.com" />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoComplete="current-password"
            placeholder="••••••••"
          />
        </label>
        {error && <p className="auth-error">{error}</p>}
        <button type="submit" className="btn-primary btn-block" disabled={loading}>
          {loading ? "Signing in…" : "Sign in"}
        </button>
      </form>

      <div className="demo-accounts">
        <p className="demo-accounts-title">Demo accounts</p>
        <p className="demo-accounts-sub">Password for all: <code>demo1234</code></p>
        <ul className="demo-accounts-list">
          {DEMO_ACCOUNTS.map((account) => (
            <li key={account.id}>
              <button
                type="button"
                className="demo-account-btn"
                disabled={loading}
                onClick={() => handleDemoLogin(account)}
              >
                <span className="demo-account-label">{account.label}</span>
                <span className="demo-account-email">{account.email}</span>
                <span className="demo-account-hint">{account.hint}</span>
              </button>
            </li>
          ))}
        </ul>
      </div>

      <p className="auth-footer">
        New here? <Link to="/register">Create an account</Link>
      </p>
    </AuthLayout>
  );
}
