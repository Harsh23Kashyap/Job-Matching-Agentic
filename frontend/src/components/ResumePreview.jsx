import { useState } from "react";

export default function ResumePreview({ text }) {
  const [expanded, setExpanded] = useState(false);
  if (!text) return null;

  return (
    <div className={`resume-preview${expanded ? " resume-preview--expanded" : ""}`}>
      <div className="resume-preview-header">
        <h3>Resume preview</h3>
        <p className="field-helper">We found this text from your resume. Review it before saving.</p>
      </div>
      <div className="resume-preview-body">{text}</div>
      {text.length > 180 && (
        <button type="button" className="btn-text" onClick={() => setExpanded(!expanded)}>
          {expanded ? "Show less" : "Show more"}
        </button>
      )}
    </div>
  );
}
