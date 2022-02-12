from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Регистрация с данными личного кабинета Мосполитеха"),
            types.BotCommand("help", "Что я могу?"),
            types.BotCommand("schedule", "Расписание твоей группы на сегодня"),
        ]
    )
