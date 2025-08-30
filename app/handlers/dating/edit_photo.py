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
from database.models.profile_media import MediaTypes
from database.services.profile_media import ProfileMedia


@dating_router.message(StateFilter(None), F.text == "🖼")
async def _edit_profile_photo_command(
    message: types.Message, state: FSMContext, user: UserModel
) -> None:
    """Редактирует фотографию пользователя"""
    await state.set_state(ProfileEdit.photo)

    # Инициализируем состояние
    await state.update_data(
        photos=[],
        photo_count=0,
    )

    kb = RegistrationFormKb.photo(user)
    await message.answer(text=mt.PHOTO_EDIT_START, reply_markup=kb)


@dating_router.message(StateFilter(ProfileEdit.photo), filters.IsPhoto())
async def _update_photo(
    message: types.Message, state: FSMContext, user: UserModel, session: AsyncSession
) -> None:
    """Обрабатывает загрузку фотографий"""
    data = await state.get_data()
    photos = data.get("photos", [])

    if message.text in filters.LEAVE_PREVIOUS_OPTIONS:
        # Пользователь хочет оставить текущие фото - завершаем без изменений
        await state.clear()
        await message.answer(mt.PHOTO_UNCHANGED)
        await profile_command(message, user, session)
        return

    elif message.text == mt.PHOTO_SAVE_FINISH_BUTTON:
        if not photos:
            await message.answer(mt.PHOTO_NO_UPLOADED)
            return

        try:
            await ProfileMedia.delete_profile_photos(session, user.id)
            for i, photo_file_id in enumerate(photos, 1):
                await ProfileMedia.add_media(
                    session=session,
                    profile_id=user.id,
                    media_url=photo_file_id,
                    media_type=MediaTypes.Photo,
                    order=i,
                )

            await state.clear()

            await message.answer(mt.PHOTO_SAVED(len(photos)))
            await profile_command(message, user, session)

        except Exception as e:
            await session.rollback()
            await message.answer(mt.PHOTO_SAVE_ERROR)
            print(f"Error saving photos: {e}")

        return

    elif message.photo:
        # Проверяем лимит фотографий
        if len(photos) >= 3:
            await message.answer("❌ Максимум 3 фото! Ваши фото уже сохранены.")
            return

        # Добавляем новое фото в список
        new_photo = message.photo[-1].file_id  # Берем фото лучшего качества
        photos.append(new_photo)

        await state.update_data(photos=photos)

        # Обновляем счетчик и отправляем сообщение
        new_count = len(photos)
        remaining = 3 - new_count

        if remaining > 0:
            await message.answer(
                text=mt.PHOTO_PROGRESS(new_count), reply_markup=RegistrationFormKb.photo_add()
            )
        else:
            # Загружены все 3 фото - автоматически сохраняем
            try:
                await ProfileMedia.delete_profile_photos(session, user.id)
                for i, photo_file_id in enumerate(photos, 1):
                    await ProfileMedia.add_media(
                        session=session,
                        profile_id=user.id,
                        media_url=photo_file_id,
                        media_type=MediaTypes.Photo,
                        order=i,
                    )

                await state.clear()

                await message.answer(mt.PHOTO_ALL_UPLOADED())
                await profile_command(message, user, session)

            except Exception as e:
                await session.rollback()
                await message.answer(mt.PHOTO_SAVE_ERROR)
                print(f"Error saving photos: {e}")
