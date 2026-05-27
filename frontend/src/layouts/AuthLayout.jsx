import { Link } from "react-router-dom";
import BackgroundOrnaments from "../components/BackgroundOrnaments.jsx";
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
    <div className="auth-page">
      <BackgroundOrnaments variant="auth" scope="auth" />
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
            Ranked matches for candidates and hiring teams. Clear profiles, no inbox clutter.
          </p>
          <AuthMiniCards />
          <ul className="auth-features">
            <li>Match scores with a short explanation</li>
            <li>Separate portals for job seekers and employers</li>
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
    </div>
  );
}
