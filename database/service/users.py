from ..models.users import Users
from fuzzywuzzy import process


async def add_user(user_id):
    Users.create(id=user_id)


async def find_user(user_id):
    return Users.select().where(Users.id == user_id)


async def get_profile(user_id):
    return Users.get(Users.id == user_id)


async def delete_profile(user_id):
    user = await get_profile(user_id)
    user.delete_instance()



async def create_profile(state, user_id):
    async with state.proxy() as data:
        Users.create(      
            id = user_id,
            gender = data["gender"],
            find_gender = data["find_gender"],
            photo = data["photo"],
            name = data["name"],
            age = data["age"],
            city = data["city"],
            description = data["desc"]
            )
 
      
async def elastic_search_city(user_id):
    user = await get_profile(user_id)
    cities_in_db = [user.city for user in Users.select()]
    matches = process.extract(user.city, cities_in_db, limit=1)

    if matches and matches[0][1] >= 50:  # Процент совпадения
        return Users.select().where(Users.city == matches[0][0])

