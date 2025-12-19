from db import db
from logger import logger
from models.channel import channel_document


async def add_channel(owner_id: int, chat):
    existing = await db.channels.find_one({
        "chat_id": chat.id,
        "owner_id": owner_id
    })
    if existing:
        return existing

    doc = channel_document(
        owner_id=owner_id,
        chat_id=chat.id,
        title=chat.title or "",
        chat_type=chat.type
    )

    await db.channels.insert_one(doc)
    logger.info(f"Channel added: {chat.id} by {owner_id}")
    return doc


async def get_user_channels(owner_id: int):
    return await db.channels.find({"owner_id": owner_id}).to_list(length=100)


async def toggle_auto_join(owner_id: int, chat_id: int, value: bool):
    await db.channels.update_one(
        {"owner_id": owner_id, "chat_id": chat_id},
        {"$set": {"auto_join": value}}
    )
