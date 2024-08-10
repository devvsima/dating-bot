from logging import getLogger
from data.config import DIR
from loguru import logger


logger.add(
    f"{DIR}/logs/logs.log", 
    format='[{time}] [{level}] [{file.name}:{line}]  {message}', 
    level='DEBUG', 
    rotation='1 week',
    compression='zip')

getLogger('aiogram').addFilter(lambda r: r.getMessage().find('Field \'database_user\' doesn\'t exist in') == -1)