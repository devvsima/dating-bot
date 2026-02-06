from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.business.create_profile_service import get_correct_description
from app.handlers.dating.profile import profile_command
from app.keyboards.default.registration_form import RegistrationFormKb
from app.routers import registration_router
from app.states.default import ProfileEdit
from app.text import message_text as mt
from database.models import UserModel
from database.services import Profile


@registration_router.message(StateFilter(None), F.text == "✍️")
async def _edit_profile_description_command(
    message: types.Message, state: FSMContext, user: UserModel
) -> None:
    """Редактирует описание пользователя"""
    await state.set_state(ProfileEdit.description)

    kb = RegistrationFormKb.description(user=user)
    await message.answer(text=mt.DESCRIPTION, reply_markup=kb)


@registration_router.message(StateFilter(ProfileEdit.description))
async def _update_description(
    message: types.Message, state: FSMContext, user: UserModel, session: AsyncSession
) -> None:
    """Обновляет описание профиля"""
    description = get_correct_description(message=message, user=user)
    await Profile.update(
        session=session,
        id=user.id,
        description=description,
    )
    await state.clear()
    await profile_command(message=message, user=user, session=session)
