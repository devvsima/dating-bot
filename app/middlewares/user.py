from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from typing import Any, Callable
from database.service.users import get_or_create_user


class UsersMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: Message | CallbackQuery, data: dict) -> Any:
        session = data["session"]
        user = await get_or_create_user(
            session,
            user_id=event.from_user.id,
            username=event.from_user.username,
            language=event.from_user.language_code,
        )
        if not user.is_banned:
            data["user"] = user
            return await handler(event, data)
        return
