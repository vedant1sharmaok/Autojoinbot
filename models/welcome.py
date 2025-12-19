from datetime import datetime


def welcome_document(
    chat_id: int,
    owner_id: int,
    text: str,
    approved: bool,
    is_default: bool = False
):
    return {
        "chat_id": chat_id,
        "owner_id": owner_id,
        "text": text,
        "approved": approved,
        "is_default": is_default,
        "created_at": datetime.utcnow()
    }
