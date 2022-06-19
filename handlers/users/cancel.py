from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import cancel_callback
from loader import dp


@dp.message_handler(commands=["cancel"], state="*")
async def bot_cancel_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    data = await state.get_data()

    if data:
        await state.reset_state(with_data=True)
        await message.answer("🤖 Действие отменено.")


@dp.callback_query_handler(cancel_callback.filter(), state="*")
async def bot_cancel_callback(call: CallbackQuery, callback_data: dict):
    state = dp.current_state(user=call.from_user.id)
    data = await state.get_data()

    if data:
        await state.reset_state(with_data=True)
        await call.message.delete()
        await call.answer("🤖 Действие отменено.")
