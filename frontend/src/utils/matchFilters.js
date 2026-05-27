import { matchScoreValue } from "./format.js";
import { resolveMatchExplanation } from "./matchExplainability.js";

export const MATCH_FILTER_DEFAULTS = {
  search: "",
  skills: [],
  remoteOnly: false,
  minMatch: 0,
  maxMatch: 100,
  expMin: "",
  expMax: "",
  salaryMin: "",
  salaryMax: "",
  sort: "best",
};

export function createMatchFilters(overrides = {}) {
  return { ...MATCH_FILTER_DEFAULTS, ...overrides };
}

export function hasActiveMatchFilters(filters) {
  const defaults = MATCH_FILTER_DEFAULTS;
  return (
    Boolean(filters.search?.trim()) ||
    (filters.skills?.length ?? 0) > 0 ||
    filters.remoteOnly ||
    Number(filters.minMatch) > defaults.minMatch ||
    Number(filters.maxMatch) < defaults.maxMatch ||
    filters.expMin !== "" ||
    filters.expMax !== "" ||
    filters.salaryMin !== "" ||
    filters.salaryMax !== "" ||
    filters.sort !== defaults.sort
  );
}

function normalizeSkill(value) {
  return String(value || "").trim().toLowerCase();
}

function rowSkills(row) {
  const matched = row.matched_skills || [];
  const missing = row.missing_skills || [];
  return [...matched, ...missing];
}

export function collectSkillOptions(rows = [], limit = 24) {
  const counts = new Map();
  for (const row of rows) {
    for (const skill of rowSkills(row)) {
      const key = normalizeSkill(skill);
      if (!key) continue;
      counts.set(key, { label: skill, count: (counts.get(key)?.count || 0) + 1 });
    }
  }
  return [...counts.values()]
    .sort((a, b) => b.count - a.count || a.label.localeCompare(b.label))
    .slice(0, limit)
    .map((entry) => entry.label);
}

function parseOptionalNumber(value) {
  if (value === "" || value == null) return null;
  const num = Number(value);
  return Number.isFinite(num) ? num : null;
}

function rowMatchScore(row) {
  return matchScoreValue(row);
}

function rowRemoteFit(row, variant) {
  const explanation = resolveMatchExplanation(row);
  if (variant === "candidate-jobs") {
    if (row.job_remote_policy) return true;
    return (explanation.remote?.score ?? 0) >= 0.85;
  }
  if (row.candidate_remote_preference) return true;
  return (explanation.remote?.score ?? 0) >= 0.85;
}

function rowExperience(row, variant) {
  if (variant === "candidate-jobs") {
    return row.job_required_experience ?? null;
  }
  return row.candidate_experience_years ?? null;
}

function rowBudgetMin(row, variant) {
  if (variant === "candidate-jobs") {
    return row.job_budget_min ?? row.job_budget ?? null;
  }
  return row.candidate_preferred_salary ?? null;
}

function rowBudgetMax(row, variant) {
  if (variant === "candidate-jobs") {
    return row.job_budget_max ?? row.job_budget ?? row.job_budget_min ?? null;
  }
  return row.candidate_preferred_salary ?? null;
}

function overlapsRange(valueMin, valueMax, filterMin, filterMax) {
  const lo = valueMin ?? valueMax;
  const hi = valueMax ?? valueMin;
  if (lo == null && hi == null) {
    return filterMin == null && filterMax == null;
  }
  const effectiveMin = lo ?? hi;
  const effectiveMax = hi ?? lo;
  if (filterMin != null && effectiveMax != null && effectiveMax < filterMin) return false;
  if (filterMax != null && effectiveMin != null && effectiveMin > filterMax) return false;
  return true;
}

function matchesSkillFilter(row, selectedSkills) {
  if (!selectedSkills.length) return true;
  const haystack = new Set(
    [...(row.matched_skills || []), ...(row.missing_skills || [])].map(normalizeSkill),
  );
  return selectedSkills.some((skill) => haystack.has(normalizeSkill(skill)));
}

function compareNewest(a, b, listOrder) {
  const aCreated = a.job_created_at ? Date.parse(a.job_created_at) : NaN;
  const bCreated = b.job_created_at ? Date.parse(b.job_created_at) : NaN;
  if (Number.isFinite(aCreated) && Number.isFinite(bCreated) && aCreated !== bCreated) {
    return bCreated - aCreated;
  }
  return (listOrder.get(b.target_id) ?? 0) - (listOrder.get(a.target_id) ?? 0);
}

export function filterAndSortMatchRows(rows, filters, variant = "candidate-jobs") {
  if (!rows?.length) return [];

  const listOrder = new Map(rows.map((row, index) => [row.target_id, index]));
  let result = [...rows];

  const query = filters.search?.trim().toLowerCase();
  if (query) {
    result = result.filter((row) => row.target_label?.toLowerCase().includes(query));
  }

  if (filters.skills?.length) {
    result = result.filter((row) => matchesSkillFilter(row, filters.skills));
  }

  if (filters.remoteOnly) {
    result = result.filter((row) => rowRemoteFit(row, variant));
  }

  const minMatch = Number(filters.minMatch) / 100;
  const maxMatch = Number(filters.maxMatch) / 100;
  result = result.filter((row) => {
    const score = rowMatchScore(row);
    return score >= minMatch && score <= maxMatch;
  });

  const expMin = parseOptionalNumber(filters.expMin);
  const expMax = parseOptionalNumber(filters.expMax);
  if (expMin != null || expMax != null) {
    result = result.filter((row) => {
      const exp = rowExperience(row, variant);
      if (exp == null) return false;
      if (expMin != null && exp < expMin) return false;
      if (expMax != null && exp > expMax) return false;
      return true;
    });
  }

  const salaryMin = parseOptionalNumber(filters.salaryMin);
  const salaryMax = parseOptionalNumber(filters.salaryMax);
  if (salaryMin != null || salaryMax != null) {
    result = result.filter((row) =>
      overlapsRange(rowBudgetMin(row, variant), rowBudgetMax(row, variant), salaryMin, salaryMax),
    );
  }

  if (filters.sort === "best") {
    result.sort((a, b) => rowMatchScore(b) - rowMatchScore(a));
  } else if (filters.sort === "newest") {
    result.sort((a, b) => compareNewest(a, b, listOrder));
  } else if (filters.sort === "compensation") {
    result.sort((a, b) => (rowBudgetMax(b, variant) ?? 0) - (rowBudgetMax(a, variant) ?? 0));
  } else if (filters.sort === "title") {
    result.sort((a, b) => a.target_label.localeCompare(b.target_label));
  }

  return result;
}

export function activeMatchFilterCount(filters) {
  let count = 0;
  if (filters.search?.trim()) count += 1;
  if (filters.skills?.length) count += 1;
  if (filters.remoteOnly) count += 1;
  if (Number(filters.minMatch) > 0) count += 1;
  if (Number(filters.maxMatch) < 100) count += 1;
  if (filters.expMin !== "" || filters.expMax !== "") count += 1;
  if (filters.salaryMin !== "" || filters.salaryMax !== "") count += 1;
  if (filters.sort !== MATCH_FILTER_DEFAULTS.sort) count += 1;
  return count;
}
