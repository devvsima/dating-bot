"""
API endpoints для поиска анкет
"""

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from api.models import SearchProfileResponse, SearchResponse
from app.services.search_service import SearchService
from database.engine import get_session
from database.models import ProfileMedia, User
from database.models.profile import Profile

router = APIRouter()


@router.get("/search/{user_id}", response_model=SearchResponse)
async def get_search_profiles(
    user_id: int,
    include_profile: bool = Query(
        default=False, description="Включать ли полные данные профилей (иначе только ID)"
    ),
):
    """
    Получение списка анкет для поиска

    Args:
        user_id: ID пользователя Telegram
        include_profile: Если False - возвращает только ID профилей, если True - полные данные

    Returns:
        JSON со списком ID профилей или полных данных профилей

    Examples:
        GET /api/search/123456                        # Только ID
        GET /api/search/123456?include_profile=true   # Полные данные
    """
    async with get_session() as session:
        user = await User.get_with_profile(session=session, id=user_id)

        if not user or not user.profile:
            raise HTTPException(status_code=404, detail="Профиль не найден")

        profile_ids = await SearchService.search_profiles(session, user.profile)

        if not profile_ids:
            return SearchResponse(profiles=[], total=0)

        if not include_profile:
            return SearchResponse(profiles=profile_ids, total=len(profile_ids))

        profiles_data = []
        for profile_id in profile_ids:
            result = await session.execute(
                select(Profile).options(joinedload(Profile.user)).where(Profile.id == profile_id)
            )
            profile = result.scalar_one_or_none()

            if profile:
                photos = []
                media_items = await ProfileMedia.get_profile_photos(
                    session=session, profile_id=profile.id
                )
                for item in media_items:
                    photos.append(f"/api/photo/{item.media}")

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
