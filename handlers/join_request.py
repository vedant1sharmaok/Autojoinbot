from aiogram import Router
from aiogram.types import ChatJoinRequest
from services.auto_join_service import handle_join_request
from services.welcome_service import get_default_welcome

router = Router()


@router.chat_join_request()
async def join_request_handler(request: ChatJoinRequest):
    await handle_join_request(request)

    welcome = await get_default_welcome()
    if welcome:
        try:
            await request.bot.send_message(
                request.user_chat_id,
                welcome["text"]
            )
        except Exception:
            pass
