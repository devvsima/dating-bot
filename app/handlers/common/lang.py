from aiogram import types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from app.handlers.message_text import user_message_text as umt
from app.keyboards.inline.lang import LangCallback, lang_ikb
from app.routers import common_router
from database.models import UserModel
from database.services import User


@common_router.message(StateFilter(None), Command("language"))
@common_router.message(StateFilter(None), Command("lang"))
async def _lang(message: types.Message) -> None:
    """Отображает список доступных языков и позволяет выбрать предпочтительный"""
    await message.answer(umt.CHANGE_LANG, reply_markup=lang_ikb())


@common_router.callback_query(StateFilter(None), LangCallback.filter())
async def _change_lang(
    callback: types.CallbackQuery, callback_data: LangCallback, user: UserModel, session
) -> None:
    """Обрабатывает выбранный пользователем язык, и устанавливает его"""
    language = callback_data.lang
    await User.update(
        session=session,
        id=user.id,
        language=language,
    )
    await callback.message.edit_text(umt.DONE_CHANGE_LANG(language))
