import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import config
from logger import logger
from db import connect_db, close_db
from middlewares.error_handler import ErrorHandlerMiddleware


async def main():
    logger.info("Starting Telegram Bot — PHASE 0")

    bot = Bot(
        token=config.BOT_TOKEN,
        parse_mode=ParseMode.HTML
    )

    dp = Dispatcher()
    dp.update.middleware(ErrorHandlerMiddleware())

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
