from ..models.likes import Likes
from utils.logging import logger

from peewee import fn


def set_new_like(liker_id, liked_id) -> None:
    # Проверяем, существует ли уже лайк от этого пользователя к указанному
    existing_like = Likes.get_or_none(liker_id=liker_id, liked_id=liked_id)

    if existing_like is None:
        logger.info(f"{liker_id} liked {liked_id}")
        Likes.create(liker_id=liker_id, liked_id=liked_id)
    else:
        logger.info(f"Duplicate like attempt: {liker_id} already liked {liked_id}")
    
def get_profile_likes(user_id) -> list:
    logger.info(user_id)
    users = Likes.select(Likes.liker_id).where((Likes.liked_id == user_id) & (Likes.status == "pending"))
    return [i.liker_id for i in users]

def del_like(liked_id, liker_id) -> None:
    logger.info(f"{liker_id} liked {liked_id} like delete")
    Likes.delete().where((Likes.liker_id == liker_id) & (Likes.liked_id == liked_id)).execute()

