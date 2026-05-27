from dataclasses import dataclass

from agents.candidate_agent import CandidateAgent
from agents.employer_agent import EmployerAgent
from agents.matchmaking_agent import MatchmakingAgent
from bus.event_bus import AgentEventBus
from bus.events import EventType
from config import Settings
from core.calibration import PlattCalibrator
from core.fusion import LearnedFusionModel
from hooks.explainer import RuleExplainer
from hooks.parser import JsonParser
from services.real_jobs_service import RealJobsService
from stores.candidate_activity_store import CandidateActivityStore
from stores.factory import create_store
from stores.feedback_store import FeedbackStore


@dataclass
class SystemContainer:
    bus: AgentEventBus
    settings: Settings
    candidate: CandidateAgent
    employer: EmployerAgent
    matchmaker: MatchmakingAgent
    feedback_store: FeedbackStore
    activity_store: CandidateActivityStore
    real_jobs: RealJobsService | None = None


def create_system(settings: Settings | None = None) -> SystemContainer:
    settings = settings or Settings()
    bus = AgentEventBus()
    parser = JsonParser()
    explainer = RuleExplainer()

    candidate_store = create_store(settings, "candidates_collection")
    job_store = create_store(settings, "jobs_collection")
    feedback_store = FeedbackStore(settings.sqlite_path)
    activity_store = CandidateActivityStore(settings.sqlite_path)

    fusion_model = LearnedFusionModel.load(settings.fusion_model_path)
    calibrator = PlattCalibrator.load(settings.calibration_model_path)

    candidate_agent = CandidateAgent(
        bus=bus,
        store=candidate_store,
        parser=parser,
        settings=settings,
    )
    employer_agent = EmployerAgent(
        bus=bus,
        store=job_store,
        parser=parser,
        settings=settings,
    )
    matchmaker = MatchmakingAgent(
        bus=bus,
        candidate_agent=candidate_agent,
        employer_agent=employer_agent,
        explainer=explainer,
        settings=settings,
        fusion_model=fusion_model,
        calibrator=calibrator,
        feedback_store=feedback_store,
    )
    matchmaker.register_handlers(bus)

    n_c = candidate_agent.bootstrap_from_file(settings.cvs_path)
    n_j = employer_agent.bootstrap_from_file(settings.jobs_path)

    bus.publish(
        bus.make_event(
            EventType.CORPUS_BOOTSTRAPPED,
            "system",
            {"candidates_loaded": n_c, "jobs_loaded": n_j},
        )
    )

    container = SystemContainer(
        bus=bus,
        settings=settings,
        candidate=candidate_agent,
        employer=employer_agent,
        matchmaker=matchmaker,
        feedback_store=feedback_store,
        activity_store=activity_store,
    )
    container.real_jobs = RealJobsService(container)
    if not container.real_jobs.boot_from_snapshot_if_available():
        container.real_jobs.state.job_count = n_j
        container.real_jobs.state.source = "local_seed"

    return container
