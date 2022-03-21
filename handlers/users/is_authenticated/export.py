from datetime import date
from io import BytesIO

from aiogram.types import Message, InputFile

from loader import dp
from utils.polyrobot.user import User


@dp.message_handler(commands=["export"], is_authenticated=True, state="*")
async def bot_profile_command(message: Message):
    user = User(message.from_user.id, message.from_user.full_name, message.from_user.username)
    calendar = await user.export_schedule()
    file = InputFile(BytesIO(calendar), f"Расписание от {date.today().isoformat()}.ics")

    await message.answer_document(file)
