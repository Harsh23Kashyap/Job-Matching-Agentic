import json
import re

import httpx

from config import Settings


class LlmUnavailableError(Exception):
    pass


class LlmParseError(Exception):
    pass


JOB_SYSTEM_PROMPT = """You extract structured job posting data from job description text.
Return ONLY valid JSON with these keys:
- title (string)
- required_skills (array of strings)
- required_experience (integer years, minimum 0)
- description (string, 1-4 sentences summarizing the role)
- company (string)
- location (string)
- remote_policy (boolean — true if remote or hybrid-friendly)
- link (string URL for application, or empty string)

Use empty string or empty array when unknown. Do not include markdown."""


SYSTEM_PROMPT = """You extract structured candidate profile data from resume text.
Return ONLY valid JSON with these keys:
- name (string)
- skills (array of strings)
- experience_years (number, can be 0.5 increments)
- preferred_salary (integer or null)
- remote_preference (boolean)
- summary (string, 1-3 sentences)
- email (string)
- phone (string)
- linkedin (string URL)
- portfolio (string URL — personal site, GitHub profile, or portfolio)
- other_links (array of string URLs — e.g. GitLab, Medium, project links)

Use empty string or empty array when unknown. Do not include markdown."""


class LlmParser:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def parse_candidate_from_text(self, text: str) -> dict:
        return self._parse_with_prompt(text, SYSTEM_PROMPT, "Resume text", self._normalize)

    def parse_job_from_text(self, text: str) -> dict:
        return self._parse_with_prompt(text, JOB_SYSTEM_PROMPT, "Job description text", self._normalize_job)

    def _parse_with_prompt(
        self,
        text: str,
        system_prompt: str,
        user_label: str,
        normalize_fn,
    ) -> dict:
        last_error: Exception | None = None
        for attempt in range(2):
            try:
                raw = self._call_llm(text, system_prompt, user_label)
                return normalize_fn(raw)
            except LlmUnavailableError:
                raise
            except (LlmParseError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
                last_error = exc
                if attempt == 1:
                    break
        raise LlmParseError(str(last_error)) from last_error

    def _call_llm(self, text: str, system_prompt: str, user_label: str) -> dict:
        if self.settings.openai_api_key:
            try:
                return self._call_openai(text, system_prompt, user_label)
            except LlmUnavailableError:
                pass
        return self._call_ollama(text, system_prompt, user_label)

    def _call_ollama(self, text: str, system_prompt: str, user_label: str) -> dict:
        url = f"{self.settings.ollama_base_url.rstrip('/')}/api/chat"
        payload = {
            "model": self.settings.ollama_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{user_label}:\n\n{text[:12000]}"},
            ],
            "stream": False,
            "format": "json",
        }
        try:
            with httpx.Client(timeout=60.0) as client:
                resp = client.post(url, json=payload)
                resp.raise_for_status()
                content = resp.json()["message"]["content"]
        except (httpx.HTTPError, KeyError, OSError) as exc:
            raise LlmUnavailableError("LLM service unavailable") from exc
        return self._parse_json_content(content)

    def _call_openai(self, text: str, system_prompt: str, user_label: str) -> dict:
        url = f"{self.settings.openai_base_url.rstrip('/')}/chat/completions"
        headers = {"Authorization": f"Bearer {self.settings.openai_api_key}"}
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{user_label}:\n\n{text[:12000]}"},
            ],
            "response_format": {"type": "json_object"},
        }
        try:
            with httpx.Client(timeout=60.0) as client:
                resp = client.post(url, json=payload, headers=headers)
                resp.raise_for_status()
                content = resp.json()["choices"][0]["message"]["content"]
        except (httpx.HTTPError, KeyError, IndexError) as exc:
            detail = "LLM service unavailable"
            if isinstance(exc, httpx.HTTPStatusError) and exc.response is not None:
                if exc.response.status_code in (401, 403):
                    detail = "OpenAI API key rejected — check OPENAI_API_KEY in backend/.env"
            raise LlmUnavailableError(detail) from exc
        return self._parse_json_content(content)

    def _parse_json_content(self, content: str) -> dict:
        content = content.strip()
        if content.startswith("```"):
            content = re.sub(r"^```(?:json)?\s*", "", content)
            content = re.sub(r"\s*```$", "", content)
        return json.loads(content)

    def _normalize(self, raw: dict) -> dict:
        skills = raw.get("skills") or []
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(",") if s.strip()]
        exp = raw.get("experience_years", 0)
        try:
            exp = float(exp)
            exp = max(0.0, min(50.0, exp))
        except (TypeError, ValueError):
            exp = 0.0
        salary = raw.get("preferred_salary")
        if salary is not None:
            try:
                salary = int(salary)
            except (TypeError, ValueError):
                salary = None
        other_links = raw.get("other_links") or []
        if isinstance(other_links, str):
            other_links = [s.strip() for s in other_links.split(",") if s.strip()]
        return {
            "name": str(raw.get("name") or "Unknown Candidate").strip(),
            "skills": [str(s) for s in skills],
            "experience_years": exp,
            "preferred_salary": salary,
            "remote_preference": bool(raw.get("remote_preference", False)),
            "summary": str(raw.get("summary") or "").strip(),
            "email": str(raw.get("email") or "").strip(),
            "phone": str(raw.get("phone") or "").strip(),
            "linkedin": str(raw.get("linkedin") or "").strip(),
            "portfolio": str(raw.get("portfolio") or "").strip(),
            "other_links": [str(link).strip() for link in other_links if str(link).strip()],
        }

    def _normalize_job(self, raw: dict) -> dict:
        skills = raw.get("required_skills") or []
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(",") if s.strip()]
        exp = raw.get("required_experience", 0)
        try:
            exp = int(float(exp))
            exp = max(0, min(50, exp))
        except (TypeError, ValueError):
            exp = 0
        link = str(raw.get("link") or "").strip() or None
        company = str(raw.get("company") or "").strip() or None
        location = str(raw.get("location") or "").strip() or None
        return {
            "title": str(raw.get("title") or "Untitled Job").strip(),
            "required_skills": [str(s) for s in skills],
            "required_experience": exp,
            "description": str(raw.get("description") or "").strip(),
            "company": company,
            "location": location,
            "remote_policy": bool(raw.get("remote_policy", False)),
            "link": link,
        }
