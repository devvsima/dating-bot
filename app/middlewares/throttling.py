from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import current_handler
from aiogram.utils.exceptions import Throttled

from aiogram import types, Dispatcher
from typing import Union
import asyncio


class TrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix="antifood_"):
        self.limit = limit
        self.prefix = key_prefix
        super(TrottlingMiddleware, self).__init__()

    async def trottle(self, target: Union[types.Message, types.CallbackQuery]):
        handler = current_handler.get()
        if not handler:
            return
        dp = Dispatcher.get_current()
        limit = getattr(handler, "trottling_rate_limit", self.limit)
        key = getattr(handler, "trottling_key", f"{self.prefix}_{handler.__name__}")

        try:
            await dp.throttle(key, rate=limit)
        except Throttled as t:
            await self.target_throttled(target, t, dp, key)

    @staticmethod
    async def target_throttled(
        self,
        target: Union[types.Message, types.CallbackQuery],
        throttled: Throttled,
        dispather: Dispatcher,
        key: str,
    ):
        msg = target.message if isinstance(target, types.CallbackQuery) else target
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count == 2:
            await msg.reply("Слишком много запросов")
            return
        elif throttled.exceeded_count == 3:
            await msg.reply(f"Временно заблокирован на - {delta} секунд")
            return
        await asyncio.sleep(delta)
        thr = await dispather.check_key(key)
        if thr.exceeded_count == thr.exceeded_count:
            await msg.reply("Временная блокировка прошла")

    async def on_process_message(self, message, data):
        await self.throttle(message)

    async def on_process_callback_query(self, call, data):
        await self.throttle(call)
