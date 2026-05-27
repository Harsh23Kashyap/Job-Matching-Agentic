import { useMemo, useState } from "react";
import EmployerJobCard from "./EmployerJobCard.jsx";
import EmptyStatePanel from "./EmptyStatePanel.jsx";
import { EmployerRolesEmpty } from "./EmptyState.jsx";

function filterEmployerJobs(jobs, { search, remoteOnly, sort }) {
  let list = [...jobs];
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

export default function EmployerJobList({ jobs, loading, onEdit, onClose, closingId, onPostRole }) {
  const [search, setSearch] = useState("");
  const [remoteOnly, setRemoteOnly] = useState(false);
  const [sort, setSort] = useState("newest");

  const filtered = useMemo(
    () => filterEmployerJobs(jobs, { search, remoteOnly, sort }),
    [jobs, search, remoteOnly, sort],
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
      <EmptyStatePanel patternVariant="employer-empty">
        <EmployerRolesEmpty
          action={
            <button type="button" className="btn-primary" onClick={onPostRole}>
              Post a role
            </button>
          }
        />
      </EmptyStatePanel>
    );
  }

  return (
    <div className="employer-role-list">
      <div className="results-filters">
        <input
          type="search"
          className="filter-search"
          placeholder="Search roles…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          aria-label="Search roles"
        />
        <label className={`filter-pill${remoteOnly ? " filter-pill--active" : ""}`}>
          <input
            type="checkbox"
            checked={remoteOnly}
            onChange={(e) => setRemoteOnly(e.target.checked)}
          />
          Remote only
        </label>
        <select
          className="filter-select"
          value={sort}
          onChange={(e) => setSort(e.target.value)}
          aria-label="Sort roles"
        >
          <option value="newest">Newest first</option>
          <option value="title">Title A–Z</option>
        </select>
      </div>

      {filtered.length === 0 ? (
        <p className="employer-role-list__empty-filter">No roles match your filters.</p>
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
