from datetime import datetime


def pending_welcome_document(
    user_id: int,
    chat_id: int,
    text: str
):
    return {
        "user_id": user_id,
        "chat_id": chat_id,
        "text": text,
        "created_at": datetime.utcnow(),
        "delivered": False
    }
