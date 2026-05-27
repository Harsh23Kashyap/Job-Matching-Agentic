import SkillChip, { SkillChipList } from "./SkillChip.jsx";
import { matchPercent, matchScoreValue } from "../utils/format.js";
import { describeMatchDrivers } from "../utils/matchScoring.js";
import { normalizeSkillList } from "../utils/skillCatalog.js";
import {
  fitLevelClass,
  formatContributionPts,
  formatFitScore,
  formatWeightPct,
  resolveMatchExplanation,
} from "../utils/matchExplainability.js";

const SCORING_NOTE =
  "Overall score blends semantic fit (28%), skills (27%), role title (10%), experience (15%), compensation (10%), and remote preference (10%).";

function FitRow({ label, fit }) {
  if (!fit) return null;
  return (
    <li className={`match-explain-fit ${fitLevelClass(fit.label)}`}>
      <div className="match-explain-fit__head">
        <span className="match-explain-fit__label">{label}</span>
        <span className="match-explain-fit__badge">{fit.label}</span>
        <span className="match-explain-fit__score">{formatFitScore(fit.score)}</span>
      </div>
      <p className="match-explain-fit__reason">{fit.reason}</p>
    </li>
  );
}

function ScoreBreakdownList({ components, compact = false }) {
  if (!components?.length) return null;

  return (
    <div className={`match-explain-breakdown${compact ? " match-explain-breakdown--compact" : ""}`}>
      {components.map((component) => {
        const pct = Math.round(Number(component.score) * 100);
        return (
          <div key={component.key} className="match-explain-breakdown__row">
            <div className="match-explain-breakdown__head">
              <span>{component.label}</span>
              <span className="match-explain-breakdown__meta">
                {!compact && (
                  <span className="match-explain-breakdown__weight">
                    {formatWeightPct(component.weight)}
                  </span>
                )}
                <strong>{pct}%</strong>
                {!compact && component.contribution != null && (
                  <span className="match-explain-breakdown__contrib">
                    {formatContributionPts(component.contribution)}
                  </span>
                )}
              </span>
            </div>
            <div className="match-explain-breakdown__bar" aria-hidden="true">
              <span style={{ width: `${Math.max(pct, 2)}%` }} />
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default function MatchExplainability({ row, variant = "compact", className = "" }) {
  if (!row) return null;

  const explanation = resolveMatchExplanation(row);
  const matched = normalizeSkillList(explanation.matched_skills || []);
  const missing = normalizeSkillList(explanation.missing_skills || []);
  const breakdown = explanation.score_breakdown || [];
  const finalScore = explanation.final_score ?? matchScoreValue(row);

  if (variant === "list") {
    const reason =
      describeMatchDrivers(row) ||
      explanation.semantic?.reason ||
      explanation.experience?.reason ||
      null;

    return (
      <div className={`match-explain match-explain--list ${className}`.trim()}>
        <div className="match-explain__skills">
          <div className="match-explain__skill-group">
            <span className="match-explain__skill-label">Matched</span>
            {matched.length > 0 ? (
              <SkillChipList skills={matched} limit={5} variant="match" />
            ) : (
              <SkillChip variant="empty">No direct overlap</SkillChip>
            )}
          </div>
          <div className="match-explain__skill-group">
            <span className="match-explain__skill-label">Missing</span>
            {missing.length > 0 ? (
              <SkillChipList skills={missing} limit={4} variant="missing" />
            ) : (
              <SkillChip variant="empty">No major gaps</SkillChip>
            )}
          </div>
        </div>
        {reason && <p className="match-explain__reason">{reason}</p>}
      </div>
    );
  }

  if (variant === "compact") {
    return (
      <div className={`match-explain match-explain--compact ${className}`.trim()}>
        <div className="match-explain__skills">
          <div className="match-explain__skill-group">
            <span className="match-explain__skill-label">Matched</span>
            {matched.length > 0 ? (
              <SkillChipList skills={matched} limit={5} variant="match" />
            ) : (
              <SkillChip variant="empty">No direct overlap</SkillChip>
            )}
          </div>
          <div className="match-explain__skill-group">
            <span className="match-explain__skill-label">Missing</span>
            {missing.length > 0 ? (
              <SkillChipList skills={missing} limit={4} variant="missing" />
            ) : (
              <SkillChip variant="empty">No major gaps</SkillChip>
            )}
          </div>
        </div>

        <ul className="match-explain__fits match-explain__fits--compact">
          <FitRow label="Experience" fit={explanation.experience} />
          <FitRow label="Compensation" fit={explanation.compensation} />
          <FitRow label="Remote" fit={explanation.remote} />
          <FitRow label="Semantic" fit={explanation.semantic} />
        </ul>

        {breakdown.length > 0 && (
          <div className="match-explain__breakdown-wrap">
            <div className="match-explain__breakdown-head">
              <span>Score breakdown</span>
              <strong>{matchPercent(finalScore)} overall</strong>
            </div>
            <ScoreBreakdownList components={breakdown} compact />
          </div>
        )}
      </div>
    );
  }

  return (
    <div className={`match-explain match-explain--full ${className}`.trim()}>
      <section className="match-explain__section">
        <h4 className="match-explain__title">Skills</h4>
        <div className="match-explain__skills">
          <div className="match-explain__skill-group">
            <span className="match-explain__skill-label">Matched</span>
            {matched.length > 0 ? (
              <SkillChipList skills={matched} variant="match" />
            ) : (
              <SkillChip variant="empty">No direct overlap</SkillChip>
            )}
          </div>
          <div className="match-explain__skill-group">
            <span className="match-explain__skill-label">Missing</span>
            {missing.length > 0 ? (
              <SkillChipList skills={missing} variant="missing" />
            ) : (
              <SkillChip variant="empty">No major gaps flagged</SkillChip>
            )}
          </div>
        </div>
      </section>

      <section className="match-explain__section">
        <h4 className="match-explain__title">Fit signals</h4>
        <ul className="match-explain__fits">
          <FitRow label="Experience fit" fit={explanation.experience} />
          <FitRow label="Compensation fit" fit={explanation.compensation} />
          <FitRow label="Remote fit" fit={explanation.remote} />
          <FitRow label="Semantic reason" fit={explanation.semantic} />
        </ul>
      </section>

      {breakdown.length > 0 && (
        <section className="match-explain__section">
          <div className="match-explain__breakdown-head">
            <h4 className="match-explain__title">Final score breakdown</h4>
            <strong>{matchPercent(finalScore)} overall</strong>
          </div>
          <ScoreBreakdownList components={breakdown} />
          <p className="match-explain__note">{SCORING_NOTE}</p>
        </section>
      )}
    </div>
  );
}
