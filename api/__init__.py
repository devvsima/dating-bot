"""
API endpoints для Telegram WebApp
"""

from fastapi import APIRouter

from .actions import router as actions_router
from .profile import router as profile_router
from .search import router as search_router

# Создаем главный роутер
api_router = APIRouter(prefix="/api")

# Подключаем роутеры
api_router.include_router(profile_router, tags=["profile"])
api_router.include_router(search_router, tags=["search"])
api_router.include_router(actions_router, tags=["actions"])

__all__ = ["api_router"]
