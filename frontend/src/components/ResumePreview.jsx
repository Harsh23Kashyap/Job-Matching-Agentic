import { useState } from "react";

export default function ResumePreview({ text, defaultCollapsed = true }) {
  const [open, setOpen] = useState(!defaultCollapsed);
  if (!text) return null;

  return (
    <div className="resume-preview-card">
      <div className="resume-preview-card-head">
        <div>
          <h3>Resume text preview</h3>
          <p className="field-helper">We extracted text from your resume. Review if needed.</p>
        </div>
        <button type="button" className="btn-secondary btn-sm" onClick={() => setOpen(!open)}>
          {open ? "Hide preview" : "Show preview"}
        </button>
      </div>
      {open && <div className="resume-preview-body">{text}</div>}
    </div>
  );
}
