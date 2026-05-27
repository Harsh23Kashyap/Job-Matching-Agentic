export function formatInr(amount) {
  if (amount == null || amount === "" || Number.isNaN(Number(amount))) return "";
  const n = Math.round(Number(amount));
  if (n <= 0) return "";
  const s = String(n);
  if (s.length <= 3) return `₹ ${s}`;
  const last3 = s.slice(-3);
  const rest = s.slice(0, -3);
  const grouped = rest.replace(/\B(?=(\d{2})+(?!\d))/g, ",");
  return `₹ ${grouped},${last3}`;
}

export function parseInr(input) {
  if (input == null || input === "") return null;
  const digits = String(input).replace(/[^\d]/g, "");
  if (!digits) return null;
  return Number(digits);
}

export function matchPercent(score) {
  if (score == null || Number.isNaN(Number(score))) return "—";
  return `${Math.round(Number(score) * 100)}%`;
}

export function matchTier(score) {
  const pct = Number(score) * 100;
  if (pct >= 80) return { label: "Strong match", className: "match-tier--strong" };
  if (pct >= 60) return { label: "Good match", className: "match-tier--good" };
  if (pct >= 40) return { label: "Moderate match", className: "match-tier--moderate" };
  return { label: "Low match", className: "match-tier--low" };
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
