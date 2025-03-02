from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from app.handlers.bot_utils import new_user_alert_to_group
from database.services import User
from utils.base62 import decode_base62


class StartMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, message: Message, data: dict) -> Any:
        session = data["session"]
        user, is_create = await User.get_or_create(
            session,
            user_id=message.from_user.id,
            username=message.from_user.username,
            language=message.from_user.language_code,
        )
        if not user.is_banned:
            data["user"] = user
            if is_create:
                if inviter := data["command"].args:
                    await new_user_alert_to_group(user)
                    inviter = await User.get(session, decode_base62(inviter))
                    await User.increment_referral_count(session, inviter)

            return await handler(message, data)
        return
