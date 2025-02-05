from pydantic import BaseModel
from app.ai.genAI import Topics

class GenerateModel(BaseModel):
    topic: Topics
    number: int
    ageGroup: str
    item: str = None