from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from app.text import message_text as mt
from data.config import tgbot
from database.services import User


class AdminMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, message: Message, data: dict) -> Any:
        session = data["session"]
        if user := await User.get_with_profile(session, message.from_user.id):
            if user.id in tgbot.ADMINS:
                data["user"] = user
                return await handler(message, data)
        await message.answer(mt.UNKNOWN_COMMAND(language=user.language))
        return
