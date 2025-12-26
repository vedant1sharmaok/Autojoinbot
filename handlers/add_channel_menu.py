from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


def add_channel_button(bot_username: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ Add Bot to Channel / Group",
                    url=f"https://t.me/{bot_username}?startgroup=true"
                )
            ]
        ]
    )


@router.message(F.text == "➕ Add Channel")
async def add_channel_menu(message: Message):
    await message.answer(
        "➕ *Add me to your channel or group as ADMIN*\n\n"
        "• You must be Owner or Admin\n"
        "• Anonymous admins are supported\n"
        "• Auto-join will start automatically",
        reply_markup=add_channel_button(message.bot.username),
        parse_mode="Markdown"
    )
      
