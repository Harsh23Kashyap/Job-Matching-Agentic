from dataclasses import dataclass

from agents.candidate_agent import CandidateAgent
from agents.employer_agent import EmployerAgent
from agents.matchmaking_agent import MatchmakingAgent
from bus.event_bus import AgentEventBus
from bus.events import EventType
from config import Settings
from hooks.explainer import RuleExplainer
from hooks.parser import JsonParser
from stores.factory import create_store


@dataclass
class SystemContainer:
    bus: AgentEventBus
    settings: Settings
    candidate: CandidateAgent
    employer: EmployerAgent
    matchmaker: MatchmakingAgent


def create_system(settings: Settings | None = None) -> SystemContainer:
    settings = settings or Settings()
    bus = AgentEventBus()
    parser = JsonParser()
    explainer = RuleExplainer()

    candidate_store = create_store(settings, "candidates_collection")
    job_store = create_store(settings, "jobs_collection")

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

    return SystemContainer(
        bus=bus,
        settings=settings,
        candidate=candidate_agent,
        employer=employer_agent,
        matchmaker=matchmaker,
    )
