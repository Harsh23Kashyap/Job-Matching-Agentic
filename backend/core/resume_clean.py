"""Normalize noisy text extracted from PDF/DOCX resumes."""
from __future__ import annotations

import re

from core.contact_extract import EMAIL_RE, GITHUB_RE, LEETCODE_RE, LINKEDIN_RE, PHONE_RE, URL_RE

# PDF font-encoding artifacts and stray punctuation common in extracted resumes.
CID_RE = re.compile(r"\(?cid:\s*\d+\s*\)?", re.IGNORECASE)
CID_COMMA_DEBRIS_RE = re.compile(r"\s*(?:,\s*)+$", re.MULTILINE)
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")
ZERO_WIDTH_RE = re.compile(r"[\u200b-\u200d\ufeff]")
REPLACEMENT_CHAR_RE = re.compile(r"\ufffd")
JUNK_SYMBOLS_RE = re.compile(r"[§¶†‡•◦·▪▫●○◆◇■□]+")
_PROTECT_PATTERNS = (
    EMAIL_RE,
    URL_RE,
    LINKEDIN_RE,
    GITHUB_RE,
    LEETCODE_RE,
    PHONE_RE,
)


def _merge_spans(spans: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    if not spans:
        return []
    spans.sort(key=lambda item: (item[0], -(item[1] - item[0])))
    merged: list[tuple[int, int, str]] = []
    for start, end, value in spans:
        if merged and start < merged[-1][1]:
            continue
        merged.append((start, end, value))
    return merged


def _protect_contact_spans(text: str) -> tuple[str, list[str]]:
    spans: list[tuple[int, int, str]] = []
    for pattern in _PROTECT_PATTERNS:
        for match in pattern.finditer(text):
            value = match.group(0).strip()
            if pattern is PHONE_RE and len(re.sub(r"\D", "", value)) < 10:
                continue
            spans.append((match.start(), match.end(), value))
    merged = _merge_spans(spans)
    protected: list[str] = []
    out = text
    for idx, (start, end, value) in enumerate(reversed(merged)):
        token = f"__RESUME_PROTECTED_{len(merged) - 1 - idx}__"
        protected.insert(0, value)
        out = out[:start] + token + out[end:]
    return out, protected


def _restore_contact_spans(text: str, protected: list[str]) -> str:
    out = text
    for idx, value in enumerate(protected):
        out = out.replace(f"__RESUME_PROTECTED_{idx}__", value)
    return out


def _strip_noise(text: str) -> str:
    cleaned = text
    cleaned = CID_RE.sub("", cleaned)
    cleaned = CID_COMMA_DEBRIS_RE.sub("", cleaned)
    cleaned = re.sub(r"^(?:,\s*)+", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r",\s*,+", ", ", cleaned)
    cleaned = CONTROL_RE.sub("", cleaned)
    cleaned = ZERO_WIDTH_RE.sub("", cleaned)
    cleaned = REPLACEMENT_CHAR_RE.sub("", cleaned)
    cleaned = JUNK_SYMBOLS_RE.sub(" ", cleaned)
    cleaned = cleaned.replace("\u00a0", " ")
    cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r" *\n *", "\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned


def _normalize_lines(text: str) -> str:
    lines: list[str] = []
    for raw_line in text.split("\n"):
        line = raw_line.strip()
        line = re.sub(r"\s*(?:,\s*)+$", "", line).strip()
        if not line:
            if lines and lines[-1] != "":
                lines.append("")
            continue
        # Drop lines that are only punctuation / encoding debris.
        if re.fullmatch(r"[\W_]+", line) and not re.search(r"[@:/.]", line):
            continue
        lines.append(line)
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def clean_resume_text(text: str) -> str:
    """Remove PDF/DOCX extraction noise while preserving contact URLs and emails."""
    if not text:
        return ""
    protected_text, protected_values = _protect_contact_spans(text)
    cleaned = _strip_noise(protected_text)
    cleaned = _restore_contact_spans(cleaned, protected_values)
    return _normalize_lines(cleaned)


def resume_preview_excerpt(text: str, *, limit: int = 500) -> str:
    cleaned = clean_resume_text(text)
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[:limit].rstrip() + "…"
