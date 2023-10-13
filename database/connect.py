from pymongo import MongoClient
from data.config import mongodb_url



client = MongoClient(mongodb_url)
db = client["michalangelo"]
db_users = db.users


async def db_close():
    client.close()
