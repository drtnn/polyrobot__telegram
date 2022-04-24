from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from data.config import FEEDBACK_LINK
from loader import dp


@dp.message_handler(CommandHelp(), state="*")
async def bot_help_command(message: types.Message):
    await message.answer(
        "🤖 Что я могу?\n" +
        "\n".join(
            [
                "    • /start – регистрация с данными личного кабинета Московского Политеха;",
                "    • /cancel – отменить действие;",
                "    • /schedule – расписание твоей группы на сегодня;",
                "    • /export – экспорт расписания в календарь;",
                "    • /profile – профиль студента и приказы;",
                "    • /performance – успеваемость студента;",
                "    • /payments – платежи студента;",
                "    • /preferences – настройки бота."
            ]
        ) +
        f"\n\n🔧 <a href='{FEEDBACK_LINK}'>Обратная связь</a>"
    )
