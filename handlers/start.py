import db
from logger import logger
from config import config
from models.user import user_document


async def get_user(user_id: int):
    if db.db is None:
        raise RuntimeError("Database not initialized")
    return await db.db.users.find_one({"user_id": user_id})


async def create_user_if_not_exists(
    user_id: int | None = None,
    ref_by: int | None = None,
    telegram_id: int | None = None
):
    # Normalize ID (supports old & new callers)
    uid = telegram_id or user_id
    if uid is None:
        raise ValueError("User ID is required")

    user = await get_user(uid)

    # 🔒 HARD GUARANTEE: OWNER CAN NEVER BE BLOCKED
    if user:
        if uid == config.OWNER_ID:
            if user.get("role") != "owner":
                await db.db.users.update_one(
                    {"user_id": uid},
                    {"$set": {"role": "owner"}}
                )
                user["role"] = "owner"
                logger.warning(f"OWNER role enforced for {uid}")
        return user

    # New user
    role = "owner" if uid == config.OWNER_ID else "free"

    doc = user_document(uid, ref_by)
    doc["role"] = role

    await db.db.users.insert_one(doc)
    logger.info(f"New user registered: {uid} ({role})")

    return doc


# Used by other flows (SAFE)
async def register_user(user):
    return await create_user_if_not_exists(
        telegram_id=user.id,
        ref_by=None
    )


# ❗ MUST BE SYNC (logic-only helpers)
def is_blocked(user: dict) -> bool:
    return user.get("role") == "blocked"


def is_restricted(user: dict) -> bool:
    return user.get("role") == "restricted"
