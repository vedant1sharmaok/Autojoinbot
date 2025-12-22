from db import db
from logger import logger
from models.credits import CreditSource


async def get_balance(user_id: int) -> int:
    record = await db.credits.find_one({"user_id": user_id})
    return record["balance"] if record else 0


async def add_credits(
    user_id: int,
    amount: int,
    source: CreditSource,
    meta: dict | None = None
):
    if amount <= 0:
        return

    await db.credits.update_one(
        {"user_id": user_id},
        {
            "$inc": {"balance": amount},
            "$push": {
                "history": {
                    "amount": amount,
                    "source": source,
                    "meta": meta
                }
            }
        },
        upsert=True
    )

    logger.info(
        f"CREDITS_ADD user={user_id} amount={amount} source={source}"
    )


async def deduct_credits(user_id: int, amount: int) -> bool:
    """
    Returns True if deduction succeeded.
    """
    record = await db.credits.find_one({"user_id": user_id})

    if not record or record["balance"] < amount:
        return False

    await db.credits.update_one(
        {"user_id": user_id},
        {"$inc": {"balance": -amount}}
    )

    logger.info(
        f"CREDITS_DEDUCT user={user_id} amount={amount}"
    )
    return True
