from aiogram import Router, F
from aiogram.types import Message
from services.welcome_service import submit_custom_welcome

router = Router()


@router.message(F.text.startswith("/setwelcome"))
async def set_welcome(message: Message):
    if not message.reply_to_message:
        await message.answer(
            "Reply to a message with /setwelcome to set it as welcome text."
        )
        return

    chat_id = message.chat.id
    text = message.reply_to_message.text

    await submit_custom_welcome(
        owner_id=message.from_user.id,
        chat_id=chat_id,
        text=text
    )

    await message.answer(
        "📩 Welcome message sent for owner approval."
    )
