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

# Rahul Sharma — strong ML Engineer match in bootstrapped corpus
DEMO_CANDIDATE_ID = "cv_01"

# Sample employer-owned roles from data/jobs.json
DEMO_EMPLOYER_JOB_IDS = ("job_01", "job_02", "job_03", "job_04", "job_05")


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
