from aiogram.types import Message, CallbackQuery
from http3.exceptions import HttpError

from keyboards.default.base import PREFERENCE_BUTTON
from keyboards.inline.callback_data import preference_callback, preferences_callback, preference_update_value_callback, \
    preference_update_enabled_callback
from keyboards.inline.preference import preference_keyboard, preference_update_value_keyboard
from loader import dp
from utils.polyrobot.preference import Preference
from utils.polyrobot.user import User


@dp.message_handler(text=PREFERENCE_BUTTON, is_authenticated=True, state="*")
@dp.message_handler(commands=["preferences"], is_authenticated=True, state="*")
async def bot_preferences_command(message: Message):
    user = await User.get(message.from_user.id)

    await message.answer(text="⚙️ Пользовательские настройки", reply_markup=preference_keyboard(user.preferences))


@dp.callback_query_handler(preferences_callback.filter(), state="*")
async def bot_preferences_callback(call: CallbackQuery, callback_data: dict):
    user = await User.get(call.from_user.id)

    await call.message.edit_text(text="⚙️ Пользовательские настройки",
                                 reply_markup=preference_keyboard(user.preferences))


@dp.callback_query_handler(preference_callback.filter(), state="*")
async def bot_preference_callback(call: CallbackQuery, callback_data: dict):
    preference = await Preference.get(id=callback_data['preference_id'])

    await call.message.edit_text(text=preference.update_value_message_text(),
                                 reply_markup=preference_update_value_keyboard(preference))


@dp.callback_query_handler(preference_update_value_callback.filter(), state="*")
async def bot_preference_update_value_callback(call: CallbackQuery, callback_data: dict):
    try:
        await Preference.update(id=callback_data["preference_id"], value=callback_data["value"])
    except HttpError:
        await call.answer("Не удалось установить значение")
    else:
        await call.answer("Значение установлено")
        await bot_preferences_callback(call=call, callback_data=callback_data)


@dp.callback_query_handler(preference_update_enabled_callback.filter(), state="*")
async def bot_preference_update_enabled_callback(call: CallbackQuery, callback_data: dict):
    try:
        preference = await Preference.update(id=callback_data["preference_id"],
                                             enabled=callback_data["enabled"] == "True")
    except HttpError:
        await call.answer("Не удалось установить значение")
    else:
        await call.answer("✔️ Включено" if preference.enabled else "❌ Отключено")
        await bot_preferences_callback(call=call, callback_data=callback_data)
