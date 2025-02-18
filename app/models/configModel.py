from pydantic import BaseModel, validator

from app.models.enums.quizMode import QuizMode
from app.models.enums.teamMode import TeamMode


class ConfigModel(BaseModel):
    """Config model to be used for the FastAPI endpoint"""

    timeLimit: int
    teamMode: TeamMode
    numberOfPlayers: int
    quizMode: QuizMode

    @validator('numberOfPlayers')
    def check_number_of_players(cls, value):
        if not 2 <= value <= 6:
            raise ValueError('numberOfPlayers must be between 2 and 6')
        return value

    @validator('timeLimit')
    def check_time_limit(cls, value):
        if not 10 <= value <= 60:
            raise ValueError('timeLimit must be between 10 and 60')
        return value
