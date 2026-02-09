"""
API endpoints для действий пользователя (лайки, дизлайки, жалобы)
"""

from fastapi import APIRouter, HTTPException

from api.models import ActionResponse, ComplaintRequest, LikeRequest
from database.engine import get_session
from database.queries.complaint import Complaint
from database.queries.match import Match
from database.queries.user import User
from utils.logging import logger

router = APIRouter()


@router.post("/like", response_model=ActionResponse)
async def like_profile(request: LikeRequest):
    """
    Лайк анкеты

    Args:
        request: Данные запроса (user_id, target_id, message)

    Returns:
        JSON со статусом операции
    """
    async with get_session() as session:
        # Проверяем существование пользователей
        user = await User.get_with_profile(session=session, id=request.user_id)
        target = await User.get_with_profile(session=session, id=request.target_id)

        if not user or not target:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        # Создаем лайк
        is_created = await Match.create(
            session=session,
            sender_id=request.user_id,
            receiver_id=request.target_id,
            mail_text=request.message,
        )

        return ActionResponse(
            status="success",
            is_new=is_created,
            message="Лайк отправлен" if is_created else "Лайк уже существует",
        )


@router.post("/dislike", response_model=ActionResponse)
async def dislike_profile(request: LikeRequest):
    """
    Дизлайк анкеты (просто пропускаем)

    Args:
        request: Данные запроса (user_id, target_id)

    Returns:
        JSON со статусом
    """
    return ActionResponse(status="success", message="Анкета пропущена")


@router.post("/complaint", response_model=ActionResponse)
async def complaint_profile(request: ComplaintRequest):
    """
    Жалоба на анкету

    Args:
        request: Данные запроса (user_id, target_id, reason)

    Returns:
        JSON со статусом
    """
    async with get_session() as session:
        # Создаем жалобу
        await Complaint.create(
            session=session,
            sender_id=request.user_id,
            profile_id=request.target_id,
            reason=request.reason,
        )

        logger.log(
            "WEBAPP",
            f"User {request.user_id} complained about {request.target_id}: {request.reason}",
        )

    return ActionResponse(status="success", message="Жалоба отправлена")
