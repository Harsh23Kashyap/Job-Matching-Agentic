import { useMemo, useState } from "react";
import { resumePreviewMeta } from "../utils/resumeClean.js";

export default function ResumePreview({ text, defaultCollapsed = true }) {
  const [open, setOpen] = useState(!defaultCollapsed);
  const meta = useMemo(() => resumePreviewMeta(text), [text]);

  if (!text) return null;

  return (
    <details className={`resume-preview-card ${open ? "resume-preview-card--open" : ""}`} open={open}>
      <summary
        className="resume-preview-summary"
        onClick={(e) => {
          e.preventDefault();
          setOpen((prev) => !prev);
        }}
      >
        <div className="resume-preview-summary-text">
          <span className="resume-preview-title">Parsed resume text</span>
          <span className="resume-preview-meta">
            {meta.lines} line{meta.lines === 1 ? "" : "s"} · {meta.chars} chars
          </span>
        </div>
        <span className="resume-preview-toggle">{open ? "Hide" : "Show"}</span>
      </summary>
      {open && (
        <div className="resume-preview-body" aria-label="Cleaned resume text preview">
          {text}
        </div>
      )}
    </details>
  );
}
