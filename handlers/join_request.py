from aiogram import Router
from aiogram.types import ChatJoinRequest
from services.auto_join_service import handle_join_request
from services.welcome_service import get_effective_welcome
from services.welcome_delivery_service import attempt_direct_welcome
from logger import logger

router = Router()


@router.chat_join_request()
async def join_request_handler(request: ChatJoinRequest):
    # Auto accept join request
    await handle_join_request(request)

    # Fetch welcome message (custom > default)
    welcome_text = await get_effective_welcome(request.chat.id)
    if not welcome_text:
        return

    # Attempt direct DM, fallback if needed
    delivered = await attempt_direct_welcome(
        bot=request.bot,
        user_id=request.from_user.id,
        chat_id=request.chat.id,
        text=welcome_text
    )

    if not delivered:
        logger.info(
            f"WELCOME_DM_DEFERRED user={request.from_user.id}"
        )
