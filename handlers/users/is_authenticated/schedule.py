from datetime import date

from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageToEditNotFound

from keyboards.default.base import SCHEDULE_BUTTON
from keyboards.inline.callback_data import schedule_callback
from keyboards.inline.schedule import generate_one_day_schedule_message_buttons
from loader import dp
from utils.polyrobot.schedule import ScheduledLesson
from utils.polyrobot.user import User
from utils.polyrobot.utils import generate_one_day_schedule_message_text


@dp.message_handler(commands=["schedule"], is_authenticated=True)
async def bot_schedule_command(message: Message):
    user = User(message.from_user.id, message.from_user.full_name, message.from_user.username)
    date_obj = date.today()
    scheduled_lessons = await user.scheduled_lesson(date_obj=date_obj)

    await message.answer(
        text=generate_one_day_schedule_message_text(date_obj=date_obj, scheduled_lessons=scheduled_lessons),
        reply_markup=generate_one_day_schedule_message_buttons(date_obj),
        disable_web_page_preview=True
    )


@dp.message_handler(text=SCHEDULE_BUTTON, is_authenticated=True)
async def bot_schedule_text(message: Message):
    await bot_schedule_command(message)


@dp.callback_query_handler(schedule_callback.filter())
async def bot_schedule_date_callback(call: CallbackQuery, callback_data: dict):
    if callback_data['date'] == ScheduledLesson.TODAY:
        date_obj = date.today()
    else:
        date_obj = date.fromisoformat(callback_data['date'])
    user = User(call.from_user.id, call.from_user.full_name, call.from_user.username)
    scheduled_lessons = await user.scheduled_lesson(date_obj=date_obj)
    text = generate_one_day_schedule_message_text(date_obj=date_obj, scheduled_lessons=scheduled_lessons)
    reply_markup = generate_one_day_schedule_message_buttons(date_obj)

    await call.message.edit_text(text=text, reply_markup=reply_markup, disable_web_page_preview=True)
