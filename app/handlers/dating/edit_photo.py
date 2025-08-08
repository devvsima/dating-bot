from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

import app.filters.create_profile_filtres as filters
from app.handlers.dating.profile import profile_command
from app.keyboards.default.registration_form import RegistrationFormKb
from app.routers import dating_router
from app.states.default import ProfileEdit
from app.text import message_text as mt
from database.models import UserModel
from database.services.profile_media import ProfileMedia


@dating_router.message(StateFilter(None), F.text == "🖼")
async def _edit_profile_photo_command(
    message: types.Message, state: FSMContext, user: UserModel
) -> None:
    """Редактирует фотографию пользователя"""
    await state.set_state(ProfileEdit.photo)

    kb = RegistrationFormKb.photo(user)
    await message.answer(
        text=mt.PHOTO,
        reply_markup=kb,
    )


@dating_router.message(StateFilter(ProfileEdit.photo), filters.IsPhoto())
async def _update_photo(
    message: types.Message, state: FSMContext, user: UserModel, session: AsyncSession
) -> None:
    """Обновляет фотографию профиля"""
    if message.text in filters.leave_previous_tuple:
        # Пользователь хочет оставить текущее фото - ничего не делаем
        pass
    else:
        # Пользователь загрузил новое фото
        new_photo_url = message.photo[0].file_id

        # Удаляем все старые фото (но не видео)
        await ProfileMedia.delete_profile_photos(session, user.id)

        # Добавляем новое фото
        await ProfileMedia.add_media(
            session=session,
            profile_id=user.id,
            media_url=new_photo_url,
            media_type="photo",
            order=1,
        )

    await state.clear()
    await profile_command(message, user, session)
