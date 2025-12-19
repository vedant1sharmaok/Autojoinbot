import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from handlers.start import router as start_router
from config import config
from logger import logger
from db import connect_db, close_db
from middlewares.error_handler import ErrorHandlerMiddleware
from handlers.add_channel import router as add_channel_router
from handlers.join_request import router as join_router
from handlers.welcome_user import router as welcome_user_router
from handlers.welcome_owner import router as welcome_owner_router

async def main():
    logger.info("Starting Telegram Bot — PHASE 0")

    bot = Bot(
        token=config.BOT_TOKEN,
        parse_mode=ParseMode.HTML
    )

    dp = Dispatcher()
    dp.update.middleware(ErrorHandlerMiddleware())
    dp.include_router(start_router)
    dp.include_router(add_channel_router)
    dp.include_router(join_router)
    dp.include_router(welcome_user_router)
    dp.include_router(welcome_owner_router)
    await connect_db()

    try:
        await dp.start_polling(bot)
    finally:
        await close_db()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Bot stopped")
