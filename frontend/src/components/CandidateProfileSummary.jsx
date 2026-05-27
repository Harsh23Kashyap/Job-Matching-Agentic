import { SkillChipList } from "./SkillChip.jsx";
import ProfileStrength from "./ProfileStrength.jsx";
import {
  formatCandidateExperience,
  formatExpectedCompensation,
  formatRemotePreference,
} from "../utils/format.js";
import { parseSkillsInput } from "../utils/skills.js";

function MetaItem({ label, value, muted = false }) {
  return (
    <div className="candidate-profile-summary__meta-item">
      <span className="candidate-profile-summary__meta-label">{label}</span>
      <span className={`candidate-profile-summary__meta-value${muted ? " candidate-profile-summary__meta-value--muted" : ""}`}>
        {value}
      </span>
    </div>
  );
}

export default function CandidateProfileSummary({
  fields,
  strength,
  onEdit,
  editAction,
  footer,
}) {
  const skills = parseSkillsInput(fields.skills);
  const experience = formatCandidateExperience(fields.experience_years);
  const compensation = formatExpectedCompensation(fields);
  const remote = formatRemotePreference(fields);

  return (
    <article className="candidate-profile-summary">
      <header className="candidate-profile-summary__head">
        <div className="candidate-profile-summary__identity">
          <h2 className="candidate-profile-summary__name">{fields.name}</h2>
          {fields.summary?.trim() ? (
            <p className="candidate-profile-summary__summary">{fields.summary}</p>
          ) : (
            <p className="candidate-profile-summary__summary candidate-profile-summary__summary--empty">
              No summary yet. Add a short intro when you edit your profile.
            </p>
          )}
        </div>
        {editAction ?? (
          onEdit && (
            <button type="button" className="btn-secondary btn-sm candidate-profile-summary__edit" onClick={onEdit}>
              Edit profile
            </button>
          )
        )}
      </header>

      <ProfileStrength percent={strength.percent} hint={strength.hint} />

      <div className="candidate-profile-summary__meta">
        <MetaItem label="Experience" value={experience || "Not set"} muted={!experience} />
        <MetaItem label="Expected compensation" value={compensation || "Not set"} muted={!compensation} />
        <MetaItem label="Remote preference" value={remote || "Not set"} muted={!remote} />
      </div>

      <div className="candidate-profile-summary__skills">
        <span className="candidate-profile-summary__meta-label">Skills</span>
        {skills.length > 0 ? (
          <SkillChipList skills={skills} />
        ) : (
          <p className="candidate-profile-summary__meta-value candidate-profile-summary__meta-value--muted">
            No skills listed yet.
          </p>
        )}
      </div>

      {footer && <div className="candidate-profile-summary__footer">{footer}</div>}
    </article>
  );
}
