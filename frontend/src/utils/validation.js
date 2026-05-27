const SUMMARY_MAX = 500;

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
    const sal = Number(String(fields.preferred_salary).replace(/[^\d]/g, ""));
    if (Number.isNaN(sal) || sal < 0) {
      errors.preferred_salary = "Enter a valid annual salary.";
    }
  }

  if (fields.summary && fields.summary.length > SUMMARY_MAX) {
    errors.summary = `Summary must be ${SUMMARY_MAX} characters or fewer.`;
  }

  return errors;
}

export function profileStrength(fields) {
  let score = 0;
  const hints = [];

  if (fields.name?.trim()) score += 20;
  else hints.push("Add your name");

  if (fields.skills?.trim()) score += 25;
  else hints.push("Add skills");

  if (fields.experience_years !== "" && fields.experience_years != null) score += 15;
  else hints.push("Add years of experience");

  if (fields.preferred_salary) score += 15;
  else hints.push("Add salary preference");

  if (fields.summary?.trim()) score += 15;
  else hints.push("Add a short summary");

  if (fields.remote_preference != null) score += 10;

  return {
    percent: Math.min(score, 100),
    hint: hints.length ? `${hints[0]} to improve matches.` : "Your profile is in great shape.",
  };
}

export { SUMMARY_MAX };
