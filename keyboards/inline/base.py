from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import POLYROBOT_ENDPOINT


def links_keyboard(telegram_id: int):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(
        InlineKeyboardButton(text="@mospolytech", url="t.me/mospolytech"),
        InlineKeyboardButton(text="@mospolychat", url="t.me/mospolychat")
    )
    keyboard.row(
        InlineKeyboardButton(text="Войти с МосПолитех", url=f"{POLYROBOT_ENDPOINT}/login-to-mospolytech/{telegram_id}/")
    )
    return keyboard
