import { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { api } from "../api/client.js";

/** Redirect to branded error pages for gateway / not-implemented API failures. */
export default function ApiErrorBridge() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const id = api.interceptors.response.use(
      (res) => res,
      (err) => {
        const path = location.pathname;
        if (path.startsWith("/error/")) return Promise.reject(err);

        const url = err.config?.url || "";
        const status = err.response?.status;

        if (url.includes("/auth/me")) return Promise.reject(err);

        if (status === 501 || status === 502) {
          navigate(`/error/${status}`, { replace: true });
          return Promise.reject(err);
        }

        if (!err.response && err.message === "Network Error" && !url.includes("/auth/")) {
          navigate("/error/502", { replace: true });
        }

        return Promise.reject(err);
      },
    );

    return () => api.interceptors.response.eject(id);
  }, [navigate, location.pathname]);

  return null;
}
