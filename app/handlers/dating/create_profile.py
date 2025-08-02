from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

import app.filters.create_profile_filtres as filters
from app.business.menu_service import menu
from app.keyboards.default.registration_form import RegistrationFormKb
from app.routers import dating_router
from app.states.default import ProfileCreate
from app.text import message_text as mt
from database.models.user import UserModel
from database.services import Profile
from database.services.profile_media import ProfileMedia

from .profile import profile_command


# -< Create profile >-
@dating_router.message(StateFilter(None), F.text == "🔄")
@dating_router.message(StateFilter(None), filters.IsCreate())
async def _create_profile_command(message: types.Message, state: FSMContext, user: UserModel):
    """Запускает процесс создания профиля пользователя.
    Также используется для пересоздания анкеты"""
    await state.set_state(ProfileCreate.name)

    kb = RegistrationFormKb.name(user)
    await message.answer(text=mt.NAME, reply_markup=kb)


# -< Name >-
@dating_router.message(StateFilter(ProfileCreate.name), F.text, filters.IsName())
async def _name(message: types.Message, state: FSMContext):
    await state.set_state(ProfileCreate.gender)
    await state.update_data(name=message.text)

    kb = RegistrationFormKb.gender()
    await message.answer(text=mt.GENDER, reply_markup=kb)


# -< Gender >-
@dating_router.message(StateFilter(ProfileCreate.gender), F.text, filters.IsGender())
async def _gender(message: types.Message, state: FSMContext, gender: str):
    await state.set_state(ProfileCreate.find_gender)
    await state.update_data(gender=gender)

    kb = RegistrationFormKb.find_gender()
    await message.answer(text=mt.FIND_GENDER, reply_markup=kb)


# -< Find gender >-
@dating_router.message(StateFilter(ProfileCreate.find_gender), F.text, filters.IsFindGender())
async def _find_gender(
    message: types.Message, state: FSMContext, find_gender: str, user: UserModel
):
    await state.set_state(ProfileCreate.city)
    await state.update_data(find_gender=find_gender)

    kb = RegistrationFormKb.city(user)
    await message.answer(text=mt.CITY, reply_markup=kb)


# -< City >-
@dating_router.message(StateFilter(ProfileCreate.city), F.text | F.location, filters.IsCity())
async def _city(
    message: types.Message, state: FSMContext, latitude: str, longitude: str, user: UserModel
):
    if not (latitude or longitude):
        city = user.profile.city
        latitude = user.profile.latitude
        longitude = user.profile.longitude
    else:
        city = message.text if message.text else "📍"

    await state.set_state(ProfileCreate.age)
    await state.update_data(
        city=city,
        latitude=latitude,
        longitude=longitude,
    )

    kb = RegistrationFormKb.age(user)
    await message.answer(text=mt.AGE, reply_markup=kb)


# -< Age >-
@dating_router.message(StateFilter(ProfileCreate.age), F.text, filters.IsAge())
async def _age(message: types.Message, state: FSMContext, user: UserModel):
    await state.set_state(ProfileCreate.photo)
    await state.update_data(age=message.text)

    kb = RegistrationFormKb.photo(user)
    await message.answer(text=mt.PHOTO, reply_markup=kb)


# -< Photo >-
@dating_router.message(StateFilter(ProfileCreate.photo), filters.IsPhoto())
async def _photo(message: types.Message, state: FSMContext, user: UserModel, session):
    if message.text in filters.leave_previous_tuple:
        # Получаем первое фото из профиля пользователя
        first_photo = await ProfileMedia.get_first_photo(session, user.id)
        photo = first_photo.media if first_photo else None
    else:
        # Новое фото от пользователя
        photo = message.photo[0].file_id

    await state.update_data(photo=photo)

    kb = RegistrationFormKb.description(user)

    await message.answer(
        text=mt.DESCRIPTION,
        reply_markup=kb,
    )
    await state.set_state(ProfileCreate.description)


# -< Description >-
@dating_router.message(StateFilter(ProfileCreate.description), F.text, filters.IsDescription())
async def _description(message: types.Message, state: FSMContext, user: UserModel, session):
    data = await state.get_data()
    description = (
        user.profile.description if message.text in filters.leave_previous_tuple else message.text
    )

    await Profile.create_or_update(
        session=session,
        id=message.from_user.id,
        gender=data["gender"],
        find_gender=data["find_gender"],
        photo=data["photo"],  # Это будет обработано отдельно в сервисе
        name=data["name"],
        age=int(data["age"]),
        city=data["city"],
        latitude=float(data["latitude"]),
        longitude=float(data["longitude"]),
        description=description,
    )

    await state.clear()
    await session.refresh(user)
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
