from datetime import datetime


def user_document(user_id: int, ref_by: int | None = None):
    return {
        "user_id": user_id,
        "role": "free",          # free | premium | restricted | blocked | owner
        "language": "en",
        "ref_by": ref_by,
        "created_at": datetime.utcnow(),
        "stats": {
            "joined_at": datetime.utcnow()
        }
    }
  
