from aiogram.types import Message, CallbackQuery

from keyboards.default.base import PROFILE_BUTTON
from keyboards.inline.callback_data import orders_callback
from keyboards.inline.profile import orders_keyboard
from loader import dp
from utils.polyrobot.user import User


@dp.message_handler(commands=["profile"], is_authenticated=True)
async def bot_profile_command(message: Message):
    user = User(message.from_user.id, message.from_user.full_name, message.from_user.username)
    profile = await user.profile()

    await message.answer(text=profile.to_message_text(), reply_markup=orders_keyboard())


@dp.message_handler(text=PROFILE_BUTTON, is_authenticated=True)
async def bot_profile_text(message: Message):
    await bot_profile_command(message)


@dp.callback_query_handler(orders_callback.filter())
async def bot_schedule_date_callback(call: CallbackQuery, callback_data: dict):
    user = User(call.from_user.id, call.from_user.full_name, call.from_user.username)
    profile = await user.profile()

    await call.message.answer(text=profile.orders_to_message_text())
