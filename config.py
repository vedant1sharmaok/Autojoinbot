import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME: str = os.getenv("DB_NAME", "telegram_bot")
    OWNER_ID: int = int(os.getenv("OWNER_ID", "0"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    HEALTH_PORT: int = int(os.getenv("HEALTH_PORT", "8000"))


config = Config()
