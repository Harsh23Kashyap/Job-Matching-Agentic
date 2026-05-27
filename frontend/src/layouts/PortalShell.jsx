import { useEffect } from "react";
import { NavLink, Outlet, useLocation } from "react-router-dom";
import { Logo, IconMoon, IconSun } from "../components/icons.jsx";
import UserMenu from "../components/UserMenu.jsx";
import PortalBackground from "../components/PortalBackground.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import { useTheme } from "../hooks/useTheme.js";

const JOBS_LAYOUT_PREFIXES = [
  "/candidate/matches",
  "/candidate/saved",
  "/employer/jobs",
  "/employer/matches",
  "/employer/applications",
];

function pageContainerClass(pathname) {
  if (JOBS_LAYOUT_PREFIXES.some((prefix) => pathname.startsWith(prefix))) {
    return "page-container page-container--jobs";
  }
  return "page-container page-container--form";
}

function navItemActive(item, pathname, routerActive) {
  if (typeof item.isActive === "function") return item.isActive(pathname);
  return routerActive;
}

export default function PortalShell({ portal = "candidate", subtitle, navItems = [] }) {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const { pathname } = useLocation();

  useEffect(() => {
    document.documentElement.dataset.portal = portal;
    return () => {
      delete document.documentElement.dataset.portal;
    };
  }, [portal]);

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

          {navItems.length > 0 && (
            <nav className="top-nav-links" aria-label="Main">
              {navItems.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.end}
                  isActive={(props) => navItemActive(item, pathname, props.isActive)}
                  className={({ isActive }) => `nav-link${isActive ? " nav-link--active" : ""}`}
                >
                  <span className="nav-link-icon">{item.icon}</span>
                  <span className="nav-link-label">{item.label}</span>
                </NavLink>
              ))}
            </nav>
          )}

          <div className="top-nav-actions">
            <button
              type="button"
              className="nav-action-btn"
              onClick={toggleTheme}
              aria-label={theme === "light" ? "Switch to dark theme" : "Switch to light theme"}
            >
              {theme === "light" ? <IconMoon size={18} /> : <IconSun size={18} />}
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
              end={item.end}
              isActive={(props) => navItemActive(item, pathname, props.isActive)}
              className={({ isActive }) => `mobile-tab${isActive ? " mobile-tab--active" : ""}`}
            >
              <span className="mobile-tab-icon">{item.icon}</span>
              <span className="mobile-tab-label">{item.label}</span>
            </NavLink>
          ))}
        </nav>
      )}
    </div>
  );
}
