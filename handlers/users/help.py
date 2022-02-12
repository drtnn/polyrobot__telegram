from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help_command(message: types.Message):
    await message.answer(
        "🤖 Что я могу?\n    • /start – регистрация с данными личного кабинета Мосполитеха.\n    • /schedule – расписание твоей группы на сегодня.\n    • /profile – профиль студента и приказы."
    )
