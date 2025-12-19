from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from logger import logger


class ErrorHandlerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        try:
            return await handler(event, data)
        except Exception:
            logger.exception("Unhandled exception occurred")
            raise
