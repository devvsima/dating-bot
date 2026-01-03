import asyncio
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from app.text import message_text as mt
from data.config import tgbot

rate_limit: int = tgbot.RATE_LIMIT
time_window: int = tgbot.TIME_WINDOW


class ThrottlingMiddleware(BaseMiddleware):
    """
    Middleware для защиты от спама.
    Ограничивает количество запросов от пользователя.
    """

    def __init__(self):
        """
        Args:
            rate_limit: Количество разрешенных запросов
            time_window: Временное окно в секундах
        """
        self.rate_limit = rate_limit
        self.time_window = timedelta(seconds=time_window)
        # Словарь для хранения последних запросов: {user_id: [timestamp1, timestamp2, ...]}
        self.user_requests = defaultdict(list)
        self.last_cleanup = datetime.now()
        self.cleanup_interval = timedelta(minutes=5)  # Очистка каждые 5 минут
        super().__init__()

    def _cleanup_old_users(self, now: datetime) -> None:
        """Удаляет записи неактивных пользователей"""
        if now - self.last_cleanup < self.cleanup_interval:
            return

        # Удаляем пользователей без активных запросов
        users_to_delete = []
        for user_id, requests in self.user_requests.items():
            # Удаляем старые запросы
            requests[:] = [req_time for req_time in requests if now - req_time < self.time_window]
            # Если запросов не осталось, помечаем пользователя для удаления
            if not requests:
                users_to_delete.append(user_id)

        # Удаляем неактивных пользователей
        for user_id in users_to_delete:
            del self.user_requests[user_id]

        self.last_cleanup = now

    async def __call__(
        self,
        handler: Callable,
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        now = datetime.now()

        # Периодическая очистка неактивных пользователей
        self._cleanup_old_users(now)

        # Получаем список запросов пользователя
        requests = self.user_requests[user_id]

        # Удаляем старые запросы за пределами временного окна
        requests[:] = [req_time for req_time in requests if now - req_time < self.time_window]

        # Проверяем лимит
        if len(requests) >= self.rate_limit:
            # Вычисляем время ожидания до следующего доступного запроса
            oldest_request = min(requests)
            wait_time = (oldest_request + self.time_window - now).total_seconds()

            if wait_time > 0:
                # Отправляем предупреждение
                if isinstance(event, Message):
                    await event.answer(mt.RATE_LIMIT_MESSAGE)

                # Ждем и затем обрабатываем запрос
                await asyncio.sleep(wait_time)

                # Обновляем время для корректной обработки после ожидания
                now = datetime.now()
                requests[:] = [
                    req_time for req_time in requests if now - req_time < self.time_window
                ]

        # Добавляем текущий запрос
        requests.append(now)

        # Продолжаем обработку
        return await handler(event, data)
