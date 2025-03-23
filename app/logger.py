import logging
from pythonjsonlogger.json import JsonFormatter

from app.config import settings

logger = logging.getLogger()

logHandler = logging.StreamHandler()
formatter = JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(settings.LOG_LEVEL)