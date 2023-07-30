from pathlib import Path

from environs import Env

env = Env()
env.read_env()


DIR = Path(__file__).absolute().parent.parent

token_api = env.str("API", default=None)
