import json
import re

import httpx

from config import Settings
from core.compensation import normalize_preferred_currency, normalize_preferred_salary


class LlmUnavailableError(Exception):
    pass


class LlmParseError(Exception):
    pass


JOB_SYSTEM_PROMPT = """You extract structured job posting data from job description text.
Return ONLY valid JSON with these keys:
- title (string)
- required_skills (array of strings)
- required_experience (integer years, minimum 0)
- budget_min (integer annual total compensation minimum, or null)
- budget_max (integer annual total compensation maximum, or null)
- budget_currency (string: INR, USD, EUR, GBP, or SGD — infer from the JD)
- company (string)
- location (string)
- remote_policy (boolean — true if remote or hybrid-friendly)
- job_type (string e.g. Full-time, Part-time, Contract, Internship)
- description (string, 1-4 sentences summarizing the role)
- link (string URL for application, or empty string)

Use empty string, empty array, or null when unknown. Do not include markdown."""


RESUME_COACH_PROMPT = """You suggest resume improvements for a specific job application.
Return ONLY valid JSON with these keys:
- missing_keywords (array of strings — ATS keywords from the job missing or weak in the resume)
- weak_skills (array of strings — skills the candidate lists but does not demonstrate in text)
- missing_skills (array of strings — required job skills not evidenced in the profile)
- suggested_summary (string — rewritten 2-3 sentence professional summary for this role)
- bullet_improvements (array of objects with keys: original, suggested, reason)
- ats_checklist (array of objects with keys: item, status, tip — status must be pass, warn, or fail)

Rules:
- Base suggestions ONLY on the candidate profile and job posting provided.
- Do NOT invent employers, degrees, tools, or metrics the candidate does not plausibly have.
- Keep suggestions actionable and specific to the target role.
- Do not include markdown."""


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

    def suggest_resume_for_job(self, candidate: dict, job: dict) -> dict:
        import json as json_module

        payload = json_module.dumps({"candidate": candidate, "job": job}, ensure_ascii=False)
        return self._parse_with_prompt(
            payload,
            RESUME_COACH_PROMPT,
            "Resume coaching context",
            self._normalize_resume_coach,
        )

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

    def _normalize_resume_coach(self, raw: dict) -> dict:
        def _str_list(key: str) -> list[str]:
            values = raw.get(key) or []
            if isinstance(values, str):
                values = [values]
            return [str(v).strip() for v in values if str(v).strip()]

        bullets: list[dict[str, str]] = []
        for row in raw.get("bullet_improvements") or []:
            if not isinstance(row, dict):
                continue
            original = str(row.get("original") or "").strip()
            suggested = str(row.get("suggested") or "").strip()
            reason = str(row.get("reason") or "").strip()
            if original and suggested:
                bullets.append({"original": original, "suggested": suggested, "reason": reason})

        checklist: list[dict[str, str]] = []
        for row in raw.get("ats_checklist") or []:
            if not isinstance(row, dict):
                continue
            item = str(row.get("item") or "").strip()
            status = str(row.get("status") or "warn").strip().lower()
            tip = str(row.get("tip") or "").strip()
            if item and status in {"pass", "warn", "fail"}:
                checklist.append({"item": item, "status": status, "tip": tip})

        return {
            "missing_keywords": _str_list("missing_keywords"),
            "weak_skills": _str_list("weak_skills"),
            "missing_skills": _str_list("missing_skills"),
            "suggested_summary": str(raw.get("suggested_summary") or "").strip(),
            "bullet_improvements": bullets,
            "ats_checklist": checklist,
        }

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
        job_type = str(raw.get("job_type") or "").strip() or None
        budget_min = normalize_preferred_salary(raw.get("budget_min"))
        budget_max = normalize_preferred_salary(raw.get("budget_max"))
        budget = normalize_preferred_salary(raw.get("budget"))
        if budget_min is None and budget_max is None:
            budget_min = budget
            budget_max = budget
        elif budget_min is None:
            budget_min = budget_max
        elif budget_max is None:
            budget_max = budget_min
        return {
            "title": str(raw.get("title") or "Untitled Job").strip(),
            "required_skills": [str(s) for s in skills],
            "required_experience": exp,
            "description": str(raw.get("description") or "").strip(),
            "company": company,
            "location": location,
            "remote_policy": bool(raw.get("remote_policy", False)),
            "job_type": job_type,
            "link": link,
            "budget_currency": normalize_preferred_currency(raw.get("budget_currency")),
            "budget_min": budget_min,
            "budget_max": budget_max,
            "budget": budget_max or budget_min,
        }
