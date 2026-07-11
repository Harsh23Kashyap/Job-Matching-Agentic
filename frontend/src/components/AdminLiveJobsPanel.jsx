import { useCallback, useEffect, useState } from "react";
import { apiErrorMessage, fetchRealJobsStatus, syncRealJobs } from "../api/client.js";
import { formatRelativeTime } from "../utils/formatRelativeTime.js";
import Button from "./Button.jsx";
import FriendlyError from "./FriendlyError.jsx";

const SOURCE_LABELS = {
  local_seed: "Local seed data",
  snapshot: "Cached snapshot",
  external_api: "Live API",
};

function sourceLabel(source) {
  return SOURCE_LABELS[source] || source || "Unknown";
}

function StatusBadge({ enabled, configured }) {
  if (!enabled) {
    return <span className="admin-live-jobs-badge admin-live-jobs-badge--off">Disabled</span>;
  }
  if (!configured) {
    return <span className="admin-live-jobs-badge admin-live-jobs-badge--warn">Missing URL</span>;
  }
  return <span className="admin-live-jobs-badge admin-live-jobs-badge--on">Ready</span>;
}

export default function AdminLiveJobsPanel({ onSynced }) {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [reindex, setReindex] = useState(true);
  const [syncMessage, setSyncMessage] = useState("");

  const load = useCallback(() => {
    setLoading(true);
    setError("");
    return fetchRealJobsStatus()
      .then(setStatus)
      .catch((err) => setError(apiErrorMessage(err, "Failed to load live jobs status")))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const handleSync = async () => {
    setSyncing(true);
    setError("");
    setSyncMessage("");
    try {
      const result = await syncRealJobs({ reindex });
      setSyncMessage(
        `${result.message}, ${result.job_count} jobs indexed`
        + (result.reindexed ? " (candidates reindexed)" : ""),
      );
      await load();
      onSynced?.();
    } catch (err) {
      setError(apiErrorMessage(err, "Live jobs sync failed"));
    } finally {
      setSyncing(false);
    }
  };

  const state = status?.state;
  const canSync = Boolean(status?.enabled && status?.base_url_configured);

  return (
    <section className="panel span-12 admin-live-jobs-panel" id="admin-section-live-jobs">
      <div className="panel-header admin-live-jobs-panel__head">
        <div>
          <h2>Live jobs API</h2>
          <p className="admin-live-jobs-panel__intro">
            Pull roles from an external provider into the employer corpus. Requires{" "}
            <code>REAL_JOBS_ENABLE</code> and <code>REAL_JOBS_BASE_URL</code> in backend env.
          </p>
        </div>
        <button type="button" className="admin-inline-refresh" onClick={load} disabled={loading || syncing}>
          Refresh status
        </button>
      </div>

      {loading && !status && !error && <p className="admin-live-jobs-panel__loading">Loading live jobs status…</p>}

      {status && (
        <>
          <div className="admin-live-jobs-panel__badges">
            <StatusBadge enabled={status.enabled} configured={status.base_url_configured} />
            {state?.source && (
              <span className="admin-live-jobs-source">Corpus: {sourceLabel(state.source)}</span>
            )}
          </div>

          <dl className="admin-kv-list admin-live-jobs-kv">
            <div className="admin-kv-row">
              <dt>Jobs in corpus</dt>
              <dd>{state?.job_count ?? ": "}</dd>
            </div>
            <div className="admin-kv-row">
              <dt>Last sync</dt>
              <dd>{state?.last_sync ? formatRelativeTime(state.last_sync) : "Never"}</dd>
            </div>
            <div className="admin-kv-row">
              <dt>API path</dt>
              <dd>
                <code>{status.jobs_path || "/jobs"}</code>
              </dd>
            </div>
            <div className="admin-kv-row">
              <dt>Page limit</dt>
              <dd>{status.page_limit ?? ": "}</dd>
            </div>
            <div className="admin-kv-row">
              <dt>Snapshot file</dt>
              <dd>
                <code className="admin-live-jobs-path">{status.snapshot_path || ": "}</code>
              </dd>
            </div>
          </dl>

          {state?.last_error && (
            <FriendlyError message={`Last sync error: ${state.last_error}`} className="admin-live-jobs-error" />
          )}

          {!status.enabled && (
            <p className="admin-live-jobs-hint">
              Set <code>REAL_JOBS_ENABLE=true</code> in <code>backend/.env</code> and restart the API.
            </p>
          )}
          {status.enabled && !status.base_url_configured && (
            <p className="admin-live-jobs-hint">
              Set <code>REAL_JOBS_BASE_URL</code> to your provider base URL, then restart the API.
            </p>
          )}

          <div className="admin-live-jobs-actions">
            <label className="admin-live-jobs-reindex">
              <input
                type="checkbox"
                checked={reindex}
                onChange={(e) => setReindex(e.target.checked)}
                disabled={syncing}
              />
              Reindex candidates after sync
            </label>
            <Button
              className="btn-primary"
              loading={syncing}
              loadingLabel="Syncing…"
              disabled={!canSync}
              onClick={handleSync}
            >
              Sync live jobs
            </Button>
          </div>

          {syncMessage && <p className="admin-live-jobs-success">{syncMessage}</p>}
        </>
      )}

      {error && <FriendlyError message={error} />}
    </section>
  );
}
