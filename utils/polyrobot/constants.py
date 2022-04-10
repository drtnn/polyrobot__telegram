WEEKDAYS = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье",
}

NOTIFICATION_SLUG_TO_BUTTON_TEXT = {
    "remind-in-minutes": "⏰ Напоминания о начале занятий",
    "notify-about-new-schedule": "🔔 Уведомление о новом расписании",
}

NOTIFICATION_SLUG_TO_UPDATE_MESSAGE_TEXT = {
    "remind-in-minutes": "⏰ За сколько минут до начала занятия мне прислать уведомление?",
    "notify-about-new-schedule": "🔔 Хочешь ли ты получать уведомления об изменении расписания?",
}

NOTIFICATION_SLUG_TO_UPDATE_BUTTON_VALUES = {
    "remind-in-minutes": [0, 5, 10, 15, 30],
    "notify-about-new-schedule": [],
}

NOTIFICATION_SLUG_TO_SWITCHABLE = {
    "remind-in-minutes": True,
    "notify-about-new-schedule": True,
}
