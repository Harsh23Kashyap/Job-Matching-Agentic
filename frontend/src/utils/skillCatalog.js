import catalog from "../../../shared/skill_catalog.json" with { type: "json" };

const SYNONYMS = Object.fromEntries(
  Object.entries(catalog.synonyms || {}).map(([key, value]) => [normalize(key), value]),
);
const DISPLAY = Object.fromEntries(
  Object.entries(catalog.display || {}).map(([key, value]) => [normalize(key), value]),
);

const AWS_PREFIX_RE = /^(?:aws|amazon)\s+/i;

export function normalize(skill) {
  return String(skill ?? "")
    .trim()
    .toLowerCase()
    .replace(/\s+/g, " ");
}

function variantKeys(key) {
  return [
    key,
    key.replace(/\./g, ""),
    key.replace(/-/g, ""),
    key.replace(/-/g, " "),
    key.replace(/_/g, " "),
    key.replace(/\s+/g, ""),
    key.replace(/\s+/g, " "),
  ].filter(Boolean);
}

function lookupSynonym(key) {
  for (const variant of variantKeys(key)) {
    if (SYNONYMS[variant]) return SYNONYMS[variant];
  }
  return null;
}

export function canonicalSkill(skill) {
  const key = normalize(skill);
  if (!key) return "";

  const mapped = lookupSynonym(key);
  if (mapped) return mapped;

  if (AWS_PREFIX_RE.test(key)) return "aws";
  return key;
}

function titleDisplay(canonical) {
  if (canonical.includes("/")) {
    return canonical
      .split("/")
      .map((part) => (part.length <= 3 ? part.toUpperCase() : part.charAt(0).toUpperCase() + part.slice(1)))
      .join("/");
  }
  if (canonical === canonical.toUpperCase()) return canonical;
  return canonical
    .split(" ")
    .map((word) => {
      if (word === "c++" || word === "c#") return word.toUpperCase();
      if (word.length <= 3 && /^[a-z]+$/.test(word)) return word.toUpperCase();
      return word.charAt(0).toUpperCase() + word.slice(1);
    })
    .join(" ");
}

function pickDisplay(canonical, originals) {
  if (DISPLAY[canonical]) return DISPLAY[canonical];

  for (const original of originals) {
    const cleaned = String(original).trim();
    if (cleaned && canonicalSkill(cleaned) === canonical && cleaned !== cleaned.toLowerCase()) {
      return cleaned;
    }
  }

  for (const original of originals) {
    const cleaned = String(original).trim();
    if (cleaned) return cleaned;
  }

  return titleDisplay(canonical);
}

export function normalizeSkill(skill) {
  const original = String(skill ?? "").trim();
  const canonical = canonicalSkill(original);
  return {
    canonical,
    display: pickDisplay(canonical, [original]),
    original,
  };
}

export function normalizeSkills(skills) {
  const buckets = new Map();

  for (const raw of skills ?? []) {
    const original = String(raw ?? "").trim();
    if (!original) continue;
    const canonical = canonicalSkill(original);
    if (!canonical) continue;
    if (!buckets.has(canonical)) buckets.set(canonical, []);
    buckets.get(canonical).push(original);
  }

  return [...buckets.entries()]
    .map(([canonical, originals]) => ({
      canonical,
      display: pickDisplay(canonical, originals),
      original: originals[0],
    }))
    .sort((a, b) => a.display.localeCompare(b.display, undefined, { sensitivity: "base" }));
}

export function normalizeSkillList(skills) {
  return normalizeSkills(skills).map((entry) => entry.display);
}
