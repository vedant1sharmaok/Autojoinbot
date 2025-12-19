from db import db
from logger import logger
from models.welcome import welcome_document
from config import config


async def set_default_welcome(text: str):
    await db.welcome.delete_many({"is_default": True})
    await db.welcome.insert_one(
        welcome_document(
            chat_id=0,
            owner_id=config.OWNER_ID,
            text=text,
            approved=True,
            is_default=True
        )
    )
    logger.info("DEFAULT_WELCOME_UPDATED")


async def get_default_welcome():
    return await db.welcome.find_one({"is_default": True})


async def submit_custom_welcome(owner_id: int, chat_id: int, text: str):
    doc = welcome_document(
        chat_id=chat_id,
        owner_id=owner_id,
        text=text,
        approved=False
    )
    await db.welcome.insert_one(doc)
    logger.info(
        f"CUSTOM_WELCOME_SUBMITTED owner={owner_id} chat={chat_id}"
    )


async def approve_welcome(chat_id: int):
    await db.welcome.update_one(
        {"chat_id": chat_id, "approved": False},
        {"$set": {"approved": True}}
    )
    logger.info(f"WELCOME_APPROVED chat={chat_id}")


async def reject_welcome(chat_id: int):
    await db.welcome.delete_many(
        {"chat_id": chat_id, "approved": False}
    )
    logger.info(f"WELCOME_REJECTED chat={chat_id}")


async def get_effective_welcome(chat_id: int) -> str | None:
    """
    Priority:
    1. Approved custom welcome for this chat
    2. Owner default welcome
    """
    custom = await db.welcome.find_one(
        {"chat_id": chat_id, "approved": True}
    )
    if custom:
        return custom["text"]

    default = await get_default_welcome()
    if default:
        return default["text"]

    return None
