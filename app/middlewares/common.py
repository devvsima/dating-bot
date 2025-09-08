import re
from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from app.business.alert_service import new_user_alert_to_group
from app.constans import REFERAL_SOURCES
from database.models.user import UserStatus
from database.services import User
from database.services.profile import Profile
from database.services.referal import Referal
from utils.base62 import decode_base62
from utils.language import get_supported_language


class CommonMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable, message: Message | CallbackQuery, data: dict
    ) -> Any:
        session = data["session"]
        
        # Определяем поддерживаемый язык
        user_language = get_supported_language(message.from_user.language_code)
        
        user, is_create = await User.get_or_create(
            session=session,
            id=message.from_user.id,
            username=message.from_user.username,
            language=user_language,
        )

        # Получаем пользователя с профилем
        user_with_profile = await User.get_with_profile(session, user.id)

        if user_with_profile.status == UserStatus.Banned:
            return

        data["user"] = user_with_profile
        if isinstance(message, Message):
            if is_create:
                code = "unk"
                try:
                    if inviter_code := getattr(data.get("command"), "args", None):
                        code, inviter_id = inviter_code.split("_")
                        inviter_id = decode_base62(inviter_id)
                        if await User.get_by_id(session, inviter_id):
                            await Referal.create(
                                session=session,
                                user_id=user.id,
                                inviter_id=inviter_id,
                                code=code,
                                source=REFERAL_SOURCES[code],
                            )
                except Exception:
                    pass
                await new_user_alert_to_group(user=user, code=code)

            if user.profile and not user.profile.is_active:
                await Profile.update(
                    session=session,
                    id=user.id,
                    is_active=True,
                )

        return await handler(message, data)
