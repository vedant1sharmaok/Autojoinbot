import asyncio
import signal

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import config
from logger import logger
from db import connect_db, close_db, ensure_indexes

from middlewares.error_handler import ErrorHandlerMiddleware

from handlers.start import router as start_router
from handlers.add_channel import router as add_channel_router
from handlers.join_request import router as join_request_router
from handlers.welcome_user import router as welcome_user_router
from handlers.welcome_owner import router as welcome_owner_router

from services.broadcast_scheduler import scheduler_worker


async def main():
    logger.info("Starting Telegram Bot — Production Mode")

    bot = Bot(
        token=config.BOT_TOKEN,
        parse_mode=ParseMode.HTML
    )

    dp = Dispatcher()
    dp.update.middleware(ErrorHandlerMiddleware())

    dp.include_router(start_router)
    dp.include_router(add_channel_router)
    dp.include_router(join_request_router)
    dp.include_router(welcome_user_router)
    dp.include_router(welcome_owner_router)

    await connect_db()
    await ensure_indexes()

    # Graceful shutdown support
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(dp.stop_polling()))

    scheduler_task = asyncio.create_task(scheduler_worker(bot))

    try:
        await dp.start_polling(bot)
    finally:
        scheduler_task.cancel()
        await close_db()
        await bot.session.close()
        logger.warning("Bot shutdown complete")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Bot stopped")
        
