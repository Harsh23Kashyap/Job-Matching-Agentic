import { cleanFieldText } from "./resumeClean.js";
import { enrichSummaryFromExtracted } from "./extractedSections.js";
import { mergeSkills, parseSkillsInput, skillsToFieldValue } from "./skills.js";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function normalizeEmail(value) {
  const cleaned = cleanFieldText(value).replace(/\s+/g, "");
  if (!cleaned) return "";
  return cleaned.toLowerCase();
}

function normalizePhone(value) {
  let cleaned = cleanFieldText(value);
  if (!cleaned) return "";
  cleaned = cleaned.replace(/[^\d+\s().-]/g, " ").replace(/\s+/g, " ").trim();
  return cleaned;
}

export function normalizeUrl(value) {
  let cleaned = cleanFieldText(value);
  if (!cleaned) return "";
  cleaned = cleaned.replace(/\s+/g, "").replace(/[>,;)]+$/, "");
  const lower = cleaned.toLowerCase();
  if (lower.startsWith("www.")) return `https://${cleaned}`;
  if (!/^https?:\/\//i.test(cleaned)) return `https://${cleaned}`;
  return cleaned;
}

function normalizeSkillsValue(value) {
  return skillsToFieldValue(parseSkillsInput(value));
}

function hasMeaningfulValue(key, value) {
  if (value == null) return false;
  if (key === "other_links") return Array.isArray(value) && value.length > 0;
  if (key === "remote_preference") return value === true;
  if (key === "experience_years") return value !== "" && value != null && Number(value) > 0;
  if (typeof value === "number") return value > 0;
  return String(value).trim().length > 0;
}

/** Clean and normalize profile field values after API or extraction. */
export function normalizeProfileFields(fields) {
  const next = { ...fields };
  next.name = cleanFieldText(fields.name).replace(/\s+/g, " ").trim();
  next.email = normalizeEmail(fields.email);
  next.phone = normalizePhone(fields.phone);
  next.linkedin = fields.linkedin ? normalizeUrl(fields.linkedin) : "";
  next.portfolio = fields.portfolio ? normalizeUrl(fields.portfolio) : "";
  next.summary = cleanFieldText(fields.summary);
  next.skills = normalizeSkillsValue(fields.skills);
  next.other_links = (fields.other_links || [])
    .map((link) => normalizeUrl(link))
    .filter(Boolean);
  if (next.preferred_currency) {
    next.preferred_currency = String(next.preferred_currency).trim().toUpperCase();
  }
  return next;
}

/**
 * Merge extracted resume fields into existing form state without wiping good data.
 * Extracted values win when present; skills are union-merged.
 */
export function mergeExtractedIntoFields(existing, extractedRaw) {
  const extracted = normalizeProfileFields({
    ...existing,
    name: extractedRaw.name ?? existing.name,
    skills: Array.isArray(extractedRaw.skills)
      ? extractedRaw.skills.join(", ")
      : extractedRaw.skills ?? existing.skills,
    experience_years: extractedRaw.experience_years ?? existing.experience_years,
    preferred_salary: extractedRaw.preferred_salary ?? existing.preferred_salary,
    preferred_currency: extractedRaw.preferred_currency ?? existing.preferred_currency,
    remote_preference: extractedRaw.remote_preference ?? existing.remote_preference,
    summary: extractedRaw.summary ?? existing.summary,
    email: extractedRaw.email ?? existing.email,
    phone: extractedRaw.phone ?? existing.phone,
    linkedin: extractedRaw.linkedin ?? existing.linkedin,
    portfolio: extractedRaw.portfolio ?? existing.portfolio,
    other_links: extractedRaw.other_links ?? existing.other_links,
  });

  const merged = { ...existing };

  for (const key of [
    "name",
    "email",
    "phone",
    "linkedin",
    "portfolio",
    "summary",
    "preferred_currency",
  ]) {
    if (hasMeaningfulValue(key, extracted[key])) {
      merged[key] = extracted[key];
    }
  }

  if (hasMeaningfulValue("experience_years", extracted.experience_years)) {
    merged.experience_years = extracted.experience_years;
  }

  if (extracted.preferred_salary != null && extracted.preferred_salary !== "") {
    merged.preferred_salary = extracted.preferred_salary;
  }

  if (extracted.remote_preference === true) {
    merged.remote_preference = true;
  }

  if (extracted.skills?.trim()) {
    merged.skills = skillsToFieldValue(mergeSkills(existing.skills, parseSkillsInput(extracted.skills)));
  }

  if (extracted.other_links?.length) {
    const seen = new Set();
    merged.other_links = [...(existing.other_links || []), ...extracted.other_links].filter((link) => {
      const key = link.toLowerCase();
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  merged.summary = enrichSummaryFromExtracted(merged.summary, extractedRaw);

  return normalizeProfileFields(merged);
}

export function isValidEmailFormat(email) {
  return !email?.trim() || EMAIL_RE.test(email.trim());
}
