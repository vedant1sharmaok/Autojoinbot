from logger import logger
from services.premium_service import get_user_premium
from models.premium_plans import PremiumPlan


async def try_pin_message(bot, chat_id: int, message_id: int, sender_id: int, is_owner: bool):
    """
    Attempts to pin a message.
    """
    try:
        if not is_owner:
            premium = await get_user_premium(sender_id)
            if not premium["limits"]["can_pin"]:
                return False

        await bot.pin_chat_message(
            chat_id=chat_id,
            message_id=message_id,
            disable_notification=True
        )

        logger.info(
            f"MESSAGE_PINNED chat={chat_id} msg={message_id}"
        )
        return True

    except Exception:
        logger.warning(
            f"PIN_FAILED chat={chat_id} msg={message_id}"
        )
        return False
