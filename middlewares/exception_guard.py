from aiogram import BaseMiddleware
from logger import logger


class ExceptionGuardMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        try:
            return await handler(event, data)
        except Exception as e:
            logger.exception(
                f"UNHANDLED_EXCEPTION event={type(event).__name__}"
            )
            # swallow exception to keep bot alive
            return None
