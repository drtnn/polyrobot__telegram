from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Регистрация"),
            types.BotCommand("cancel", "Отменить действие"),
            types.BotCommand("help", "Что я могу?"),
            types.BotCommand("schedule", "Расписание студента"),
            types.BotCommand("export", "Экспорт расписания"),
            types.BotCommand("profile", "Профиль студента"),
            types.BotCommand("performance", "Успеваемость студента"),
            types.BotCommand("payments", "Платежи студента"),
            types.BotCommand("preferences", "Настройки бота"),
        ]
    )
