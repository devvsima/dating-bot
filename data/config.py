from pathlib import Path

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
    RATE_LIMIT: int = env.int("RATE_LIMIT", default=2)
    TIME_WINDOW: int = env.int("TIME_WINDOW", default=1)

    # Admin
    ADMINS: list = env.list("ADMINS", default=None, subcast=int)
    NEW_USER_ALET_TO_GROUP: bool = env.bool("NEW_USER_ALET_TO_GROUP", default=True)
    MODERATOR_GROUP_ID: int = env.int("MODERATOR_GROUP_ID", default=None)
    BOT_CHANNEL_URL: str = env.str("BOT_CHANNEL_URL", default=None)

    # Other
    TIME_ZONE = "UTC"
    I18N_DOMAIN = "bot"


# -< Webapp >-
class WebAppSettings:
    HOST: str = env.str("WEBAPP_HOST", default="localhost")
    PORT: int = env.int("WEBAPP_PORT", default=8080)
    DOMEN: str = env.str("WEBAPP_DOMEN", default=None)

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
LOGO_DIR = f"{IMAGES_DIR}/logo.png"

GRAPH_FILE_PATH: Path = IMAGES_DIR / "stats_graph.png"

LOCALES_DIR: Path = DIR / "data" / "locales"

LOG_FILE_PATH: Path = DIR / "logs" / "logs.log"

# -< Other >-
database = DatabaseSettings()
redis = RedisSettings()
tgbot = TelegramBotSettings()
webapp = WebAppSettings()
search = SearchSettings()
