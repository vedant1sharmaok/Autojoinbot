from aiogram import Router, types
from admin.permissions import is_owner
from admin.stats_service import (
    get_global_stats,
    get_broadcast_stats,
    get_task_stats,
)
from admin.user_controls import (
    restrict_user,
    unrestrict_user,
    block_user,
)
from admin.channel_controls import (
    get_user_channels,
    disable_channel,
)
from admin.broadcast_controls import list_broadcasts

router = Router()


@router.message(commands=["admin"])
async def admin_panel(message: types.Message):
    if not is_owner(message.from_user.id):
        return

    stats = await get_global_stats()
    text = (
        "🛠 *Admin Panel*\n\n"
        f"👥 Users: {stats['users']}\n"
        f"📢 Channels: {stats['channels']}\n"
        f"📨 Broadcasts: {stats['broadcasts']}\n"
        f"⭐ Premium: {stats['premium_users']}\n"
    )

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="📊 Broadcast Stats", callback_data="admin_broadcast_stats")],
        [types.InlineKeyboardButton(text="📋 Task Stats", callback_data="admin_task_stats")],
        [types.InlineKeyboardButton(text="🧍 User Controls", callback_data="admin_user_controls")],
    ])

    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")


@router.callback_query(lambda c: c.data == "admin_broadcast_stats")
async def admin_broadcast_stats(call: types.CallbackQuery):
    if not is_owner(call.from_user.id):
        return

    stats = await get_broadcast_stats()
    await call.message.answer(
        f"📊 *Broadcast Stats*\n\n"
        f"✅ Sent: {stats['sent']}\n"
        f"❌ Failed: {stats['failed']}\n"
        f"⏳ Pending: {stats['pending']}",
        parse_mode="Markdown"
    )


@router.callback_query(lambda c: c.data == "admin_task_stats")
async def admin_task_stats(call: types.CallbackQuery):
    if not is_owner(call.from_user.id):
        return

    stats = await get_task_stats()
    await call.message.answer(
        f"📝 *Task Stats*\n\n"
        f"📌 Tasks: {stats['tasks']}\n"
        f"📨 Submissions: {stats['submissions']}\n"
        f"⏳ Pending: {stats['pending']}",
        parse_mode="Markdown"
    )
