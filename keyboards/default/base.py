from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

PROFILE_BUTTON = "👨🏻‍🎓 Профиль"
SCHEDULE_BUTTON = "📆 Расписание"
ACADEMIC_PERFORMANCE_BUTTON = "📓 Успеваемость"
PAYMENTS_BUTTON = "💴 Платежи"
PREFERENCE_BUTTON = "⚙️ Настройки"

MENU_KEYBOARD = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(PROFILE_BUTTON)],
    [KeyboardButton(SCHEDULE_BUTTON)],
    [KeyboardButton(ACADEMIC_PERFORMANCE_BUTTON)],
    [KeyboardButton(PAYMENTS_BUTTON)],
    [KeyboardButton(PREFERENCE_BUTTON)],
], resize_keyboard=True)
