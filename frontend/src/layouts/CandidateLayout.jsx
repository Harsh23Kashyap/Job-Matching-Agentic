import { Link, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import { useTheme } from "../hooks/useTheme.js";
import { IconMoon, IconSun } from "../components/icons.jsx";

export default function CandidateLayout() {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-brand">
          <div>
            <h1>Job Matching</h1>
            <p>Candidate portal</p>
          </div>
        </div>
        <nav className="portal-nav">
          <Link to="/candidate/onboarding">Upload resume</Link>
          <Link to="/candidate/profile">Profile</Link>
          <Link to="/candidate/matches">Find jobs</Link>
        </nav>
        <div className="header-actions">
          <span className="user-pill">{user?.email}</span>
          <button type="button" className="theme-toggle" onClick={toggleTheme} aria-label="Toggle theme">
            {theme === "light" ? <IconMoon /> : <IconSun />}
          </button>
          <button type="button" className="btn-secondary" onClick={handleLogout}>
            Log out
          </button>
        </div>
      </header>
      <main className="dashboard portal-main">{<Outlet />}</main>
    </div>
  );
}
