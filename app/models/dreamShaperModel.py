from pydantic import BaseModel

from app.ai.enums.topic import Topic


class DreamShaperModel(BaseModel):
    """
    Model for the parameters of the dreamShaper endpoint
    """
    topic: Topic
    ageGroup: str
