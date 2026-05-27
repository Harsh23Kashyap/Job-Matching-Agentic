import { Link, useLocation, useNavigate, useParams } from "react-router-dom";
import { Logo, IconMoon, IconSun } from "../../components/icons.jsx";
import { ROLE_HOME, useAuth } from "../../context/AuthContext.jsx";
import { useTheme } from "../../hooks/useTheme.js";
import { ERROR_CODES, ERROR_CONTENT } from "./errorConfig.js";
import { ErrorIllustration } from "./ErrorIllustrations.jsx";

export default function ErrorPage({ code: codeProp }) {
  const { code: codeParam } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useAuth();
  const { theme, toggleTheme } = useTheme();

  const code = Number(codeProp || codeParam);
  const content = ERROR_CONTENT[code];

  if (!content || !ERROR_CODES.includes(code)) {
    return (
      <div className="error-shell">
        <div className="error-card">
          <p className="auth-sub">Unknown error page.</p>
          <Link to="/" className="btn-primary">
            Go home
          </Link>
        </div>
      </div>
    );
  }

  const handlePrimary = () => {
    const primary = content.primary;
    if (primary.action === "reload") {
      window.location.reload();
      return;
    }
    if (primary.action === "roleHome") {
      navigate(user ? ROLE_HOME[user.role] || "/login" : "/login");
      return;
    }
    if (primary.to === "/login" && location.state?.from) {
      navigate("/login", { state: { from: location.state.from } });
      return;
    }
    if (primary.to) navigate(primary.to);
  };

  const handleSecondary = () => {
    const secondary = content.secondary;
    if (secondary?.to) navigate(secondary.to);
  };

  return (
    <div className={`error-shell error-shell--${content.tone}`}>
      <header className="error-topbar">
        <Link to="/" className="brand-mark">
          <Logo size={32} />
          <span className="brand-name">JobMatch</span>
        </Link>
        <button type="button" className="icon-btn" onClick={toggleTheme} aria-label="Toggle theme">
          {theme === "light" ? <IconMoon /> : <IconSun />}
        </button>
      </header>

      <main className="error-main">
        <div className="error-card">
          <div className="error-art">
            <ErrorIllustration code={code} />
          </div>
          <p className="error-code">{code}</p>
          <h1>{content.title}</h1>
          <p className="error-desc">{content.description}</p>
          <div className="error-actions">
            <button type="button" className="btn-primary" onClick={handlePrimary}>
              {content.primary.label}
            </button>
            {content.secondary && (
              <button type="button" className="btn-secondary" onClick={handleSecondary}>
                {content.secondary.label}
              </button>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
