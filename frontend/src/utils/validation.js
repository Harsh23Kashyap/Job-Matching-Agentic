import { parseAmount } from "./format.js";

const SUMMARY_MAX = 500;

function isValidUrl(value) {
  if (!value?.trim()) return true;
  try {
    const url = new URL(value.includes("://") ? value : `https://${value}`);
    return Boolean(url.hostname);
  } catch {
    return false;
  }
}

export function validateProfileFields(fields, { requireSkills = false } = {}) {
  const errors = {};

  if (!fields.name?.trim()) {
    errors.name = "Name is required.";
  }

  if (requireSkills && !fields.skills?.trim()) {
    errors.skills = "Add at least one skill.";
  }

  const exp = fields.experience_years;
  if (exp !== "" && exp != null) {
    const n = Number(exp);
    if (Number.isNaN(n) || n < 0 || n > 50) {
      errors.experience_years = "Enter a value between 0 and 50 years.";
    }
  }

  if (fields.preferred_salary !== "" && fields.preferred_salary != null) {
    const sal = parseAmount(fields.preferred_salary);
    if (sal == null) {
      errors.preferred_salary = "Enter a valid annual compensation amount (whole numbers only).";
    }
  }

  if (fields.summary && fields.summary.length > SUMMARY_MAX) {
    errors.summary = `Summary must be ${SUMMARY_MAX} characters or fewer.`;
  }

  if (fields.email?.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(fields.email.trim())) {
    errors.email = "Enter a valid email address.";
  }

  for (const [key, label] of [
    ["linkedin", "LinkedIn"],
    ["portfolio", "Portfolio"],
  ]) {
    if (fields[key]?.trim() && !isValidUrl(fields[key])) {
      errors[key] = `Enter a valid ${label} URL.`;
    }
  }

  return errors;
}

export function profileStrength(fields) {
  let score = 0;
  const hints = [];

  if (fields.name?.trim()) score += 15;
  else hints.push("Add your name");

  if (fields.skills?.trim()) score += 20;
  else hints.push("Add skills");

  if (fields.experience_years !== "" && fields.experience_years != null) score += 10;
  else hints.push("Add years of experience");

  if (fields.preferred_salary) score += 10;
  else hints.push("Add expected compensation");

  if (fields.summary?.trim()) score += 10;
  else hints.push("Add a short summary");

  if (fields.remote_preference != null) score += 5;

  const hasContact = Boolean(
    fields.email?.trim()
      || fields.phone?.trim()
      || fields.linkedin?.trim()
      || fields.portfolio?.trim()
      || (fields.other_links?.length > 0),
  );
  if (hasContact) score += 15;
  else hints.push("Add contact details");

  if (fields.linkedin?.trim() || fields.portfolio?.trim()) score += 15;

  return {
    percent: Math.min(score, 100),
    hint: hints.length ? `${hints[0]} to improve matches.` : "Your profile is in great shape.",
  };
}

export { SUMMARY_MAX };
