from aiogram import Router, F
from aiogram.types import Message
from db import db
from logger import logger
from models.premium_plans import PremiumPlan
from services.premium_service import grant_premium, revoke_premium
from config import BOT_OWNER_ID

router = Router()


def _is_owner(user_id: int) -> bool:
    return user_id == BOT_OWNER_ID


@router.message(F.text.startswith("/grant_premium"))
async def grant_premium_cmd(message: Message):
    if not _is_owner(message.from_user.id):
        return

    """
    Usage:
    /grant_premium user_id plan days | optional message
    """
    try:
        parts = message.text.split("|")
        args = parts[0].split()

        user_id = int(args[1])
        plan = PremiumPlan(args[2])
        days = int(args[3])

        reason = parts[1].strip() if len(parts) > 1 else "Granted by owner"

        await grant_premium(
            user_id=user_id,
            plan=plan,
            duration_days=days,
            granted_by=message.from_user.id,
            reason=reason
        )

        await message.bot.send_message(
            user_id,
            f"🎉 Premium Activated!\nPlan: {plan}\nDays: {days}\n\n{reason}"
        )

        await message.answer("✅ Premium granted")

    except Exception as e:
        logger.exception("GRANT_PREMIUM_FAILED")
        await message.answer("❌ Invalid command format")


@router.message(F.text.startswith("/revoke_premium"))
async def revoke_premium_cmd(message: Message):
    if not _is_owner(message.from_user.id):
        return

    """
    Usage:
    /revoke_premium user_id | optional message
    """
    try:
        parts = message.text.split("|")
        args = parts[0].split()

        user_id = int(args[1])
        reason = parts[1].strip() if len(parts) > 1 else "Revoked by owner"

        await revoke_premium(
            user_id=user_id,
            revoked_by=message.from_user.id,
            reason=reason
        )

        await message.bot.send_message(
            user_id,
            f"⚠️ Premium Revoked\n\nReason:\n{reason}"
        )

        await message.answer("✅ Premium revoked")

    except Exception:
        logger.exception("REVOKE_PREMIUM_FAILED")
        await message.answer("❌ Invalid command format")
