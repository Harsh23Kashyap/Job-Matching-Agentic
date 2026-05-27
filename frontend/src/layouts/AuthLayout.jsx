import { Link } from "react-router-dom";
import {
  AuthBlobs,
  AuthDividerShadow,
  AuthMatchingScene,
  AuthMiniCards,
  AuthRightDecor,
} from "../components/AuthIllustrations.jsx";
import { Logo, IconMoon, IconSun } from "../components/icons.jsx";
import { useTheme } from "../hooks/useTheme.js";

export default function AuthLayout({ children, title, subtitle, variant = "login" }) {
  const { theme, toggleTheme } = useTheme();
  const isRegister = variant === "register";

  return (
    <div className="auth-split">
      <aside className="auth-brand">
        <AuthBlobs />
        <div className="auth-brand-inner">
          <Link to="/" className="auth-brand-logo">
            <Logo size={40} />
            <span>JobMatch</span>
          </Link>
          <h1>Match people to roles that fit</h1>
          <p className="auth-tagline">
            A hiring workspace for candidates and employers — ranked matches, clear profiles, no spam inbox.
          </p>
          <AuthMiniCards />
          <ul className="auth-features">
            <li>See why a role or candidate scored the way it did</li>
            <li>Separate workspaces for job seekers and hiring teams</li>
          </ul>
        </div>
        <AuthMatchingScene />
        <p className="auth-trust-strip">Candidates · Employers · Hiring ops</p>
        <div className="auth-brand-bg" aria-hidden="true" />
      </aside>

      <AuthDividerShadow />

      <main className="auth-form-panel">
        <AuthRightDecor />
        <div className="auth-form-top">
          <button type="button" className="theme-toggle" onClick={toggleTheme} aria-label="Toggle theme">
            {theme === "light" ? <IconMoon /> : <IconSun />}
          </button>
        </div>
        <div className={`auth-panel-center${isRegister ? " auth-panel-center--register" : ""}`}>
          <div className={`auth-card${isRegister ? " auth-card--register" : ""}`}>
            <h1>{title}</h1>
            {subtitle && <p className="auth-sub">{subtitle}</p>}
            {children}
          </div>
        </div>
      </main>
    </div>
  );
}
