from pydantic import BaseModel


class SearchHit(BaseModel):
    entity_id: str
    distance: float
    metadata: dict
