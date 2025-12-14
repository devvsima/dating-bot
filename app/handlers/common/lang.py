from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.business.menu_service import menu
from app.handlers.common.start import start_command
from app.keyboards.inline.lang import LangCallback, lang_ikb
from app.routers import common_router
from app.text import message_text as mt
from database.models import UserModel
from database.services import User


@common_router.message(StateFilter("*"), Command("language"))
@common_router.message(StateFilter("*"), Command("lang"))
async def _lang(message: types.Message) -> None:
    """Отображает список доступных языков и позволяет выбрать предпочтительный"""
    await message.answer(mt.CHANGE_LANG, reply_markup=lang_ikb())


@common_router.callback_query(StateFilter("*"), LangCallback.filter())
async def _change_lang(
    callback: types.CallbackQuery,
    callback_data: LangCallback,
    user: UserModel,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """Обрабатывает выбранный пользователем язык, и устанавливает его"""
    language = callback_data.lang
    await User.update(
        session=session,
        id=user.id,
        language=language,
    )
    await callback.message.edit_text(mt.DONE_CHANGE_LANG(language))

    # > Нужно реализовать отправку на актуальном языке меню <
    # user = await User.get_with_profile(session, callback.from_user.id)
    # await start_command(callback.message, user, state)
