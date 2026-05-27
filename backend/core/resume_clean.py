import re


def clean_resume_text(text: str) -> str:
    if not text:
        return ""
    cleaned = text
    cleaned = re.sub(r"\(cid:\d+\)", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.replace("\u00a7", "")
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n[ \t]+", "\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = re.sub(r"([a-zA-Z0-9])@([a-zA-Z])", r"\1 @\2", cleaned)
    cleaned = re.sub(r"([a-zA-Z])\.([a-zA-Z])", r"\1. \2", cleaned)
    lines = [ln.strip() for ln in cleaned.splitlines()]
    return "\n".join(ln for ln in lines if ln).strip()
