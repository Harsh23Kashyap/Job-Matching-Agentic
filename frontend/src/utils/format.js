export const CURRENCIES = ["INR", "USD", "EUR", "GBP", "SGD"];

const CURRENCY_META = {
  INR: { symbol: "₹", grouping: "indian" },
  USD: { symbol: "$", grouping: "western" },
  EUR: { symbol: "€", grouping: "western" },
  GBP: { symbol: "£", grouping: "western" },
  SGD: { symbol: "S$", grouping: "western" },
};

function formatWestern(n) {
  return n.toLocaleString("en-US");
}

export function formatAmount(amount, currency = "INR") {
  if (amount == null || amount === "" || Number.isNaN(Number(amount))) return "";
  const n = Math.round(Number(amount));
  if (n <= 0) return "";
  const meta = CURRENCY_META[currency] || CURRENCY_META.INR;
  if (meta.grouping === "indian") {
    const s = String(n);
    if (s.length <= 3) return s;
    const last3 = s.slice(-3);
    const rest = s.slice(0, -3);
    return `${rest.replace(/\B(?=(\d{2})+(?!\d))/g, ",")},${last3}`;
  }
  return formatWestern(n);
}

export function formatCompensationPreview(amount, currency = "INR") {
  const formatted = formatAmount(amount, currency);
  if (!formatted) return "";
  const meta = CURRENCY_META[currency] || CURRENCY_META.INR;
  return `Shown as ${meta.symbol}${formatted} total compensation / year`;
}

export function formatInr(amount) {
  const formatted = formatAmount(amount, "INR");
  return formatted ? `₹ ${formatted}` : "";
}

export function formatBudgetRange(job, currency = "INR") {
  const cur = job?.budget_currency || currency;
  const meta = CURRENCY_META[cur] || CURRENCY_META.INR;
  const sym = meta.symbol;
  const min = job?.budget_min ?? null;
  const max = job?.budget_max ?? job?.budget ?? null;
  if (min && max) {
    return `${sym}${formatAmount(min, cur)} – ${sym}${formatAmount(max, cur)} / year`;
  }
  if (max) return `${sym}${formatAmount(max, cur)} / year budget`;
  if (min) return `From ${sym}${formatAmount(min, cur)} / year`;
  return "";
}

export function formatPostedDate(iso) {
  if (!iso) return "—";
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return "—";
  return date.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
}

export function formatExperienceYears(years) {
  if (years == null || years === "") return "—";
  const value = Number(years);
  if (!Number.isFinite(value)) return "—";
  if (value === 0) return "No minimum";
  if (value === 1) return "1 yr min";
  return `${value} yrs min`;
}

export function filterAmountInput(raw) {
  return String(raw ?? "").replace(/[^\d,]/g, "");
}

export function parseAmount(input) {
  if (input == null || input === "") return null;
  const digits = String(input).replace(/[^\d]/g, "");
  if (!digits) return null;
  const amount = Number(digits);
  if (!Number.isFinite(amount) || amount <= 0) return null;
  return Math.round(amount);
}

export function parseInr(input) {
  return parseAmount(input);
}

export function matchPercent(score) {
  if (score == null || Number.isNaN(Number(score))) return "—";
  return `${Math.round(Number(score) * 100)}%`;
}

export function matchTier(score) {
  const pct = Math.round(Number(score) * 100);
  if (Number.isNaN(pct)) return { label: "Low fit", className: "match-tier--low" };
  if (pct >= 80) return { label: "Strong fit", className: "match-tier--strong" };
  if (pct >= 60) return { label: "Good fit", className: "match-tier--good" };
  if (pct >= 40) return { label: "Moderate fit", className: "match-tier--moderate" };
  return { label: "Low fit", className: "match-tier--low" };
}

export function formatCandidateMatchScore(score) {
  return matchPercent(score);
}

export function formatSkillExperienceLine(matched) {
  if (!matched?.length) return "";
  if (matched.length === 1) return `Matches your ${matched[0]} experience.`;
  if (matched.length === 2) return `Matches your ${matched[0]} and ${matched[1]} experience.`;
  const head = matched.slice(0, -1).join(", ");
  return `Matches your ${head}, and ${matched[matched.length - 1]} experience.`;
}

export function isApplyAvailable(row) {
  return row?.apply_available !== false;
}

export function humanizeStrategy(strategy) {
  const map = {
    semantic: "Meaning-based resume match",
    multimodal: "Skills + meaning blend",
    ensemble: "Combined ranking",
    batch: "Batch review",
  };
  return map[strategy] || "Profile match";
}

const WHY_MAP = {
  "High semantic similarity": "Strong alignment with role requirements",
  "Moderate semantic similarity": "Reasonable alignment with role requirements",
};

export function humanizeWhyRanked(lines = []) {
  return lines.map((line) => {
    if (WHY_MAP[line]) return WHY_MAP[line];
    if (line.startsWith("Matching skills:")) return line.replace("Matching skills:", "Matched skills:");
    if (line.startsWith("Title/summary overlap:")) return line.replace("Title/summary overlap:", "Role overlap:");
    if (line.includes("Multimodal blend")) return "Combined skills and experience signals";
    return line;
  });
}

export function parseWhySignals(lines = []) {
  const matched = [];
  const other = [];
  for (const line of humanizeWhyRanked(lines)) {
    if (line.startsWith("Matched skills:")) {
      matched.push(...line.replace("Matched skills:", "").split(",").map((s) => s.trim()).filter(Boolean));
    } else {
      other.push(line);
    }
  }
  return { matched, other };
}

export function deriveWhyMatch(row) {
  const { matched } = matchSkills(row);
  const sim = Number(row.similarity) || 0;

  if (matched.length >= 1) {
    return formatSkillExperienceLine(matched);
  }
  if (sim >= 0.45) {
    return "Limited direct skill overlap, but role context is close.";
  }
  return "Limited direct skill overlap — review details before applying.";
}

export function pluralGoodMatches(count) {
  return count === 1 ? "Good match" : "Good matches";
}

export function pluralStrongMatches(count) {
  return count === 1 ? "Strong match" : "Strong matches";
}

export function formatRefreshedAt(iso) {
  if (!iso) return "Just now";
  const diff = Date.now() - new Date(iso).getTime();
  if (diff < 60000) return "Just now";
  const mins = Math.floor(diff / 60000);
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  return `${hrs}h ago`;
}

export function formatCandidateExperience(years) {
  if (years == null || years === "") return null;
  const value = Number(years);
  if (!Number.isFinite(value)) return null;
  if (value === 0) return "No experience listed";
  if (value === 1) return "1 year";
  return `${value} years`;
}

export function formatExpectedCompensation(row) {
  const amount = row?.candidate_preferred_salary ?? row?.preferred_salary;
  if (amount == null || amount === "") return null;
  const currency = row?.candidate_preferred_currency ?? row?.preferred_currency ?? "INR";
  const meta = CURRENCY_META[currency] || CURRENCY_META.INR;
  const formatted = formatAmount(amount, currency);
  if (!formatted) return null;
  return `${meta.symbol}${formatted} / year expected`;
}

export function formatRemotePreference(row) {
  const pref = row?.candidate_remote_preference ?? row?.remote_preference;
  if (pref == null) return null;
  return pref ? "Open to remote" : "On-site preferred";
}

export function deriveEmployerWhyMatch(row) {
  const { matched, other } = parseWhySignals(row.why_ranked || []);
  const sim = Number(row.similarity) || 0;

  if (matched.length >= 2) {
    return `Strong overlap on ${matched.slice(0, 3).join(", ")}.`;
  }
  if (matched.length === 1) {
    return `Matches required skill: ${matched[0]}.`;
  }
  if (other.length > 0) {
    return other[0];
  }
  if (sim >= 0.45) {
    return "Profile context aligns with the role beyond listed skills.";
  }
  return "Limited direct skill overlap — review the full profile.";
}

export function countStrongMatches(results, threshold = 0.8) {
  return (results || []).filter((row) => Number(row.similarity) >= threshold).length;
}

export function candidateHasContact(row) {
  return Boolean(
    row?.contact_email ||
      row?.contact_phone ||
      row?.contact_linkedin ||
      row?.contact_portfolio,
  );
}

export function matchSkills(row) {
  const parsed = parseWhySignals(row.why_ranked);
  return {
    matched: row.matched_skills?.length ? row.matched_skills : parsed.matched,
    missing: row.missing_skills || [],
  };
}

export function explainMatchScore(row) {
  const overall = matchPercent(row.similarity);
  const skills = row.skills_score != null ? matchPercent(row.skills_score) : null;
  const semantic = matchPercent(row.semantic_score);

  if (skills != null) {
    return `Overall ${overall} blends ${skills} required-skills overlap with ${semantic} profile alignment.`;
  }
  return `Overall ${overall} reflects ${semantic} profile-to-role alignment.`;
}
