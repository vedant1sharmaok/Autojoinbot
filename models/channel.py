from datetime import datetime


def channel_document(owner_id: int, chat_id: int, title: str, chat_type: str):
    return {
        "chat_id": chat_id,
        "owner_id": owner_id,
        "title": title,
        "type": chat_type,          # channel | group | supergroup
        "auto_join": True,
        "created_at": datetime.utcnow(),
        "stats": {
            "joins_accepted": 0
        }
    }
