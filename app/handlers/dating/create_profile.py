from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

import app.filters.create_profile_filtres as filters
from app.handlers.message_text import user_message_text as umt
from app.keyboards.default.base import hints_kb, leave_previous_kb
from app.keyboards.default.create_profile import find_gender_kb, gender_kb, location_kb
from app.others.states import ProfileCreate, ProfileEdit
from app.routers import dating_router
from database.models.user import UserModel
from database.services import Profile

from .profile import profile_command


# create profile
@dating_router.message(F.text == "🔄", StateFilter(None))
@dating_router.message(filters.IsCreate(), StateFilter(None))
async def _create_profile_command(message: types.Message, state: FSMContext):
    """Запускает процесс создания профиля пользователя.
    Также используется для пересоздания анкеты"""
    await message.answer(umt.GENDER, reply_markup=gender_kb())
    await state.set_state(ProfileCreate.gender)


# < gender >
@dating_router.message(StateFilter(ProfileCreate.gender), F.text, filters.IsGender())
async def _gender(message: types.Message, state: FSMContext, gender: str):
    await state.update_data(gender=gender)
    await message.reply(umt.FIND_GENDER, reply_markup=find_gender_kb())
    await state.set_state(ProfileCreate.find_gender)


@dating_router.message(StateFilter(ProfileCreate.gender))
async def _incorrect_gender(message: types.Message):
    """Ошибка фильтра гендера"""
    await message.answer(umt.INVALID_RESPONSE)


# < find gender >
@dating_router.message(StateFilter(ProfileCreate.find_gender), F.text, filters.IsFindGender())
async def _find_gender(
    message: types.Message, state: FSMContext, find_gender: str, user: UserModel
):
    await state.update_data(find_gender=find_gender)

    await message.reply(umt.PHOTO, reply_markup=leave_previous_kb(user.profile))
    await state.set_state(ProfileCreate.photo)


@dating_router.message(StateFilter(ProfileCreate.find_gender))
async def _incorrect_find_gender(message: types.Message):
    """Ошибка фильтра гендера"""
    await message.answer(umt.INVALID_RESPONSE)


# < photo >
@dating_router.message(StateFilter(ProfileCreate.photo, ProfileEdit.photo), filters.IsPhoto())
async def _photo(message: types.Message, state: FSMContext, user: UserModel, session):
    if await state.get_state() == ProfileEdit.photo.state:
        await Profile.update_photo(session, user.profile, message.photo[0].file_id)
        await profile_command(message, user)
        await state.clear()
        return

    photo = (
        user.profile.photo
        if message.text in filters.leave_previous_tuple
        else message.photo[0].file_id
    )
    kb = hints_kb(user.profile.name) if user.profile else None

    await state.update_data(photo=photo)
    await message.reply(umt.NAME, reply_markup=kb)
    await state.set_state(ProfileCreate.name)


@dating_router.message(StateFilter(ProfileCreate.photo, ProfileEdit.photo))
async def _incorrect_photo(message: types.Message):
    """Ошибка фильтра фото"""
    await message.answer(umt.INVALID_PHOTO)


# < name >
@dating_router.message(StateFilter(ProfileCreate.name), F.text, filters.IsName())
async def _name(message: types.Message, state: FSMContext, user: UserModel):
    await state.update_data(name=message.text)

    kb = hints_kb(str(user.profile.age)) if user.profile else None

    await message.reply(umt.AGE, reply_markup=kb)
    await state.set_state(ProfileCreate.age)


@dating_router.message(StateFilter(ProfileCreate.name))
async def _incorrect_name(message: types.Message):
    """Ошибка фильтра имени"""
    await message.answer(umt.INVALID_LONG_RESPONSE)


# < age >
@dating_router.message(StateFilter(ProfileCreate.age), F.text, filters.IsAge())
async def _age(message: types.Message, state: FSMContext, user: UserModel):
    await state.update_data(age=message.text)
    await message.reply(umt.CITY, reply_markup=location_kb(user.profile))
    await state.set_state(ProfileCreate.city)


@dating_router.message(StateFilter(ProfileCreate.age))
async def _incorrect_age(message: types.Message):
    """Ошибка фильтра возраста"""
    await message.answer(umt.INVALID_AGE)


# < city >
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

    await state.update_data(
        city=city,
        latitude=latitude,
        longitude=longitude,
    )
    await message.reply(umt.DESCRIPTION, reply_markup=leave_previous_kb(user.profile))
    await state.set_state(ProfileCreate.desc)


@dating_router.message(StateFilter(ProfileCreate.city))
async def _incorrect_city(message: types.Message):
    """Ошибка фильтра города"""
    await message.answer(umt.INVALID_CITY_RESPONSE)


# < description >
@dating_router.message(
    StateFilter(ProfileCreate.desc, ProfileEdit.desc), F.text, filters.IsDescription()
)
async def _description(message: types.Message, state: FSMContext, user: UserModel, session):
    if await state.get_state() == ProfileEdit.desc.state:
        await Profile.update_description(session, user.profile, message.text)
    else:
        data = await state.get_data()
        description = (
            user.profile.description
            if message.text in filters.leave_previous_tuple
            else message.text
        )

        await Profile.create(
            session=session,
            user_id=message.from_user.id,
            gender=data["gender"],
            find_gender=data["find_gender"],
            photo=data["photo"],
            name=data["name"],
            age=int(data["age"]),
            city=data["city"],
            latitude=float(data["latitude"]),
            longitude=float(data["longitude"]),
            description=description,
        )

    await state.clear()
    await session.refresh(user)
    await profile_command(message, user)


@dating_router.message(StateFilter(ProfileCreate.desc, ProfileEdit.desc))
async def _incorrect_description(message: types.Message):
    """Ошибка фильтра описания"""
    await message.answer(umt.INVALID_LONG_RESPONSE)
