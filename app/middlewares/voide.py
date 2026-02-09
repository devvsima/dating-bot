from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from database.models.user import UserStatus
from database.queries import User


class VoideMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable, message: Message | CallbackQuery, data: dict
    ) -> Any:
        session = data["session"]
        user, is_create = await User.get_or_create(
            session=session,
            id=message.from_user.id,
            username=message.from_user.username,
            language=message.from_user.language_code,
        )
        if user.status == UserStatus.Banned:
            return

        data["user"] = user
        return await handler(message, data)
