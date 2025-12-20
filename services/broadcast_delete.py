from db import db
from logger import logger


async def delete_broadcast_globally(bot, broadcast_id: str):
    """
    Deletes a broadcast message from all chats where it was sent.
    Owner-only operation.
    """
    logs = db.broadcast_logs.find(
        {"broadcast_id": broadcast_id, "status": "sent"}
    )

    deleted = 0
    failed = 0

    async for entry in logs:
        try:
            await bot.delete_message(
                chat_id=entry["user_id"],
                message_id=entry["message_id"]
            )
            deleted += 1
        except Exception:
            failed += 1

    await db.broadcasts.update_one(
        {"broadcast_id": broadcast_id},
        {"$set": {"status": "deleted"}}
    )

    logger.warning(
        f"BROADCAST_GLOBAL_DELETE id={broadcast_id} deleted={deleted} failed={failed}"
    )
