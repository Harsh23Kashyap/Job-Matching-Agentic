import re

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(
    r"(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{3,4}(?:[\s.-]?\d{1,6})?"
)
URL_RE = re.compile(r"https?://[^\s<>\"']+|(?:www\.)[^\s<>\"']+", re.IGNORECASE)
LINKEDIN_RE = re.compile(r"https?://(?:[\w.-]+\.)?linkedin\.com/in/[\w%-]+/?", re.IGNORECASE)
GITHUB_PROFILE_RE = re.compile(r"https?://(?:[\w.-]+\.)?github\.com/[\w-]+/?$", re.IGNORECASE)

CONTACT_KEYS = ("email", "phone", "linkedin", "portfolio", "other_links")


def _normalize_url(url: str) -> str:
    u = url.strip().rstrip(".,;)")
    if u.lower().startswith("www."):
        return f"https://{u}"
    return u


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for v in values:
        key = v.lower()
        if key and key not in seen:
            seen.add(key)
            out.append(v)
    return out


def extract_contact_from_text(text: str) -> dict:
    emails = _unique(EMAIL_RE.findall(text))
    phones = [p.strip() for p in PHONE_RE.findall(text) if len(re.sub(r"\D", "", p)) >= 10]
    phones = _unique(phones)

    urls = [_normalize_url(u) for u in URL_RE.findall(text)]
    urls = _unique(urls)

    linkedin = next((u for u in urls if "linkedin.com/in/" in u.lower()), "")
    if not linkedin:
        m = LINKEDIN_RE.search(text)
        linkedin = _normalize_url(m.group(0)) if m else ""

    portfolio = ""
    for u in urls:
        lower = u.lower()
        if "linkedin.com" in lower:
            continue
        if GITHUB_PROFILE_RE.match(u) or any(x in lower for x in (".github.io", "behance.net", "dribbble.com")):
            portfolio = u
            break

    used = {linkedin, portfolio}
    other_links = [u for u in urls if u not in used and "linkedin.com" not in u.lower()][:5]

    return {
        "email": emails[0] if emails else "",
        "phone": phones[0] if phones else "",
        "linkedin": linkedin,
        "portfolio": portfolio,
        "other_links": other_links,
    }


def merge_contact_fields(primary: dict, fallback: dict) -> dict:
    merged = dict(primary)
    for key in ("email", "phone", "linkedin", "portfolio"):
        if not str(merged.get(key) or "").strip() and fallback.get(key):
            merged[key] = fallback[key]
    links = _unique([*(merged.get("other_links") or []), *(fallback.get("other_links") or [])])
    merged["other_links"] = links[:8]
    return merged
