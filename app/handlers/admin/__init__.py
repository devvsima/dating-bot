from .admin import admin_router
from .ban import admin_router
from .logs import admin_router
from .mailing import admin_router
from .profile import admin_router
from .restart import admin_router
from .stats import admin_router

__all__ = ["admin_router"]
