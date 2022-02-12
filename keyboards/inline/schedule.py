from datetime import date, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.polyrobot.constants import WEEKDAYS
from utils.polyrobot.schedule import ScheduledLesson
from .callback_data import schedule_callback


def generate_one_day_schedule_message_buttons(date_obj: date) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    yesterday = date_obj - timedelta(days=1)
    tomorrow = date_obj + timedelta(days=1)

    keyboard.row(
        InlineKeyboardButton(
            text=f"🔙 {WEEKDAYS[yesterday.weekday()]}",
            callback_data=schedule_callback.new(date=yesterday.isoformat())
        ),
        InlineKeyboardButton(
            text=f"🔜 {WEEKDAYS[tomorrow.weekday()]}",
            callback_data=schedule_callback.new(date=tomorrow.isoformat())
        )
    )
    if date.today() != date_obj:
        keyboard.row(
            InlineKeyboardButton(text="📅 Сегодня", callback_data=schedule_callback.new(date=ScheduledLesson.TODAY))
        )
    return keyboard
