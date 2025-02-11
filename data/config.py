from pathlib import Path

from environs import Env

DIR = Path(__file__).absolute().parent.parent

env = Env()
env.read_env()


# ---< Database >---
class DatabaseSettings:
    NAME: str = env.str("DB_NAME", default=None)
    HOST: str = env.str("DB_HOST", default="localhost")
    PORT: int = env.int("DB_PORT", default=5432)
    USER: str = env.str("DB_USER", default="postgres")
    PASS: str = env.str("DB_PASS", default="postgres")

    URL: str = env.str("DB_URL", default=f"sqlite+aiosqlite:///{DIR}/database/db.sqlite3")

    if all([NAME, HOST, PORT, USER, PASS]):
        URL = f"postgresql+asyncpg://{USER}:{PASS}@{HOST}:{PORT}/{NAME}"

    ECHO = False
    POOL_SIZE = 5
    MAX_OVERFLOW = 10


# ---< Redis >---
class RedisSettings:
    HOST: str = env.str("REDIS_HOST", default=None)
    PORT: int = env.int("REDIS_PORT", default=6379)
    DB: int = env.int("REDIS_DB", default=5)

    URL: str = env.str("RD_URL", default=None)

    if all([HOST, PORT, DB]):
        URL = f"redis://{HOST}:{PORT}/{DB}"


# ---< Telegram bot >---
BOT_TOKEN: str = env.str("TOKEN", default=None)
SKIP_UPDATES: bool = env.bool("SKIP_UPDATES", default=False)

ADMINS: list = env.list("ADMINS", default=None, subcast=int)
MODERATOR_GROUP: int = env.int("MODERATOR_GROUP_ID", default=None)

TIME_ZONE = "UTC"

I18N_DOMAIN = "bot"


# ---< Other >---
IMAGES_DIR = rf"{DIR}/images"
LOCALES_DIR = f"{DIR}/data/locales"

database = DatabaseSettings()
redis = RedisSettings()
