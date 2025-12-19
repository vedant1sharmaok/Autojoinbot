from db import db
from logger import logger
from models.broadcast import broadcast_document
from datetime import datetime


async def create_broadcast(
    owner_id: int,
    scope: str,
    target_chat_id: int | None,
    content_type: str,
    content: dict
):
    doc = broadcast_document(
        owner_id=owner_id,
        scope=scope,
        target_chat_id=target_chat_id,
        content_type=content_type,
        content=content
    )
    await db.broadcasts.insert_one(doc)
    logger.info(
        f"BROADCAST_CREATED id={doc['broadcast_id']} owner={owner_id}"
    )
    return doc


async def approve_broadcast(broadcast_id: str):
    await db.broadcasts.update_one(
        {"broadcast_id": broadcast_id},
        {
            "$set": {
                "status": "approved",
                "approved_at": datetime.utcnow()
            }
        }
    )
    logger.info(f"BROADCAST_APPROVED id={broadcast_id}")


async def reject_broadcast(broadcast_id: str, reason: str):
    await db.broadcasts.update_one(
        {"broadcast_id": broadcast_id},
        {
            "$set": {
                "status": "rejected",
                "reason": reason
            }
        }
    )
    logger.info(f"BROADCAST_REJECTED id={broadcast_id}")


async def get_pending_broadcast(broadcast_id: str):
    return await db.broadcasts.find_one(
        {"broadcast_id": broadcast_id, "status": "pending"}
              )
