/** Helpers for education/projects extracted from resume parse responses. */

export function formatEducationEntry(entry) {
  if (!entry) return "";
  if (typeof entry === "string") return entry.trim();
  const parts = [entry.degree, entry.institution, entry.text, entry.year].filter(Boolean);
  return parts.join(" · ").trim();
}

export function formatProjectEntry(entry) {
  if (!entry) return "";
  if (typeof entry === "string") return entry.trim();
  const name = entry.name || "Project";
  const tech = Array.isArray(entry.technologies) && entry.technologies.length
    ? ` (${entry.technologies.slice(0, 4).join(", ")})`
    : "";
  return `${name}${tech}`;
}

export function enrichSummaryFromExtracted(summary, extractedRaw = {}) {
  const base = String(summary || "").trim();
  const education = (extractedRaw.education || []).map(formatEducationEntry).filter(Boolean);
  const projects = (extractedRaw.projects || []).map(formatProjectEntry).filter(Boolean);

  if (base.length >= 40 || (!education.length && !projects.length)) {
    return base;
  }

  const parts = [];
  if (base) parts.push(base);
  if (education.length) {
    parts.push(`Education: ${education.slice(0, 2).join("; ")}.`);
  }
  if (projects.length) {
    parts.push(`Projects: ${projects.slice(0, 2).join("; ")}.`);
  }
  return parts.join(" ").trim().slice(0, 1200);
}

export function hasExtractedSections(extractedRaw = {}) {
  return Boolean(
    (extractedRaw.education || []).length ||
      (extractedRaw.projects || []).length ||
      (extractedRaw.responsibilities || []).length ||
      (extractedRaw.education_requirements || []).length,
  );
}
