import json
from .users import Users
from .profile import Profile
from .likes import Likes
# Подключение к SQLite
from datetime import datetime
from data.config import DIR
from playhouse.migrate import PostgresqlMigrator, migrate

from ..connect import db


def export_data(db, model, file):
    # Экспорт данных
    data = []
    for model in [model]:  # Добавьте сюда все ваши модели
        rows = [item.__data__ for item in model.select()]
        data.append({model._meta.table_name: rows})

    def json_serial(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # Преобразование в ISO 8601
        raise TypeError(f"Type {type(obj)} not serializable")

    with open(file, 'w') as f:
        json.dump(data, f, default=json_serial)


def import_data(db, model, file):
    with open(file, 'r') as f:
        data = json.load(f)

    # Импорт данных
    for table in data:
        table_name = list(table.keys())[0]  # Имя таблицы из JSON
        rows = table[table_name]

        if model is None:
            print(f"Не удалось найти модель для таблицы {table_name}")
            continue

        # Вставка данных в PostgreSQL
        with db.atomic():
            model.insert_many(rows).execute()

# import_data(db, Profile, f"{DIR}/profile.json")
# import_data(db, Profile, f"{DIR}/profile.json")
# import_data(db, Likes, "like.json")

# migrator = PostgresqlMigrator(db)
# from peewee import CharField, BigIntegerField, DateTimeField, IntegerField, BooleanField

# migrate(
#     migrator.drop_column('users', 'role'),
#     migrator.drop_column('users', 'is_invited'),
#     migrator.add_column('users', 'is_banned', BooleanField(default=False)),
# )

# import_data()
# db.execute_sql("ALTER TABLE users DROP COLUMN role;")
# db.execute_sql("ALTER TABLE users DROP COLUMN is_invited;")
# db.execute_sql("UPDATE users SET is_banned = NOT is_invited;")
# db.execute_sql("ALTER TABLE users DROP COLUMN is_invited;")
