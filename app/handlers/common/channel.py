from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from app.routers import common_router
from app.text import message_text as mt
from data.config import BOT_CHANNEL_URL


@common_router.message(StateFilter("*"), Command("channel"))
async def channel_command(message: types.Message) -> None:
    """Отправляет ссылку на канал бота"""
    if url := BOT_CHANNEL_URL:
        await message.answer(mt.CHANNEL.format(url))
