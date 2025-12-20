from aiogram import Router, F
from aiogram.types import Message
from datetime import datetime
from db import db
from logger import logger
from services.broadcast_scheduler import schedule_broadcast
from services.premium_service import get_user_premium

router = Router()


@router.message(F.text.startswith("/schedule_broadcast"))
async def schedule_broadcast_cmd(message: Message):
    """
    Usage:
    /schedule_broadcast BROADCAST_ID YYYY-MM-DD HH:MM
    """
    try:
        parts = message.text.split()
        broadcast_id = parts[1]
        date_str = parts[2]
        time_str = parts[3]

        run_at = datetime.strptime(
            f"{date_str} {time_str}", "%Y-%m-%d %H:%M"
        )

        premium = await get_user_premium(message.from_user.id)
        if not premium["limits"]["can_schedule"]:
            await message.answer("❌ Scheduling is a premium feature")
            return

        broadcast = await db.broadcasts.find_one(
            {"broadcast_id": broadcast_id}
        )

        if not broadcast:
            await message.answer("❌ Broadcast not found")
            return

        await schedule_broadcast(broadcast_id, run_at)

        await message.answer(
            f"✅ Broadcast scheduled for {run_at}"
        )

        logger.info(
            f"BROADCAST_SCHEDULE_REQUEST user={message.from_user.id} id={broadcast_id}"
        )

    except Exception:
        logger.exception("SCHEDULE_BROADCAST_FAILED")
        await message.answer("❌ Invalid format")
