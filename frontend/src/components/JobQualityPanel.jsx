import Button from "./Button.jsx";

const GRADE_LABELS = {
  strong: "Strong posting",
  good: "Good posting",
  fair: "Fair — room to improve",
  needs_work: "Needs work",
};

function IssueList({ title, items = [] }) {
  if (!items.length) return null;
  return (
    <div className="job-quality-panel__block">
      <h4>{title}</h4>
      <ul className="job-quality-panel__issues">
        {items.map((item) => (
          <li
            key={item.id}
            className={item.severity === "error" ? "job-quality-panel__issue--error" : ""}
          >
            {item.message}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function JobQualityPanel({
  quality,
  loading = false,
  onAddSkill,
  addingSkill = "",
}) {
  if (!quality && !loading) return null;

  const score = quality?.score ?? 0;
  const filled = Math.round(score / 10);
  const grade = quality?.grade ? GRADE_LABELS[quality.grade] || quality.grade : "Analyzing…";

  return (
    <section className="job-quality-panel portal-panel portal-panel--elevated" aria-live="polite">
      <div className="job-quality-panel__head">
        <div>
          <h3 className="job-quality-panel__title">Job quality</h3>
          <p className="form-helper job-quality-panel__subtitle">
            {loading ? "Checking your posting…" : quality?.summary}
          </p>
        </div>
        <div className="job-quality-panel__score-badge" data-grade={quality?.grade || "fair"}>
          <span className="job-quality-panel__score-value">{loading ? "…" : score}</span>
          <span className="job-quality-panel__score-label">{loading ? "Score" : grade}</span>
        </div>
      </div>

      <div className="profile-strength-bar job-quality-panel__bar" aria-hidden="true">
        {Array.from({ length: 10 }).map((_, i) => (
          <span key={i} className={i < filled ? "filled" : ""} />
        ))}
      </div>

      {!loading && quality && (
        <>
          <IssueList title="Missing fields" items={quality.missing_fields} />
          <IssueList title="Unclear requirements" items={quality.unclear_requirements} />
          <IssueList title="Salary & budget" items={quality.salary_warnings} />
          <IssueList title="Experience alignment" items={quality.experience_warnings} />

          {quality.skill_suggestions?.length > 0 && (
            <div className="job-quality-panel__block">
              <h4>Suggested skills</h4>
              <p className="form-helper">Common skills for this role that are not listed yet.</p>
              <div className="job-quality-panel__suggestions">
                {quality.skill_suggestions.map((skill) => (
                  <Button
                    key={skill}
                    type="button"
                    className="btn-secondary btn-sm job-quality-panel__skill-btn"
                    loading={addingSkill === skill}
                    loadingLabel="Adding…"
                    onClick={() => onAddSkill?.(skill)}
                  >
                    + {skill}
                  </Button>
                ))}
              </div>
            </div>
          )}

          {!quality.missing_fields?.length
            && !quality.unclear_requirements?.length
            && !quality.salary_warnings?.length
            && !quality.experience_warnings?.length
            && !quality.skill_suggestions?.length && (
              <p className="form-helper job-quality-panel__all-clear">
                No issues flagged — posting looks ready for matching.
              </p>
          )}
        </>
      )}
    </section>
  );
}
