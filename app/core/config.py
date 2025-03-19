from dataclasses import field
from typing import Literal, List

from pydantic_settings import BaseSettings

"""
Author: Jack Pan
Date: 2025-2-5
Description:
    This file is for settings of the application
"""


class Settings(BaseSettings):
    version:str = "1.0.0"
    BASE_URL: str = f"/api/v{version}"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    BACKEND_CORS_ORIGINS: List[str] = field(default_factory=lambda: ["*"])


    PROJECT_NAME: str = "EducationalQuizQuestionGenerator"


settings = Settings()  # type: ignore