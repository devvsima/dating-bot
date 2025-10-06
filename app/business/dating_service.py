from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.inline.archive import check_archive_ikb
from app.text import message_text as mt
from database.models.user import UserModel
from database.services.match import Match
from database.services.profile import Profile
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
    except TelegramForbiddenError:
        logger.info(
            f"Пользователь {user.id} @{user.username} заблокировал бота. Оповещение не отправлено."
        )
        await Profile.update(
            session=session,
            id=user.id,
            is_active=False,
        )

    except Exception as e:
        logger.error(f"Ошибка при отправке оповещения пользователю {user.id} @{user.username}: {e}")
