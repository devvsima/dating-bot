from aiogram import BaseMiddleware

from database.service.users import get_or_create_user
from typing import Any, Callable, Dict
from aiogram.types import Update

class UsersMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: Update, data: Dict[str, Any]) -> Any:
        from_user = None
        if event.message:
            from_user = event.message.from_user
        if event.callback_query:
            from_user = event.callback_query.from_user
        if event.inline_query:
            from_user = event.inline_query.from_user
        if from_user:
            user = await get_or_create_user(
                user_id=from_user.id,
                username=from_user.username,
                language=from_user.language_code,
            )
            if not user.is_banned:
                data["user"] = user
                return await handler(event, data)

            return
        return await handler(event, data)