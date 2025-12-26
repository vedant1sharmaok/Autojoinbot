from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatMemberStatus

from services.channel_service import add_channel
from keyboards.channel_menu import channel_controls

router = Router()


@router.message(F.new_chat_members)
async def bot_added_to_chat(message: Message):
    for member in message.new_chat_members:
        if member.id == message.bot.id:

            # 🔐 SAFE permission check (supports anonymous admins)
            chat_member = await message.chat.get_member(message.from_user.id)

            if chat_member.status not in (
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.OWNER,
            ):
                await message.answer(
                    "❌ Only channel/group OWNER or ADMIN can add this bot."
                )
                return

            # ✅ Save channel
            await add_channel(message.from_user.id, message.chat)

            await message.answer(
                "✅ Channel added successfully!\n"
                "Auto-join is now enabled.",
                reply_markup=channel_controls(message.chat.id, True)
            )
            
