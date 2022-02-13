from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Регистрация"),
            types.BotCommand("help", "Что я могу?"),
            types.BotCommand("schedule", "Расписание студента"),
            types.BotCommand("profile", "Профиль студента"),
            types.BotCommand("performance", "Успеваемость студента"),
        ]
    )
