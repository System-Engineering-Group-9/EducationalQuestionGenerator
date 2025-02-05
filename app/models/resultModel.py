from typing import Any

from pydantic import BaseModel


class ResultModel(BaseModel):
    message: str
    data: Any = None