import asyncio
from datetime import datetime
from db import db
from logger import logger
from services.broadcast_delivery import deliver_broadcast
from services.premium_service import get_user_premium
from models.premium_plans import PremiumPlan


CHECK_INTERVAL = 30  # seconds


async def schedule_broadcast(broadcast_id: str, run_at: datetime):
    """
    Save broadcast schedule.
    """
    await db.broadcasts.update_one(
        {"broadcast_id": broadcast_id},
        {
            "$set": {
                "scheduled_at": run_at,
                "status": "scheduled"
            }
        }
    )

    logger.info(
        f"BROADCAST_SCHEDULED id={broadcast_id} at={run_at}"
    )


async def scheduler_worker(bot):
    """
    Background worker.
    Must be started once at bot startup.
    """
    while True:
        now = datetime.utcnow()

        cursor = db.broadcasts.find({
            "status": "scheduled",
            "scheduled_at": {"$lte": now}
        })

        async for broadcast in cursor:
            try:
                await db.broadcasts.update_one(
                    {"broadcast_id": broadcast["broadcast_id"]},
                    {"$set": {"status": "approved"}}
                )

                await deliver_broadcast(bot, broadcast)

                logger.info(
                    f"BROADCAST_EXECUTED id={broadcast['broadcast_id']}"
                )

            except Exception as e:
                logger.exception(
                    f"SCHEDULED_BROADCAST_FAILED id={broadcast['broadcast_id']}"
                )

        await asyncio.sleep(CHECK_INTERVAL)
