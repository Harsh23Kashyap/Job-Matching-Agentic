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

export default function AuthLayout({ children, title, subtitle }) {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="auth-split">
      <aside className="auth-brand">
        <AuthBlobs />
        <div className="auth-brand-inner">
          <Link to="/" className="auth-brand-logo">
            <Logo size={40} />
            <span>JobMatch</span>
          </Link>
          <h1>Find roles that actually fit</h1>
          <p className="auth-tagline">For candidates, employers, and teams.</p>
          <AuthMiniCards />
          <ul className="auth-features">
            <li>Match on skills and experience, not buzzwords</li>
            <li>Separate portals for each role</li>
          </ul>
        </div>
        <AuthMatchingScene />
        <p className="auth-trust-strip">Built for candidates · employers · hiring teams</p>
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
        <div className="auth-panel-center">
          <div className="auth-card">
            <h1>{title}</h1>
            {subtitle && <p className="auth-sub">{subtitle}</p>}
            {children}
          </div>
        </div>
      </main>
    </div>
  );
}
