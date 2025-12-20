from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from services.premium_service import get_user_premium
from services.payment_gateways.stars import TelegramStarsGateway
from services.payment_gateways.upi import UPIGateway
from models.premium_plans import PREMIUM_PLANS, PremiumPlan

router = Router()

stars_gateway = TelegramStarsGateway()
upi_gateway = UPIGateway()


def premium_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⭐ Buy via Telegram Stars", callback_data="buy:stars"),
            ],
            [
                InlineKeyboardButton(text="💳 Buy via UPI", callback_data="buy:upi"),
            ],
            [
                InlineKeyboardButton(text="ℹ️ My Plan", callback_data="premium:status"),
            ]
        ]
    )


@router.message(F.text == "/premium")
async def premium_entry(message: Message):
    await message.answer(
        "💎 Premium Panel\n\nChoose an option:",
        reply_markup=premium_menu()
    )


@router.callback_query(F.data == "premium:status")
async def premium_status(callback):
    data = await get_user_premium(callback.from_user.id)

    text = f"📦 Current Plan: {data['plan']}\n"
    if data["expires_at"]:
        text += f"⏳ Expires at: {data['expires_at']}"
    else:
        text += "⏳ No expiry (Free)"

    await callback.message.edit_text(text, reply_markup=premium_menu())


@router.callback_query(F.data == "buy:stars")
async def buy_stars(callback):
    if not stars_gateway.is_available():
        await callback.answer("Stars payment under maintenance", show_alert=True)
        return

    await callback.message.answer(
        "⭐ Telegram Stars purchase\n\n"
        "Please contact owner if invoice does not appear."
    )
    # Invoice sending will be handled in payment update handler


@router.callback_query(F.data == "buy:upi")
async def buy_upi(callback):
    if not upi_gateway.is_available():
        await callback.answer("UPI payment under maintenance", show_alert=True)
        return

    await callback.message.answer(
        "💳 UPI Autopay\n\n"
        "You will receive a payment link shortly.\n"
        "After payment, premium activates automatically."
  )
