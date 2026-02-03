from .profile import dating_router
from .search import dating_router
from .inbox import dating_router

from .create_profile import registration_router
from .edit_description import dating_router
from .edit_photo import dating_router
from .disable_profile import dating_router
from .form_errors import registration_router


__all__ = ["dating_router", "registration_router"]
