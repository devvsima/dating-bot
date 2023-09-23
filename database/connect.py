from pymongo import MongoClient
# from data.config import mongodb_url

mongodb_url="mongodb+srv://devvsima:lTXUQNQtmNW10pwL@studybot.apxoslt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(mongodb_url)
db = client["michalangelo"]
db_users = db.users



async def db_close():
    client.close()
