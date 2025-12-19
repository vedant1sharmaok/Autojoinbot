from datetime import datetime, timedelta
from db import db
from logger import logger
from models.premium_plans import PremiumPlan, PREMIUM_PLANS


async def get_user_premium(user_id: int) -> dict:
    """
    Returns active premium record or FREE plan.
    """
    premium = await db.premium.find_one(
        {"user_id": user_id, "active": True}
    )

    if not premium:
        return {
            "plan": PremiumPlan.FREE,
            "expires_at": None,
            "limits": PREMIUM_PLANS[PremiumPlan.FREE]
        }

    if premium["expires_at"] and premium["expires_at"] < datetime.utcnow():
        await revoke_premium(
            user_id,
            reason="Expired"
        )
        return {
            "plan": PremiumPlan.FREE,
            "expires_at": None,
            "limits": PREMIUM_PLANS[PremiumPlan.FREE]
        }

    return {
        "plan": premium["plan"],
        "expires_at": premium["expires_at"],
        "limits": PREMIUM_PLANS[premium["plan"]]
    }


async def grant_premium(
    user_id: int,
    plan: PremiumPlan,
    duration_days: int,
    granted_by: int,
    reason: str = None
):
    """
    Owner/manual grant or payment success.
    """
    expires_at = datetime.utcnow() + timedelta(days=duration_days)

    await db.premium.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "user_id": user_id,
                "plan": plan,
                "active": True,
                "expires_at": expires_at,
                "granted_by": granted_by,
                "reason": reason,
                "updated_at": datetime.utcnow()
            }
        },
        upsert=True
    )

    logger.info(
        f"PREMIUM_GRANTED user={user_id} plan={plan} days={duration_days}"
    )


async def revoke_premium(
    user_id: int,
    revoked_by: int = None,
    reason: str = None
):
    """
    Owner revoke or auto-expiry.
    """
    await db.premium.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "active": False,
                "revoked_by": revoked_by,
                "revoke_reason": reason,
                "revoked_at": datetime.utcnow()
            }
        }
    )

    logger.info(
        f"PREMIUM_REVOKED user={user_id} reason={reason}"
    )


async def is_premium(user_id: int) -> bool:
    data = await get_user_premium(user_id)
    return data["plan"] != PremiumPlan.FREE
