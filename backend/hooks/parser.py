from contracts.profiles import CandidateProfile, JobProfile
from core.compensation import normalize_preferred_currency, normalize_preferred_salary


class JsonParser:
    def parse_candidate(self, raw: dict) -> CandidateProfile:
        return CandidateProfile(
            id=raw["id"],
            name=raw["name"],
            skills=list(raw.get("skills", [])),
            experience_years=float(raw.get("experience_years", 0)),
            preferred_salary=normalize_preferred_salary(raw.get("preferred_salary")),
            preferred_currency=normalize_preferred_currency(raw.get("preferred_currency")),
            remote_preference=bool(raw.get("remote_preference", False)),
            summary=str(raw.get("summary", "")),
            email=str(raw.get("email") or "").strip(),
            phone=str(raw.get("phone") or "").strip(),
            linkedin=str(raw.get("linkedin") or "").strip(),
            portfolio=str(raw.get("portfolio") or "").strip(),
            other_links=[str(link).strip() for link in (raw.get("other_links") or []) if str(link).strip()],
        )

    def parse_job(self, raw: dict) -> JobProfile:
        budget_min = normalize_preferred_salary(raw.get("budget_min"))
        budget_max = normalize_preferred_salary(raw.get("budget_max"))
        budget = normalize_preferred_salary(raw.get("budget"))
        if budget is None:
            budget = budget_max or budget_min
        status = str(raw.get("status") or "open").lower()
        if status not in {"open", "closed", "draft"}:
            status = "open"
        return JobProfile(
            id=raw["id"],
            title=raw["title"],
            required_skills=list(raw.get("required_skills", [])),
            preferred_skills=list(raw.get("preferred_skills", [])),
            required_experience=float(raw.get("required_experience", 0)),
            budget=budget,
            budget_currency=normalize_preferred_currency(raw.get("budget_currency")),
            budget_min=budget_min,
            budget_max=budget_max,
            remote_policy=bool(raw.get("remote_policy", False)),
            description=str(raw.get("description", "")),
            company=raw.get("company"),
            location=raw.get("location"),
            job_type=raw.get("job_type"),
            link=raw.get("link"),
            accepts_applications=bool(raw.get("accepts_applications", True)),
            status=status,
            created_at=str(raw.get("created_at") or ""),
            updated_at=str(raw.get("updated_at") or ""),
        )
