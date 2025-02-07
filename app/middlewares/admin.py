from aiogram import BaseMiddleware
from aiogram.types import Message

from data.config import tgbot
from database.service.users import get_user

from typing import Any, Callable

ADMINS = tgbot.ADMINS


class AdminMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, message: Message, data: dict) -> Any:
        session = data["session"]
        if user := await get_user(session, message.from_user.id):
            if user.id in ADMINS:
                data["user"] = user
                return await handler(message, data)
        return
