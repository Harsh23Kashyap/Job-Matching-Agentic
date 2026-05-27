const CID_RE = /\(?cid:\s*\d+\s*\)?/gi;
const CONTROL_RE = /[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]/g;
const ZERO_WIDTH_RE = /[\u200b-\u200d\ufeff]/g;
const REPLACEMENT_CHAR_RE = /\ufffd/g;
const JUNK_SYMBOLS_RE = /[§¶†‡•◦·▪▫●○◆◇■□]+/g;

const EMAIL_RE = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
const URL_RE = /https?:\/\/[^\s<>"']+|(?:www\.)[^\s<>"']+/gi;
const LINKEDIN_RE = /https?:\/\/(?:[\w.-]+\.)?linkedin\.com\/in\/[\w%-]+\/?/gi;
const GITHUB_RE = /https?:\/\/(?:[\w.-]+\.)?github\.com\/[\w-]+\/?/gi;
const LEETCODE_RE = /https?:\/\/(?:[\w.-]+\.)?leetcode\.com\/(?:u\/)?[\w-]+\/?/gi;
const PHONE_RE = /(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{3,4}(?:[\s.-]?\d{1,6})?/g;

const PROTECT_PATTERNS = [EMAIL_RE, URL_RE, LINKEDIN_RE, GITHUB_RE, LEETCODE_RE, PHONE_RE];

function mergeSpans(spans) {
  if (!spans.length) return [];
  const sorted = [...spans].sort((a, b) => a.start - b.start || b.end - b.start - (a.end - a.start));
  const merged = [];
  for (const span of sorted) {
    if (merged.length && span.start < merged[merged.length - 1].end) continue;
    merged.push(span);
  }
  return merged;
}

function protectContactSpans(text) {
  const spans = [];
  for (const pattern of PROTECT_PATTERNS) {
    pattern.lastIndex = 0;
    let match = pattern.exec(text);
    while (match) {
      const value = match[0].trim();
      if (pattern === PHONE_RE && value.replace(/\D/g, "").length < 10) {
        match = pattern.exec(text);
        continue;
      }
      spans.push({ start: match.index, end: match.index + match[0].length, value });
      match = pattern.exec(text);
    }
  }
  const merged = mergeSpans(spans);
  const protectedValues = [];
  let out = text;
  for (let i = merged.length - 1; i >= 0; i -= 1) {
    const { start, end, value } = merged[i];
    const token = `__RESUME_PROTECTED_${i}__`;
    protectedValues[i] = value;
    out = out.slice(0, start) + token + out.slice(end);
  }
  return { text: out, protectedValues };
}

function restoreContactSpans(text, protectedValues) {
  let out = text;
  protectedValues.forEach((value, idx) => {
    out = out.split(`__RESUME_PROTECTED_${idx}__`).join(value);
  });
  return out;
}

function stripNoise(text) {
  let cleaned = text;
  cleaned = cleaned.replace(CID_RE, "");
  cleaned = cleaned.replace(/\s*(?:,\s*)+$/gm, "");
  cleaned = cleaned.replace(/^(?:,\s*)+/gm, "");
  cleaned = cleaned.replace(/,\s*,+/g, ", ");
  cleaned = cleaned.replace(CONTROL_RE, "");
  cleaned = cleaned.replace(ZERO_WIDTH_RE, "");
  cleaned = cleaned.replace(REPLACEMENT_CHAR_RE, "");
  cleaned = cleaned.replace(JUNK_SYMBOLS_RE, " ");
  cleaned = cleaned.replace(/\u00a0/g, " ");
  cleaned = cleaned.replace(/\r\n/g, "\n").replace(/\r/g, "\n");
  cleaned = cleaned.replace(/[ \t]+/g, " ");
  cleaned = cleaned.replace(/ *\n */g, "\n");
  cleaned = cleaned.replace(/\n{3,}/g, "\n\n");
  return cleaned;
}

function normalizeLines(text) {
  const lines = [];
  for (const rawLine of text.split("\n")) {
    let line = rawLine.trim().replace(/\s*(?:,\s*)+$/, "").trim();
    if (!line) {
      if (lines.length && lines[lines.length - 1] !== "") lines.push("");
      continue;
    }
    if (/^[\W_]+$/.test(line) && !/[@:/.]/.test(line)) continue;
    lines.push(line);
  }
  while (lines.length && lines[lines.length - 1] === "") lines.pop();
  return lines.join("\n");
}

export function cleanResumeText(text) {
  if (!text) return "";
  const { text: protectedText, protectedValues } = protectContactSpans(text);
  let cleaned = stripNoise(protectedText);
  cleaned = restoreContactSpans(cleaned, protectedValues);
  return normalizeLines(cleaned);
}

export function resumePreviewFromUpload(data) {
  if (data?.cleaned_text) return data.cleaned_text;
  return cleanResumeText(data?.raw_text_preview || "");
}

export function resumePreviewExcerpt(text, limit = 500) {
  const cleaned = cleanResumeText(text);
  if (cleaned.length <= limit) return cleaned;
  return `${cleaned.slice(0, limit).trimEnd()}…`;
}

export function resumePreviewMeta(text) {
  const cleaned = cleanResumeText(text);
  const lines = cleaned ? cleaned.split("\n").filter(Boolean).length : 0;
  return { lines, chars: cleaned.length };
}
