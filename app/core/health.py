from app.db.mongo import mongo

async def bot_health():
    try:
        await mongo.db.command("ping")
        return True
    except Exception:
        return False
