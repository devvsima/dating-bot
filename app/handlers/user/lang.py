from aiogram import F, types
from aiogram.filters import Command

from loader import _

from app.routers import user_router as router

from database.service.users import change_language
    
from app.keyboards.inline.lang import lang_ikb


@router.message(Command('language'))
@router.message(Command('lang'))
async def _lang(message: types.Message) -> None:
    """Предлагает клавиатуру с доступными языками"""
    await message.answer(_("Select the language you want to switch"), reply_markup=lang_ikb())


@router.callback_query(F.data.in_(['ru', 'uk', 'en']))
async def _lang_change(callback: types.CallbackQuery) -> None:
    """Меняет язык пользователя на выбранный"""
    change_language(callback.from_user.id, callback.data)
    await callback.message.edit_text(_("Language changed"))
