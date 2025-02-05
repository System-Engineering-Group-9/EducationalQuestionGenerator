from fastapi import APIRouter

from app.api.routes import ai, config

"""
Author: Jack Pan
Date: 2025-2-5
Description:
    This module defines the routers and paths of the services
"""


api_router = APIRouter()
api_router.include_router(ai.router)
api_router.include_router(config.router)
