# app/models/generateModel.py
from pydantic import BaseModel, field_validator

from app.ai.enums.subject import Subject


class GenerateModel(BaseModel):
    """
    Model for the parameters of the generate endpoint
    """
    subject: Subject
    number: int
    ageGroup: str
    item: str = None

    @field_validator('number')
    def validate_message(cls, value):
        if not 1 <= value <= 5:
            raise ValueError('number must be between 1 and 5')
        return value
