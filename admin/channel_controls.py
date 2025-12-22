from db import db
from logger import logger


async def get_user_channels(user_id: int):
    """
    List all channels added by a specific user
    """
    channels = []
    async for ch in db.channels.find({"owner_id": user_id}):
        channels.append(ch)
    return channels


async def disable_channel(channel_id: int, reason: str | None = None):
    await db.channels.update_one(
        {"channel_id": channel_id},
        {"$set": {"disabled": True}}
    )

    logger.warning(
        f"CHANNEL_DISABLED channel={channel_id} reason={reason}"
    )


async def enable_channel(channel_id: int):
    await db.channels.update_one(
        {"channel_id": channel_id},
        {"$unset": {"disabled": ""}}
    )

    logger.info(f"CHANNEL_ENABLED channel={channel_id}")


async def reset_welcome_message(channel_id: int):
    """
    Revert channel welcome message to owner default
    """
    await db.channels.update_one(
        {"channel_id": channel_id},
        {"$unset": {"welcome_message": ""}}
    )

    logger.info(f"WELCOME_RESET channel={channel_id}")
