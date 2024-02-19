from ..models.users import Users


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


async def elastic_search_user_ids(user_id):
    user = await get_profile(user_id)
    users = Users.select(Users.id).where((Users.city == user.city) & (Users.id != user_id))
    return [i.id for i in users]


