import time
from db import db
from logger import logger

START_TIME = time.time()


async def get_uptime_seconds() -> int:
    return int(time.time() - START_TIME)


async def db_health() -> bool:
    try:
        # Lightweight ping
        await db.command("ping")
        return True
    except Exception as e:
        logger.error(f"DB_HEALTH_FAIL {e}")
        return False


async def bot_health() -> dict:
    """
    Aggregate health snapshot
    """
    return {
        "uptime_seconds": await get_uptime_seconds(),
        "db_ok": await db_health(),
    }
