from datetime import datetime
from uuid import uuid4


def broadcast_document(
    owner_id: int,
    scope: str,           # "channel" | "global"
    target_chat_id: int | None,
    content_type: str,    # text, photo, video, document, etc.
    content: dict
):
    return {
        "broadcast_id": str(uuid4()),
        "owner_id": owner_id,
        "scope": scope,
        "target_chat_id": target_chat_id,
        "content_type": content_type,
        "content": content,
        "status": "pending",   # pending | approved | rejected | sent
        "reason": None,
        "created_at": datetime.utcnow(),
        "approved_at": None
    }
