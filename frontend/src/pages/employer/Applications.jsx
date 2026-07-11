import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import PageHeader from "../../components/PageHeader.jsx";
import PortalSection from "../../components/PortalSection.jsx";
import { fetchEmployerApplications } from "../../api/client.js";

function formatApplicantDate(value) {
  if (!value) return ": ";
  return new Date(value).toLocaleDateString(undefined, {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
}

function formatMatchScore(score) {
  if (score == null) return ": ";
  return `${Math.round(score * 100)}% match`;
}

function formatStatus(status) {
  if (!status || status === "applied") return "Applied";
  return status.charAt(0).toUpperCase() + status.slice(1);
}

export default function EmployerApplications() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState("");
  const [roleFilter, setRoleFilter] = useState("all");
  const [sort, setSort] = useState("newest");

  useEffect(() => {
    fetchEmployerApplications()
      .then(setApplications)
      .catch((err) => setError(err.response?.data?.detail?.error || err.message))
      .finally(() => setLoading(false));
  }, []);

  const jobTitles = useMemo(
    () => [...new Set(applications.map((row) => row.job_title).filter(Boolean))].sort(),
    [applications],
  );

  const filtered = useMemo(() => {
    let rows = [...applications];
    const query = search.trim().toLowerCase();
    if (query) {
      rows = rows.filter(
        (row) =>
          row.candidate_name?.toLowerCase().includes(query)
          || row.job_title?.toLowerCase().includes(query),
      );
    }
    if (roleFilter !== "all") {
      rows = rows.filter((row) => row.job_title === roleFilter);
    }
    rows.sort((a, b) => {
      if (sort === "match") {
        return (b.match_score ?? 0) - (a.match_score ?? 0);
      }
      return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
    });
    return rows;
  }, [applications, search, roleFilter, sort]);

  return (
    <>
      <PageHeader
        eyebrow="Employer"
        title="Applicants"
        subtitle="Applications to your posted roles."
      />
      <PortalSection title="Application feed" className="applicant-feed-panel scroll-content">
        <div className="applicant-feed-toolbar results-filters">
          <input
            type="search"
            className="filter-search"
            placeholder="Search applicants…"
            aria-label="Search applicants"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <select
            className="filter-select"
            value={roleFilter}
            onChange={(e) => setRoleFilter(e.target.value)}
            aria-label="Filter by role"
          >
            <option value="all">All roles</option>
            {jobTitles.map((title) => (
              <option key={title} value={title}>
                {title}
              </option>
            ))}
          </select>
          <select
            className="filter-select"
            value={sort}
            onChange={(e) => setSort(e.target.value)}
            aria-label="Sort applicants"
          >
            <option value="newest">Newest first</option>
            <option value="match">Highest match</option>
          </select>
        </div>

        {loading && <p className="auth-sub">Loading…</p>}
        {error && <p className="notice-warning">{error}</p>}
        {!loading && !error && applications.length === 0 && (
          <p className="auth-sub">No applications yet. Candidates apply from their job match list.</p>
        )}
        {!loading && !error && applications.length > 0 && filtered.length === 0 && (
          <p className="auth-sub">No applicants match your search.</p>
        )}

        {filtered.length > 0 && (
          <>
            <div className="applicant-list-head" aria-hidden="true">
              <span>Candidate</span>
              <span>Role</span>
              <span>Match</span>
              <span>Applied</span>
              <span>Action</span>
            </div>
            <ul className="applicant-list">
              {filtered.map((row) => (
                <li key={row.id}>
                  <Link
                    to={`/employer/matches?job=${encodeURIComponent(row.job_title)}`}
                    className="applicant-row applicant-row--interactive"
                  >
                    <span className="applicant-row__name">{row.candidate_name}</span>
                    <span className="applicant-row__role">{row.job_title}</span>
                    <span className="applicant-row__match">{formatMatchScore(row.match_score)}</span>
                    <span className="applicant-row__date">{formatApplicantDate(row.created_at)}</span>
                    <span className="applicant-row__action">
                      <span className="applicant-status">{formatStatus(row.status)}</span>
                      <span className="applicant-row__view">View</span>
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          </>
        )}
      </PortalSection>
    </>
  );
}
