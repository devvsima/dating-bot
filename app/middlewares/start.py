from aiogram import BaseMiddleware

from database.service.users import create_user, get_user, new_referral
from typing import Any, Callable, Dict
from aiogram.types import Update


class StartMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: Update, data: Dict[str, Any]) -> Any:
        user = get_user(event.from_user.id)
        if not user:
            user = create_user(
                user_id=event.from_user.id,
                username=event.from_user.username,
                language=event.from_user.language_code,
            )

        from app.handlers.bot_utils import new_user_alert_to_group
        await new_user_alert_to_group(user)
        
        inviter: str = data["command"].args

        if inviter:
            new_referral(inviter)
            
        if not user.is_banned:
            data["user"] = user
            return await handler(event, data)

        return await handler(event, data)