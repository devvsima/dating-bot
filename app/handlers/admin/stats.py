from aiogram import F, types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.kb_filter import StatsCallback
from app.keyboards.inline.admin import stats_ikb
from app.routers import admin_router
from app.services.stats_service import StatsService
from core.config import GRAPH_FILE_PATH
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


REFERRAL_STATS = """
📊 Total Referrals: {}

📈 Sources breakdown:
{}
"""


@admin_router.message(StateFilter(None), Command("stats"))
@admin_router.message(StateFilter(None), F.text == "📊 Statistics")
async def _stats_command(message: types.Message, session: AsyncSession) -> None:
    """Отправляет администратору меню статистики"""
    await message.answer("Stats sending...")

    data = await StatsService.get_registration_data(session)
    stats_graph.create_user_registration_graph(data)
    users_stats = await StatsService.user_stats(session)

    text = USER_STATS.format(
        users_stats["count"],
        users_stats["banned_count"],
        users_stats["total_referrals"],
        users_stats["most_popular_language"],
    )

    photo = types.FSInputFile(GRAPH_FILE_PATH)
    await message.answer_photo(photo=photo, caption=text, reply_markup=stats_ikb("User"))


@admin_router.callback_query(StateFilter(None), StatsCallback.filter())
async def _stats_callback(
    callback: types.CallbackQuery, callback_data: StatsCallback, session: AsyncSession
) -> None:
    """Отправляет администратору график и статистику"""
    if callback_data.type == "User":
        data = await StatsService.get_registration_data(session)
        stats_graph.create_user_registration_graph(data)
        users_stats = await StatsService.user_stats(session)

        text = USER_STATS.format(
            users_stats["count"],
            users_stats["banned_count"],
            users_stats["total_referrals"],
            users_stats["most_popular_language"],
        )

    elif callback_data.type == "Profile":
        gender_data = await StatsService.get_gender_data(session)

        stats_graph.create_gender_pie_chart(gender_data)
        match_stats = await StatsService.match_stats(session)
        profile_stats = await StatsService.profile_stats(session)
        text = PROFILE_STATS.format(
            profile_stats["count"],
            profile_stats["inactive_profile"],
            profile_stats["male_count"],
            profile_stats["female_count"],
            match_stats[0],
            profile_stats["average_age"],
            profile_stats["most_popular_city"],
        )

    elif callback_data.type == "Referral":
        referral_stats = await StatsService.referral_stats(session)
        stats_graph.create_referral_sources_chart(referral_stats["sources"])

        # Форматируем список источников
        sources_text = ""
        for source, count in referral_stats["sources"].items():
            percentage = (
                (count / referral_stats["total_referrals"] * 100)
                if referral_stats["total_referrals"] > 0
                else 0
            )
            sources_text += f"• {source}: {count} ({percentage:.1f}%)\n"

        if not sources_text:
            sources_text = "No referral data available"

        text = REFERRAL_STATS.format(referral_stats["total_referrals"], sources_text)

    media = types.InputMediaPhoto(media=types.FSInputFile(GRAPH_FILE_PATH), caption=text)
    await callback.message.edit_media(media=media, reply_markup=stats_ikb(callback_data.type))
