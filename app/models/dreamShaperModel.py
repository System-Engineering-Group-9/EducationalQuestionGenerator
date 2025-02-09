from pydantic import BaseModel


class DreamShaperModel(BaseModel):
    """
    Model for the parameters of the dreamShaper endpoint
    """
    prompt: str
