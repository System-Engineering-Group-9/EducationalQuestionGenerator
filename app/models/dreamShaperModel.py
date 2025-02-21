from pydantic import BaseModel

from app.ai.enums.subject import Subject


class DreamShaperModel(BaseModel):
    """
    Model for the parameters of the dreamShaper endpoint
    """
    subject: Subject
    ageGroup: str
