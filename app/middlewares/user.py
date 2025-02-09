from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from database.services import User


class UsersMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: Message | CallbackQuery, data: dict) -> Any:
        session = data["session"]
        user = await User.get_or_create(
            session,
            user_id=event.from_user.id,
            username=event.from_user.username,
            language=event.from_user.language_code,
        )
        if not user.is_banned:
            data["user"] = user
            return await handler(event, data)
        return
