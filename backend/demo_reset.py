"""Reload demo corpus and reset local demo state for repeatable demos."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from demo_seed import (
    DEMO_ADMIN_EMAIL,
    DEMO_CANDIDATE_EMAIL,
    DEMO_CANDIDATE_ID,
    DEMO_EMPLOYER_EMAIL,
    DEMO_EMPLOYER_JOB_IDS,
    seed_demo_accounts,
    seed_demo_activity,
)
from stores.factory import create_store

if TYPE_CHECKING:
    from auth.store import UserStore
    from bootstrap import SystemContainer

logger = logging.getLogger(__name__)

DEMO_EMAILS = (DEMO_CANDIDATE_EMAIL, DEMO_EMPLOYER_EMAIL, DEMO_ADMIN_EMAIL)


def reload_corpus(container: SystemContainer) -> dict[str, int]:
    """Clear in-memory profiles and vector index, then reload JSON corpus."""
    settings = container.settings
    container.matchmaker.state.sessions.clear()

    container.candidate.state.profiles.clear()
    container.candidate.state.name_index.clear()
    container.candidate.state.store_version = 0
    container.candidate.store = create_store(settings, "candidates_collection")

    container.employer.state.profiles.clear()
    container.employer.state.title_index.clear()
    container.employer.state.store_version = 0
    container.employer.store = create_store(settings, "jobs_collection")

    candidates_loaded = container.candidate.bootstrap_from_file(settings.cvs_path)
    jobs_loaded = container.employer.bootstrap_from_file(settings.jobs_path)
    logger.info("Demo corpus reloaded: %s candidates, %s jobs", candidates_loaded, jobs_loaded)
    return {"candidates_loaded": candidates_loaded, "jobs_loaded": jobs_loaded}


def clear_demo_sqlite(container: SystemContainer, auth_store: UserStore) -> None:
    """Remove demo users, activity, and feedback so seeding starts clean."""
    container.activity_store.clear_all()
    container.feedback_store.clear_all()
    removed = auth_store.purge_users_by_email(DEMO_EMAILS)
    logger.info("Demo SQLite cleared (%s demo users removed)", removed)


def reset_demo_data(container: SystemContainer, auth_store: UserStore) -> dict:
    """Full demo reset: corpus reload, SQLite wipe, accounts + sample activity."""
    corpus = reload_corpus(container)
    clear_demo_sqlite(container, auth_store)
    accounts = seed_demo_accounts(auth_store, container)
    activity = seed_demo_activity(container, auth_store, container.activity_store, container.feedback_store)
    return {
        **corpus,
        **accounts,
        **activity,
        "candidate_count": len(container.candidate.state.profiles),
        "job_count": len(container.employer.state.profiles),
        "demo_candidate_id": DEMO_CANDIDATE_ID,
        "demo_job_ids": list(DEMO_EMPLOYER_JOB_IDS),
    }


def demo_snapshot(container: SystemContainer, auth_store: UserStore) -> dict:
    """Counts for admin UI without mutating state."""
    candidate_user = auth_store.get_by_email(DEMO_CANDIDATE_EMAIL)
    candidate_id = auth_store.get_candidate_id(candidate_user.id) if candidate_user else None
    saved_count = 0
    application_count = 0
    if candidate_id:
        saved_count = len(container.activity_store.list_saved_jobs(candidate_id))
        application_count = len(container.activity_store.list_applications_for_candidate(candidate_id))

    employer_user = auth_store.get_by_email(DEMO_EMPLOYER_EMAIL)
    employer_saves = 0
    if employer_user:
        employer_saves = sum(
            1
            for row in container.feedback_store.list_latest_for_user(employer_user.id)
            if row.action == "save"
        )

    return {
        "candidates_in_corpus": len(container.candidate.state.profiles),
        "jobs_in_corpus": len(container.employer.state.profiles),
        "saved_jobs": saved_count,
        "applications": application_count,
        "employer_shortlist": employer_saves,
    }
