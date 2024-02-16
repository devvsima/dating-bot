from pathlib import Path
from environs import Env
from peewee import PostgresqlDatabase

DIR = Path(__file__).absolute().parent.parent

env = Env()
env.read_env()

#  tgbot
token_api = env.str("TOKEN", default=None)
banned_users = env("BANED", default=None)
admins = [env("ADMINS", default=None)]

# db
db_name = env.str("DB_NAME", default=None)
db_host = env.str("DB_HOST", default="localhost")
db_port = env.int("MONGH_PORT", default=5432)
db_user = env.str("DB_USER", default="postgres")
db_password = env.str("DB_PASS", default="postgres")
 

I18N_DOMAIN = 'bot'
LOCALES_DIR = f'{DIR}\config\locales'

