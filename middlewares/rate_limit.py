import time
from aiogram import BaseMiddleware
from aiogram.types import Message
from logger import logger


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 3, window: int = 5):
        """
        limit: number of messages
        window: seconds
        """
        self.limit = limit
        self.window = window
        self.user_calls = {}

    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            user_id = event.from_user.id
            now = time.time()

            calls = self.user_calls.get(user_id, [])
            calls = [t for t in calls if now - t < self.window]

            if len(calls) >= self.limit:
                logger.warning(f"RATE_LIMIT user={user_id}")
                return None  # silently drop

            calls.append(now)
            self.user_calls[user_id] = calls

        return await handler(event, data)
