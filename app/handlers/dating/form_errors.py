from aiogram import types
from aiogram.filters.state import StateFilter

from app.handlers.message_text import user_message_text as umt
from app.others.states import ProfileCreate, ProfileEdit
from app.routers import dating_router


@dating_router.message(StateFilter(ProfileCreate.gender))
async def _incorrect_gender(message: types.Message):
    """Ошибка фильтра гендера"""
    await message.answer(umt.INVALID_RESPONSE)


@dating_router.message(StateFilter(ProfileCreate.find_gender))
async def _incorrect_find_gender(message: types.Message):
    """Ошибка фильтра гендера"""
    await message.answer(umt.INVALID_RESPONSE)


@dating_router.message(StateFilter(ProfileCreate.photo, ProfileEdit.photo))
async def _incorrect_photo(message: types.Message):
    """Ошибка фильтра фото"""
    await message.answer(umt.INVALID_PHOTO)


@dating_router.message(StateFilter(ProfileCreate.name))
async def _incorrect_name(message: types.Message):
    """Ошибка фильтра имени"""
    await message.answer(umt.INVALID_LONG_RESPONSE)


@dating_router.message(StateFilter(ProfileCreate.age))
async def _incorrect_age(message: types.Message):
    """Ошибка фильтра возраста"""
    await message.answer(umt.INVALID_AGE)


@dating_router.message(StateFilter(ProfileCreate.city))
async def _incorrect_city(message: types.Message):
    """Ошибка фильтра города"""
    await message.answer(umt.INVALID_CITY_RESPONSE)


@dating_router.message(StateFilter(ProfileCreate.description, ProfileEdit.description))
async def _incorrect_description(message: types.Message):
    """Ошибка фильтра описания"""
    await message.answer(umt.INVALID_LONG_RESPONSE)
