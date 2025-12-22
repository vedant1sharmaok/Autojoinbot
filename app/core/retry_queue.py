import asyncio
from logger import logger
from db import db


class RetryQueue:
    def __init__(self, bot, max_retries: int = 3, delay: int = 5):
        self.bot = bot
        self.max_retries = max_retries
        self.delay = delay
        self.queue = asyncio.Queue()
        self.running = False

    async def add(self, payload: dict):
        """
        payload must contain:
        - chat_id
        - message_method (callable)
        - kwargs
        - retry_count
        """
        await self.queue.put(payload)

    async def worker(self):
        self.running = True
        while self.running:
            job = await self.queue.get()
            try:
                await job["message_method"](**job["kwargs"])

                await db.broadcast_logs.update_one(
                    {
                        "chat_id": job["kwargs"]["chat_id"],
                        "broadcast_id": job["broadcast_id"]
                    },
                    {"$set": {"status": "sent"}}
                )

            except Exception as e:
                retries = job.get("retry_count", 0) + 1

                if retries <= self.max_retries:
                    job["retry_count"] = retries
                    logger.warning(
                        f"RETRY {retries}/{self.max_retries} chat={job['kwargs']['chat_id']}"
                    )
                    await asyncio.sleep(self.delay * retries)
                    await self.queue.put(job)
                else:
                    logger.error(
                        f"RETRY_FAILED chat={job['kwargs']['chat_id']} error={e}"
                    )

                    await db.broadcast_logs.update_one(
                        {
                            "chat_id": job["kwargs"]["chat_id"],
                            "broadcast_id": job["broadcast_id"]
                        },
                        {"$set": {"status": "failed"}}
                    )

            self.queue.task_done()

    async def stop(self):
        self.running = False
