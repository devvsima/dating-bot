from pathlib import Path
from environs import Env

DIR = Path(__file__).absolute().parent.parent

env = Env()
env.read_env()

#  tgbot
TG_TOKEN = env.str("TOKEN", default=None)
ADMINS = env.list("ADMINS", default=None, subcast=int)
MODERATOR_GROUP = env.int("MODERATOR_GROUP_ID", default=None)

# db
DB_NAME = env.str("DB_NAME", default=None)
DB_HOST = env.str("DB_HOST", default="localhost")
DB_PORT = env.int("DB_PORT", default=5432)
DB_USER = env.str("DB_USER", default="postgres")
DB_PASS = env.str("DB_PASS", default="postgres")

I18N_DOMAIN = 'bot'

IMAGES_DIR = fr"{DIR}/images" 
LOCALES_DIR = f'{DIR}/data/locales'