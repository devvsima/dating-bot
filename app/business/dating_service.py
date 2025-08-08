from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.inline.archive import check_archive_ikb
from app.text import message_text as mt
from database.models.user import UserModel
from database.services.match import Match
from loader import bot
from utils.logging import logger


async def send_user_like_alert(session: AsyncSession, user: UserModel):
    matchs = await Match.get_user_matchs(session, user.id)
    try:
        await bot.send_message(
            chat_id=user.id,
            text=mt.LIKE_PROFILE(user.language).format(len(matchs)),
            reply_markup=check_archive_ikb(user.language),
        )
    except:
        logger.info(
            f"Пользователю {user.id} @{user.username}:\
            не было отправлнно оповещение, вероятно из за блокироваки бота"
        )
