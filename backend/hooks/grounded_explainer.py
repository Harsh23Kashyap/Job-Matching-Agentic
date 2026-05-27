"""LLM explainer grounded in structured match features; no hallucinated fields."""
from __future__ import annotations

import json
import re

import httpx

from config import Settings
from contracts.interfaces import Explainer
from contracts.matching import ScoreBreakdown
from contracts.snapshots import CandidateSnapshot, JobSnapshot
from core.explain import build_why_ranked
from core.skills import skill_overlap_details
from hooks.llm_parser import LlmUnavailableError

EXPLAIN_SYSTEM_PROMPT = """You explain job-candidate match rankings using ONLY the structured facts provided.
Return ONLY valid JSON: {"bullets": ["...", "..."]} with 2-4 concise bullets.
Do not invent skills, scores, or requirements not in the facts. Do not use markdown."""


class GroundedLlmExplainer(Explainer):
    """Template fallback with optional LLM polish when Ollama/OpenAI is available."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings

    def explain(
        self,
        candidate: CandidateSnapshot,
        job: JobSnapshot,
        scores: ScoreBreakdown,
    ) -> list[str]:
        base = self._template_explain(candidate, job, scores)
        if self.settings is None:
            return base
        try:
            llm_bullets = self._call_llm(candidate, job, scores, base)
            if llm_bullets:
                return llm_bullets[:5]
        except LlmUnavailableError:
            pass
        return base

    def _template_explain(
        self,
        candidate: CandidateSnapshot,
        job: JobSnapshot,
        scores: ScoreBreakdown,
    ) -> list[str]:
        base = build_why_ranked(candidate, job, scores)
        matched, missing = skill_overlap_details(candidate.skills, job.required_skills)
        if scores.constraint_factor is not None and scores.constraint_factor < 0.95:
            base.append(f"Constraint adjustment applied (×{scores.constraint_factor:.2f})")
        if scores.calibrated_score is not None:
            base.append(f"Calibrated relevance: {scores.calibrated_score:.0%}")
        if scores.routing_reason:
            base.append(scores.routing_reason)
        if missing:
            base.append(f"Gaps: {', '.join(missing[:3])}")
        if matched:
            base.append(f"Matched skills: {', '.join(matched[:4])}")
        return base[:5]

    def _facts_payload(
        self,
        candidate: CandidateSnapshot,
        job: JobSnapshot,
        scores: ScoreBreakdown,
        template_bullets: list[str],
    ) -> str:
        matched, missing = skill_overlap_details(candidate.skills, job.required_skills)
        facts = {
            "candidate_name": candidate.name,
            "candidate_skills": candidate.skills[:12],
            "candidate_experience_years": candidate.experience_years,
            "candidate_remote_preference": candidate.remote_preference,
            "job_title": job.title,
            "required_skills": job.required_skills,
            "preferred_skills": job.preferred_skills,
            "required_experience": job.required_experience,
            "remote_policy": job.remote_policy,
            "semantic_score": round(scores.semantic_score, 3),
            "skills_score": round(scores.skills_score, 3) if scores.skills_score is not None else None,
            "final_score": round(scores.final_score, 3),
            "matched_skills": matched,
            "missing_skills": missing,
            "constraint_factor": scores.constraint_factor,
            "routing_reason": scores.routing_reason,
            "template_bullets": template_bullets,
        }
        return json.dumps(facts, indent=2)

    def _call_llm(
        self,
        candidate: CandidateSnapshot,
        job: JobSnapshot,
        scores: ScoreBreakdown,
        template_bullets: list[str],
    ) -> list[str]:
        facts = self._facts_payload(candidate, job, scores, template_bullets)
        user_msg = f"Explain this match using only these facts:\n\n{facts}"
        if self.settings.openai_api_key:
            try:
                return self._parse_bullets(self._openai_chat(user_msg))
            except LlmUnavailableError:
                pass
        return self._parse_bullets(self._ollama_chat(user_msg))

    def _ollama_chat(self, user_msg: str) -> dict:
        url = f"{self.settings.ollama_base_url.rstrip('/')}/api/chat"
        payload = {
            "model": self.settings.ollama_model,
            "messages": [
                {"role": "system", "content": EXPLAIN_SYSTEM_PROMPT},
                {"role": "user", "content": user_msg[:8000]},
            ],
            "stream": False,
            "format": "json",
        }
        try:
            with httpx.Client(timeout=45.0) as client:
                resp = client.post(url, json=payload)
                resp.raise_for_status()
                content = resp.json()["message"]["content"]
        except (httpx.HTTPError, KeyError, OSError) as exc:
            raise LlmUnavailableError("LLM unavailable") from exc
        return self._parse_json(content)

    def _openai_chat(self, user_msg: str) -> dict:
        url = f"{self.settings.openai_base_url.rstrip('/')}/chat/completions"
        headers = {"Authorization": f"Bearer {self.settings.openai_api_key}"}
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": EXPLAIN_SYSTEM_PROMPT},
                {"role": "user", "content": user_msg[:8000]},
            ],
            "response_format": {"type": "json_object"},
        }
        try:
            with httpx.Client(timeout=45.0) as client:
                resp = client.post(url, json=payload, headers=headers)
                resp.raise_for_status()
                content = resp.json()["choices"][0]["message"]["content"]
        except (httpx.HTTPError, KeyError, IndexError) as exc:
            raise LlmUnavailableError("LLM unavailable") from exc
        return self._parse_json(content)

    def _parse_json(self, content: str) -> dict:
        content = content.strip()
        if content.startswith("```"):
            content = re.sub(r"^```(?:json)?\s*", "", content)
            content = re.sub(r"\s*```$", "", content)
        return json.loads(content)

    def _parse_bullets(self, payload: dict) -> list[str]:
        bullets = payload.get("bullets") or []
        if isinstance(bullets, str):
            bullets = [bullets]
        return [str(b).strip() for b in bullets if str(b).strip()]

    def narrative(self, candidate: CandidateSnapshot, job: JobSnapshot, scores: ScoreBreakdown) -> str:
        return " ".join(self.explain(candidate, job, scores))
