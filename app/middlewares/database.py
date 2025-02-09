from typing import Any

from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(self, handler, event, data) -> Any:
        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)
