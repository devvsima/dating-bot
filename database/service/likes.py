from ..models.likes import Likes

from utils.logging import logger


async def set_new_like(liker_id: int, liked_id: int) -> None:
    """Добавляет в БД лайк пользователя liker_id к пользователю liked_id, если лайк уже есть - ничего не делает"""
    existing_like = Likes.get_or_none(liker_id=liker_id, liked_id=liked_id)

    if existing_like:
        logger.info(f"Повторился лайк: {liker_id} & {liked_id}")
    else:
        Likes.create(liker_id=liker_id, liked_id=liked_id)
        logger.info(f"User: {liker_id} | лайкнул пользователя {liked_id}")
    
async def get_profile_likes(user_id: int) -> list:
    """Возращает список пользователей которые лайкнули анкету"""
    ids = Likes.select(Likes).where(Likes.liked_id == user_id)
    return [i.liker_id.id for i in ids]

async def del_like(liked_id: int, liker_id: int) -> None:
    """Удаляет из лайк из БД"""
    logger.info(f"{liker_id} & {liked_id} | лайк удален")
    Likes.delete().where((Likes.liker_id == liker_id) & (Likes.liked_id == liked_id)).execute()

