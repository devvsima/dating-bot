from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.inline.admin import block_user_ikb
from app.text import message_text as mt
from data.config import MODERATOR_GROUP
from database.models.profile import ProfileModel
from database.models.user import UserModel
from database.services.profile_media import ProfileMedia
from database.services.search import haversine_distance
from loader import bot
from utils.logging import logger


async def send_profile(chat_id: int, profile: ProfileModel, session: AsyncSession) -> None:
    """Отправляет пользователю переданный в функцию профиль"""
    media_items = await ProfileMedia.get_profile_photos(session=session, profile_id=profile.id)
    text = f"{profile.name}, {profile.age}, {profile.city}\n{profile.description}"

    media_list = []
    for i, media_obj in enumerate(media_items):
        if i == 0:
            media_list.append(InputMediaPhoto(media=media_obj.media, caption=text, parse_mode=None))
        else:
            media_list.append(InputMediaPhoto(media=media_obj.media))

    await bot.send_media_group(chat_id=chat_id, media=media_list)


async def send_profile_with_dist(
    user: UserModel, profile: ProfileModel, session: AsyncSession
) -> None:
    """Отправляет профиль пользователя с расстоянием до него в киломтерах"""
    media_items = await ProfileMedia.get_profile_photos(session=session, profile_id=profile.id)

    if profile.city == "📍":
        distance = haversine_distance(
            user.profile.latitude, user.profile.longitude, profile.latitude, profile.longitude
        )
        city = f"📍 {round(distance, 2)} km"
    else:
        city = profile.city
    text = f"{profile.name}, {profile.age}, {city}\n{profile.description}"

    media_list = []
    for i, media_obj in enumerate(media_items):
        if i == 0:
            media_list.append(InputMediaPhoto(media=media_obj.media, caption=text, parse_mode=None))
        else:
            media_list.append(InputMediaPhoto(media=media_obj.media))

    await bot.send_media_group(chat_id=user.id, media=media_list)


async def complaint_to_profile(
    complainant: UserModel, reason: str, complaint_user: UserModel, session: AsyncSession
) -> None:
    """Отправляет в группу модераторов анкету пользователя
    на которого пришла жалоба"""
    if MODERATOR_GROUP:
        try:
            await send_profile(MODERATOR_GROUP, complaint_user.profile, session)

            text = mt.REPORT_TO_USER.format(
                complainant.id,
                complainant.username,
                complaint_user.id,
                complaint_user.username,
                reason,
            )

            await bot.send_message(
                chat_id=MODERATOR_GROUP,
                text=text,
                reply_markup=block_user_ikb(
                    id=complaint_user.id,
                    username=complaint_user.username,
                ),
            )
        except:
            logger.error("Сообщение в модераторскую группу не отправленно")
