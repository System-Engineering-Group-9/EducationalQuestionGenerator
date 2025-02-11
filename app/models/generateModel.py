# app/models/generateModel.py
from pydantic import BaseModel

from app.ai.enums.topic import Topic


class GenerateModel(BaseModel):
    """
    Model for the parameters of the generate endpoint
    """
    topic: Topic
    number: int
    ageGroup: str
    item: str = None