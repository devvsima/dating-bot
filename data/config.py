from pathlib import Path

from environs import Env

env = Env()
env.read_env()


DIR = Path(__file__).absolute().parent.parent

token_api = env.str("TOKEN", default=None)
banned_users = env.str("BANED", default=None)
admins = env.str("ADMINS", default=None)
mongodb_url = env.str("MONGODB_URL", default=None)

I18N_DOMAIN = 'bot'
LOCALES_DIR = f'{DIR}\config\locales'

