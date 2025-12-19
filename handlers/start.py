from aiogram import Router
from aiogram.types import Message
from services.welcome_delivery_service import deliver_pending_welcomes
from services.user_service import register_user
from logger import logger

router = Router()


@router.message()
async def start_handler(message: Message):
    if message.text != "/start":
        return

    user = message.from_user

    # Register user (Phase 1 logic)
    await register_user(user)

    # Deliver any pending welcome messages
    await deliver_pending_welcomes(
        bot=message.bot,
        user_id=user.id
    )

    logger.info(f"USER_STARTED_BOT user={user.id}")

    await message.answer(
        "👋 Welcome! Use the menu below to continue."
    )
