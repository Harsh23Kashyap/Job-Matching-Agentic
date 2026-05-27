import { useRef, useState } from "react";

function normalizeUrl(raw) {
  const trimmed = raw.trim().replace(/[,;]+$/, "");
  if (!trimmed) return "";
  if (/^https?:\/\//i.test(trimmed)) return trimmed;
  if (/^www\./i.test(trimmed)) return `https://${trimmed}`;
  if (trimmed.includes(".") && !trimmed.includes(" ")) return `https://${trimmed}`;
  return trimmed;
}

export default function LinksChipsInput({ id, value = [], onChange, error }) {
  const links = Array.isArray(value) ? value : [];
  const [adding, setAdding] = useState(false);
  const [draft, setDraft] = useState("");
  const inputRef = useRef(null);

  const commit = (raw) => {
    const next = normalizeUrl(raw);
    if (!next) {
      setAdding(false);
      return;
    }
    if (!links.includes(next)) {
      onChange([...links, next]);
    }
    setDraft("");
    setAdding(false);
  };

  const remove = (link) => {
    onChange(links.filter((l) => l !== link));
  };

  const startAdding = () => {
    setAdding(true);
    setTimeout(() => inputRef.current?.focus(), 0);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      commit(draft);
    }
    if (e.key === "Escape") {
      setDraft("");
      setAdding(false);
    }
    if (e.key === "Backspace" && !draft && links.length) {
      remove(links[links.length - 1]);
    }
  };

  return (
    <div className={`skills-chips-scroll${error ? " field-error-border" : ""}`}>
      <div className="skills-chips-wrap">
        {links.map((link) => (
          <span key={link} className="skill-chip">
            <a href={link} target="_blank" rel="noreferrer noopener" className="link-chip-text">
              {link.replace(/^https?:\/\//, "")}
            </a>
            <button type="button" onClick={() => remove(link)} aria-label={`Remove ${link}`}>
              ×
            </button>
          </span>
        ))}
        {adding ? (
          <input
            ref={inputRef}
            id={id}
            className="skills-chips-field"
            type="url"
            placeholder="https://…"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={handleKeyDown}
            onBlur={() => commit(draft)}
          />
        ) : (
          <button type="button" className="skill-chip skill-chip--add" onClick={startAdding}>
            + Add link
          </button>
        )}
      </div>
    </div>
  );
}
