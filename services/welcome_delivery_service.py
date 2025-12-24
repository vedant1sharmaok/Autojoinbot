from typing import Optional
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from logger import logger

# ✅ Correct DB import (runtime-safe)
import db


async def attempt_direct_welcome(
    bot: Bot,
    user_id: int,
    message: str,
    channel_id: Optional[int] = None
) -> bool:
    """
    Try to send welcome message directly.
    If user cannot be messaged, store it for later delivery.
    """

    try:
        await bot.send_message(
            chat_id=user_id,
            text=message,
            disable_web_page_preview=True
        )
        logger.info(f"Direct welcome sent to user {user_id}")
        return True

    except TelegramForbiddenError:
        # User has not started bot / DMs closed
        logger.info(
            f"User {user_id} unreachable, queueing welcome"
        )
        await queue_pending_welcome(
            user_id=user_id,
            message=message,
            channel_id=channel_id
        )
        return False

    except Exception as e:
        logger.error(
            f"Unexpected error sending welcome to {user_id}: {e}"
        )
        return False


async def deliver_pending_welcomes(
    bot: Bot,
    user_id: int
):
    """
    Deliver all pending welcome messages when user becomes reachable.
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
    Store welcome message for later delivery.
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
