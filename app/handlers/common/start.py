from aiogram import F, types
from aiogram.filters import Command, CommandStart
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.keyboards.default.registration_form import create_profile_kb
from app.routers import common_router
from app.services.menu_service import menu
from app.text import message_text as mt
from core.config import LOGO
from database.models import User


@common_router.message(StateFilter("*"), F.text == "💤")
@common_router.message(StateFilter("*"), Command("cancel"))
@common_router.message(StateFilter("*"), CommandStart())
async def start_command(message: types.Message, user: User, state: FSMContext) -> None:
    """
    Команда /start запускает бота и возвращает пользователя в начальное меню.
    Сброс состояния помогает, если пользователь запутался — всегда можно начать сначала.
    """
    await state.clear()

    if user.profile:
        await menu(user.id)
    else:
        await message.answer_photo(
            photo=LOGO,
            caption=mt.WELCOME,
            reply_markup=create_profile_kb(),
        )
