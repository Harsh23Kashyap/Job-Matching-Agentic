import { useCallback, useEffect, useState } from "react";
import { fetchAgentStatus } from "../api/client.js";
import { parseAdminError } from "../utils/adminErrors.js";

export function useAgentStatus(intervalMs = 5000) {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);
  const [lastRefreshed, setLastRefreshed] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const load = useCallback(async (manual = false) => {
    if (manual) setRefreshing(true);
    try {
      const data = await fetchAgentStatus();
      setStatus(data);
      setError(null);
      setLastRefreshed(new Date());
      return true;
    } catch (err) {
      const code = err.response?.status;
      const raw = code === 404 ? "Backend not found on port 8001" : err.message || "Connection failed";
      const parsed = parseAdminError(raw);
      setError(parsed.summary);
      return false;
    } finally {
      if (manual) setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    load();
    const id = setInterval(() => load(), intervalMs);
    return () => clearInterval(id);
  }, [load, intervalMs]);

  return { status, error, lastRefreshed, refreshing, refresh: () => load(true) };
}
