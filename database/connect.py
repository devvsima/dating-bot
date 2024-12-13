from peewee import PostgresqlDatabase, SqliteDatabase,Model

from data.config import DB_NAME, DB_HOST ,DB_PORT, DB_USER, DB_PASS, DIR

from utils.logging import logger


if DB_NAME and DB_HOST and DB_PORT and DB_USER and DB_PASS:
    db = PostgresqlDatabase(DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS)
    logger.info('Database: PostgreSql')
    
else:
    db = SqliteDatabase(f"{DIR}/database/db.sqlite3")
    logger.info('Database: Sqlite')
    
db.connect()

class BaseModel(Model):
    class Meta:
        database = db