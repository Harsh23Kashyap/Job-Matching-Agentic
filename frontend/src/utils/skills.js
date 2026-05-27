/** Parse skills from comma-separated form value or API array. */
export function parseSkillsInput(value) {
  if (Array.isArray(value)) {
    return dedupeSkills(value.map((skill) => String(skill).trim()).filter(Boolean));
  }
  if (value == null || !String(value).trim()) return [];
  return dedupeSkills(
    String(value)
      .split(",")
      .map((skill) => skill.trim())
      .filter(Boolean),
  );
}

/** Remove duplicates case-insensitively while preserving first-seen casing. */
export function dedupeSkills(skills) {
  const seen = new Set();
  const out = [];
  for (const skill of skills) {
    const trimmed = String(skill).trim();
    if (!trimmed) continue;
    const key = trimmed.toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(trimmed);
  }
  return out;
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
