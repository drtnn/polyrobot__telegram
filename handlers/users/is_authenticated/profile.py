from aiogram.types import Message, CallbackQuery

from keyboards.default.base import PROFILE_BUTTON
from keyboards.inline.callback_data import orders_callback, profile_callback
from keyboards.inline.profile import profile_keyboard, orders_keyboard
from loader import dp
from utils.polyrobot.user import User


@dp.message_handler(text=PROFILE_BUTTON, is_authenticated=True, state="*")
@dp.message_handler(commands=["profile"], is_authenticated=True, state="*")
async def bot_profile_command(message: Message):
    user = User(message.from_user.id, message.from_user.full_name, message.from_user.username)
    profile = await user.profile()

    await message.answer(text=profile.to_message_text(), reply_markup=profile_keyboard())


@dp.callback_query_handler(orders_callback.filter(), state="*")
async def bot_orders_callback(call: CallbackQuery, callback_data: dict):
    user = User(call.from_user.id, call.from_user.full_name, call.from_user.username)
    profile = await user.profile()

    await call.message.edit_text(text=profile.orders_to_message_text(), reply_markup=orders_keyboard())


@dp.callback_query_handler(profile_callback.filter(), state="*")
async def bot_profile_callback(call: CallbackQuery, callback_data: dict):
    user = User(call.from_user.id, call.from_user.full_name, call.from_user.username)
    profile = await user.profile()

    await call.message.edit_text(text=profile.to_message_text(), reply_markup=profile_keyboard())
