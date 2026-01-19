"""
API endpoints для поиска анкет
"""

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from api.models import SearchProfileResponse, SearchResponse
from database.connect import get_session
from database.models.profile import ProfileModel
from database.services.profile_media import ProfileMedia
from database.services.search import search_profiles
from database.services.user import User
from utils.telegram_requests import get_photo_url_by_file_id

router = APIRouter()


@router.get("/search/{user_id}", response_model=SearchResponse)
async def get_search_profiles(user_id: int):
    """
    Получение списка анкет для поиска

    Args:
        user_id: ID пользователя Telegram

    Returns:
        JSON со списком подходящих анкет
    """
    async with get_session() as session:
        # Получаем пользователя с профилем
        user = await User.get_with_profile(session=session, id=user_id)

        if not user or not user.profile:
            raise HTTPException(status_code=404, detail="Профиль не найден")

        # Получаем список ID анкет для поиска
        profile_ids = await search_profiles(session, user.profile)

        if not profile_ids:
            return SearchResponse(profiles=[], total=0)

        # Загружаем полные данные профилей
        profiles_data = []
        for profile_id in profile_ids[:50]:  # Ограничиваем 50 анкетами
            result = await session.execute(
                select(ProfileModel)
                .options(joinedload(ProfileModel.user))
                .where(ProfileModel.id == profile_id)
            )
            profile = result.scalar_one_or_none()

            if profile:
                # Получаем все фото профиля
                photos = []
                media_items = await ProfileMedia.get_profile_photos(
                    session=session, profile_id=profile.id
                )
                for item in media_items:
                    photos.append(get_photo_url_by_file_id(item.media))

                profiles_data.append(
                    SearchProfileResponse(
                        id=profile.id,
                        user_id=profile.user.id,
                        username=profile.user.username,
                        name=profile.name,
                        age=profile.age,
                        gender=profile.gender,
                        city=profile.city,
                        description=profile.description,
                        instagram=profile.instagram,
                        photos=photos,
                    )
                )

        return SearchResponse(profiles=profiles_data, total=len(profiles_data))
