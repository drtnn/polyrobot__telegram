import logging

from aiogram import Dispatcher

from utils.polyrobot.user import User


async def on_startup_notify(dp: Dispatcher):
    for admin in await User.admins():
        try:
            await dp.bot.send_message(admin.id, "Бот Запущен")

        except Exception as err:
            logging.exception(err)
