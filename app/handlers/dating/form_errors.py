from aiogram import types
from aiogram.filters.state import StateFilter

from app.routers import dating_router, registration_router
from app.states.default import ProfileCreate, ProfileEdit
from app.text import message_text as mt


@registration_router.message(StateFilter(ProfileCreate.gender))
async def _incorrect_gender(message: types.Message):
    """Ошибка фильтра гендера"""
    await message.answer(mt.INVALID_RESPONSE)


@registration_router.message(StateFilter(ProfileCreate.find_gender))
async def _incorrect_find_gender(message: types.Message):
    """Ошибка фильтра гендера"""
    await message.answer(mt.INVALID_RESPONSE)


@registration_router.message(StateFilter(ProfileCreate.photo))
async def _incorrect_photo_create(message: types.Message):
    """Ошибка фильтра фото при создании"""
    await message.answer(mt.INVALID_PHOTO)


@dating_router.message(StateFilter(ProfileEdit.photo))
async def _incorrect_photo_edit(message: types.Message):
    """Ошибка фильтра фото при редактировании"""
    await message.answer(mt.INVALID_PHOTO)


@registration_router.message(StateFilter(ProfileCreate.name))
async def _incorrect_name(message: types.Message):
    """Ошибка фильтра имени"""
    await message.answer(mt.INVALID_NAME)


@registration_router.message(StateFilter(ProfileCreate.age))
async def _incorrect_age(message: types.Message):
    """Ошибка фильтра возраста"""
    await message.answer(mt.INVALID_AGE)


@registration_router.message(StateFilter(ProfileCreate.city))
async def _incorrect_city(message: types.Message):
    """Ошибка фильтра города"""
    await message.answer(mt.INVALID_CITY_RESPONSE)


@registration_router.message(StateFilter(ProfileCreate.description))
async def _incorrect_description_create(message: types.Message):
    """Ошибка фильтра описания при создании"""
    await message.answer(mt.INVALID_DESCIPTION)


@registration_router.message(StateFilter(ProfileEdit.description))
async def _incorrect_description_edit(message: types.Message):
    """Ошибка фильтра описания при редактировании"""
    await message.answer(mt.INVALID_DESCIPTION)
