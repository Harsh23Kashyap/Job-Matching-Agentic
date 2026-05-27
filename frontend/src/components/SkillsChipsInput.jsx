import { useRef, useState } from "react";
import {
  commitSkillDraft,
  parseSkillsInput,
  skillsToFieldValue,
  splitSkillTokens,
} from "../utils/skills.js";

export default function SkillsChipsInput({
  id,
  value,
  onChange,
  error,
  required,
  suggestedSkills = [],
  onAddSuggested,
  addingSkill = "",
}) {
  const chips = parseSkillsInput(value);
  const [draft, setDraft] = useState("");
  const inputRef = useRef(null);

  const updateSkills = (nextSkills) => {
    onChange(skillsToFieldValue(nextSkills));
  };

  const commitDraft = (raw) => {
    const next = commitSkillDraft(chips, raw);
    if (next.length === chips.length && !splitSkillTokens(raw).length) return;
    updateSkills(next);
    setDraft("");
  };

  const remove = (skill) => {
    updateSkills(chips.filter((item) => item !== skill));
  };

  const handleChange = (event) => {
    const next = event.target.value;
    if (/[,;\n|\t]/.test(next)) {
      commitDraft(next);
      return;
    }
    setDraft(next);
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      commitDraft(draft);
    }
    if (event.key === "Backspace" && !draft && chips.length) {
      remove(chips[chips.length - 1]);
    }
  };

  const handlePaste = (event) => {
    const pasted = event.clipboardData.getData("text");
    if (!/[,;\n|\t]/.test(pasted)) return;
    event.preventDefault();
    commitDraft(draft ? `${draft},${pasted}` : pasted);
  };

  const handleBlur = () => {
    if (draft.trim()) commitDraft(draft);
  };

  const handleContainerClick = () => {
    inputRef.current?.focus();
  };

  return (
    <div className={`skills-chips-input${error ? " has-error" : ""}`}>
      <div
        className="skills-chips-scroll"
        onClick={handleContainerClick}
        role="group"
        aria-label="Skills"
      >
        <div className="skills-chips-wrap">
          {chips.map((skill) => (
            <span key={skill} className="skill-chip">
              <span className="skill-chip-label">{skill}</span>
              <button type="button" aria-label={`Remove ${skill}`} onClick={() => remove(skill)}>
                ×
              </button>
            </span>
          ))}
          <input
            ref={inputRef}
            id={id}
            type="text"
            className="skill-chip-input skill-chip-input--inline"
            placeholder={chips.length ? "Add another…" : "Add a skill…"}
            value={draft}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            onPaste={handlePaste}
            onBlur={handleBlur}
            aria-invalid={Boolean(error)}
          />
        </div>
      </div>
      {!chips.length && required && (
        <input
          type="text"
          required
          className="skills-required-fallback"
          tabIndex={-1}
          aria-hidden="true"
          value=""
          onChange={() => {}}
        />
      )}
      {suggestedSkills.length > 0 && (
        <div className="skills-suggestions">
          <p className="skills-suggestions__label">Suggested skills</p>
          <div className="skills-suggestions__list">
            {suggestedSkills.map((skill) => {
              const added = chips.includes(skill);
              return (
                <button
                  key={skill}
                  type="button"
                  className={`skill-suggestion-chip${added ? " skill-suggestion-chip--added" : ""}`}
                  disabled={added || addingSkill === skill}
                  onClick={() => onAddSuggested?.(skill)}
                >
                  {addingSkill === skill ? "Adding…" : added ? skill : `+ ${skill}`}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
