import asyncio
from db import db
from logger import logger
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest


SEND_DELAY = 0.05   # anti-flood base delay


async def _send_content(bot, user_id: int, content_type: str, content: dict):
    """
    Sends content based on type.
    Supports ALL Telegram message types.
    """
    if content_type == "text":
        await bot.send_message(user_id, content["text"])

    elif content_type == "photo":
        await bot.send_photo(user_id, content["file_id"], caption=content.get("caption"))

    elif content_type == "video":
        await bot.send_video(user_id, content["file_id"], caption=content.get("caption"))

    elif content_type == "audio":
        await bot.send_audio(user_id, content["file_id"], caption=content.get("caption"))

    elif content_type == "document":
        await bot.send_document(user_id, content["file_id"], caption=content.get("caption"))

    elif content_type == "voice":
        await bot.send_voice(user_id, content["file_id"])

    elif content_type == "animation":
        await bot.send_animation(user_id, content["file_id"], caption=content.get("caption"))

    else:
        raise ValueError("Unsupported broadcast content type")


async def deliver_broadcast(bot, broadcast: dict):
    """
    Main delivery entry point.
    """
    if broadcast["scope"] == "global":
        await _deliver_global(bot, broadcast)

    elif broadcast["scope"] == "channel":
        await _deliver_channel(bot, broadcast)

    await db.broadcasts.update_one(
        {"broadcast_id": broadcast["broadcast_id"]},
        {"$set": {"status": "sent"}}
    )


async def _deliver_global(bot, broadcast: dict):
    """
    Bot-owner broadcast → all users.
    """
    cursor = db.users.find({"blocked": {"$ne": True}})

    async for user in cursor:
        await _safe_send(
            bot,
            user["user_id"],
            broadcast
        )


async def _deliver_channel(bot, broadcast: dict):
    """
    Channel-owner broadcast → users of that channel only.
    """
    cursor = db.channel_users.find(
        {"chat_id": broadcast["target_chat_id"]}
    )

    async for item in cursor:
        await _safe_send(
            bot,
            item["user_id"],
            broadcast
        )


async def _safe_send(bot, user_id: int, broadcast: dict):
    """
    Safe send with retry + logging.
    """
    try:
        await _send_content(
            bot,
            user_id,
            broadcast["content_type"],
            broadcast["content"]
        )

        await db.broadcast_logs.insert_one({
            "broadcast_id": broadcast["broadcast_id"],
            "user_id": user_id,
            "status": "sent"
        })

        await asyncio.sleep(SEND_DELAY)

    except (TelegramForbiddenError, TelegramBadRequest) as e:
        await db.broadcast_logs.insert_one({
            "broadcast_id": broadcast["broadcast_id"],
            "user_id": user_id,
            "status": "failed",
            "error": str(e)
        })

        logger.warning(
            f"BROADCAST_SEND_FAILED broadcast={broadcast['broadcast_id']} user={user_id}"
                             )
