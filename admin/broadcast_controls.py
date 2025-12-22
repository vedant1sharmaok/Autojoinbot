from db import db
from logger import logger
from services.broadcast_delete import delete_broadcast_globally


async def list_broadcasts(limit: int = 50):
    broadcasts = []
    async for b in db.broadcasts.find({}).sort("created_at", -1).limit(limit):
        broadcasts.append(b)
    return broadcasts


async def stop_broadcast(broadcast_id: str):
    """
    Emergency stop (prevents further delivery)
    """
    await db.broadcasts.update_one(
        {"broadcast_id": broadcast_id},
        {"$set": {"status": "stopped"}}
    )

    logger.critical(f"BROADCAST_STOPPED id={broadcast_id}")


async def delete_broadcast(broadcast_id: str, bot):
    """
    Full delete from all user chats
    """
    await delete_broadcast_globally(bot, broadcast_id)

    logger.critical(f"BROADCAST_DELETED id={broadcast_id}")
