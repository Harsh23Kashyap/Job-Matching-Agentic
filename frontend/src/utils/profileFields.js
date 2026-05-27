import { parseAmount } from "./format.js";
import { skillsToPayload } from "./skills.js";

export const EMPTY_PROFILE_FIELDS = {
  name: "",
  skills: "",
  experience_years: 0,
  preferred_salary: "",
  preferred_currency: "INR",
  remote_preference: false,
  summary: "",
  email: "",
  phone: "",
  linkedin: "",
  portfolio: "",
  other_links: [],
};

export function profileFromApi(profile) {
  return {
    id: profile.id,
    name: profile.name || "",
    skills: (profile.skills || []).join(", "),
    experience_years: profile.experience_years ?? 0,
    preferred_salary: profile.preferred_salary ?? "",
    preferred_currency: profile.preferred_currency || "INR",
    remote_preference: profile.remote_preference ?? false,
    summary: profile.summary || "",
    email: profile.email || "",
    phone: profile.phone || "",
    linkedin: profile.linkedin || "",
    portfolio: profile.portfolio || "",
    other_links: profile.other_links || [],
  };
}

export function fieldsFromExtracted(ext) {
  return {
    name: ext.name || "",
    skills: (ext.skills || []).join(", "),
    experience_years: ext.experience_years ?? 0,
    preferred_salary: ext.preferred_salary ?? "",
    preferred_currency: ext.preferred_currency || "INR",
    remote_preference: ext.remote_preference ?? false,
    summary: ext.summary || "",
    email: ext.email || "",
    phone: ext.phone || "",
    linkedin: ext.linkedin || "",
    portfolio: ext.portfolio || "",
    other_links: ext.other_links || [],
  };
}

export function profileToPayload(fields) {
  return {
    id: fields.id,
    name: fields.name.trim(),
    skills: skillsToPayload(fields.skills),
    experience_years: Number(fields.experience_years) || 0,
    preferred_salary: parseAmount(fields.preferred_salary),
    preferred_currency: fields.preferred_currency || "INR",
    remote_preference: fields.remote_preference,
    summary: fields.summary,
    email: fields.email?.trim() || "",
    phone: fields.phone?.trim() || "",
    linkedin: fields.linkedin?.trim() || "",
    portfolio: fields.portfolio?.trim() || "",
    other_links: (fields.other_links || []).map((l) => l.trim()).filter(Boolean),
  };
}
