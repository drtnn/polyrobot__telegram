WEEKDAYS = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье",
}

YES_SWITCH = "✔️ Да, включить {preference}"
NO_SWITCH = "❌ Нет, отключить {preference}"

TURN_ON_FUNCTION_SWITCH = "✔️ Включить {preference}"
TURN_OFF_FUNCTION_SWITCH = "❌ Отключить {preference}"

RESULT_IS_ON = "✔️ {preference} включены"
RESULT_IS_OFF = "❌️ {preference} отключены"

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

NOTIFICATION_SLUG_TO_SWITCH_TEXT = {
    "remind-in-minutes": {
        0: TURN_ON_FUNCTION_SWITCH.format(preference="напоминания"),
        1: TURN_OFF_FUNCTION_SWITCH.format(preference="напоминания")
    },
    "notify-about-new-schedule": {
        0: YES_SWITCH.format(preference="уведомления"),
        1: NO_SWITCH.format(preference="уведомления")
    },
}

NOTIFICATION_SLUG_TO_RESULT_TEXT = {
    "remind-in-minutes": {
        0: RESULT_IS_OFF.format(preference="Напоминания"),
        1: RESULT_IS_ON.format(preference="Напоминания")
    },
    "notify-about-new-schedule": {
        0: RESULT_IS_OFF.format(preference="Уведомления"),
        1: RESULT_IS_ON.format(preference="Уведомления")
    },
}
