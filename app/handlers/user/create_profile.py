from aiogram import F, types
from aiogram.fsm.context import FSMContext

from app.routers import user_router as router

from database.service.profile import create_profile, edit_profile_photo, edit_profile_description

from app.handlers.msg_text import msg_text
from app.handlers.user.profile import profile_command
from app.keyboards.default import gender_kb, find_gender_kb, del_kb
from app.others.states import ProfileEdit, ProfileCreate
import app.filters.create_profile_filtres as filters
from aiogram.filters.state import StateFilter
from aiogram.enums import ContentType


@router.message(F.text == "🔄")
async def _retry_create_profile_command(message: types.Message, state: FSMContext):
    """Запускает создания профиля заново"""
    await _create_profile_command(message, state)


# create profile
@router.message(filters.IsCreate())
async def _create_profile_command(message: types.Message, state: FSMContext):
    """Начало создание профиля"""
    await message.answer(msg_text.GENDER, reply_markup=gender_kb())
    
    await state.set_state(ProfileCreate.gender)


# gender
@router.message(filters.IsGender(), StateFilter(ProfileCreate.gender))
async def _gender(message: types.Message, state: FSMContext, gender: str):
    await state.update_data(gender=gender)
    await message.reply(msg_text.FIND_GENDER, reply_markup=find_gender_kb())
    await state.set_state(ProfileCreate.find_gender)
    
    
@router.message(StateFilter(ProfileCreate.gender))
async def _incorrect_gender(message: types.Message):
    """Ошибка фильтра гендера"""
    await message.answer(msg_text.INVALID_RESPONSE)


# gender of interest
@router.message(filters.IsFindGender(), StateFilter(ProfileCreate.find_gender))
async def _find_gender(message: types.Message, state: FSMContext, find_gender: str):
    await state.update_data(find_gender=find_gender)
    await message.reply(msg_text.PHOTO, reply_markup=del_kb)
    await state.set_state(ProfileCreate.photo)

@router.message(StateFilter(ProfileCreate.find_gender))
async def _incorrect_find_gender(message: types.Message):
    """Ошибка фильтра гендера"""
    await message.answer(msg_text.INVALID_RESPONSE)


# photo
@router.message(filters.IsPhoto(), StateFilter(ProfileCreate.photo, ProfileEdit.photo))
async def _photo(message: types.Message, state: FSMContext):
    photo = message.photo[0].file_id
    if await state.get_state() == ProfileEdit.photo.state:
        await edit_profile_photo(message.from_user.id, photo)
        await profile_command(message)
        await state.clear()
        return
    
    await state.update_data(photo=photo)
    await message.reply(msg_text.NAME)
    await state.set_state(ProfileCreate.name)

    
@router.message(StateFilter([ProfileEdit.photo, ProfileCreate.photo]))
async def _incorrect_photo(message: types.Message):
    """Ошибка фильтра фотографии"""
    await message.answer(msg_text.INVALID_PHOTO)


# name
@router.message(filters.IsName(), StateFilter(ProfileCreate.name))
async def _name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.reply(msg_text.AGE)
    await state.set_state(ProfileCreate.age)

    
@router.message(StateFilter(ProfileCreate.name))
async def _incorrect_name(message: types.Message):
    """Ошибка фильтра имени"""
    await message.answer(msg_text.INVALID_LONG_RESPONSE)


# age
@router.message(filters.IsAge(), StateFilter(ProfileCreate.age))
async def _age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.reply(msg_text.CITY)
    await state.set_state(ProfileCreate.city)

        
@router.message(StateFilter(ProfileCreate.age))
async def _incorrect_age(message: types.Message):
    """Ошибка фильтра возраста"""
    await message.answer(msg_text.INVALID_AGE)


# city
@router.message(filters.IsCity(), StateFilter(ProfileCreate.city))
async def _city(message: types.Message, state: FSMContext, coordinates: dict):
    await state.update_data(
        city=message.text,
        latitude= coordinates[0], 
        longitude = coordinates[1]
        )
    
    await message.reply(msg_text.DESCRIPTION)
    await state.set_state(ProfileCreate.desc)

    
@router.message(StateFilter(ProfileCreate.city))
async def _incorrect_city(message: types.Message):
    """Ошибка фильтра города"""
    await message.answer(msg_text.INVALID_LONG_RESPONSE)


# description
@router.message(filters.IsDescription(), StateFilter(ProfileCreate.desc, ProfileEdit.desc))
async def _description(message: types.Message, state: FSMContext):
    if await state.get_state() == ProfileEdit.desc.state:
        await edit_profile_description(message.from_user.id, message.text)
    else:
        await state.update_data(desc=message.text)
        await create_profile(await state.get_data(), user_id=message.from_user.id)
    
    await state.clear()
    await profile_command(message)
    
@router.message(StateFilter([ProfileCreate.desc, ProfileEdit.desc]))
async def _incorrect_description(message: types.Message):
    """Ошибка фильтра описания"""
    await message.answer(msg_text.INVALID_LONG_RESPONSE)