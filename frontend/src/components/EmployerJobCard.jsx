import { Link } from "react-router-dom";
import { formatBudgetRange, formatExperienceYears, formatPostedDate } from "../utils/format.js";
import { SkillChipList } from "./SkillChip.jsx";

const STATUS_LABELS = { open: "Open", closed: "Closed", draft: "Draft" };

function JobStatusBadge({ status }) {
  const value = status || "open";
  return (
    <span className={`role-status role-status--${value}`}>{STATUS_LABELS[value] || value}</span>
  );
}

export default function EmployerJobCard({ job, onEdit, onClose, closing }) {
  const isClosed = job.status === "closed";
  const skills = job.required_skills || [];

  return (
    <article className={`portal-card employer-role-card${isClosed ? " employer-role-card--closed" : ""}`}>
      <div className="employer-role-card__head">
        <div className="employer-role-card__title-row">
          <h3 className="employer-role-card__title">{job.title}</h3>
          <JobStatusBadge status={job.status} />
          {job.remote_policy && <span className="job-card-badge">Remote</span>}
        </div>
      </div>

      <div className="employer-role-card__meta-grid job-meta-grid">
        <div className="employer-role-card__meta-item">
          <span className="employer-role-card__meta-label">Company</span>
          <span className="employer-role-card__meta-value">{job.company || "—"}</span>
        </div>
        <div className="employer-role-card__meta-item">
          <span className="employer-role-card__meta-label">Location</span>
          <span className="employer-role-card__meta-value">{job.location || "—"}</span>
        </div>
        <div className="employer-role-card__meta-item">
          <span className="employer-role-card__meta-label">Experience</span>
          <span className="employer-role-card__meta-value">{formatExperienceYears(job.required_experience)}</span>
        </div>
        <div className="employer-role-card__meta-item">
          <span className="employer-role-card__meta-label">Budget</span>
          <span className="employer-role-card__meta-value">{formatBudgetRange(job) || "—"}</span>
        </div>
        <div className="employer-role-card__meta-item">
          <span className="employer-role-card__meta-label">Posted</span>
          <span className="employer-role-card__meta-value">{formatPostedDate(job.created_at)}</span>
        </div>
      </div>

      {skills.length > 0 && (
        <div className="employer-role-card__skills">
          <span className="employer-role-card__meta-label">Required skills</span>
          <SkillChipList skills={skills} limit={8} variant="default" />
        </div>
      )}

      <div className="employer-role-card__actions">
        <Link
          to={`/employer/matches?job=${encodeURIComponent(job.title)}`}
          className="btn-primary btn-sm"
        >
          View candidates
        </Link>
        <button type="button" className="btn-ghost btn-ghost--sm" onClick={() => onEdit(job)} disabled={closing}>
          Edit
        </button>
        {!isClosed && (
          <button
            type="button"
            className={`btn-ghost btn-ghost--sm${closing ? " btn-loading" : ""}`}
            onClick={() => onClose(job)}
            disabled={closing}
          >
            {closing ? "Closing…" : "Close role"}
          </button>
        )}
      </div>
    </article>
  );
}
