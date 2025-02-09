# app/models/generateModel.py
from pydantic import BaseModel

from app.ai.questionGenerator import Topics


class GenerateModel(BaseModel):
    """
    Model for the parameters of the generate endpoint
    """
    topic: Topics
    number: int
    ageGroup: str
    item: str = None