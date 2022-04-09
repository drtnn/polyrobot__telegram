from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import preference_callback, preference_update_value_callback, \
    preference_update_enabled_callback, preferences_callback
from utils.polyrobot.preference import Preference


def preference_keyboard(preferences: List[Preference]):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for preference in preferences:
        keyboard.add(
            InlineKeyboardButton(text=preference.button_text(),
                                 callback_data=preference_callback.new(preference_id=preference.id))
        )
    return keyboard


def preference_update_value_keyboard(preference: Preference):
    keyboard = InlineKeyboardMarkup(row_width=len(preference.update_values()))
    for value in preference.update_values():
        keyboard.insert(
            InlineKeyboardButton(text=str(value),
                                 callback_data=preference_update_value_callback.new(preference_id=preference.id,
                                                                                    value=value))
        )
    if preference.is_switchable():
        switch_text = "❌ Отключить" if preference.enabled else "✔️ Включить"
        keyboard.row(
            InlineKeyboardButton(
                text=switch_text, callback_data=preference_update_enabled_callback.new(
                    preference_id=preference.id, enabled=not preference.enabled
                )
            )
        )
    keyboard.row(InlineKeyboardButton(text="🔙", callback_data=preferences_callback.new()))
    return keyboard
