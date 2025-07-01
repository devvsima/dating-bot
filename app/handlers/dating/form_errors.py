from aiogram import types
from aiogram.filters.state import StateFilter

from app.routers import dating_router
from app.states.default import ProfileCreate, ProfileEdit
from app.text import message_text as mt


@dating_router.message(StateFilter(ProfileCreate.gender))
async def _incorrect_gender(message: types.Message):
    """Ошибка фильтра гендера"""
    await message.answer(mt.INVALID_RESPONSE)


@dating_router.message(StateFilter(ProfileCreate.find_gender))
async def _incorrect_find_gender(message: types.Message):
    """Ошибка фильтра гендера"""
    await message.answer(mt.INVALID_RESPONSE)


@dating_router.message(StateFilter(ProfileCreate.photo, ProfileEdit.photo))
async def _incorrect_photo(message: types.Message):
    """Ошибка фильтра фото"""
    await message.answer(mt.INVALID_PHOTO)


@dating_router.message(StateFilter(ProfileCreate.name))
async def _incorrect_name(message: types.Message):
    """Ошибка фильтра имени"""
    await message.answer(mt.INVALID_LONG_RESPONSE)


@dating_router.message(StateFilter(ProfileCreate.age))
async def _incorrect_age(message: types.Message):
    """Ошибка фильтра возраста"""
    await message.answer(mt.INVALID_AGE)


@dating_router.message(StateFilter(ProfileCreate.city))
async def _incorrect_city(message: types.Message):
    """Ошибка фильтра города"""
    await message.answer(mt.INVALID_CITY_RESPONSE)


@dating_router.message(StateFilter(ProfileCreate.description, ProfileEdit.description))
async def _incorrect_description(message: types.Message):
    """Ошибка фильтра описания"""
    await message.answer(mt.INVALID_LONG_RESPONSE)
