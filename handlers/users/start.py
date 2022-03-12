from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message

from keyboards.default.base import MENU_KEYBOARD
from keyboards.inline.base import links_keyboard
from loader import dp
from utils.polyrobot.user import User


@dp.message_handler(CommandStart(), state='*')
async def bot_start_command(message: Message):
    await User.get_or_create(message.from_user.id, message.from_user.full_name, message.from_user.username)
    await message.answer("🤖 Привет, я – Робот Политеха.", reply_markup=MENU_KEYBOARD)
    await message.answer(
        "✍️ Могу показать тебе расписание занятий, историю платежей, успеваемость и многое другое.\n\n🧑‍💻 Для начала работы перейди по ссылке ниже и авторизуйся с данными личного кабинета Московского Политеха.\n\n💬 Не забудь подписаться на наш канал @mospolytech и вступить в чат @mospolychat.",
        reply_markup=links_keyboard(telegram_id=message.from_user.id)
    )
