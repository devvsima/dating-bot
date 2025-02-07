from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User
from ..models.profile import Profile


async def get_all_users_registration_data(session: AsyncSession) -> list:
    """Возвращает список пользователей с датой регистрации"""
    stmt = select(User.id, User.username, User.created_at).order_by(User.referral.desc())
    result = await session.execute(stmt)
    users = result.fetchall()

    return [{"username": user.username, "timestamp": user.created_at} for user in users]


async def get_users_stats(session: AsyncSession) -> tuple[int, int]:
    """Возвращает количество пользователей и заблокированных пользователей"""
    stmt = select(
        func.count(User.id).label("count"),
        func.sum(case((User.is_banned == True, 1), else_=0)).label("banned_count"),
    )
    result = await session.execute(stmt)
    stats = result.fetchone()

    return {"count": stats[0], "banned_count": stats[1]}


async def get_profile_stats(session: AsyncSession) -> dict:
    """Возвращает количество анкет (всего, мужчин, женщин, неактивных)"""
    stmt = select(
        func.count(Profile.user_id).label("count"),
        func.sum(case((Profile.gender == "male", 1), else_=0)).label("male_count"),
        func.sum(case((Profile.gender == "female", 1), else_=0)).label("female_count"),
        func.sum(case((Profile.is_active == False, 1), else_=0)).label("inactive_profile"),
    )
    result = await session.execute(stmt)
    stats = result.fetchone()

    return {
        "count": stats[0],
        "male_count": stats[1],
        "female_count": stats[2],
        "inactive_profile": stats[3],
    }
