from aiogram import F, types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from app.filters.kb_filter import StatsCallback
from app.keyboards.inline.admin import stats_ikb
from app.routers import admin_router
from data.config import GRAPH_FILE_PATH
from database.services.stats import Stats
from utils.graphs import StatsGraph

stats_graph = StatsGraph()


USER_STATS = """
👤 Users: {}\t| 🚫 Blocked: {}
✉️ Referrals: {}

🌍 Most popular language: {}
"""


PROFILE_STATS = """
📂 Profile: {} | 🔕 Inactive: {}
🙍‍♂ Guys: {} | 🙍‍♀ Girls: {}

💘 Matches: {}

🕘 Age: {}
🏙 City: {}
"""


@admin_router.message(Command("stats"), StateFilter(None))
@admin_router.message(F.text == "📊 Statistics", StateFilter(None))
async def _stats_command(message: types.Message, session) -> None:
    """Отправляет администратору меню статистики"""
    await message.answer("Stats sending...")

    data = await Stats.get_registration_data(session)
    stats_graph.create_user_registration_graph(data)
    users_stats = await Stats.user_stats(session)

    text = USER_STATS.format(
        users_stats["count"],
        users_stats["banned_count"],
        users_stats["total_referrals"],
        users_stats["most_popular_language"],
    )

    photo = types.FSInputFile(GRAPH_FILE_PATH)
    await message.answer_photo(photo=photo, caption=text, reply_markup=stats_ikb("Profile"))


@admin_router.callback_query(StatsCallback.filter(), StateFilter(None))
async def _stats_callback(
    callback: types.CallbackQuery, callback_data: StatsCallback, session
) -> None:
    """Отправляет администратору график и статистику"""
    if callback_data.type == "User":
        data = await Stats.get_registration_data(session)
        stats_graph.create_user_registration_graph(data)
        users_stats = await Stats.user_stats(session)

        text = USER_STATS.format(
            users_stats["count"],
            users_stats["banned_count"],
            users_stats["total_referrals"],
            users_stats["most_popular_language"],
        )
        kb_text = "Profile"

    elif callback_data.type == "Profile":
        gender_data = await Stats.get_gender_data(session)

        stats_graph.create_gender_pie_chart(gender_data)
        match_stats = await Stats.match_stats(session)
        profile_stats = await Stats.profile_stats(session)
        text = PROFILE_STATS.format(
            profile_stats["count"],
            profile_stats["inactive_profile"],
            profile_stats["male_count"],
            profile_stats["female_count"],
            match_stats[0],
            profile_stats["average_age"],
            profile_stats["most_popular_city"],
        )
        kb_text = "User"

    media = types.InputMediaPhoto(media=types.FSInputFile(GRAPH_FILE_PATH), caption=text)
    await callback.message.edit_media(media=media, reply_markup=stats_ikb(kb_text))
