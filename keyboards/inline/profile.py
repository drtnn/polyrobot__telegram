from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import orders_callback, profile_callback


def profile_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Приказы", callback_data=orders_callback.new()))
    return keyboard


def orders_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="🔙", callback_data=profile_callback.new()))
    return keyboard
