from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from services.menu_service import menu_by_role


def main_menu(role: str) -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text=btn)]
        for btn in menu_by_role(role)
    ]

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
