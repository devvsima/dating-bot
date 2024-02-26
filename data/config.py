from pathlib import Path
from environs import Env

DIR = Path(__file__).absolute().parent.parent

env = Env()
env.read_env()

#  tgbot
token_api = env.str("TOKEN", default=None)
banned_users = env.list("BANED", default=None, subcast=int)
admins = env.list("ADMINS", default=None, subcast=int)

# db
DB_NAME = env.str("DB_NAME", default=None)
DB_HOST = env.str("DB_HOST", default="localhost")
DB_PORT = env.int("DB_PORT", default=5432)
DB_USER = env.str("DB_USER", default="postgres")
DB_PASS = env.str("DB_PASS", default="postgres")
RATE_LIMIT = env.int("RATE_LIMIT", default=5)

I18N_DOMAIN = 'bot'
LOCALES_DIR = f'{DIR}\config\locales'

