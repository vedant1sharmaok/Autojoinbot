from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from db import db
from logger import logger
from services.broadcast_delivery import deliver_broadcast

router = Router()


@router.callback_query(F.data.startswith("broadcast:approve"))
async def approve_broadcast(callback: CallbackQuery):
    _, _, broadcast_id, requester_type = callback.data.split(":")

    broadcast = await db.broadcasts.find_one(
        {"broadcast_id": broadcast_id}
    )

    if not broadcast:
        await callback.answer("Broadcast not found", show_alert=True)
        return

    await db.broadcasts.update_one(
        {"broadcast_id": broadcast_id},
        {"$set": {"status": "approved"}}
    )

    await callback.answer("Broadcast approved")

    logger.info(
        f"BROADCAST_APPROVED id={broadcast_id} type={requester_type}"
    )

    await deliver_broadcast(
        callback.bot,
        broadcast
    )


@router.callback_query(F.data.startswith("broadcast:reject"))
async def reject_broadcast(callback: CallbackQuery):
    _, _, broadcast_id, requester_type = callback.data.split(":")

    await db.broadcasts.update_one(
        {"broadcast_id": broadcast_id},
        {"$set": {"status": "rejected"}}
    )

    await callback.answer("Send rejection reason")

    await db.pending_rejections.insert_one({
        "broadcast_id": broadcast_id,
        "admin_id": callback.from_user.id,
        "requester_type": requester_type
    })


@router.message()
async def rejection_reason_handler(message: Message):
    """
    Admin sends rejection reason as normal message.
    """
    pending = await db.pending_rejections.find_one(
        {"admin_id": message.from_user.id}
    )

    if not pending:
        return

    await db.pending_rejections.delete_one(
        {"admin_id": message.from_user.id}
    )

    broadcast = await db.broadcasts.find_one(
        {"broadcast_id": pending["broadcast_id"]}
    )

    if not broadcast:
        return

    requester_id = broadcast["requester_id"]

    await message.bot.send_message(
        requester_id,
        f"❌ Your broadcast was rejected.\n\nReason:\n{message.text}"
    )

    logger.info(
        f"BROADCAST_REJECTED id={pending['broadcast_id']} by={message.from_user.id}"
)
