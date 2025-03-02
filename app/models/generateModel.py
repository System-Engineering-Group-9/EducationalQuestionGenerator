# app/models/generateModel.py
from pydantic import BaseModel, validator

from app.ai.enums.subject import Subject


class GenerateModel(BaseModel):
    """
    Model for the parameters of the generate endpoint
    """
    subject: Subject
    number: int
    ageGroup: str
    item: str = None

    @validator('number')
    def check_number(cls, value):
        if not 1 <= value <= 5:
            raise ValueError('number must be between 1 and 5')
        return value
