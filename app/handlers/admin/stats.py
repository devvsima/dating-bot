from aiogram import types
from aiogram.dispatcher.filters import Text, Command
from app.filters.admin import Admin

from loader import dp, bot

from database.service.stats import get_profile_stats, get_users_stats
from utils.graphs import get_or_create_registration_graph, get_or_create_invites_graph

from app.handlers.msg_text import msg_text
from app.keyboards.inline.admin import stats_ikb



# @dp.message_handler(Admin(), Command("inv"))
# async def _stats_command(message: types.Message): 
#     profile_stats = get_profile_stats()
#     graph_path = get_or_create_invites_graph()
#     text = msg_text.USERS_STATS.format(get_users_stats(), profile_stats['total_users'], profile_stats['male_users'], profile_stats['female_users'])
#     with open(graph_path, "rb") as photo:
#         await message.answer_photo(photo, text)
        
@dp.message_handler(Admin(), Command("reg"))
async def _stats_command(message: types.Message): 
    profile_stats = get_profile_stats()
    graph_path = get_or_create_registration_graph()
    text = msg_text.USERS_STATS.format(get_users_stats(), profile_stats['total_users'], profile_stats['male_users'], profile_stats['female_users'])
    with open(graph_path, "rb") as photo:
        await message.answer_photo(photo, text)

@dp.callback_query_handler(Text("stats"))
async def _stats(callaback: types.CallbackQuery): 
    profile_stats = get_profile_stats()
    text = msg_text.USERS_STATS.format(get_users_stats(), profile_stats['total_users'], profile_stats['male_users'], profile_stats['female_users'])
    await callaback.message.edit_text(text, reply_markup=stats_ikb())

