import { useEffect, useState } from "react";
import { fetchMyProfileOrNull, fetchResumeSuggestions, upsertCandidateProfile, apiErrorMessage } from "../api/client.js";
import { copyToClipboard } from "../utils/copyToClipboard.js";
import { profileFromApi, profileToPayload } from "../utils/profileFields.js";
import { notifyProfileUpdated } from "../utils/profileEvents.js";
import SkillChip, { SkillChipList } from "./SkillChip.jsx";
import { useToast } from "./Toast.jsx";

function ChecklistStatus({ status }) {
  const label = status === "pass" ? "Pass" : status === "fail" ? "Needs work" : "Review";
  return <span className={`resume-coach-status resume-coach-status--${status}`}>{label}</span>;
}

export default function ResumeImprovementPanel({ jobId, jobTitle, onClose }) {
  const { showToast } = useToast();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [data, setData] = useState(null);
  const [applying, setApplying] = useState(false);
  const [currentSummary, setCurrentSummary] = useState("");

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoading(true);
      setError("");
      try {
        const [result, profile] = await Promise.all([
          fetchResumeSuggestions(jobId),
          fetchMyProfileOrNull(),
        ]);
        if (!cancelled) {
          setData(result);
          setCurrentSummary(profile?.summary?.trim() || "");
        }
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
        <p className="resume-coach-loading">Checking your profile against {jobTitle}…</p>
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

  const bulletsText = (data.bullet_improvements || [])
    .map((row) => `• ${row.suggested}`)
    .join("\n");
  const canApplySummary =
    Boolean(data.suggested_summary?.trim()) &&
    data.suggested_summary.trim() !== currentSummary;

  const handleCopySummary = async () => {
    const ok = await copyToClipboard(data.suggested_summary || "");
    showToast(ok ? "Summary copied to clipboard." : "Could not copy summary.");
  };

  const handleCopyBullets = async () => {
    const ok = await copyToClipboard(bulletsText);
    showToast(ok ? "Bullets copied to clipboard." : "Could not copy bullets.");
  };

  const handleApplySummary = async () => {
    if (!canApplySummary || applying) return;
    setApplying(true);
    try {
      const profile = await fetchMyProfileOrNull();
      if (!profile) {
        showToast("Set up your profile before applying suggestions.");
        return;
      }
      const fields = profileFromApi(profile);
      const saved = await upsertCandidateProfile(
        profileToPayload({ ...fields, summary: data.suggested_summary.trim() }),
      );
      setCurrentSummary(saved.summary?.trim() || data.suggested_summary.trim());
      notifyProfileUpdated();
      showToast("Summary applied to your saved profile.");
    } catch (err) {
      showToast(apiErrorMessage(err, "Could not update your profile."));
    } finally {
      setApplying(false);
    }
  };

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
        <div className="resume-coach-section-head">
          <h4>Suggested summary rewrite</h4>
          <div className="resume-coach-copy-actions">
            <button type="button" className="btn-secondary btn-sm" onClick={handleCopySummary}>
              Copy summary
            </button>
            {canApplySummary && (
              <button
                type="button"
                className="btn-primary btn-sm"
                onClick={handleApplySummary}
                disabled={applying}
              >
                {applying ? "Applying…" : "Apply to profile"}
              </button>
            )}
          </div>
        </div>
        <blockquote className="resume-coach-quote">{data.suggested_summary}</blockquote>
      </div>

      {data.bullet_improvements?.length > 0 && (
        <div className="resume-coach-section">
          <div className="resume-coach-section-head">
            <h4>Suggested bullet improvements</h4>
            <button type="button" className="btn-secondary btn-sm" onClick={handleCopyBullets}>
              Copy bullets
            </button>
          </div>
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
