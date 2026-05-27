import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ROLE_HOME } from "../context/AuthContext.jsx";

function userInitials(email) {
  if (!email) return "?";
  return email.split("@")[0].slice(0, 2).toUpperCase();
}

const PROFILE_PATH = {
  candidate: "/candidate/profile",
  employer: "/employer/jobs",
  admin: "/admin/console",
};

const SETTINGS_PATH = {
  candidate: "/candidate/profile",
  employer: "/employer/jobs",
  admin: "/admin/console",
};

export default function UserMenu({ user, onLogout }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const close = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    };
    document.addEventListener("click", close);
    return () => document.removeEventListener("click", close);
  }, []);

  useEffect(() => {
    const onKey = (e) => {
      if (e.key === "Escape") setOpen(false);
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, []);

  const profilePath = PROFILE_PATH[user?.role] || ROLE_HOME[user?.role] || "/";
  const settingsPath = SETTINGS_PATH[user?.role] || profilePath;

  return (
    <div className="user-menu" ref={ref}>
      <button
        type="button"
        className="user-menu-trigger user-menu-trigger--avatar"
        onClick={() => setOpen(!open)}
        aria-expanded={open}
        aria-haspopup="menu"
        aria-label="Account menu"
      >
        <div className="avatar avatar--nav">{userInitials(user?.email)}</div>
      </button>
      {open && (
        <div className="user-menu-dropdown" role="menu">
          <p className="user-menu-email">{user?.email}</p>
          <Link to={profilePath} role="menuitem" onClick={() => setOpen(false)}>
            View profile
          </Link>
          <Link to={settingsPath} role="menuitem" onClick={() => setOpen(false)}>
            Settings
          </Link>
          <button
            type="button"
            role="menuitem"
            onClick={async () => {
              setOpen(false);
              await onLogout();
              navigate("/login");
            }}
          >
            Sign out
          </button>
        </div>
      )}
    </div>
  );
}
