from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from db import db
from logger import logger
from models.pending_welcome import pending_welcome_document


async def attempt_direct_welcome(bot, user_id: int, chat_id: int, text: str) -> bool:
    """
    Try to DM user immediately after join approval.
    Returns True if delivered, False if fallback required.
    """
    try:
        await bot.send_message(user_id, text)
        logger.info(
            f"WELCOME_DM_DIRECT_SUCCESS user={user_id} chat={chat_id}"
        )
        return True

    except (TelegramForbiddenError, TelegramBadRequest):
        await db.pending_welcomes.insert_one(
            pending_welcome_document(
                user_id=user_id,
                chat_id=chat_id,
                text=text
            )
        )
        logger.warning(
            f"WELCOME_DM_PENDING_STORED user={user_id} chat={chat_id}"
        )
        return False


async def deliver_pending_welcomes(bot, user_id: int):
    """
    Deliver all pending welcomes when user starts bot.
    """
    cursor = db.pending_welcomes.find(
        {"user_id": user_id, "delivered": False}
    )

    async for item in cursor:
        try:
            await bot.send_message(user_id, item["text"])
            await db.pending_welcomes.update_one(
                {"_id": item["_id"]},
                {"$set": {"delivered": True}}
            )
            logger.info(
                f"WELCOME_DM_PENDING_DELIVERED user={user_id}"
            )
        except Exception as e:
            logger.error(
                f"WELCOME_DM_PENDING_FAILED user={user_id} error={e}"
            )
