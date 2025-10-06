from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.inline.admin import block_user_ikb
from app.text import message_text as mt
from data.config import tgbot
from database.models.profile import ProfileModel
from database.models.user import UserModel
from database.services.complaint import Compleint
from database.services.profile_media import ProfileMedia
from database.services.search import haversine_distance
from loader import bot
from utils.logging import logger

MODERATOR_GROUP_ID = tgbot.MODERATOR_GROUP_ID


async def send_profile(chat_id: int, profile: ProfileModel, session: AsyncSession) -> None:
    """Отправляет пользователю переданный в функцию профиль"""
    media_items = await ProfileMedia.get_profile_photos(session=session, profile_id=profile.id)

    city = "📍 " + profile.city if profile.is_shared_location else profile.city
    text = f"{profile.name}, {profile.age}, {city}\n{profile.description}"

    media_list = []
    for i, media_obj in enumerate(media_items):
        if i == 0:
            media_list.append(InputMediaPhoto(media=media_obj.media, caption=text, parse_mode=None))
        else:
            media_list.append(InputMediaPhoto(media=media_obj.media))

    # Проверяем, есть ли медиа для отправки
    if media_list:
        await bot.send_media_group(chat_id=chat_id, media=media_list)
    else:
        # Если нет медиа, отправляем просто текстовое сообщение
        await bot.send_message(chat_id=chat_id, text=text)


async def send_profile_with_dist(
    user: UserModel, profile: ProfileModel, session: AsyncSession
) -> None:
    """Отправляет профиль пользователя с расстоянием до него в киломтерах"""
    media_items = await ProfileMedia.get_profile_photos(session=session, profile_id=profile.id)

    if user.profile.is_shared_location and profile.is_shared_location:
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

    # Проверяем, есть ли медиа для отправки
    if media_list:
        await bot.send_media_group(chat_id=user.id, media=media_list)
    else:
        # Если нет медиа, отправляем просто текстовое сообщение
        await bot.send_message(chat_id=user.id, text=text)


async def complaint_to_profile(
    session: AsyncSession, sender: UserModel, receiver: UserModel, reason: str
) -> None:
    """Отправляет в группу модераторов анкету пользователя
    на которого пришла жалоба"""
    if MODERATOR_GROUP_ID:
        try:
            complaint = await Compleint.create(
                session=session,
                sender_id=sender.id,
                receiver_id=receiver.id,
                reason=reason,
            )

            await send_profile(MODERATOR_GROUP_ID, receiver.profile, session)

            text = mt.REPORT_TO_USER.format(
                sender.id,
                sender.username,
                receiver.id,
                receiver.username,
                reason,
            )

            await bot.send_message(
                chat_id=MODERATOR_GROUP_ID,
                text=text,
                reply_markup=block_user_ikb(
                    complaint_id=complaint.id,
                    user_id=receiver.id,
                    username=receiver.username,
                ),
            )
        except:
            logger.error("Сообщение в модераторскую группу не отправленно")
