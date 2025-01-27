from aiogram import BaseMiddleware
from aiogram.types import Update

from app.handlers.bot_utils import new_user_alert_to_group
from database.service.users import create_user, get_user, new_referral
from typing import Any, Callable, Dict


class StartMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: Update, data: Dict[str, Any]) -> Any:
        user = await get_user(event.from_user.id)
        if not user:
            user = await create_user(
                user_id=event.from_user.id,
                username=event.from_user.username,
                language=event.from_user.language_code,
            )
            await new_user_alert_to_group(user)
        
        inviter: str = data["command"].args

        if inviter:
            await new_referral(inviter)
            
        if not user.is_banned:
            data["user"] = user
            return await handler(event, data)

        return await handler(event, data)