import { useRef, useState } from "react";

function parseSkills(value) {
  if (!value?.trim()) return [];
  return value.split(",").map((s) => s.trim()).filter(Boolean);
}

export default function SkillsChipsInput({ id, value, onChange, error, required }) {
  const chips = parseSkills(value);
  const [adding, setAdding] = useState(false);
  const [draft, setDraft] = useState("");
  const inputRef = useRef(null);

  const commit = (raw) => {
    const next = raw.trim();
    if (!next) {
      setAdding(false);
      return;
    }
    const merged = [...new Set([...chips, ...next])];
    onChange(merged.join(", "));
    setDraft("");
    setAdding(false);
  };

  const remove = (skill) => {
    onChange(chips.filter((s) => s !== skill).join(", "));
  };

  const startAdding = () => {
    setAdding(true);
    setTimeout(() => inputRef.current?.focus(), 0);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault();
      commit(draft.replace(/,$/, ""));
    }
    if (e.key === "Escape") {
      setDraft("");
      setAdding(false);
    }
    if (e.key === "Backspace" && !draft && chips.length) {
      remove(chips[chips.length - 1]);
    }
  };

  const handlePaste = (e) => {
    const pasted = e.clipboardData.getData("text");
    if (!pasted.includes(",") && !pasted.includes(";") && !pasted.includes("\n")) return;
    e.preventDefault();
    const parts = pasted.split(/[,;\n]+/).map((s) => s.trim()).filter(Boolean);
    if (parts.length) {
      onChange([...new Set([...chips, ...parts])].join(", "));
      setDraft("");
      setAdding(false);
    }
  };

  return (
    <div className={`skills-chips-input${error ? " has-error" : ""}`}>
      <div className="skills-chips-scroll">
        <div className="skills-chips-wrap">
          {chips.map((skill) => (
            <span key={skill} className="skill-chip">
              {skill}
              <button type="button" aria-label={`Remove ${skill}`} onClick={() => remove(skill)}>
                ×
              </button>
            </span>
          ))}
          {adding ? (
            <input
              ref={inputRef}
              id={id}
              type="text"
              className="skill-chip-input"
              value={draft}
              placeholder="Skill name"
              onChange={(e) => setDraft(e.target.value)}
              onKeyDown={handleKeyDown}
              onPaste={handlePaste}
              onBlur={() => commit(draft.replace(/,$/, ""))}
            />
          ) : (
            <button type="button" className="skill-chip skill-chip--add" onClick={startAdding}>
              + Add skill
            </button>
          )}
        </div>
      </div>
      {!chips.length && required && (
        <input type="text" required className="skills-required-fallback" tabIndex={-1} aria-hidden="true" value="" onChange={() => {}} />
      )}
    </div>
  );
}
