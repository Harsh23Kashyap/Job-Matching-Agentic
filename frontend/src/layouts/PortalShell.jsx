import { NavLink, Outlet } from "react-router-dom";
import { Logo, IconMoon, IconSun } from "../components/icons.jsx";
import UserMenu from "../components/UserMenu.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import { useTheme } from "../hooks/useTheme.js";

export default function PortalShell({ subtitle, navItems = [] }) {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="app">
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
            <button type="button" className="icon-btn" onClick={toggleTheme} aria-label="Toggle theme">
              {theme === "light" ? <IconMoon /> : <IconSun />}
            </button>
            <UserMenu user={user} onLogout={logout} />
          </div>
        </div>
      </header>

      <main className="page-shell">
        <div className="page-container">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
