from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from data.config import FEEDBACK_LINK
from loader import dp


@dp.message_handler(CommandHelp(), state="*")
async def bot_help_command(message: types.Message):
    await message.answer(
        f"🤖 Что я могу?\n    • /start – регистрация с данными личного кабинета Мосполитеха;\n    • /schedule – расписание твоей группы на сегодня;\n    • /export – экспорт расписания в календарь;\n    • /profile – профиль студента и приказы;\n    • /performance – успеваемость студента.\n\n🔧 <a href='{FEEDBACK_LINK}'>Обратная связь для багов.</a>"
    )
