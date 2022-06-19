from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import POLYROBOT_ENDPOINT
from keyboards.inline.callback_data import cancel_callback


def links_keyboard(telegram_id: int):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="@mospolytech", url="t.me/mospolytech"),
        InlineKeyboardButton(text="@mospolychat", url="t.me/mospolychat"),
        InlineKeyboardButton(text="Войти через Московский Политех",
                             url=f"{POLYROBOT_ENDPOINT}/login-to-mospolytech/{telegram_id}/")
    )
    return keyboard


def cancel_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="🛑 Отмена", callback_data=cancel_callback.new()),
    )
    return keyboard
