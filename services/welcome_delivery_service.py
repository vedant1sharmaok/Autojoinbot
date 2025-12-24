from typing import Optional
from aiogram import Bot
from logger import logger
import db


async def deliver_pending_welcomes(
    bot: Bot,
    user_id: int
):
    """
    Deliver all pending welcome messages to a user
    when they start the bot or become reachable.
    """

    if not db.db:
        logger.error("DB not initialized while delivering pending welcomes")
        return

    cursor = db.db.pending_welcomes.find(
        {"user_id": user_id}
    )

    async for item in cursor:
        try:
            await bot.send_message(
                chat_id=user_id,
                text=item["message"],
                disable_web_page_preview=True
            )

            # Remove after successful delivery
            await db.db.pending_welcomes.delete_one(
                {"_id": item["_id"]}
            )

            logger.info(
                f"Delivered pending welcome to user {user_id}"
            )

        except Exception as e:
            logger.error(
                f"Failed to deliver pending welcome to {user_id}: {e}"
            )


async def queue_pending_welcome(
    user_id: int,
    message: str,
    channel_id: Optional[int] = None
):
    """
    Store welcome message for later delivery
    if user cannot be messaged immediately.
    """

    if not db.db:
        logger.error("DB not initialized while queueing welcome")
        return

    await db.db.pending_welcomes.insert_one(
        {
            "user_id": user_id,
            "message": message,
            "channel_id": channel_id
        }
    )

    logger.info(
        f"Queued pending welcome for user {user_id}"
    )
    
