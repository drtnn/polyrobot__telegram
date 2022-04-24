from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.polyrobot.payments import Payment


def payment_keyboard(payment: Payment):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="Договор", url=payment.file),
        InlineKeyboardButton(text="QR-код на оплату текущей задолженности", url=payment.qr_current),
        InlineKeyboardButton(text="QR-код на оплату общей задолженности", url=payment.qr_total),
    )
    return keyboard
