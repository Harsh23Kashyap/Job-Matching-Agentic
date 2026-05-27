"""Idempotent demo accounts for local development and thesis demos."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from auth.store import UserStore
    from bootstrap import SystemContainer

logger = logging.getLogger(__name__)

DEMO_PASSWORD = "demo1234"

DEMO_CANDIDATE_EMAIL = "demo.candidate@test.com"
DEMO_EMPLOYER_EMAIL = "demo.employer@test.com"
DEMO_ADMIN_EMAIL = "demo.admin@test.com"

# Rahul Sharma · strong ML Engineer match in bootstrapped corpus
DEMO_CANDIDATE_ID = "cv_01"

# Sample employer-owned roles from data/jobs.json
DEMO_EMPLOYER_JOB_IDS = ("job_01", "job_02", "job_03", "job_04", "job_05")

DEMO_PRIMARY_JOB_ID = "job_01"


def seed_demo_accounts(auth_store: UserStore, container: SystemContainer) -> dict[str, str]:
    """Ensure demo users, linked profile, and sample jobs exist. Safe to call on every startup."""
    actions: list[str] = []

    candidate_user = _ensure_user(auth_store, DEMO_CANDIDATE_EMAIL, "candidate", actions)
    if container.candidate.get_by_id(DEMO_CANDIDATE_ID) is None:
        logger.warning("Demo candidate profile %s missing from corpus", DEMO_CANDIDATE_ID)
    else:
        auth_store.link_candidate(candidate_user.id, DEMO_CANDIDATE_ID)
        actions.append(f"candidate linked to {DEMO_CANDIDATE_ID}")

    employer_user = _ensure_user(auth_store, DEMO_EMPLOYER_EMAIL, "employer", actions)
    linked_jobs = 0
    for job_id in DEMO_EMPLOYER_JOB_IDS:
        if container.employer.get_by_id(job_id) is None:
            continue
        if auth_store.link_job_if_unowned(employer_user.id, job_id):
            linked_jobs += 1
    if linked_jobs:
        actions.append(f"employer linked to {linked_jobs} jobs")

    _ensure_user(auth_store, DEMO_ADMIN_EMAIL, "admin", actions)

    summary = "; ".join(actions) if actions else "demo accounts already present"
    logger.info("Demo seed: %s", summary)
    return {
        "candidate_email": DEMO_CANDIDATE_EMAIL,
        "employer_email": DEMO_EMPLOYER_EMAIL,
        "admin_email": DEMO_ADMIN_EMAIL,
        "password": DEMO_PASSWORD,
        "summary": summary,
    }


def _ensure_user(auth_store: UserStore, email: str, role: str, actions: list[str]):
    existing = auth_store.get_by_email(email)
    if existing is not None:
        return existing
    user = auth_store.create_user(email, DEMO_PASSWORD, role)
    actions.append(f"created {role} {email}")
    return user


def seed_demo_activity(
    container: "SystemContainer",
    auth_store: "UserStore",
    activity_store,
    feedback_store,
) -> dict[str, int]:
    """Pre-populate saved jobs, applications, and employer shortlist for live demos."""
    from contracts.matching import MatchRequest

    stats = {"saved_jobs": 0, "applications": 0, "employer_shortlist": 0}

    candidate_user = auth_store.get_by_email(DEMO_CANDIDATE_EMAIL)
    if candidate_user is None:
        return stats

    candidate_id = auth_store.get_candidate_id(candidate_user.id) or DEMO_CANDIDATE_ID
    profile = container.candidate.get_by_id(candidate_id)
    if profile is None:
        return stats

    existing_saved = activity_store.list_saved_jobs(candidate_id)
    existing_apps = activity_store.list_applications_for_candidate(candidate_id)
    if existing_saved or existing_apps:
        stats["saved_jobs"] = len(existing_saved)
        stats["applications"] = len(existing_apps)
        employer_user = auth_store.get_by_email(DEMO_EMPLOYER_EMAIL)
        if employer_user:
            stats["employer_shortlist"] = sum(
                1
                for row in feedback_store.list_latest_for_user(employer_user.id)
                if row.action == "save"
            )
        return stats

    match_request = MatchRequest(
        query_key=profile.name,
        top_k=10,
        strategy="composite",
        metric="cosine",
        skills_mode="jaccard",
        semantic_weight=0.7,
        retrieval="exhaustive",
    )
    match_response = container.matchmaker.match_candidate_to_jobs(match_request)
    results = match_response.results or []

    if results:
        top = results[0]
        activity_store.apply(
            candidate_id=candidate_id,
            candidate_name=profile.name,
            job_id=top.target_id,
            job_title=top.target_label,
            match_score=top.similarity,
        )
        feedback_store.record(
            candidate_id=candidate_id,
            job_id=top.target_id,
            action="apply",
            user_id=candidate_user.id,
        )
        stats["applications"] = 1

    for row in results[1:3]:
        activity_store.save_job(candidate_id, row.target_id, row.target_label)
        feedback_store.record_user_action(
            user_id=candidate_user.id,
            target_id=row.target_id,
            action="save",
            role="candidate",
        )
        stats["saved_jobs"] += 1

    employer_user = auth_store.get_by_email(DEMO_EMPLOYER_EMAIL)
    primary_job = container.employer.get_by_id(DEMO_PRIMARY_JOB_ID)
    if employer_user is None or primary_job is None:
        return stats

    employer_match = container.matchmaker.match_job_to_candidates(
        MatchRequest(
            query_key=primary_job.title,
            top_k=10,
            strategy="composite",
            metric="cosine",
            skills_mode="jaccard",
            semantic_weight=0.7,
            retrieval="exhaustive",
        )
    )
    for row in (employer_match.results or [])[:3]:
        feedback_store.record_user_action(
            user_id=employer_user.id,
            target_id=row.target_id,
            action="save",
            context_id=primary_job.id,
            role="employer",
        )
        stats["employer_shortlist"] += 1

    logger.info(
        "Demo activity seeded: %s saved jobs, %s applications, %s employer saves",
        stats["saved_jobs"],
        stats["applications"],
        stats["employer_shortlist"],
    )
    return stats
