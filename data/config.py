from pathlib import Path
from environs import Env

DIR = Path(__file__).absolute().parent.parent

env = Env()
env.read_env()

#  tgbot
token_api = env.str("TOKEN", default=None)
banned_users = env("BANED", default=None)
admins = [env("ADMINS", default=None)]

# mongodb
mongo_host = env.str("MONGO_HOST", default=None)
mongo_port = env.int("MONGH_PORT", default=27017)
mongo_user = env.str("MONGO_USER", default=None)
mongo_password = env.str("MONGO_PASS", default=None)
auth_source = env.str("AUTH_SOURC", default=None)

if not mongo_host:
    mongodb_url = f'mongodb://localhost:{mongo_port}/'
else:
    mongodb_url = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{auth_source}"

 

I18N_DOMAIN = 'bot'
LOCALES_DIR = f'{DIR}\config\locales'

