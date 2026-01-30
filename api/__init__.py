"""
API endpoints для Telegram WebApp
"""

from fastapi import APIRouter

from .actions import router as actions_router
from .admin import router as admin_router
from .home import router as home_router
from .profile import router as profile_router
from .search import router as search_router

# Создаем главный роутер
api_router = APIRouter(prefix="/api")

# Подключаем роутеры
api_router.include_router(home_router, tags=[""])
api_router.include_router(profile_router, tags=["profile"])
api_router.include_router(search_router, tags=["search"])
api_router.include_router(actions_router, tags=["actions"])
api_router.include_router(admin_router, tags=["admin"])

__all__ = ["api_router"]
