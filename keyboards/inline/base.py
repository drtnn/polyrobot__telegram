from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import POLYROBOT_LINK


def links_keyboard(telegram_id: int):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="@mospolytech", url="t.me/mospolytech"),
        InlineKeyboardButton(text="@mospolychat", url="t.me/mospolychat"),
        InlineKeyboardButton(text="Войти через Московский Политех",
                             url=f"{POLYROBOT_LINK}/login-to-mospolytech/{telegram_id}/")
    )
    return keyboard
