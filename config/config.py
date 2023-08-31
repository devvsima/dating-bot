from pathlib import Path

from environs import Env

env = Env()
env.read_env()


DIR = Path(__file__).absolute().parent.parent

token_api = env.str("TOKEN", default=None)
admins_id = env.str("ADMINS", default=None)
