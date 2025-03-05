from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.types import FSInputFile

from app.keyboards.default.admin import admin_menu_kb
from app.routers import admin_router as router
from data.config import DIR

LOG_FILE_DIR = f"{DIR}/logs/logs.log"


@router.message(Command("logs"), StateFilter(None))
async def _logs_command(message: types.Message) -> None:
    """Отправляет администратору последний файл логов бота"""
    await message.answer_document(
        document=FSInputFile(LOG_FILE_DIR),
        reply_markup=admin_menu_kb(),
    )
