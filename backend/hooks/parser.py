from contracts.profiles import CandidateProfile, JobProfile


class JsonParser:
    def parse_candidate(self, raw: dict) -> CandidateProfile:
        return CandidateProfile(
            id=raw["id"],
            name=raw["name"],
            skills=list(raw.get("skills", [])),
            experience_years=float(raw.get("experience_years", 0)),
            preferred_salary=raw.get("preferred_salary"),
            remote_preference=bool(raw.get("remote_preference", False)),
            summary=str(raw.get("summary", "")),
        )

    def parse_job(self, raw: dict) -> JobProfile:
        return JobProfile(
            id=raw["id"],
            title=raw["title"],
            required_skills=list(raw.get("required_skills", [])),
            required_experience=int(raw.get("required_experience", 0)),
            budget=raw.get("budget"),
            remote_policy=bool(raw.get("remote_policy", False)),
            description=str(raw.get("description", "")),
            company=raw.get("company"),
            location=raw.get("location"),
            job_type=raw.get("job_type"),
            link=raw.get("link"),
        )
