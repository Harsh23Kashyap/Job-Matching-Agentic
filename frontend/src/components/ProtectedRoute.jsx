import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function ProtectedRoute({ role }) {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="auth-form-panel" style={{ minHeight: "100vh" }}>
        <p className="auth-sub">Loading…</p>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/error/401" replace state={{ from: location.pathname }} />;
  }

  if (role && user.role !== role) {
    return <Navigate to="/error/403" replace />;
  }

  return <Outlet />;
}
