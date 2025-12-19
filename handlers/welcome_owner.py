from aiogram import Router, F
from aiogram.types import CallbackQuery
from services.welcome_service import approve_welcome, reject_welcome
from config import config

router = Router()


@router.callback_query(F.data.startswith("welcome_"))
async def review_welcome(callback: CallbackQuery):
    if callback.from_user.id != config.OWNER_ID:
        return

    action, chat_id = callback.data.split(":")
    chat_id = int(chat_id)

    if action == "welcome_approve":
        await approve_welcome(chat_id)
        await callback.message.answer("✅ Welcome approved")

    elif action == "welcome_reject":
        await reject_welcome(chat_id)
        await callback.message.answer("❌ Welcome rejected")

    await callback.answer()
