from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

import app.filters.create_profile_filtres as filters
from app.handlers.msg_text import msg_text
from app.handlers.user.profile import profile_command
from app.keyboards.default.base import hints_kb, leave_previous_kb
from app.keyboards.default.create_profile import find_gender_kb, gender_kb
from app.others.states import ProfileCreate, ProfileEdit
from app.routers import user_router as router
from database.models.user import UserModel
from database.services import Profile


# create profile
@router.message(F.text == "🔄", StateFilter(None))
@router.message(filters.IsCreate(), StateFilter(None))
async def _create_profile_command(message: types.Message, state: FSMContext):
    """Начало создание профиля"""
    await message.answer(msg_text.GENDER, reply_markup=gender_kb())

    await state.set_state(ProfileCreate.gender)


# < gender >
@router.message(filters.IsGender(), StateFilter(ProfileCreate.gender))
async def _gender(message: types.Message, state: FSMContext, gender: str):
    await state.update_data(gender=gender)
    await message.reply(msg_text.FIND_GENDER, reply_markup=find_gender_kb())
    await state.set_state(ProfileCreate.find_gender)


@router.message(StateFilter(ProfileCreate.gender))
async def _incorrect_gender(message: types.Message):
    """Ошибка фильтра гендера"""
    await message.answer(msg_text.INVALID_RESPONSE)


# < find gender >
@router.message(filters.IsFindGender(), StateFilter(ProfileCreate.find_gender))
async def _find_gender(
    message: types.Message, state: FSMContext, find_gender: str, user: UserModel
):
    await state.update_data(find_gender=find_gender)

    await message.reply(msg_text.PHOTO, reply_markup=leave_previous_kb(user.profile))
    await state.set_state(ProfileCreate.photo)


@router.message(StateFilter(ProfileCreate.find_gender))
async def _incorrect_find_gender(message: types.Message):
    """Ошибка фильтра гендера"""
    await message.answer(msg_text.INVALID_RESPONSE)


# < photo >
@router.message(filters.IsPhoto(), StateFilter(ProfileCreate.photo, ProfileEdit.photo))
async def _photo(message: types.Message, state: FSMContext, user: UserModel, session):
    if await state.get_state() == ProfileEdit.photo.state:
        await Profile.update_photo(session, user.profile, photo)
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
    await message.reply(msg_text.NAME, reply_markup=kb)
    await state.set_state(ProfileCreate.name)


@router.message(StateFilter(ProfileEdit.photo))
async def _incorrect_photo(message: types.Message):
    """Ошибка фильтра фотографии"""
    await message.answer(msg_text.INVALID_PHOTO)


# < name >
@router.message(filters.IsName(), StateFilter(ProfileCreate.name))
async def _name(message: types.Message, state: FSMContext, user):
    await state.update_data(name=message.text)

    kb = hints_kb(str(user.profile.age)) if user.profile else None

    await message.reply(msg_text.AGE, reply_markup=kb)
    await state.set_state(ProfileCreate.age)


@router.message(StateFilter(ProfileCreate.name))
async def _incorrect_name(message: types.Message):
    """Ошибка фильтра имени"""
    await message.answer(msg_text.INVALID_LONG_RESPONSE)


# < age >
@router.message(filters.IsAge(), StateFilter(ProfileCreate.age))
async def _age(message: types.Message, state: FSMContext, user: UserModel):
    await state.update_data(age=message.text)

    kb = hints_kb(user.profile.city) if user.profile else None

    await message.reply(msg_text.CITY, reply_markup=kb)
    await state.set_state(ProfileCreate.city)


@router.message(StateFilter(ProfileCreate.age))
async def _incorrect_age(message: types.Message):
    """Ошибка фильтра возраста"""
    await message.answer(msg_text.INVALID_AGE)


# < city >
@router.message(filters.IsCity(), StateFilter(ProfileCreate.city))
async def _city(message: types.Message, state: FSMContext, coordinates: dict, user: UserModel):
    await state.update_data(
        city=message.text,
        latitude=coordinates[0],
        longitude=coordinates[1],
    )
    await message.reply(msg_text.DESCRIPTION, reply_markup=leave_previous_kb(user.profile))
    await state.set_state(ProfileCreate.desc)


@router.message(StateFilter(ProfileCreate.city))
async def _incorrect_city(message: types.Message):
    """Ошибка фильтра города"""
    await message.answer(msg_text.INVALID_LONG_RESPONSE)


# < description >
@router.message(filters.IsDescription(), StateFilter(ProfileCreate.desc, ProfileEdit.desc))
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


@router.message(StateFilter(ProfileCreate.desc, ProfileEdit.desc))
async def _incorrect_description(message: types.Message):
    """Ошибка фильтра описания"""
    await message.answer(msg_text.INVALID_LONG_RESPONSE)
