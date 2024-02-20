from aiogram import types
from aiogram.dispatcher.filters import Text


from loader import dp, bot
from database.service.users import delete_profile
from app.keyboards import delete_profile_yes_or_not
from .start import start_command
# from app.handlers.user.start import lang_command


@dp.message_handler(Text("❌"))
async def delete_comm(message: types.Message):
    await message.answer(
        text=("Вы точно хотите удалить анкету?"),
        reply_markup=delete_profile_yes_or_not(),
    )


@dp.callback_query_handler(Text(["delete_yes", "delete_no"]))
async def delete_yes_or_no(callback: types.CallbackQuery):
    if callback.data == "delete_yes":
        await delete_profile(callback.from_user.id)
        await callback.answer(text=("Ваша анкета успешно удалена."))
        await callback.message.answer("Если хотите снова создать вашу анкету напиши команду /create")
    elif callback.data == "delete_no":
        pass