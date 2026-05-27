import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth, ROLE_HOME } from "../context/AuthContext.jsx";

function userInitials(email) {
  if (!email) return "?";
  return email.split("@")[0].slice(0, 2).toUpperCase();
}

const PROFILE_PATH = {
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

  const profilePath = PROFILE_PATH[user?.role] || ROLE_HOME[user?.role] || "/";

  return (
    <div className="user-menu" ref={ref}>
      <button type="button" className="user-menu-trigger" onClick={() => setOpen(!open)} aria-expanded={open}>
        <div className="avatar">{userInitials(user?.email)}</div>
        <span className="user-menu-name">Me</span>
        <span className="user-menu-chevron" aria-hidden="true">
          ▾
        </span>
      </button>
      {open && (
        <div className="user-menu-dropdown">
          <p className="user-menu-email">{user?.email}</p>
          <Link to={profilePath} onClick={() => setOpen(false)}>
            Profile
          </Link>
          <Link to={profilePath} onClick={() => setOpen(false)}>
            Settings
          </Link>
          <button
            type="button"
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
