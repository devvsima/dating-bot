from pathlib import Path

from aiogram.types import FSInputFile
from environs import Env

DIR = Path(__file__).absolute().parent.parent

env = Env()
env.read_env()


# -< Telegram bot >-
class TelegramBotSettings:
    BOT_TOKEN: str = env.str("TELEGRAM_BOT_TOKEN", default=None)
    SKIP_UPDATES: bool = env.bool("SKIP_UPDATES", default=False)
    SET_COMMANDS: bool = env.bool("SET_COMMANDS", default=True)

    # Throtling
    RATE_LIMIT: int = env.int("RATE_LIMIT", default=3)
    TIME_WINDOW: int = env.int("TIME_WINDOW", default=1)

    # Admin
    ADMINS: list = env.list("ADMINS", default=None, subcast=int)
    NEW_USER_ALET_TO_GROUP: bool = env.bool("NEW_USER_ALET_TO_GROUP", default=True)
    MODERATOR_GROUP_ID: int = env.int("MODERATOR_GROUP_ID", default=None)
    BOT_CHANNEL_URL: str = env.str("BOT_CHANNEL_URL", default=None)

    # Webhook
    WEBHOOK_HOST: str = env.str("WEBHOOK_HOST", default=None)
    WEBHOOK_PORT: int = env.int("WEBHOOK_PORT", default=None)
    WEBHOOK_URL: str = env.str("WEBHOOK_URL", default=None)
    WEBHOOK_SECRET: str = env.str("WEBHOOK_SECRET", default=None)

    WEBHOOK_PATH: str = env.str("WEBHOOK_PATH", default=f"/webhook/{BOT_TOKEN}")

    IS_WEBHOOK = False
    if all((WEBHOOK_HOST, WEBHOOK_PORT, WEBHOOK_URL, WEBHOOK_SECRET, WEBHOOK_PATH)):
        IS_WEBHOOK = True

    # Other
    TIME_ZONE = "UTC"
    I18N_DOMAIN = "bot"


# -< Webрр >-
class WebAppSettings:
    HOST: str = env.str("WEBAPP_HOST", default="localhost")
    PORT: int = env.int("WEBAPP_PORT", default=8080)
    DOMEN: str = env.str("WEBAPP_DOMEN", default=None)

    # API Access Token для тестирования (без Telegram WebApp)
    ACCESS_TOKEN: str = env.str("API_ACCESS_TOKEN", default=None)

    URL: str = env.str("WEBAPP_URL", default=None)
    if not URL:
        if all((HOST, PORT, DOMEN)):
            URL = f"https://{DOMEN}/"


# -< Database >-
class DatabaseSettings:
    NAME: str = env.str("DB_NAME", default=None)
    HOST: str = env.str("DB_HOST", default="localhost")
    PORT: int = env.int("DB_PORT", default=5432)
    USER: str = env.str("DB_USER", default="postgres")
    PASS: str = env.str("DB_PASS", default="postgres")

    URL: str = env.str("DB_URL", default=f"sqlite+aiosqlite:///{DIR}/database/db.sqlite3")
    if not URL:
        if all((NAME, HOST, PORT, USER, PASS)):
            URL = f"postgresql+asyncpg://{USER}:{PASS}@{HOST}:{PORT}/{NAME}"

    ECHO: bool = env.bool("ECHO", default=False)
    POOL_SIZE: int = env.int("POOL_SIZE", default=12)
    MAX_OVERFLOW: int = env.int("MAX_OVERFLOW", default=18)


# -< Redis >-
class RedisSettings:
    DB: int = env.int("REDIS_DB", default=5)
    HOST: str = env.str("REDIS_HOST", default=None)
    PORT: int = env.int("REDIS_PORT", default=6379)
    USER: int = env.int("REDIS_USER", default="default")
    PASS: int = env.str("REDIS_PASS", default=None)

    URL: str = env.str("RD_URL", default=None)
    if not URL:
        if all((DB, HOST, PORT)):
            URL = f"redis://{HOST}:{PORT}/{DB}"
            if all((USER, PASS)):
                URL = f"redis://{USER}:{PASS}@{HOST}:{PORT}/{DB}"


# -< Search >-
class SearchSettings:
    INITIAL_DISTANCE: float = env.float("INITIAL_DISTANCE", default=200.0)  # Стартовый радиус
    MAX_DISTANCE: float = env.float("MAX_DISTANCE", default=10000.0)  # Максимальный радиус
    RADIUS_STEP: float = env.float("RADIUS_STEP", default=200.0)  # Шаг увеличения радиуса
    MIN_PROFILES: int = env.int("MIN_PROFILES", default=100)  # Минимальное количество анкет
    EARTH_RADIUS: int = env.int("EARTH_RADIUS", default=6371)  # Радиус Земли
    BLOCK_SIZE: float = env.float("BLOCK_SIZE", default=15.0)  # Размер блока для перемешивания

    AGE_RANGE_MULTIPLIER: float = env.float(
        "AGE_RANGE_MULTIPLIER", default=0.15
    )  # Коэффициент для расчета диапазона
    MIN_AGE_RANGE: int = env.int("MIN_AGE_RANGE", default=2)  # Минимальный возрастной диапазон
    MAX_AGE_RANGE: int = env.int("MAX_AGE_RANGE", default=15)  # Максимальный возрастной диапазон


# -< Path\Dir >-
IMAGES_DIR: Path = DIR / "images"

LOGO_FILE_ID: str = env.str("LOGO_FILE_ID", default=f"None")
LOGO_DIR = f"{IMAGES_DIR}/send_logo.png"
LOGO = LOGO_FILE_ID if LOGO_FILE_ID else FSInputFile(LOGO_DIR)

GRAPH_FILE_PATH: Path = IMAGES_DIR / "stats_graph.png"

LOCALES_DIR: Path = DIR / "data" / "locales"

LOG_FILE_PATH: Path = DIR / "logs" / "logs.log"

# -< Other >-
database = DatabaseSettings()
redis = RedisSettings()
tgbot = TelegramBotSettings()
webapp = WebAppSettings()
search = SearchSettings()
