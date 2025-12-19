from aiogram.types import ChatJoinRequest
from db import db
from logger import logger


async def handle_join_request(request: ChatJoinRequest):
    channel = await db.channels.find_one({
        "chat_id": request.chat.id,
        "auto_join": True
    })

    if not channel:
        return

    try:
        await request.approve()
        await db.channels.update_one(
            {"chat_id": request.chat.id},
            {"$inc": {"stats.joins_accepted": 1}}
        )
        logger.info(f"Join approved: {request.user_chat_id}")
    except Exception:
        logger.exception("Failed to approve join request")
