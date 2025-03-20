from sqlalchemy import case, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import MatchModel, ProfileModel, UserModel


class Stats:
    @staticmethod
    async def get_registration_data(session: AsyncSession) -> list:
        """Возвращает список пользователей с датой регистрации"""
        stmt = select(UserModel.id, UserModel.username, UserModel.created_at).order_by(
            UserModel.referral.desc()
        )
        result = await session.execute(stmt)
        users = result.fetchall()

        return [{"username": user.username, "timestamp": user.created_at} for user in users]

    @staticmethod
    async def match_stats(session: AsyncSession) -> dict:
        """Возвращает количество пользователей, заблокированных пользователей, самый популярный язык и общее количество рефералов"""
        stmt = select(
            func.count(MatchModel.id).label("count"),
        )
        result = await session.execute(stmt)
        stats = result.fetchone()
        return stats

    @staticmethod
    async def user_stats(session: AsyncSession) -> dict:
        """Возвращает количество пользователей, заблокированных пользователей, самый популярный язык и общее количество рефералов"""

        # Основная статистика
        stmt = select(
            func.count(UserModel.id).label("count"),
            func.sum(case((UserModel.is_banned == True, 1), else_=0)).label("banned_count"),
            func.sum(UserModel.referral).label("total_referrals"),
        )
        result = await session.execute(stmt)
        stats = result.fetchone()

        # Самый популярный язык
        language_stmt = (
            select(UserModel.language, func.count(UserModel.language).label("language_count"))
            .group_by(UserModel.language)
            .order_by(desc("language_count"))
            .limit(1)
        )
        language_result = await session.execute(language_stmt)
        popular_language = language_result.fetchone()

        return {
            "count": stats[0],
            "banned_count": stats[1],
            "total_referrals": stats[2] if stats[2] else 0,
            "most_popular_language": popular_language[0] if popular_language else None,
        }

    @staticmethod
    async def get_gender_data(session: AsyncSession) -> dict:
        """Возвращает количество мужчин и женщин среди пользователей"""
        stmt = select(ProfileModel.gender)
        result = await session.execute(stmt)
        users = result.fetchall()

        # Подсчитываем количество мужчин и женщин
        gender_count = {"male": 0, "female": 0}
        for user in users:
            gender = user[0]
            if gender in gender_count:
                gender_count[gender] += 1

        return gender_count

    @staticmethod
    async def profile_stats(session: AsyncSession) -> dict:
        """Возвращает количество анкет (всего, мужчин, женщин, неактивных),
        средний возраст и самый популярный город"""

        # Основная статистика
        stmt = select(
            func.count(ProfileModel.user_id).label("count"),
            func.sum(case((ProfileModel.gender == "male", 1), else_=0)).label("male_count"),
            func.sum(case((ProfileModel.gender == "female", 1), else_=0)).label("female_count"),
            func.sum(case((ProfileModel.is_active == False, 1), else_=0)).label("inactive_profile"),
            func.avg(ProfileModel.age).label("average_age"),
        )
        result = await session.execute(stmt)
        stats = result.fetchone()

        # Получаем самый популярный город
        city_stmt = (
            select(ProfileModel.city, func.count(ProfileModel.city).label("city_count"))
            .group_by(ProfileModel.city)
            .order_by(desc("city_count"))
            .limit(1)
        )
        city_result = await session.execute(city_stmt)
        popular_city = city_result.fetchone()

        return {
            "count": stats[0],
            "male_count": stats[1],
            "female_count": stats[2],
            "inactive_profile": stats[3],
            "average_age": round(stats[4], 1)
            if stats[4]
            else None,  # Округление до 1 знака после запятой
            "most_popular_city": popular_city[0] if popular_city else None,
        }
