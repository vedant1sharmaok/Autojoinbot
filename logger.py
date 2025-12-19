import sys
from loguru import logger
from config import config

logger.remove()

logger.add(
    sys.stdout,
    level=config.LOG_LEVEL,
    format="<green>{time}</green> | "
           "<level>{level}</level> | "
           "<cyan>{name}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>",
)
