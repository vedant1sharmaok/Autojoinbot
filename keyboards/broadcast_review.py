from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def broadcast_review_keyboard(
    broadcast_id: str,
    requester_type: str
):
    """
    requester_type:
        'A' = Channel Owner
        'B' = Bot Owner
    """

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Approve",
                    callback_data=f"broadcast:approve:{broadcast_id}:{requester_type}"
                ),
                InlineKeyboardButton(
                    text="❌ Reject",
                    callback_data=f"broadcast:reject:{broadcast_id}:{requester_type}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ View Details",
                    callback_data=f"broadcast:details:{broadcast_id}"
                )
            ]
        ]
  )
