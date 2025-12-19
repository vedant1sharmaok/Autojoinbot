from aiogram import Router
from aiogram.types import ChatJoinRequest
from services.auto_join_service import handle_join_request

router = Router()


@router.chat_join_request()
async def join_request_handler(request: ChatJoinRequest):
    await handle_join_request(request)
