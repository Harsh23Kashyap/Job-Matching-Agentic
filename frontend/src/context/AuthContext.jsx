import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchMe, login as apiLogin, logout as apiLogout, register as apiRegister } from "../api/client.js";

const AuthContext = createContext(null);

const ROLE_HOME = {
  candidate: "/candidate/matches",
  employer: "/employer/jobs",
  admin: "/admin/console",
};

export function AuthProvider({ children }) {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    try {
      const me = await fetchMe();
      setUser(me);
      return me;
    } catch {
      setUser(null);
      return null;
    }
  }, []);

  useEffect(() => {
    refresh().finally(() => setLoading(false));
  }, [refresh]);

  const login = async (email, password) => {
    const me = await apiLogin(email, password);
    setUser(me);
    return me;
  };

  const register = async (email, password, role) => {
    const me = await apiRegister(email, password, role);
    setUser(me);
    return me;
  };

  const logout = useCallback(async () => {
    try {
      await apiLogout();
    } catch {
      /* Still clear local session if the API call fails. */
    }
    setUser(null);
    navigate("/login", { replace: true });
  }, [navigate]);

  const value = useMemo(
    () => ({ user, loading, login, register, logout, refresh, roleHome: ROLE_HOME }),
    [user, loading, logout, refresh],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}

export { ROLE_HOME };
