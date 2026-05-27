import { useMemo, useState } from "react";
import EmployerJobCard from "./EmployerJobCard.jsx";
import EmptyStatePanel from "./EmptyStatePanel.jsx";
import { ActivePostingsEmpty, EmployerRolesEmpty } from "./EmptyState.jsx";

function filterEmployerJobs(jobs, { search, remoteOnly, sort, statusFilter }) {
  let list = [...jobs];
  if (statusFilter === "open") {
    list = list.filter((job) => (job.status || "open") === "open");
  } else if (statusFilter === "closed") {
    list = list.filter((job) => job.status === "closed");
  }
  if (remoteOnly) {
    list = list.filter((job) => job.remote_policy);
  }
  const query = search.trim().toLowerCase();
  if (query) {
    list = list.filter((job) => {
      const haystack = [
        job.title,
        job.company,
        job.location,
        ...(job.required_skills || []),
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      return haystack.includes(query);
    });
  }
  if (sort === "title") {
    list.sort((a, b) => (a.title || "").localeCompare(b.title || ""));
  } else {
    list.sort((a, b) => (b.created_at || "").localeCompare(a.created_at || ""));
  }
  return list;
}

export default function EmployerJobList({
  jobs,
  openCount = 0,
  loading,
  onEdit,
  onClose,
  closingId,
  onPostRole,
}) {
  const [search, setSearch] = useState("");
  const [remoteOnly, setRemoteOnly] = useState(false);
  const [sort, setSort] = useState("newest");
  const [statusFilter, setStatusFilter] = useState("open");

  const filtered = useMemo(
    () => filterEmployerJobs(jobs, { search, remoteOnly, sort, statusFilter }),
    [jobs, search, remoteOnly, sort, statusFilter],
  );

  if (loading) {
    return (
      <div className="loading-shimmer" aria-hidden="true">
        <span className="skeleton-block skeleton-block--lg" />
        <span className="skeleton-block skeleton-block--md" />
        <span className="skeleton-block skeleton-block--md" />
      </div>
    );
  }

  if (jobs.length === 0) {
    return (
      <EmptyStatePanel className="employer-roles-empty-panel">
        <EmployerRolesEmpty
          action={
            <button type="button" className="btn-primary" onClick={onPostRole}>
              Post your first role
            </button>
          }
        />
      </EmptyStatePanel>
    );
  }

  if (openCount === 0) {
    return (
      <div className="employer-role-list">
        <EmptyStatePanel className="employer-roles-empty-panel employer-roles-empty-panel--compact">
          <ActivePostingsEmpty
            action={
              <button type="button" className="btn-primary" onClick={onPostRole}>
                Post a new role
              </button>
            }
          />
        </EmptyStatePanel>
        <div className="employer-role-list__closed-section">
          <p className="form-helper employer-role-list__closed-hint">
            {jobs.length} closed {jobs.length === 1 ? "role" : "roles"}. Open Closed to review or edit.
          </p>
          <RoleListControls
            search={search}
            onSearchChange={setSearch}
            remoteOnly={remoteOnly}
            onRemoteOnlyChange={setRemoteOnly}
            sort={sort}
            onSortChange={setSort}
            statusFilter={statusFilter}
            onStatusFilterChange={setStatusFilter}
            openCount={openCount}
            closedCount={jobs.filter((j) => j.status === "closed").length}
          />
          {filtered.length === 0 ? (
            <p className="inline-empty-hint">No roles match your filters.</p>
          ) : (
            <div className="employer-role-list__cards">
              {filtered.map((job) => (
                <EmployerJobCard
                  key={job.id}
                  job={job}
                  onEdit={onEdit}
                  onClose={onClose}
                  closing={closingId === job.id}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="employer-role-list">
      <RoleListControls
        search={search}
        onSearchChange={setSearch}
        remoteOnly={remoteOnly}
        onRemoteOnlyChange={setRemoteOnly}
        sort={sort}
        onSortChange={setSort}
        statusFilter={statusFilter}
        onStatusFilterChange={setStatusFilter}
        openCount={openCount}
        closedCount={jobs.filter((j) => j.status === "closed").length}
      />

      {filtered.length === 0 ? (
        <p className="inline-empty-hint">No roles match your filters.</p>
      ) : (
        <div className="employer-role-list__cards">
          {filtered.map((job) => (
            <EmployerJobCard
              key={job.id}
              job={job}
              onEdit={onEdit}
              onClose={onClose}
              closing={closingId === job.id}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function RoleListControls({
  search,
  onSearchChange,
  remoteOnly,
  onRemoteOnlyChange,
  sort,
  onSortChange,
  statusFilter,
  onStatusFilterChange,
  openCount,
  closedCount,
}) {
  return (
    <div className="results-filters employer-role-filters">
      <input
        type="search"
        className="filter-search"
        placeholder="Search roles…"
        value={search}
        onChange={(e) => onSearchChange(e.target.value)}
        aria-label="Search roles"
      />
      <div className="employer-role-filters__status" role="group" aria-label="Role status">
        <button
          type="button"
          className={`filter-pill filter-pill--btn${statusFilter === "open" ? " filter-pill--active" : ""}`}
          onClick={() => onStatusFilterChange("open")}
        >
          Open ({openCount})
        </button>
        <button
          type="button"
          className={`filter-pill filter-pill--btn${statusFilter === "closed" ? " filter-pill--active" : ""}`}
          onClick={() => onStatusFilterChange("closed")}
        >
          Closed ({closedCount})
        </button>
        <button
          type="button"
          className={`filter-pill filter-pill--btn${statusFilter === "all" ? " filter-pill--active" : ""}`}
          onClick={() => onStatusFilterChange("all")}
        >
          All
        </button>
      </div>
      <label className={`filter-pill${remoteOnly ? " filter-pill--active" : ""}`}>
        <input
          type="checkbox"
          checked={remoteOnly}
          onChange={(e) => onRemoteOnlyChange(e.target.checked)}
        />
        Remote only
      </label>
      <select
        className="filter-select"
        value={sort}
        onChange={(e) => onSortChange(e.target.value)}
        aria-label="Sort roles"
      >
        <option value="newest">Newest first</option>
        <option value="title">Title A–Z</option>
      </select>
    </div>
  );
}
