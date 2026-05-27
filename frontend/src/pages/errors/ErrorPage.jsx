import { Link, useLocation, useNavigate, useParams } from "react-router-dom";
import { Logo, IconMoon, IconSun } from "../../components/icons.jsx";
import { ROLE_HOME, useAuth } from "../../context/AuthContext.jsx";
import { useTheme } from "../../hooks/useTheme.js";
import ErrorBackground from "./ErrorBackground.jsx";
import { ERROR_CODES, ERROR_CONTENT } from "./errorConfig.js";
import { ErrorIllustration } from "./ErrorIllustrations.jsx";

function ErrorCard({ code, title, description, primary, secondary, onPrimary, onSecondary }) {
  return (
    <div className="error-card">
      <div className="error-art">
        <ErrorIllustration code={code} variant={code ? "default" : "broken"} />
      </div>
      {code ? <p className="error-code sr-only">{code}</p> : null}
      <h1>{title}</h1>
      <p className="error-desc">{description}</p>
      <div className="error-actions">
        {secondary && (
          <button type="button" className="btn-secondary" onClick={onSecondary}>
            {secondary.label}
          </button>
        )}
        <button type="button" className="btn-primary" onClick={onPrimary}>
          {primary.label}
        </button>
      </div>
    </div>
  );
}

export default function ErrorPage({ code: codeProp }) {
  const { code: codeParam } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useAuth();
  const { theme, toggleTheme } = useTheme();

  const code = Number(codeProp || codeParam);
  const content = ERROR_CONTENT[code];
  const isKnown = content && ERROR_CODES.includes(code);

  const handlePrimary = () => {
    if (!isKnown) {
      navigate("/");
      return;
    }
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
    if (!isKnown) return;
    const secondary = content.secondary;
    if (secondary?.action === "reload") {
      window.location.reload();
      return;
    }
    if (secondary?.to) navigate(secondary.to);
  };

  const cardProps = isKnown
    ? {
        code,
        title: content.title,
        description: content.description,
        primary: content.primary,
        secondary: content.secondary,
        onPrimary: handlePrimary,
        onSecondary: handleSecondary,
      }
    : {
        code: null,
        title: "Something went wrong",
        description: "We couldn't load this page. You can return home and try again.",
        primary: { label: "Go home" },
        secondary: null,
        onPrimary: () => navigate("/"),
        onSecondary: () => {},
      };

  return (
    <div className={`error-shell${isKnown ? ` error-shell--${content.tone}` : " error-shell--unknown"}`}>
      <header className="error-topbar">
        <Link to="/" className="brand-mark">
          <Logo size={32} />
          <span className="brand-name">JobMatch</span>
        </Link>
        <button type="button" className="icon-btn" onClick={toggleTheme} aria-label="Toggle theme">
          {theme === "light" ? <IconMoon /> : <IconSun />}
        </button>
      </header>

      <main className="error-page">
        <ErrorBackground />
        <ErrorCard {...cardProps} />
      </main>
    </div>
  );
}
