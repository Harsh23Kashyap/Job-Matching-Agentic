export function cleanResumeText(text) {
  if (!text) return "";
  let cleaned = text;
  cleaned = cleaned.replace(/\(cid:\d+\)/gi, "");
  cleaned = cleaned.replace(/\u00a7/g, "");
  cleaned = cleaned.replace(/[ \t]+/g, " ");
  cleaned = cleaned.replace(/\n[ \t]+/g, "\n");
  cleaned = cleaned.replace(/\n{3,}/g, "\n\n");
  return cleaned
    .split("\n")
    .map((ln) => ln.trim())
    .filter(Boolean)
    .join("\n");
}
