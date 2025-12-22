from db import db
from logger import logger
from models.credits import CREDIT_RULES


async def register_referral(referrer_id: int, new_user_id: int):
    """
    Called when a new user starts the bot with a referral code.
    """
    if referrer_id == new_user_id:
        return  # self-referral blocked

    existing = await db.referrals.find_one({"user_id": new_user_id})
    if existing:
        return  # referral already registered

    await db.referrals.insert_one({
        "referrer_id": referrer_id,
        "user_id": new_user_id,
        "completed": False
    })

    logger.info(f"REFERRAL_REGISTERED {referrer_id} -> {new_user_id}")


async def complete_referral(new_user_id: int):
    """
    Marks referral as complete and awards credits.
    Called AFTER required joins / conditions are satisfied.
    """
    referral = await db.referrals.find_one({
        "user_id": new_user_id,
        "completed": False
    })

    if not referral:
        return

    credits = CREDIT_RULES["referral_join"]

    await db.credits.update_one(
        {"user_id": referral["referrer_id"]},
        {"$inc": {"balance": credits}},
        upsert=True
    )

    await db.referrals.update_one(
        {"user_id": new_user_id},
        {"$set": {"completed": True}}
    )

    logger.info(
        f"REFERRAL_COMPLETED referrer={referral['referrer_id']} +{credits}"
    )
