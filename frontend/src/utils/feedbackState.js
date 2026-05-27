/** Build UI state maps from /feedback/me rows (latest per target). */
export function buildFeedbackMaps(feedbackRows = [], { contextId } = {}) {
  const saved = new Set();
  const notInterested = new Set();
  const applied = new Set();
  const rejected = new Set();
  const contacted = new Set();

  for (const row of feedbackRows) {
    if (contextId != null && row.context_id !== contextId) continue;
    const id = row.target_id;
    switch (row.action) {
      case "save":
        saved.add(id);
        break;
      case "unsave":
        saved.delete(id);
        break;
      case "not_interested":
        notInterested.add(id);
        break;
      case "apply":
        applied.add(id);
        break;
      case "reject":
        rejected.add(id);
        break;
      case "contact":
        contacted.add(id);
        break;
      default:
        break;
    }
  }

  return { saved, notInterested, applied, rejected, contacted };
}
