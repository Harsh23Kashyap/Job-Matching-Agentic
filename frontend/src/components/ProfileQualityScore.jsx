import { profileQualityGradeLabel } from "../utils/profileQualityLabels.js";

export default function ProfileQualityScore({ quality, loading = false, compact = false }) {
  const score = quality?.score;
  const grade = profileQualityGradeLabel(quality?.grade);
  const hint = quality?.summary || quality?.missing_fields?.[0]?.message || null;
  const filled = typeof score === "number" ? Math.round(score / 10) : 0;

  return (
    <div className={`profile-quality-score${compact ? " profile-quality-score--compact" : ""}`}>
      <div className="profile-quality-score__head">
        <span className="profile-quality-score__label">
          Profile strength:{" "}
          <strong>{loading ? "…" : typeof score === "number" ? `${score} / 100` : ": "}</strong>
        </span>
        {!loading && grade ? <span className="profile-quality-score__grade">{grade}</span> : null}
      </div>
      <div className="profile-quality-score__bar" aria-hidden="true">
        {Array.from({ length: 10 }).map((_, i) => (
          <span key={i} className={i < filled ? "filled" : ""} />
        ))}
      </div>
      {!loading && hint ? <p className="profile-quality-score__hint">{hint}</p> : null}
      {loading ? <p className="profile-quality-score__hint">Analyzing profile…</p> : null}
    </div>
  );
}
