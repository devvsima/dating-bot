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

    if all((NAME, HOST, PORT, USER, PASS)):
        URL = f"postgresql+asyncpg://{USER}:{PASS}@{HOST}:{PORT}/{NAME}"

    ECHO = False
    POOL_SIZE = 5
    MAX_OVERFLOW = 10


# ---< Redis >---
class RedisSettings:
    DB: int = env.int("REDIS_DB", default=5)
    HOST: str = env.str("REDIS_HOST", default=None)
    PORT: int = env.int("REDIS_PORT", default=6379)
    USER: int = env.int("REDIS_USER", default="default")
    PASS: int = env.int("REDIS_PASS", default=None)

    URL: str = env.str("RD_URL", default=None)

    if all((DB, HOST, PORT)):
        URL = f"redis://{HOST}:{PORT}/{DB}"
        if all((USER, PASS)):
            URL = f"redis://{USER}:{PASS}@{HOST}:{PORT}/{DB}"


# ---< Telegram bot >---
BOT_TOKEN: str = env.str("TELEGRAM_BOT_TOKEN", default=None)
SKIP_UPDATES: bool = env.bool("SKIP_UPDATES", default=False)
NEW_USER_ALET_TO_GROUP: bool = env.bool("NEW_USER_ALET_TO_GROUP", default=True)

ADMINS: list = env.list("ADMINS", default=None, subcast=int)
MODERATOR_GROUP: int = env.int("MODERATOR_GROUP_ID", default=None)
BOT_CHANNEL_URL: str = env.str("BOT_CHANNEL_URL", default=None)

TIME_ZONE = "UTC"

I18N_DOMAIN = "bot"

# ---< Search >---
AGE_RANGE: int = env.int("AGE_RANGE", default=4)
INITIAL_DISTANCE: float = env.str("INITIAL_DISTANCE", default=200.0)  # Стартовый радиус
MAX_DISTANCE: float = env.int("MAX_DISTANCE", default=10000.0)  # Максимальный радиус
RADIUS_STEP: float = env.int("RADIUS_STEP", default=200.0)  # Шаг увеличения радиуса
MIN_PROFILES: int = env.int("MIN_PROFILES", default=100)  # Минимальное количество анкет
RADIUS: int = env.int("RADIUS", default=6371)  # Радиус Земли
BLOCK_SIZE: float = env.float("BLOCK_SIZE", default=50.0)  # Размер блока для перемешивания

# ---< Path\Dir >---
IMAGES_DIR: Path = DIR / "images"
LOGO_DIR = f"{IMAGES_DIR}/logo.png"

GRAPH_FILE_PATH: Path = IMAGES_DIR / "stats_graph.png"

LOCALES_DIR: Path = DIR / "data" / "locales"

LOG_FILE_PATH: Path = DIR / "logs" / "logs.log"

# ---< Other >---
database = DatabaseSettings()
redis = RedisSettings()
