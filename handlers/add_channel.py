from aiogram import Router, F
from aiogram.types import Message
from services.channel_service import add_channel
from keyboards.channel_menu import channel_controls

router = Router()


# ✅ MENU BUTTON HANDLER (THIS WAS MISSING)
@router.message(F.text == "➕ Add Channel")
async def add_channel_from_menu(message: Message):
    await message.answer(
        "➕ Add me to your channel or group as ADMIN.\n"
        "Once added, I will auto-configure it."
    )


# ✅ BOT ADDED TO CHAT
@router.message(F.new_chat_members)
async def bot_added_to_chat(message: Message):
    for member in message.new_chat_members:
        if member.id == message.bot.id:
            admins = await message.chat.get_administrators()
            admin_ids = [a.user.id for a in admins]

            if message.from_user.id not in admin_ids:
                await message.answer(
                    "❌ Only channel/group OWNER or ADMIN can add this bot."
                )
                return

            await add_channel(message.from_user.id, message.chat)

            await message.answer(
                "✅ Channel added successfully.\nAuto-join is enabled.",
                reply_markup=channel_controls(message.chat.id, True)
            )
            
