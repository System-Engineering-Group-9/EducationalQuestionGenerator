from pydantic import BaseModel


class RecognitionModel(BaseModel):

    """
    Recognition model to be used for the FastAPI endpoint
    """

    item: str