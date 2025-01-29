from pathlib import Path
from environs import Env

DIR = Path(__file__).absolute().parent.parent

env = Env()
env.read_env()

# ---< Telegram bot >---
TG_TOKEN: str = env.str("TOKEN", default=None)
ADMINS: list = env.list("ADMINS", default=None, subcast=int)
MODERATOR_GROUP: int = env.int("MODERATOR_GROUP_ID", default=None)
SKIP_UPDATES: bool = True

# ---< Database >---
DB_NAME: str = env.str("DB_NAME", default=None)
DB_HOST: str = env.str("DB_HOST", default="localhost")
DB_PORT: int = env.int("DB_PORT", default=5432)
DB_USER: str = env.str("DB_USER", default="postgres")
DB_PASS: str = env.str("DB_PASS", default="postgres")

# ---< Redis >---
REDIS_HOST: str = env.str("REDIS_HOST", default=None)
REDIS_PORT: int = env.int("REDIS_PORT", default=6379)
REDIS_DB: int = env.int("REDIS_DB", default=5)

REDIS_URL: str = env.str("RD_URI", default=None)

if all([REDIS_DB, REDIS_HOST, REDIS_PORT]):
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

# ---< Other >---
I18N_DOMAIN = "bot"

IMAGES_DIR = rf"{DIR}/images"
LOCALES_DIR = f"{DIR}/data/locales"
