"""
API endpoints для работы с профилями пользователей
"""

from fastapi import APIRouter, HTTPException

from api.models import ProfileResponse
from database.connect import get_session
from database.services.profile_media import ProfileMedia
from database.services.user import User
from utils.telegram_requests import get_photo_url_by_file_id

router = APIRouter()


@router.get("/profile/{user_id}", response_model=ProfileResponse)
async def get_profile(user_id: int):
    """
    Получение профиля пользователя

    Args:
        user_id: ID пользователя Telegram

    Returns:
        JSON с данными профиля и фотографиями
    """
    async with get_session() as session:
        # Получаем пользователя с профилем и медиа
        user = await User.get_with_profile(session=session, id=user_id)

        if not user or not user.profile:
            raise HTTPException(status_code=404, detail="Профиль не найден")

        # Получаем все фото из медиа
        photos = []
        media_items = await ProfileMedia.get_profile_photos(
            session=session, profile_id=user.profile.id
        )
        for item in media_items:
            photos.append(get_photo_url_by_file_id(item.media))

        # Возвращаем данные профиля
        return ProfileResponse(
            id=user.id,
            username=user.username,
            name=user.profile.name,
            age=user.profile.age,
            gender=user.profile.gender,
            city=user.profile.city,
            description=user.profile.description,
            instagram=user.profile.instagram,
            photos=photos,
        )
