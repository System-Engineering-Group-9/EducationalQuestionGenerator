# app/models/questionModel.py
from typing import List
from pydantic import BaseModel

class QuestionModel(BaseModel):
    """
    Question model to be used for the FastAPI endpoint
    """
    question_text: str
    choiceA: str
    choiceB: str
    choiceC: str
    choiceD: str
    answer: str

class QuestionsModel(BaseModel):
    """
    Questions model to be used for the FastAPI endpoint
    """
    questions: List[QuestionModel]