from peewee import PostgresqlDatabase
from data.config import db_name, db_host ,db_port, db_user, db_password

db = PostgresqlDatabase(db_name, host=db_host, port=db_port, user=db_user, password=db_password)
db.connect()