from aiogram import types
from aiogram.filters import CommandStart
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.business.menu_service import menu
from app.keyboards.default.registration_form import create_profile_kb
from app.routers import common_router
from app.text import message_text as mt
from data.config import LOGO_DIR
from database.models import UserModel


@common_router.message(StateFilter("*"), CommandStart())
async def _start_command(message: types.Message, user: UserModel, state: FSMContext) -> None:
    """
    Команда /start запускает бота и возвращает пользователя в начальное меню.
    Сброс состояния помогает, если пользователь запутался — всегда можно начать сначала.
    """
    await state.clear()

    if user.profile:
        await menu(user.id)
    else:
        photo = types.FSInputFile(LOGO_DIR)
        await message.answer_photo(
            photo=photo,
            caption=mt.WELCOME,
            reply_markup=create_profile_kb(),
        )
