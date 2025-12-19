from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def channel_controls(chat_id: int, auto_join: bool):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Auto-Join ON" if auto_join else "❌ Auto-Join OFF",
                    callback_data=f"toggle_autojoin:{chat_id}"
                )
            ]
        ]
    )
