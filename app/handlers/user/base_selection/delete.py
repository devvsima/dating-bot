from aiogram import types, Dispatcher
from loader import dp, bot
from database.bd import delete_profile
from app.keyboards import delete_profile_yes_or_not


@dp.message_handler(text="❌")
async def delete_comm(message: types.Message):
    await message.answer("Вы уверены?", reply_markup=delete_profile_yes_or_not())


@dp.callback_query_handler(text=["delete_yes", "delete_no"])
async def delete_yes_or_no(callback: types.CallbackQuery):
    if callback.data == "delete_yes":
        delete_profile(str(callback.from_user.id))
        await callback.answer(text="Ваша анкета успешно удалена.")
    elif callback.data == "delete_no":
        pass
