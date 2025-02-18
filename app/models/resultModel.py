from typing import Any

from pydantic import BaseModel


class ResultModel(BaseModel):
    """
    Result model to be used for the FastAPI endpoint
    """

    message: str
    data: Any = None