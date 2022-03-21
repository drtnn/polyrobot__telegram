from aiogram.types import Message

from handlers.users.start import bot_start_command
from loader import dp


@dp.message_handler(state='*')
async def bot_unauthorized_command(message: Message):
    await bot_start_command(message)
