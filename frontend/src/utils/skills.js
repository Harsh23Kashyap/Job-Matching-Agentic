/** Parse skills from comma-separated form value or API array. */
import { normalizeSkillList } from "./skillCatalog.js";

export function parseSkillsInput(value) {
  if (Array.isArray(value)) {
    return normalizeSkillList(value.map((skill) => String(skill).trim()).filter(Boolean));
  }
  if (value == null || !String(value).trim()) return [];
  return normalizeSkillList(
    String(value)
      .split(",")
      .map((skill) => skill.trim())
      .filter(Boolean),
  );
}

/** Remove duplicates case-insensitively while preserving first-seen casing. */
export function dedupeSkills(skills) {
  return normalizeSkillList(skills);
}

export function mergeSkills(existing, incoming) {
  return dedupeSkills([...parseSkillsInput(existing), ...incoming.map((s) => String(s).trim()).filter(Boolean)]);
}

export function skillsToFieldValue(skills) {
  return dedupeSkills(parseSkillsInput(skills)).join(", ");
}

/** Clean array for backend payloads. */
export function skillsToPayload(value) {
  return dedupeSkills(parseSkillsInput(value));
}

/** Split pasted or typed bulk input into individual skills. */
export function splitSkillTokens(raw) {
  return String(raw ?? "")
    .split(/[,;\n|\t]+/)
    .map((skill) => skill.trim())
    .filter(Boolean);
}

export function commitSkillDraft(existing, draft) {
  const tokens = splitSkillTokens(draft);
  if (!tokens.length) return parseSkillsInput(existing);
  return mergeSkills(existing, tokens);
}
