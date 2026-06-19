from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from app.keyboards.inline.help import help_ikb
from app.routers import common_router
from app.text import message_text as mt
from core.config import get_logo
from database.models import User


@common_router.message(StateFilter(None), Command("info"))
@common_router.message(StateFilter(None), Command("help"))
async def _help_command(message: types.Message, user: User) -> None:
    """Отправляет пользователю небольшое описание бота"""
    await message.answer_photo(
        photo=get_logo(),
        caption=mt.INFO,
        reply_markup=help_ikb(user.language),
    )
