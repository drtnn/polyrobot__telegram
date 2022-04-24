from aiogram.types import Message

from keyboards.default.base import PAYMENTS_BUTTON
from keyboards.inline.payments import payment_keyboard
from loader import dp
from utils.polyrobot.user import User


@dp.message_handler(text=PAYMENTS_BUTTON, is_authenticated=True, state="*")
@dp.message_handler(commands=["payments"], is_authenticated=True, state="*")
async def bot_payments_command(message: Message):
    user = User(message.from_user.id, message.from_user.full_name, message.from_user.username)
    payments = await user.payments()

    for education_payment in payments.education:
        await message.answer(text=education_payment.message_text(), reply_markup=payment_keyboard(education_payment))

    for dormitory_payment in payments.dormitory:
        await message.answer(text=dormitory_payment.message_text(), reply_markup=payment_keyboard(dormitory_payment))

    if not (payments.education or payments.dormitory):
        await message.answer(text="💴 Платежи не найдены!")
