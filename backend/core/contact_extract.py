import re

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(
    r"(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{3,4}(?:[\s.-]?\d{1,6})?"
)
URL_RE = re.compile(r"https?://[^\s<>\"']+|(?:www\.)[^\s<>\"']+", re.IGNORECASE)
LINKEDIN_RE = re.compile(
    r"(?:https?://(?:[\w.-]+\.)?|(?<![/\w@.]))linkedin\.com/in/[\w%-]+/?",
    re.IGNORECASE,
)
GITHUB_RE = re.compile(
    r"(?:https?://(?:[\w.-]+\.)?|(?<![/\w@.]))github\.com/[\w-]+/?",
    re.IGNORECASE,
)
LEETCODE_RE = re.compile(
    r"(?:https?://(?:[\w.-]+\.)?|(?<![/\w@.]))leetcode\.com/(?:u/)?[\w-]+/?",
    re.IGNORECASE,
)
CERTIFICATE_RE = re.compile(
    r"(?:https?://(?:[\w.-]+\.)?|(?<![/\w@.]))(?:"
    r"www\.)?(?:credly\.com/[\w./-]+|"
    r"coursera\.org/(?:account/accomplishments|verify)/[\w./-]+|"
    r"accredible\.com/[\w./-]+|"
    r"badgr\.io/[\w./-]+"
    r")/?",
    re.IGNORECASE,
)

NAME_SKIP_RE = re.compile(
    r"\b(resume|curriculum|vitae|profile|contact|skills|experience|education|summary|objective)\b",
    re.IGNORECASE,
)
NAME_WORD_RE = re.compile(r"^[\w.'-]+$")
CID_INLINE_RE = re.compile(r"\(?cid:\s*\d+\s*\)?", re.IGNORECASE)

CONTACT_KEYS = ("name", "email", "phone", "linkedin", "portfolio", "other_links")

PORTFOLIO_HOST_MARKERS = (".github.io", "behance.net", "dribbble.com", "notion.site", "vercel.app")
SOCIAL_HOST_MARKERS = (
    "linkedin.com",
    "github.com",
    "leetcode.com",
    "credly.com",
    "coursera.org",
    "accredible.com",
    "badgr.io",
    "twitter.com",
    "x.com",
    "medium.com",
)


def _normalize_url(url: str) -> str:
    u = url.strip().rstrip(".,;)")
    lower = u.lower()
    if lower.startswith("www."):
        return f"https://{u}"
    if not lower.startswith("http://") and not lower.startswith("https://"):
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


def _first_match(pattern: re.Pattern[str], text: str) -> str:
    match = pattern.search(text)
    return _normalize_url(match.group(0)) if match else ""


def _is_github_profile(url: str) -> bool:
    lower = url.lower()
    return "github.com/" in lower and ".github.io" not in lower


def _is_portfolio_site(url: str) -> bool:
    lower = url.lower()
    if any(host in lower for host in SOCIAL_HOST_MARKERS):
        return False
    if any(marker in lower for marker in PORTFOLIO_HOST_MARKERS):
        return True
    host = lower.split("://", 1)[-1].split("/", 1)[0]
    if host.endswith((".dev", ".io", ".me", ".app")):
        return True
    return False


def extract_name_from_text(text: str) -> str:
    for raw_line in text.split("\n")[:10]:
        line = CID_INLINE_RE.sub("", raw_line).strip()
        line = re.sub(r"\s*(?:,\s*)+$", "", line).strip()
        if not line or len(line) > 64:
            continue
        if EMAIL_RE.search(line) or PHONE_RE.search(line) or "http" in line.lower() or "www." in line.lower():
            continue
        if "@" in line or NAME_SKIP_RE.search(line):
            continue
        if re.search(r"linkedin\.com|github\.com|leetcode\.com", line, re.IGNORECASE):
            continue
        words = line.split()
        if not (2 <= len(words) <= 5):
            continue
        if not all(NAME_WORD_RE.match(word) for word in words):
            continue
        if not all(word[0].isupper() or word.isupper() for word in words if any(ch.isalpha() for ch in word)):
            continue
        return line
    return ""


def _collect_urls(text: str) -> list[str]:
    urls = [_normalize_url(u) for u in URL_RE.findall(text)]
    for pattern in (LINKEDIN_RE, GITHUB_RE, LEETCODE_RE, CERTIFICATE_RE):
        for match in pattern.finditer(text):
            urls.append(_normalize_url(match.group(0)))
    return _unique(urls)


def extract_contact_from_text(text: str) -> dict:
    emails = _unique(EMAIL_RE.findall(text))
    phones = [p.strip() for p in PHONE_RE.findall(text) if len(re.sub(r"\D", "", p)) >= 10]
    phones = _unique(phones)

    urls = _collect_urls(text)

    linkedin = next((u for u in urls if "linkedin.com/in/" in u.lower()), "")
    if not linkedin:
        linkedin = _first_match(LINKEDIN_RE, text)

    github = next((u for u in urls if _is_github_profile(u)), "")
    if not github:
        github = _first_match(GITHUB_RE, text)

    leetcode = next((u for u in urls if "leetcode.com/" in u.lower()), "")
    if not leetcode:
        leetcode = _first_match(LEETCODE_RE, text)

    certificates = next((u for u in urls if CERTIFICATE_RE.search(u)), "")
    if not certificates:
        certificates = _first_match(CERTIFICATE_RE, text)

    portfolio = next((u for u in urls if _is_portfolio_site(u)), "")

    reserved = {linkedin, github, leetcode, certificates, portfolio}
    other_links: list[str] = []
    for url in (github, leetcode, certificates):
        if url and url not in other_links:
            other_links.append(url)
    for url in urls:
        if url in reserved:
            continue
        lower = url.lower()
        if any(host in lower for host in SOCIAL_HOST_MARKERS):
            continue
        other_links.append(url)
    other_links = _unique(other_links)[:8]

    if not portfolio and github:
        portfolio = github
        if github in other_links and len(other_links) > 1:
            other_links = [u for u in other_links if u != github]
        elif github in other_links:
            other_links = []

    return {
        "name": extract_name_from_text(text),
        "email": emails[0] if emails else "",
        "phone": phones[0] if phones else "",
        "linkedin": linkedin,
        "portfolio": portfolio,
        "other_links": other_links,
    }


def merge_contact_fields(primary: dict, fallback: dict) -> dict:
    merged = dict(primary)
    for key in CONTACT_KEYS:
        if key == "other_links":
            continue
        if not str(merged.get(key) or "").strip() and fallback.get(key):
            merged[key] = fallback[key]
    links = _unique([*(merged.get("other_links") or []), *(fallback.get("other_links") or [])])
    merged["other_links"] = links[:8]
    return merged
