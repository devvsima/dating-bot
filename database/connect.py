from peewee import PostgresqlDatabase, SqliteDatabase,Model
from data.config import DB_NAME, DB_HOST ,DB_PORT, DB_USER, DB_PASS, DIR


if DB_NAME and DB_HOST and DB_PORT and DB_USER and DB_PASS:
    db = PostgresqlDatabase(DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS)

else:
    db = SqliteDatabase(f"{DIR}/database/db.sqlite3")
db.connect()

class BaseModel(Model):
    class Meta:
        database = db