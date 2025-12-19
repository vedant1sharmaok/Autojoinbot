from datetime import datetime, timedelta
from db import db
from models.premium_plans import PremiumPlan
from services.premium_service import get_user_premium


async def _reset_if_needed(record: dict) -> dict:
    """
    Resets daily usage counters.
    """
    now = datetime.utcnow()

    if record["reset_at"] <= now:
        record["count"] = 0
        record["reset_at"] = now + timedelta(days=1)

    return record


async def can_send_broadcast(user_id: int) -> bool:
    """
    Checks if user can send a broadcast today.
    """
    premium = await get_user_premium(user_id)
    limit = premium["limits"]["broadcast_limit_per_day"]

    record = await db.broadcast_limits.find_one(
        {"user_id": user_id}
    )

    if not record:
        await db.broadcast_limits.insert_one({
            "user_id": user_id,
            "count": 0,
            "reset_at": datetime.utcnow() + timedelta(days=1)
        })
        return True

    record = await _reset_if_needed(record)

    return record["count"] < limit


async def increment_broadcast_usage(user_id: int):
    """
    Increments usage after successful broadcast submission.
    """
    record = await db.broadcast_limits.find_one(
        {"user_id": user_id}
    )

    if not record:
        await db.broadcast_limits.insert_one({
            "user_id": user_id,
            "count": 1,
            "reset_at": datetime.utcnow() + timedelta(days=1)
        })
        return

    record = await _reset_if_needed(record)

    await db.broadcast_limits.update_one(
        {"user_id": user_id},
        {"$set": {"count": record["count"] + 1, "reset_at": record["reset_at"]}}
  )
