from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

import app.filters.create_profile_filtres as filters
from app.handlers.msg_text import msg_text
from app.handlers.user.profile import profile_command
from app.keyboards.default.base import del_kb
from app.keyboards.default.create_profile import find_gender_kb, gender_kb
from app.others.states import ProfileCreate, ProfileEdit
from app.routers import user_router as router
from database.services import Profile


# create profile
@router.message(F.text == "🔄", StateFilter(None))
@router.message(filters.IsCreate(), StateFilter(None))
async def _create_profile_command(message: types.Message, state: FSMContext):
    """Начало создание профиля"""
    await message.answer(msg_text.GENDER, reply_markup=gender_kb())

    await state.set_state(ProfileCreate.gender)


# < gender >
@router.message(ProfileCreate.gender, filters.IsGender())
async def _gender(message: types.Message, state: FSMContext, gender: str):
    await state.update_data(gender=gender)
    await message.reply(msg_text.FIND_GENDER, reply_markup=find_gender_kb())
    await state.set_state(ProfileCreate.find_gender)


@router.message(ProfileCreate.gender)
async def _incorrect_gender(message: types.Message):
    """Ошибка фильтра гендера"""
    await message.answer(msg_text.INVALID_RESPONSE)


# < find gender >
@router.message(ProfileCreate.find_gender, filters.IsFindGender())
async def _find_gender(message: types.Message, state: FSMContext, find_gender: str):
    await state.update_data(find_gender=find_gender)
    await message.reply(msg_text.PHOTO, reply_markup=del_kb)
    await state.set_state(ProfileCreate.photo)


@router.message(ProfileCreate.find_gender)
async def _incorrect_find_gender(message: types.Message):
    """Ошибка фильтра гендера"""
    await message.answer(msg_text.INVALID_RESPONSE)


# < photo >
@router.message(StateFilter(ProfileCreate.photo, ProfileEdit.photo), filters.IsPhoto())
async def _photo(message: types.Message, state: FSMContext, session):
    photo = message.photo[0].file_id
    if await state.get_state() == ProfileEdit.photo.state:
        await Profile.update_photo(session, message.from_user.id, photo)
        await profile_command(message, session)
        await state.clear()
        return

    await state.update_data(photo=photo)
    await message.reply(msg_text.NAME)
    await state.set_state(ProfileCreate.name)


@router.message(StateFilter(ProfileEdit.photo, ProfileCreate.photo))
async def _incorrect_photo(message: types.Message):
    """Ошибка фильтра фотографии"""
    await message.answer(msg_text.INVALID_PHOTO)


# < name >
@router.message(filters.IsName(), ProfileCreate.name)
async def _name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.reply(msg_text.AGE)
    await state.set_state(ProfileCreate.age)


@router.message(ProfileCreate.name)
async def _incorrect_name(message: types.Message):
    """Ошибка фильтра имени"""
    await message.answer(msg_text.INVALID_LONG_RESPONSE)


# < age >
@router.message(ProfileCreate.age, filters.IsAge())
async def _age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.reply(msg_text.CITY)
    await state.set_state(ProfileCreate.city)


@router.message(ProfileCreate.age)
async def _incorrect_age(message: types.Message):
    """Ошибка фильтра возраста"""
    await message.answer(msg_text.INVALID_AGE)


# < city >
@router.message(ProfileCreate.city, filters.IsCity())
async def _city(message: types.Message, state: FSMContext, coordinates: dict):
    await state.update_data(
        city=message.text,
        latitude=coordinates[0],
        longitude=coordinates[1],
    )

    await message.reply(msg_text.DESCRIPTION)
    await state.set_state(ProfileCreate.desc)


@router.message(ProfileCreate.city)
async def _incorrect_city(message: types.Message):
    """Ошибка фильтра города"""
    await message.answer(msg_text.INVALID_LONG_RESPONSE)


# < description >
@router.message(StateFilter(ProfileCreate.desc, ProfileEdit.desc), filters.IsDescription())
async def _description(message: types.Message, state: FSMContext, session):
    if await state.get_state() == ProfileEdit.desc.state:
        await Profile.update_description(session, message.from_user.id, message.text)
    else:
        data = await state.get_data()
        await Profile.create(
            session,
            user_id=message.from_user.id,
            gender=data["gender"],
            find_gender=data["find_gender"],
            photo=data["photo"],
            name=data["name"],
            age=int(data["age"]),
            city=data["city"],
            latitude=float(data["latitude"]),
            longitude=float(data["longitude"]),
            description=message.text,
        )

    await state.clear()
    await profile_command(message, session)


@router.message(StateFilter(ProfileCreate.desc, ProfileEdit.desc))
async def _incorrect_description(message: types.Message):
    """Ошибка фильтра описания"""
    await message.answer(msg_text.INVALID_LONG_RESPONSE)
