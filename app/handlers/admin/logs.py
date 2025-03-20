from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.types import FSInputFile

from app.handlers.message_text import admin_message_text as amt
from app.routers import admin_router
from data.config import LOG_FILE_PATH


@admin_router.message(Command("log"), StateFilter(None))
@admin_router.message(Command("logs"), StateFilter(None))
async def _logs_command(message: types.Message) -> None:
    """Отправляет администратору последний файл логов бота"""
    await message.answer(amt.SENDING)
    await message.answer_document(document=FSInputFile(LOG_FILE_PATH))
