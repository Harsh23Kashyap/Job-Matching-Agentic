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

export function parseAmount(input) {
  if (input == null || input === "") return null;
  const digits = String(input).replace(/[^\d]/g, "");
  if (!digits) return null;
  return Number(digits);
}

export function parseInr(input) {
  return parseAmount(input);
}

export function matchPercent(score) {
  if (score == null || Number.isNaN(Number(score))) return "—";
  return `${Math.round(Number(score) * 100)}%`;
}

export function matchTier(score) {
  const pct = Number(score) * 100;
  if (pct >= 80) return { label: "Strong fit", className: "match-tier--strong" };
  if (pct >= 60) return { label: "Good fit", className: "match-tier--good" };
  if (pct >= 40) return { label: "Moderate fit", className: "match-tier--moderate" };
  return { label: "Low fit", className: "match-tier--low" };
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
  const { matched } = parseWhySignals(row.why_ranked);
  const sim = Number(row.similarity) || 0;
  const skillsScore = row.skills_score != null ? Number(row.skills_score) : null;

  if (matched.length >= 3) {
    return `Strong overlap with ${matched.slice(0, 2).join(", ")} and related skills.`;
  }
  if (matched.length === 2) {
    return `Matches your ${matched.join(" and ")} experience.`;
  }
  if (matched.length === 1) {
    return `Matches your ${matched[0]} experience.`;
  }
  if (skillsScore != null && skillsScore >= 0.5) {
    return "Similar to your cloud and backend skills.";
  }
  if (sim >= 0.65) {
    return "Strong backend overlap based on your profile.";
  }
  if (sim >= 0.45) {
    return "Limited direct skill overlap, but role context is close.";
  }
  return "Limited direct skill overlap — review details before applying.";
}

export function pluralGoodMatches(count) {
  return count === 1 ? "Good match" : "Good matches";
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
