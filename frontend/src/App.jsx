import { Navigate, Route, Routes } from "react-router-dom";
import ApiErrorBridge from "./components/ApiErrorBridge.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import { ToastProvider } from "./components/Toast.jsx";
import { AuthProvider, useAuth, ROLE_HOME } from "./context/AuthContext.jsx";
import AdminLayout from "./layouts/AdminLayout.jsx";
import CandidateLayout from "./layouts/CandidateLayout.jsx";
import EmployerLayout from "./layouts/EmployerLayout.jsx";
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";
import AdminConsole from "./pages/admin/AdminConsole.jsx";
import Onboarding from "./pages/candidate/Onboarding.jsx";
import CandidateMatches from "./pages/candidate/Matches.jsx";
import Profile from "./pages/candidate/Profile.jsx";
import EmployerApplications from "./pages/employer/Applications.jsx";
import EmployerJobs from "./pages/employer/Jobs.jsx";
import EmployerMatches from "./pages/employer/Matches.jsx";
import CandidateSaved from "./pages/candidate/Saved.jsx";
import ErrorPage from "./pages/errors/ErrorPage.jsx";
import { ERROR_CODES } from "./pages/errors/errorConfig.js";
import "./App.css";
import "./theme/auth.css";

function HomeRedirect() {
  const { user, loading } = useAuth();
  if (loading) {
    return (
      <div className="auth-form-panel" style={{ minHeight: "100vh" }}>
        <p className="auth-sub">Loading…</p>
      </div>
    );
  }
  if (!user) return <Navigate to="/login" replace />;
  return <Navigate to={ROLE_HOME[user.role] || "/login"} replace />;
}

export default function App() {
  return (
    <AuthProvider>
      <ToastProvider>
        <ApiErrorBridge />
        <Routes>
        <Route path="/" element={<HomeRedirect />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {ERROR_CODES.map((code) => (
          <Route key={code} path={`/error/${code}`} element={<ErrorPage />} />
        ))}

        <Route element={<ProtectedRoute role="admin" />}>
          <Route element={<AdminLayout />}>
            <Route path="/admin/console" element={<AdminConsole />} />
          </Route>
        </Route>

        <Route element={<ProtectedRoute role="candidate" />}>
          <Route element={<CandidateLayout />}>
            <Route path="/candidate/onboarding" element={<Onboarding />} />
            <Route path="/candidate/profile" element={<Profile />} />
            <Route path="/candidate/matches" element={<CandidateMatches />} />
            <Route path="/candidate/saved" element={<CandidateSaved />} />
          </Route>
        </Route>

        <Route element={<ProtectedRoute role="employer" />}>
          <Route element={<EmployerLayout />}>
            <Route path="/employer/jobs" element={<EmployerJobs />} />
            <Route path="/employer/matches" element={<EmployerMatches />} />
            <Route path="/employer/applications" element={<EmployerApplications />} />
          </Route>
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </ToastProvider>
    </AuthProvider>
  );
}
