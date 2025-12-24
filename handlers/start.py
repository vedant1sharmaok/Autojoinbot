from aiogram import Router, F
from aiogram.types import Message

from services.user_service import (
    create_user_if_not_exists,
    is_blocked,
    is_restricted,
)
from services.welcome_delivery_service import deliver_pending_welcomes
from keyboards.main_menu import main_menu
from logger import logger

# ✅ MUST be at top-level (this fixes your error)
router = Router()


@router.message(F.text.startswith("/start"))
async def start_handler(message: Message):
    args = message.text.split()
    ref_by = int(args[1]) if len(args) > 1 and args[1].isdigit() else None

    user = await create_user_if_not_exists(
        telegram_id=message.from_user.id,
        ref_by=ref_by
    )

    # 🔒 Block check
    if is_blocked(user):
        await message.answer("🚫 You are blocked from using this bot.")
        return

    # ⚠️ Restricted check
    if is_restricted(user):
        await message.answer(
            "⚠️ Your account is restricted.\nContact support.",
            reply_markup=main_menu(user["role"])
        )
        return

    # 📦 Deliver pending welcomes (safe)
    await deliver_pending_welcomes(
        bot=message.bot,
        user_id=message.from_user.id
    )

    logger.info(f"USER_STARTED_BOT user={message.from_user.id}")

    # ✅ Final response WITH menu
    await message.answer(
        "👋 Welcome to the bot!\nUse the menu below to continue.",
        reply_markup=main_menu(user["role"])
    )
