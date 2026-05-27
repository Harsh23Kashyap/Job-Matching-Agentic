import { useEffect, useState } from "react";
import { fetchSimilarCandidates, fetchSimilarJobs, apiErrorMessage } from "../api/client.js";
import { matchPercent } from "../utils/format.js";
import SkillChip, { SkillChipList } from "./SkillChip.jsx";

function SimilarCard({ item }) {
  return (
    <article className="similar-card">
      <div className="similar-card__head">
        <div>
          <h4>{item.label}</h4>
          {item.subtitle && <p className="similar-card__subtitle">{item.subtitle}</p>}
        </div>
        <span className="similar-card__score">{matchPercent(item.similarity_score)}</span>
      </div>
      {item.matched_skills?.length > 0 && (
        <div className="similar-card__skills">
          <p className="similar-card__skills-label">Shared skills</p>
          <SkillChipList skills={item.matched_skills} limit={4} variant="match" />
        </div>
      )}
      {!item.matched_skills?.length && (
        <SkillChip variant="empty">Similar profile, few shared skill tags</SkillChip>
      )}
    </article>
  );
}

export default function SimilarRecommendations({ entityId, entityType, title }) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [items, setItems] = useState([]);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoading(true);
      setError("");
      try {
        const data =
          entityType === "jobs"
            ? await fetchSimilarJobs(entityId)
            : await fetchSimilarCandidates(entityId);
        if (!cancelled) setItems(data.items || []);
      } catch (err) {
        if (!cancelled) setError(apiErrorMessage(err, "Could not load recommendations."));
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [entityId, entityType]);

  if (loading) {
    return (
      <MatchDrawerCardShell title={title}>
        <p className="similar-panel__loading">Finding recommendations…</p>
      </MatchDrawerCardShell>
    );
  }

  if (error) {
    return (
      <MatchDrawerCardShell title={title}>
        <p className="similar-panel__error">{error}</p>
      </MatchDrawerCardShell>
    );
  }

  if (!items.length) {
    return (
      <MatchDrawerCardShell title={title}>
        <SkillChip variant="empty">No similar {entityType} found in the pool</SkillChip>
      </MatchDrawerCardShell>
    );
  }

  return (
    <MatchDrawerCardShell title={title}>
      <div className="similar-card-grid">
        {items.map((item) => (
          <SimilarCard key={item.id} item={item} />
        ))}
      </div>
    </MatchDrawerCardShell>
  );
}

function MatchDrawerCardShell({ title, children }) {
  return (
    <section className="match-drawer-card similar-panel">
      <h3 className="match-drawer-card__title">{title}</h3>
      {children}
    </section>
  );
}
