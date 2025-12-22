from db import db
from logger import logger


async def restrict_user(user_id: int, reason: str | None = None):
    await db.users.update_one(
        {"user_id": user_id},
        {"$set": {"restricted": True}},
        upsert=True
    )

    logger.warning(
        f"USER_RESTRICTED user={user_id} reason={reason}"
    )


async def unrestrict_user(user_id: int):
    await db.users.update_one(
        {"user_id": user_id},
        {"$unset": {"restricted": ""}}
    )

    logger.info(f"USER_UNRESTRICTED user={user_id}")


async def block_user(user_id: int, reason: str | None = None):
    await db.users.update_one(
        {"user_id": user_id},
        {"$set": {"blocked": True}},
        upsert=True
    )

    logger.critical(
        f"USER_BLOCKED user={user_id} reason={reason}"
    )


async def grant_premium(
    user_id: int,
    plan: str,
    expires_at: int | None = None
):
    await db.users.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "is_premium": True,
                "premium_plan": plan,
                "premium_expires": expires_at
            }
        },
        upsert=True
    )

    logger.info(
        f"PREMIUM_GRANTED user={user_id} plan={plan}"
    )


async def revoke_premium(user_id: int, reason: str | None = None):
    await db.users.update_one(
        {"user_id": user_id},
        {
            "$unset": {
                "is_premium": "",
                "premium_plan": "",
                "premium_expires": ""
            }
        }
    )

    logger.warning(
        f"PREMIUM_REVOKED user={user_id} reason={reason}"
    )
