from aiogram import types

from loader import dp


@dp.message_handler(commands=["cancel"], state="*")
async def bot_cancel_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    data = await state.get_data()

    if data:
        await state.reset_state(with_data=True)
        await message.answer("🤖 Действие отменено.")
