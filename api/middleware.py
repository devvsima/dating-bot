"""
Middleware для проверки подписи Telegram WebApp initData
"""

import hashlib
import hmac
from urllib.parse import parse_qsl

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware

from core.config import tgbot


class TelegramWebAppMiddleware(BaseHTTPMiddleware):
    """
    Middleware для проверки подлинности запросов от Telegram WebApp.

    Поддерживает два типа аутентификации:
    1. Authorization: tma <initData> - проверка подписи Telegram WebApp
    2. Authorization: Bearer <access_token> - токен доступа для тестирования
    """

    def __init__(self, app, bot_token: str, access_token: str | None = None):
        super().__init__(app)
        self.bot_token = bot_token
        self.access_token = access_token

    async def dispatch(self, request: Request, call_next):
        # Пропускаем OPTIONS запросы (для CORS)
        if request.method == "OPTIONS":
            return await call_next(request)

        # Пропускаем корневой путь и документацию
        if request.url.path in ["/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Получаем Authorization заголовок
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing authorization header. Use 'Authorization: tma <initData>' or 'Authorization: Bearer <token>'",
            )

        # Проверяем тип аутентификации
        if auth_header.startswith("Bearer "):
            # Токен доступа для тестирования
            token = auth_header[7:]
            if not self.access_token or token != self.access_token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid access token",
                )
        elif auth_header.startswith("tma "):
            # Telegram WebApp подпись
            init_data = auth_header[4:]
            if not self._validate_init_data(init_data):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Telegram WebApp signature",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format. Use 'Authorization: tma <initData>' or 'Authorization: Bearer <token>'",
            )

        # Продолжаем обработку запроса
        response = await call_next(request)
        return response

    def _validate_init_data(self, init_data: str) -> bool:
        """
        Проверяет подпись initData от Telegram WebApp.

        Алгоритм проверки согласно документации Telegram:
        https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app

        Args:
            init_data: Строка с данными от Telegram WebApp

        Returns:
            True если подпись валидна, False если нет
        """
        try:
            # Парсим initData
            parsed_data = dict(parse_qsl(init_data))

            # Извлекаем hash из данных
            received_hash = parsed_data.pop("hash", None)
            if not received_hash:
                return False

            # Создаем data_check_string из оставшихся данных
            # Сортируем ключи в алфавитном порядке
            data_check_arr = [f"{k}={v}" for k, v in sorted(parsed_data.items())]
            data_check_string = "\n".join(data_check_arr)

            # Создаем secret_key используя HMAC-SHA256 с "WebAppData" и bot_token
            secret_key = hmac.new(
                key="WebAppData".encode(),
                msg=self.bot_token.encode(),
                digestmod=hashlib.sha256,
            ).digest()

            # Вычисляем hash используя secret_key и data_check_string
            calculated_hash = hmac.new(
                key=secret_key,
                msg=data_check_string.encode(),
                digestmod=hashlib.sha256,
            ).hexdigest()

            # Сравниваем полученный hash с вычисленным
            return hmac.compare_digest(received_hash, calculated_hash)

        except Exception as e:
            print(f"Error validating init data: {e}")
            return False


def get_user_id_from_init_data(init_data: str) -> int | None:
    """
    Извлекает user_id из initData.

    Args:
        init_data: Строка с данными от Telegram WebApp

    Returns:
        ID пользователя или None
    """
    try:
        import json

        parsed_data = dict(parse_qsl(init_data))
        user_data = json.loads(parsed_data.get("user", "{}"))
        return user_data.get("id")
    except Exception:
        return None
