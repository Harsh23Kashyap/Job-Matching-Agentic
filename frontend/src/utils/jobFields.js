import { skillsToPayload } from "./skills.js";

export const JOB_DESCRIPTION_MAX = 2000;

export const JOB_TYPE_OPTIONS = [
  "",
  "Full-time",
  "Part-time",
  "Contract",
  "Internship",
  "Temporary",
];

export const EMPTY_JOB_FIELDS = {
  title: "",
  company: "",
  location: "",
  job_type: "",
  required_skills: "",
  required_experience: "",
  budget_currency: "INR",
  budget_min: null,
  budget_max: null,
  remote_policy: false,
  description: "",
};

export function jobFieldsFromExtracted(ext = {}) {
  return {
    title: ext.title || "",
    company: ext.company || "",
    location: ext.location || "",
    job_type: ext.job_type || "",
    required_skills: Array.isArray(ext.required_skills) ? ext.required_skills.join(", ") : "",
    required_experience: ext.required_experience != null ? String(ext.required_experience) : "",
    budget_currency: ext.budget_currency || "INR",
    budget_min: ext.budget_min ?? ext.budget ?? null,
    budget_max: ext.budget_max ?? ext.budget ?? null,
    remote_policy: Boolean(ext.remote_policy),
    description: ext.description || "",
  };
}

export function jobToPayload(fields, jobId = null) {
  const min = fields.budget_min != null && fields.budget_min !== "" ? Number(fields.budget_min) : null;
  const max = fields.budget_max != null && fields.budget_max !== "" ? Number(fields.budget_max) : null;
  const exp = parseFloat(fields.required_experience);

  const payload = {
    title: fields.title.trim(),
    company: fields.company?.trim() || null,
    location: fields.location?.trim() || null,
    job_type: fields.job_type?.trim() || null,
    required_skills: skillsToPayload(fields.required_skills),
    required_experience: Number.isFinite(exp) && exp >= 0 ? exp : 0,
    budget_currency: fields.budget_currency || "INR",
    budget_min: min,
    budget_max: max,
    budget: max ?? min ?? null,
    remote_policy: fields.remote_policy,
    description: fields.description.trim(),
  };
  if (jobId) payload.id = jobId;
  return payload;
}

export function jobFromApi(job) {
  return {
    title: job.title || "",
    company: job.company || "",
    location: job.location || "",
    job_type: job.job_type || "",
    required_skills: Array.isArray(job.required_skills) ? job.required_skills.join(", ") : "",
    required_experience: job.required_experience != null ? String(job.required_experience) : "",
    budget_currency: job.budget_currency || "INR",
    budget_min: job.budget_min ?? job.budget ?? null,
    budget_max: job.budget_max ?? job.budget ?? null,
    remote_policy: Boolean(job.remote_policy),
    description: job.description || "",
  };
}

export function validateJobFields(fields) {
  const errors = {};
  if (!fields.title?.trim()) errors.title = "Job title is required.";
  const skills = skillsToPayload(fields.required_skills);
  if (!skills.length) {
    errors.required_skills = "Add at least one required skill.";
  }
  if (fields.required_experience !== "" && fields.required_experience != null) {
    const exp = parseFloat(fields.required_experience);
    if (Number.isNaN(exp) || exp < 0 || exp > 50) {
      errors.required_experience = "Enter a value between 0 and 50 years.";
    }
  }
  const min = fields.budget_min != null ? Number(fields.budget_min) : null;
  const max = fields.budget_max != null ? Number(fields.budget_max) : null;
  if (min != null && max != null && min > max) {
    errors.budget_max = "Max budget should be at least the min budget.";
  }
  if (fields.description && fields.description.length > JOB_DESCRIPTION_MAX) {
    errors.description = `Description must be ${JOB_DESCRIPTION_MAX} characters or fewer.`;
  }
  return errors;
}
