from ..models.profile import Profile
from utils.logging import logger


async def get_profile(user_id):
    return Profile.get(Profile.user_id == user_id)

async def is_profile(user_id):
    return Profile.select().where(Profile.user_id == user_id).exists()

async def delete_profile(user_id):
    user = await get_profile(user_id)
    user.delete_instance()
    logger.info(f"User | {user_id} delete profile")
    
async def edit_profile_photo(user_id, photo):
    Profile.update(photo=photo).where(Profile.user_id == user_id).execute()
    logger.info(f"User | {user_id} edit photo")

async def edit_profile_description(user_id, description):
    Profile.update(description=description).where(Profile.user_id == user_id).execute()
    logger.info(f"User | {user_id} edit description")

async def create_profile(state, user_id):
    if await is_profile(user_id):
        await delete_profile(user_id)
        
    async with state.proxy() as data:
        Profile.create(      
            user_id = user_id,
            gender = data["gender"],
            find_gender = data["find_gender"],
            photo = data["photo"],
            name = data["name"],
            age = data["age"],
            city = data["city"],
            latitude = data["latitude"],
            longitude = data["longitude"],
            description = data["desc"]
            )
    logger.info(f"User | {user_id} created new profile")
