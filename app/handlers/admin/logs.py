from aiogram import F, types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.types import FSInputFile

from app.routers import admin_router
from data.config import LOG_FILE_PATH


@admin_router.message(StateFilter(None), Command("log"))
@admin_router.message(StateFilter(None), Command("logs"))
@admin_router.message(StateFilter(None), F.text == "📝 Logs")
async def _logs_command(message: types.Message) -> None:
    """Отправляет администратору последний файл логов бота"""
    await message.answer("Logs sending...")
    await message.answer_document(document=FSInputFile(LOG_FILE_PATH))
