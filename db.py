from motor.motor_asyncio import AsyncIOMotorClient
from logger import logger
from config import config

client: AsyncIOMotorClient | None = None
db = None


async def connect_db():
    global client, db
    try:
        client = AsyncIOMotorClient(config.MONGO_URI)
        db = client[config.DB_NAME]
        await db.command("ping")
        logger.success("MongoDB connected successfully")
    except Exception:
        logger.exception("MongoDB connection failed")
        raise


async def close_db():
    if client:
        client.close()
        logger.info("MongoDB connection closed")
        
async def ensure_indexes():
    await db.broadcast_logs.create_index("broadcast_id")
