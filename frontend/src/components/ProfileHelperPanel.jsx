import { IconCheck } from "./icons.jsx";
import { parseSkillsInput } from "../utils/skills.js";
import { hasExtractedSections } from "../utils/extractedSections.js";

import ProfileQualityScore from "./ProfileQualityScore.jsx";

const PARSE_LABELS = {
  high: "High confidence",
  medium: "Medium confidence",
  low: "Low confidence",
  manual: "Manual entry",
};

function CheckRow({ ok, label }) {
  return (
    <li className={`profile-helper-check${ok ? " profile-helper-check--ok" : " profile-helper-check--pending"}`}>
      <span className="profile-helper-check__icon" aria-hidden="true">
        {ok ? <IconCheck size={12} /> : "○"}
      </span>
      <span>{label}</span>
    </li>
  );
}

export default function ProfileHelperPanel({
  fields,
  quality,
  loading = false,
  extractedSections = null,
  tips = [],
  hideScore = false,
}) {
  const parsing = quality?.parsing_confidence;

  const hasContact = Boolean(fields?.email?.trim() || fields?.phone?.trim());
  const hasSkills = parseSkillsInput(fields?.skills || "").length > 0;
  const hasProjects =
    Boolean(extractedSections?.projects?.length) ||
    (hasExtractedSections(extractedSections) && (extractedSections?.projects || []).length > 0);

  const salaryWarning =
    quality?.salary_guidance?.find((item) => item.severity !== "info")?.message ||
    quality?.salary_guidance?.[0]?.message;

  const missingFields = quality?.missing_fields?.slice(0, 4) ?? [];
  const matchTips = [
    ...(quality?.match_suggestions?.slice(0, 2).map((item) => item.message) ?? []),
    ...tips,
  ].slice(0, 3);

  return (
    <aside className="profile-helper-panel" aria-label="Profile helper">
      {!hideScore && (
        <ProfileQualityScore quality={quality} loading={loading} />
      )}

      <section className="profile-helper-panel__block">
        <h3>{hideScore ? "Profile quality" : "Completeness checks"}</h3>
        <ul className="profile-helper-checklist">
          <CheckRow ok={hasContact} label="Contact details found" />
          <CheckRow ok={hasSkills} label="Skills extracted" />
          <CheckRow ok={hasProjects} label="Projects detected" />
        </ul>
        {salaryWarning && (
          <p className="profile-helper-panel__warning">{salaryWarning}</p>
        )}
      </section>

      {(loading || parsing) && (
        <section className="profile-helper-panel__block">
          <h3>Parsing confidence</h3>
          {loading ? (
            <p className="profile-helper-panel__muted">Analyzing resume fields…</p>
          ) : (
            <>
              <p className="profile-helper-panel__parse-level">
                {PARSE_LABELS[parsing.level] || parsing.level}
                {typeof parsing.score === "number" ? ` · ${parsing.score}%` : ""}
              </p>
              <p className="profile-helper-panel__muted">{parsing.message}</p>
            </>
          )}
        </section>
      )}

      {missingFields.length > 0 && (
        <section className="profile-helper-panel__block">
          <h3>Missing fields</h3>
          <ul className="profile-helper-list">
            {missingFields.map((item) => (
              <li key={item.id}>{item.message}</li>
            ))}
          </ul>
        </section>
      )}

      {matchTips.length > 0 && (
        <section className="profile-helper-panel__block">
          <h3>Tips to improve matches</h3>
          <ul className="profile-helper-list">
            {matchTips.map((tip) => (
              <li key={tip}>{tip}</li>
            ))}
          </ul>
        </section>
      )}
    </aside>
  );
}
