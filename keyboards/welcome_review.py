from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def welcome_review_keyboard(chat_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Approve",
                    callback_data=f"welcome_approve:{chat_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Reject",
                    callback_data=f"welcome_reject:{chat_id}"
                )
            ]
        ]
    )
