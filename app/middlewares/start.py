from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from app.handlers.bot_utils import new_user_alert_to_group
from database.services import User
from utils.base62 import decode_base62


class StartMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, message: Message, data: dict) -> Any:
        session = data["session"]
        if user := await User.get_with_profile(session, message.from_user.id):
            if not user.is_banned:
                data["user"] = user
                return await handler(message, data)
            return

        user = await User.create_user(
            session,
            user_id=message.from_user.id,
            username=message.from_user.username,
            language=message.from_user.language_code,
        )
        data["user"] = user
        await new_user_alert_to_group(user)

        if inviter := data["command"].args:
            inviter = User.get(decode_base62(inviter))
            await User.increment_referral_count(session, inviter)

        return await handler(message, data)
