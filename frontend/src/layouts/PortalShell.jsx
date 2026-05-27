import { NavLink, Outlet, useLocation } from "react-router-dom";
import { Logo, IconMoon, IconSun } from "../components/icons.jsx";
import UserMenu from "../components/UserMenu.jsx";
import PortalBackground from "../components/PortalBackground.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import { useTheme } from "../hooks/useTheme.js";

const PORTAL_LABELS = {
  candidate: "Candidate workspace",
  employer: "Employer workspace",
  admin: "Admin console",
};

const JOBS_LAYOUT_PREFIXES = [
  "/candidate/matches",
  "/candidate/saved",
  "/employer/matches",
  "/employer/applications",
];

function pageContainerClass(pathname) {
  if (JOBS_LAYOUT_PREFIXES.some((prefix) => pathname.startsWith(prefix))) {
    return "page-container page-container--jobs";
  }
  return "page-container page-container--form";
}

export default function PortalShell({ portal = "candidate", subtitle, navItems = [] }) {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const { pathname } = useLocation();

  return (
    <div className="app" data-portal={portal}>
      <header className="top-nav">
        <div className="top-nav-inner">
          <NavLink to="/" className="brand-mark">
            <Logo size={34} />
            <div className="brand-text">
              <span className="brand-name">JobMatch</span>
              {subtitle && <span className="brand-sub">{subtitle}</span>}
            </div>
          </NavLink>

          <nav className="top-nav-links" aria-label="Main">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) => `nav-link${isActive ? " nav-link--active" : ""}`}
              >
                {item.icon}
                <span>{item.label}</span>
              </NavLink>
            ))}
          </nav>

          <div className="top-nav-actions">
            <span className="portal-pill">{PORTAL_LABELS[portal] || subtitle}</span>
            <button type="button" className="icon-btn" onClick={toggleTheme} aria-label="Toggle theme">
              {theme === "light" ? <IconMoon /> : <IconSun />}
            </button>
            <UserMenu user={user} onLogout={logout} />
          </div>
        </div>
      </header>

      <main className="page-shell page">
        <PortalBackground />
        <div className={pageContainerClass(pathname)}>
          <Outlet />
        </div>
      </main>

      {navItems.length > 0 && (
        <nav className="mobile-tab-bar" aria-label="Mobile navigation">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) => `mobile-tab${isActive ? " mobile-tab--active" : ""}`}
            >
              {item.icon}
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
      )}
    </div>
  );
}
