import signal
import asyncio
from logger import logger


class GracefulShutdown:
    def __init__(self):
        self.stop_event = asyncio.Event()

    def _signal_handler(self, sig):
        logger.warning(f"SHUTDOWN_SIGNAL_RECEIVED {sig}")
        self.stop_event.set()

    def setup(self):
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    async def wait(self):
        await self.stop_event.wait()
        logger.warning("GRACEFUL_SHUTDOWN_INITIATED")
