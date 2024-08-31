from ..models.likes import Likes
from utils.logging import logger

from peewee import fn

# async def get_profile(user_id):
#     return Likes.get(Profile.id == user_id)

def set_new_like(user_id, liked_by) -> None:
    logger.info("New like")
    Likes.create(user_id = user_id, liked_profile_id = liked_by )
    
def get_profile_likes(user_id) -> list:
    users = Likes.select().where(Likes.liked_profile_id == user_id)
    return [i.user_id for i in users]