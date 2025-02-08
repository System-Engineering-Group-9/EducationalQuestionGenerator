from typing import List

from pydantic import BaseModel


class RecognitionsModel(BaseModel):

    """
    Recognition model to be used for the FastAPI endpoint
    """

    items: List[dict]
