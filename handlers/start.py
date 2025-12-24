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

router = Router()


@router.message(F.text.startswith("/start"))
async def start_handler(message: Message):
    args = message.text.split()
    ref_by = int(args[1]) if len(args) > 1 and args[1].isdigit() else None

    # Create / fetch user (Phase 2 logic)
    user = await create_user_if_not_exists(
        telegram_id=message.from_user.id,
        ref_by=ref_by
    )

    # Blocked user
    if is_blocked(user):
        await message.answer("🚫 You are blocked from using this bot.")
        return

    # Restricted user
    if is_restricted(user):
        await message.answer(
            "⚠️ Your account is restricted.\nContact support.",
            reply_markup=main_menu(user["role"])
        )
        return

    # Phase 3: Deliver pending welcomes (SAFE here)
    await deliver_pending_welcomes(
        bot=message.bot,
        user_id=message.from_user.id
    )

    logger.info(f"USER_STARTED_BOT user={message.from_user.id}")

    # FINAL response with MENU ✅
    await message.answer(
        "👋 Welcome to the bot!\nUse the menu below to continue.",
        reply_markup=main_menu(user["role"])
    )
    
