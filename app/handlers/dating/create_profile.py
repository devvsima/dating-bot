from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

import app.filters.create_profile_filtres as filters
from app.keyboards.default.registration_form import RegistrationFormKb
from app.routers import registration_router
from app.services.create_profile_service import get_correct_description
from app.services.menu_service import menu
from app.states.default import ProfileCreate
from app.text import message_text as mt
from database.models import Profile, ProfileMedia
from database.models.user import User


@registration_router.message(StateFilter(None), F.text == "🔄")
@registration_router.message(StateFilter(None), filters.IsCreate())
async def _create_profile_command(message: types.Message, state: FSMContext, user: User):
    """Запускает процесс создания профиля пользователя.
    Также используется для пересоздания анкеты"""
    await state.set_state(ProfileCreate.name)

    kb = RegistrationFormKb.name(user)
    await message.answer(text=mt.NAME, reply_markup=kb)


# -< Name >-
@registration_router.message(StateFilter(ProfileCreate.name), F.text, filters.IsName())
async def _name(message: types.Message, state: FSMContext):
    await state.set_state(ProfileCreate.gender)
    await state.update_data(name=message.text)

    kb = RegistrationFormKb.gender()
    await message.answer(text=mt.GENDER, reply_markup=kb)


# -< Gender >-
@registration_router.message(StateFilter(ProfileCreate.gender), F.text, filters.IsGender())
async def _gender(message: types.Message, state: FSMContext, gender: str):
    await state.set_state(ProfileCreate.find_gender)
    await state.update_data(gender=gender)

    kb = RegistrationFormKb.find_gender()
    await message.answer(text=mt.FIND_GENDER, reply_markup=kb)


# -< Find gender >-
@registration_router.message(StateFilter(ProfileCreate.find_gender), F.text, filters.IsFindGender())
async def _find_gender(message: types.Message, state: FSMContext, find_gender: str, user: User):
    await state.set_state(ProfileCreate.city)
    await state.update_data(find_gender=find_gender)

    kb = RegistrationFormKb.city(user)
    await message.answer(text=mt.CITY, reply_markup=kb)


# -< City >-
@registration_router.message(StateFilter(ProfileCreate.city), F.text | F.location, filters.IsCity())
async def _city(
    message: types.Message,
    state: FSMContext,
    use_previous: bool,
    latitude: float | None,
    longitude: float | None,
    city: str | None,
    is_shared_location: bool | None,
    user: User,
):
    if use_previous:
        city = user.profile.city
        latitude = user.profile.latitude
        longitude = user.profile.longitude
        is_shared_location = user.profile.is_shared_location

    # Переходим к следующему шагу
    await state.set_state(ProfileCreate.age)
    await state.update_data(
        city=city,
        latitude=latitude,
        longitude=longitude,
        is_shared_location=is_shared_location,
    )

    kb = RegistrationFormKb.age(user)
    await message.answer(text=mt.AGE, reply_markup=kb)


# -< Age >-
@registration_router.message(StateFilter(ProfileCreate.age), F.text, filters.IsAge())
async def _age(message: types.Message, state: FSMContext, user: User):
    await state.set_state(ProfileCreate.photo)
    await state.update_data(age=message.text)

    await state.update_data(photos=[])
    kb = RegistrationFormKb.photo(user)
    await message.answer(text=mt.PHOTO, reply_markup=kb)


# -< Photo >-
@registration_router.message(StateFilter(ProfileCreate.photo), filters.IsPhoto())
async def _photo(message: types.Message, state: FSMContext, user: User, session: AsyncSession):
    data = await state.get_data()
    photos = data.get("photos", [])

    if message.text in filters.LEAVE_PREVIOUS_OPTIONS:
        # Получаем существующие фото из профиля пользователя
        existing_photos = await ProfileMedia.get_profile_media(session, user.id)
        if existing_photos:
            photos = [photo.media for photo in existing_photos]
            await state.update_data(photos=photos)

        # Переходим к описанию
        kb = RegistrationFormKb.description(user)
        await message.answer(text=mt.DESCRIPTION, reply_markup=kb)
        await state.set_state(ProfileCreate.description)
        return

    elif message.text == mt.PHOTO_SAVE_FINISH_BUTTON:
        if not photos:
            await message.answer(mt.PHOTO_NO_UPLOADED)
            return

        # Обновляем данные состояния с текущими фото
        await state.update_data(photos=photos)

        # Переходим к описанию
        kb = RegistrationFormKb.description(user)
        await message.answer(text=mt.DESCRIPTION, reply_markup=kb)
        await state.set_state(ProfileCreate.description)
        return

    elif message.photo:
        # Проверяем лимит фотографий
        if len(photos) >= 3:
            await message.answer(mt.PHOTO_LIMIT_REACHED)
            return

        new_photo = message.photo[-1].file_id
        photos.append(new_photo)
        await state.update_data(photos=photos)

        new_count = len(photos)

        if new_count < 3:
            await message.answer(
                text=mt.PHOTO_PROGRESS(current=new_count),
                reply_markup=RegistrationFormKb.photo_add(),
            )
        else:
            # Загружены все 3 фото - переходим к описанию
            await message.answer(mt.PHOTO_ALL_UPLOADED())

            kb = RegistrationFormKb.description(user)
            await message.answer(text=mt.DESCRIPTION, reply_markup=kb)
            await state.set_state(ProfileCreate.description)
    else:
        await message.answer(mt.PHOTO_UPLOAD_INSTRUCTION)


# -< Description >-
@registration_router.message(
    StateFilter(ProfileCreate.description), F.text, filters.IsDescription()
)
async def _description(
    message: types.Message, state: FSMContext, user: User, session: AsyncSession
):
    data = await state.get_data()
    photos = data.get("photos", [])

    await state.clear()
    description = get_correct_description(message=message, user=user)
    await Profile.create_or_update(
        session=session,
        id=message.from_user.id,
        gender=data["gender"],
        find_gender=data["find_gender"],
        photos=photos,
        name=data["name"],
        age=int(data["age"]),
        city=data["city"],
        latitude=float(data["latitude"]),
        longitude=float(data["longitude"]),
        is_shared_location=bool(data["is_shared_location"]),
        description=description,
    )

    await message.answer(mt.PROFILE_CREATED)
    await menu(chat_id=user.id)

    # -< OLD >-

    # 1. -< Gender >-
    # 2. -< Find gender >-
    # 3. -< Photo >-
    # 4. -< Name >-
    # 5. -< Age >-
    # 6. -< City >-
    # 7. -< Description >-

    # -< NEW >-

    # 1. -< Name >-
    # 2. -< Gender >-
    # 3. -< Find gender >-
    # 4. -< City >-
    # 5. -< Age >-
    # 6. -< Photo >-
    # 7. -< Description >-
