"""Canonical skill names, synonym mapping, and display normalization."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

_CATALOG_PATH = Path(__file__).resolve().parents[2] / "shared" / "skill_catalog.json"

AWS_PREFIX_RE = re.compile(r"^(?:aws|amazon)\s+", re.I)


@dataclass(frozen=True)
class NormalizedSkill:
    canonical: str
    display: str
    original: str


@lru_cache(maxsize=1)
def _catalog() -> tuple[dict[str, str], dict[str, str]]:
    data = json.loads(_CATALOG_PATH.read_text(encoding="utf-8"))
    synonyms = {normalize(key): value for key, value in data.get("synonyms", {}).items()}
    display = {normalize(key): value for key, value in data.get("display", {}).items()}
    return synonyms, display


def _synonyms() -> dict[str, str]:
    return _catalog()[0]


def _display_names() -> dict[str, str]:
    return _catalog()[1]


def normalize(skill: str) -> str:
    return re.sub(r"\s+", " ", skill.strip().lower())


def _variant_keys(key: str) -> list[str]:
    variants = {
        key,
        key.replace(".", ""),
        key.replace("-", ""),
        key.replace("-", " "),
        key.replace("_", " "),
        re.sub(r"\s+", "", key),
        re.sub(r"\s+", " ", key),
    }
    return [variant for variant in variants if variant]


def _lookup_synonym(key: str) -> str | None:
    synonyms = _synonyms()
    for variant in _variant_keys(key):
        if variant in synonyms:
            return synonyms[variant]
    return None


def canonical_skill(skill: str) -> str:
    key = normalize(skill)
    if not key:
        return ""

    mapped = _lookup_synonym(key)
    if mapped:
        return mapped

    if AWS_PREFIX_RE.match(key):
        return "aws"

    return key


def _title_display(canonical: str) -> str:
    if "/" in canonical:
        return "/".join(part.upper() if len(part) <= 3 else part.capitalize() for part in canonical.split("/"))
    if canonical.isupper() or canonical.isnumeric():
        return canonical
    words = canonical.split()
    out: list[str] = []
    for word in words:
        if word in {"c++", "c#"}:
            out.append(word.upper())
        elif len(word) <= 3 and word.isalpha():
            out.append(word.upper())
        else:
            out.append(word.capitalize())
    return " ".join(out)


def display_for(canonical: str, original: str) -> str:
    preferred = _display_names().get(canonical)
    if preferred:
        return preferred

    cleaned = original.strip()
    if cleaned and canonical_skill(cleaned) == canonical and cleaned != cleaned.lower():
        return cleaned

    return _title_display(canonical)


def _pick_display(canonical: str, originals: list[str]) -> str:
    preferred = _display_names().get(canonical)
    if preferred:
        return preferred

    for original in originals:
        cleaned = original.strip()
        if cleaned and canonical_skill(cleaned) == canonical and cleaned != cleaned.lower():
            return cleaned

    for original in originals:
        cleaned = original.strip()
        if cleaned:
            return cleaned

    return _title_display(canonical)


def normalize_skill(skill: str) -> NormalizedSkill:
    original = skill.strip()
    canonical = canonical_skill(original)
    display = display_for(canonical, original)
    return NormalizedSkill(canonical=canonical, display=display, original=original)


def normalize_skills(skills: list[str]) -> list[NormalizedSkill]:
    buckets: dict[str, list[str]] = {}
    for raw in skills:
        if raw is None:
            continue
        original = str(raw).strip()
        if not original:
            continue
        canonical = canonical_skill(original)
        if not canonical:
            continue
        buckets.setdefault(canonical, []).append(original)

    entries = [
        NormalizedSkill(
            canonical=canonical,
            display=_pick_display(canonical, originals),
            original=originals[0],
        )
        for canonical, originals in buckets.items()
    ]
    return sorted(entries, key=lambda entry: entry.display.lower())


def normalize_skill_list(skills: list[str]) -> list[str]:
    return [entry.display for entry in normalize_skills(skills)]


def canonicalize_skills(skills: list[str]) -> list[str]:
    """Return deduplicated canonical keys (for matching and embeddings)."""
    seen: set[str] = set()
    out: list[str] = []
    for skill in skills:
        canon = canonical_skill(skill)
        if canon and canon not in seen:
            seen.add(canon)
            out.append(canon)
    return sorted(out)


def display_skills(skills: list[str]) -> list[str]:
    """Return deduplicated display names suitable for UI and API storage."""
    return normalize_skill_list(skills)
