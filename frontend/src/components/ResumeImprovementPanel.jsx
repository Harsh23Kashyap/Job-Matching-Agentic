import { useEffect, useState } from "react";
import { fetchResumeSuggestions, apiErrorMessage } from "../api/client.js";
import SkillChip, { SkillChipList } from "./SkillChip.jsx";

function ChecklistStatus({ status }) {
  const label = status === "pass" ? "Pass" : status === "fail" ? "Needs work" : "Review";
  return <span className={`resume-coach-status resume-coach-status--${status}`}>{label}</span>;
}

export default function ResumeImprovementPanel({ jobId, jobTitle, onClose }) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [data, setData] = useState(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoading(true);
      setError("");
      try {
        const result = await fetchResumeSuggestions(jobId);
        if (!cancelled) setData(result);
      } catch (err) {
        if (!cancelled) setError(apiErrorMessage(err, "Could not load resume suggestions."));
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [jobId]);

  if (loading) {
    return (
      <section className="match-drawer-card resume-coach-panel">
        <p className="resume-coach-loading">Analyzing your profile for {jobTitle}…</p>
      </section>
    );
  }

  if (error) {
    return (
      <section className="match-drawer-card resume-coach-panel">
        <p className="resume-coach-error">{error}</p>
        <button type="button" className="btn-secondary resume-coach-close" onClick={onClose}>
          Close suggestions
        </button>
      </section>
    );
  }

  if (!data) return null;

  return (
    <section className="match-drawer-card resume-coach-panel" aria-labelledby="resume-coach-title">
      <div className="resume-coach-head">
        <div>
          <h3 id="resume-coach-title">Resume suggestions for {data.job_title || jobTitle}</h3>
          <p className="resume-coach-disclaimer">{data.disclaimer}</p>
          {data.message && <p className="resume-coach-note">{data.message}</p>}
        </div>
        <button type="button" className="btn-secondary resume-coach-close" onClick={onClose}>
          Close
        </button>
      </div>

      <div className="resume-coach-section">
        <h4>Missing keywords</h4>
        {data.missing_keywords?.length ? (
          <SkillChipList skills={data.missing_keywords} variant="missing" />
        ) : (
          <SkillChip variant="empty">No major keyword gaps flagged</SkillChip>
        )}
      </div>

      <div className="resume-coach-section">
        <h4>Weak or missing skills</h4>
        <div className="resume-coach-skills-grid">
          <div>
            <p className="resume-coach-label">Missing required skills</p>
            {data.missing_skills?.length ? (
              <SkillChipList skills={data.missing_skills} variant="missing" />
            ) : (
              <SkillChip variant="empty">Required skills covered in your profile</SkillChip>
            )}
          </div>
          <div>
            <p className="resume-coach-label">Under-emphasized skills</p>
            {data.weak_skills?.length ? (
              <SkillChipList skills={data.weak_skills} variant="match" />
            ) : (
              <SkillChip variant="empty">Listed skills appear in your summary or resume text</SkillChip>
            )}
          </div>
        </div>
      </div>

      <div className="resume-coach-section">
        <h4>Suggested summary rewrite</h4>
        <blockquote className="resume-coach-quote">{data.suggested_summary}</blockquote>
      </div>

      {data.bullet_improvements?.length > 0 && (
        <div className="resume-coach-section">
          <h4>Suggested bullet improvements</h4>
          <ul className="resume-coach-bullets">
            {data.bullet_improvements.map((row, index) => (
              <li key={`${row.original}-${index}`}>
                <p className="resume-coach-bullet-original">
                  <span>Current</span> {row.original}
                </p>
                <p className="resume-coach-bullet-suggested">
                  <span>Suggested</span> {row.suggested}
                </p>
                {row.reason && <p className="resume-coach-bullet-reason">{row.reason}</p>}
              </li>
            ))}
          </ul>
        </div>
      )}

      {data.ats_checklist?.length > 0 && (
        <div className="resume-coach-section">
          <h4>ATS-style checklist</h4>
          <ul className="resume-coach-checklist">
            {data.ats_checklist.map((row) => (
              <li key={row.item}>
                <div className="resume-coach-checklist-row">
                  <strong>{row.item}</strong>
                  <ChecklistStatus status={row.status} />
                </div>
                <p>{row.tip}</p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}
