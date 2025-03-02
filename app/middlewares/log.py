from typing import Any, Awaitable, Callable, Dict

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from utils.logging import logger


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message):
            logger.log(
                "MESSAGE", f"{event.from_user.id} ({event.from_user.username}): {event.text}"
            )

        elif isinstance(event, CallbackQuery):
            logger.log(
                "CALLBACK", f"{event.from_user.id} ({event.from_user.username}): {event.data}"
            )

        return await handler(event, data)
