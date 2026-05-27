import Button from "./Button.jsx";

const GRADE_LABELS = {
  strong: "Strong profile",
  good: "Good profile",
  fair: "Fair — room to improve",
  needs_work: "Needs work",
};

const PARSE_LEVEL_LABELS = {
  high: "High confidence",
  medium: "Medium confidence",
  low: "Low confidence",
  manual: "Manual entry",
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
            className={
              item.severity === "error"
                ? "job-quality-panel__issue--error"
                : item.severity === "info"
                  ? "job-quality-panel__issue--info"
                  : ""
            }
          >
            {item.message}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function ProfileQualityPanel({
  quality,
  loading = false,
  onAddSkill,
  addingSkill = "",
}) {
  if (!quality && !loading) return null;

  const score = quality?.score ?? 0;
  const filled = Math.round(score / 10);
  const grade = quality?.grade ? GRADE_LABELS[quality.grade] || quality.grade : "Analyzing…";
  const parsing = quality?.parsing_confidence;

  return (
    <section className="job-quality-panel profile-quality-panel portal-panel portal-panel--elevated" aria-live="polite">
      <div className="job-quality-panel__head">
        <div>
          <h3 className="job-quality-panel__title">Profile quality</h3>
          <p className="form-helper job-quality-panel__subtitle">
            {loading ? "Analyzing your profile…" : quality?.summary}
          </p>
          {!loading && quality?.completeness_percent != null && (
            <p className="form-helper profile-quality-panel__completeness">
              Completeness: {quality.completeness_percent}%
            </p>
          )}
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

      {!loading && parsing && (
        <div className="profile-quality-panel__parse" data-level={parsing.level}>
          <span className="profile-quality-panel__parse-label">
            Resume parsing: {PARSE_LEVEL_LABELS[parsing.level] || parsing.level}
            {typeof parsing.score === "number" ? ` (${parsing.score}%)` : ""}
          </span>
          <p className="form-helper">{parsing.message}</p>
        </div>
      )}

      {!loading && quality && (
        <>
          <IssueList title="Missing or incomplete" items={quality.missing_fields} />
          <IssueList title="Skills gaps" items={quality.missing_skills} />
          <IssueList title="Summary" items={quality.summary_warnings} />
          <IssueList title="Salary expectations" items={quality.salary_guidance} />
          <IssueList title="Improve match quality" items={quality.match_suggestions} />

          {quality.skill_suggestions?.length > 0 && (
            <div className="job-quality-panel__block">
              <h4>Suggested skills</h4>
              <p className="form-helper">Add skills commonly expected for your background.</p>
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
        </>
      )}
    </section>
  );
}
