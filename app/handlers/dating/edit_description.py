from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.handlers.dating.profile import profile_command
from app.keyboards.default.registration_form import RegistrationFormKb
from app.routers import dating_router
from app.states.default import ProfileEdit
from app.text import message_text as mt
from database.models import UserModel
from database.services import Profile


@dating_router.message(StateFilter(None), F.text == "✍️")
async def _edit_profile_description_command(
    message: types.Message, state: FSMContext, user: UserModel
) -> None:
    """Редактирует описание пользователя"""
    await state.set_state(ProfileEdit.description)

    kb = RegistrationFormKb.description(user)

    await message.answer(text=mt.DESCRIPTION, reply_markup=kb)


@dating_router.message(StateFilter(ProfileEdit.description))
async def _update_photo(
    message: types.Message, state: FSMContext, user: UserModel, session: AsyncSession
) -> None:
    """Обновляет описание профиля"""
    await Profile.update(
        session=session,
        id=user.id,
        description=message.text,
    )
    await state.clear()
    await profile_command(message, user)
