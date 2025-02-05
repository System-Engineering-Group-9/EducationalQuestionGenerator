from pydantic import BaseModel


class Question(BaseModel):

    """
    Question model to be used for the FastAPI endpoint
    """

    question_text: str
    choiceA: str
    choiceB: str
    choiceC: str
    choiceD: str
    answer: str