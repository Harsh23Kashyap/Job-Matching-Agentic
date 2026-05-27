import re
import uuid

from config import Settings
from hooks.llm_parser import LlmParser
from hooks.parser import JsonParser


def create_llm_parser(settings: Settings) -> LlmParser:
    return LlmParser(settings)


def slugify_name(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "candidate"


def make_entity_id(label: str) -> str:
    return f"{slugify_name(label)}-{uuid.uuid4().hex[:8]}"


def make_candidate_id(name: str) -> str:
    return make_entity_id(name)
