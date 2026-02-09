"""
API endpoints для работы с медиафайлами
Прокси для изображений из Telegram API
"""

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from core.config import tgbot

router = APIRouter()

BOT_TOKEN = tgbot.BOT_TOKEN


@router.get("/photo/{file_id}")
async def get_photo(file_id: str):
    """
    Проксирование фотографии из Telegram API

    Этот endpoint скрывает токен бота от клиентов,
    получая изображение от Telegram и отдавая его клиенту

    Args:
        file_id: ID файла в Telegram

    Returns:
        Изображение в формате JPEG
    """

    async with httpx.AsyncClient() as client:
        file_response = await client.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile", params={"file_id": file_id}
        )
        file_data = file_response.json()

        if not file_data.get("ok"):
            raise HTTPException(status_code=404, detail="Файл не найден в Telegram")

        file_path = file_data["result"]["file_path"]

        # Получаем само изображение
        photo_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        photo_response = await client.get(photo_url)

        if photo_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Не удалось загрузить изображение")

        return StreamingResponse(
            iter([photo_response.content]),
            media_type="image/jpeg",
            headers={
                "Cache-Control": "public, max-age=86400",  # Кеш на 24 часа
            },
        )
