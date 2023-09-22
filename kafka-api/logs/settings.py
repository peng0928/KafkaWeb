import os
import time
from loguru import logger

# -----------------------系统调试------------------------------------
DEBUG = True
# -----------------------日志-----------------------------------------
LOG_DIR = os.path.join(
    os.getcwd(), f'kafka-api\logs\log\{time.strftime("%Y-%m-%d")}.log')
LOG_FORMAT = '<level>{level: <8}</level>  <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>'

logger.add(LOG_DIR, rotation='0:00', enqueue=True,
           serialize=False, encoding="utf-8", retention="1 days")
logger.debug("服务器Start.")
loggers = logger
