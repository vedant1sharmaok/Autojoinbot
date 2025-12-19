from db import db
from logger import logger
from config import config
from models.user import user_document


async def get_user(user_id: int):
    return await db.users.find_one({"user_id": user_id})


async def create_user_if_not_exists(user_id: int, ref_by: int | None = None):
    user = await get_user(user_id)

    if user:
        return user

    role = "owner" if user_id == config.OWNER_ID else "free"

    doc = user_document(user_id, ref_by)
    doc["role"] = role

    await db.users.insert_one(doc)
    logger.info(f"New user registered: {user_id} ({role})")

    return doc


async def is_blocked(user: dict) -> bool:
    return user["role"] == "blocked"


async def is_restricted(user: dict) -> bool:
    return user["role"] == "restricted"
