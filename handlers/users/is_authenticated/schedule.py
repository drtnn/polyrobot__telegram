import mimetypes
import os
from datetime import datetime, date
from io import BytesIO
from time import time_ns

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.default.base import SCHEDULE_BUTTON
from keyboards.inline.callback_data import schedule_callback, scheduled_lesson_callback, scheduled_lesson_note_callback, \
    scheduled_lesson_add_note_callback, scheduled_lesson_note_add_file_callback, scheduled_lesson_delete_note_callback
from keyboards.inline.schedule import schedule_buttons, scheduled_lesson_buttons, scheduled_lesson_note_buttons, \
    scheduled_lesson_add_file_buttons
from loader import dp, bot, tz
from states.schedule import ScheduledLessonNoteState
from utils.polyrobot.messages import schedule_message_text
from utils.polyrobot.schedule import ScheduledLesson, ScheduledLessonNote
from utils.polyrobot.user import User


@dp.message_handler(text=SCHEDULE_BUTTON, is_authenticated=True, state="*")
@dp.message_handler(commands=["schedule"], is_authenticated=True, state="*")
async def bot_schedule_command(message: Message):
    user = User(message.from_user.id, message.from_user.full_name, message.from_user.username)
    date_obj = datetime.now(tz=tz).date()
    scheduled_lessons = await user.scheduled_lesson(datetime_obj=date_obj)

    await message.answer(text=schedule_message_text(date_obj=date_obj, scheduled_lessons=scheduled_lessons),
                         reply_markup=schedule_buttons(date_obj, scheduled_lessons), disable_web_page_preview=True)


@dp.callback_query_handler(schedule_callback.filter(), state="*")
async def bot_schedule_date_callback(call: CallbackQuery, callback_data: dict):
    if callback_data["date"] == ScheduledLesson.TODAY:
        date_obj = datetime.now(tz=tz).date()
    else:
        date_obj = date.fromisoformat(callback_data["date"])
    user = User(call.from_user.id, call.from_user.full_name, call.from_user.username)
    scheduled_lessons = await user.scheduled_lesson(datetime_obj=date_obj)

    await call.message.edit_text(text=schedule_message_text(date_obj=date_obj, scheduled_lessons=scheduled_lessons),
                                 reply_markup=schedule_buttons(date_obj=date_obj, scheduled_lessons=scheduled_lessons),
                                 disable_web_page_preview=True)


@dp.callback_query_handler(scheduled_lesson_callback.filter(), state="*")
async def bot_scheduled_lesson_callback(call: CallbackQuery, callback_data: dict):
    scheduled_lesson: ScheduledLesson = await ScheduledLesson.get(id=callback_data["scheduled_lesson_id"])
    notes = await scheduled_lesson.notes()

    await call.message.edit_text(text=scheduled_lesson.message_text(),
                                 reply_markup=scheduled_lesson_buttons(scheduled_lesson=scheduled_lesson, notes=notes),
                                 disable_web_page_preview=True)


@dp.callback_query_handler(scheduled_lesson_add_note_callback.filter(), state="*")
async def bot_scheduled_lesson_add_note_callback(call: CallbackQuery, callback_data: dict):
    state = dp.current_state(user=call.from_user.id)
    await state.update_data(scheduled_lesson_id=callback_data["scheduled_lesson_id"])
    await ScheduledLessonNoteState.text.set()

    await call.answer(text="🤖 Пришли текст для новой заметки ")


@dp.message_handler(is_authenticated=True, state=ScheduledLessonNoteState.text)
async def bot_scheduled_lesson_add_note_text(message: Message, state: FSMContext):
    data = await state.get_data()
    note = await ScheduledLessonNote.create(created_by=message.from_user.id,
                                            scheduled_lesson_id=data["scheduled_lesson_id"], text=message.text)
    await state.update_data(scheduled_lesson_note_id=note.id, text=message.text)
    await ScheduledLessonNoteState.file.set()

    await message.answer(
        text="🤖 Теперь можешь прислать мне файл/фото/видео, а я прикреплю его к заметке. Или нажми на кнопку ниже, чтобы сохранить заметку без вложений.",
        reply_markup=scheduled_lesson_add_file_buttons(scheduled_lesson_note=note)
    )


@dp.message_handler(content_types=["photo", "video", "document"], is_authenticated=True,
                    state=ScheduledLessonNoteState.file)
async def bot_scheduled_lesson_add_note_file(message: Message, state: FSMContext):
    data = await state.get_data()
    note = ScheduledLessonNote(id=data["scheduled_lesson_note_id"], scheduled_lesson=data["scheduled_lesson_id"],
                               text=data["text"], created_by=message.from_user.id)

    bytes_io = BytesIO()

    if message.document:
        file = message.document
    elif message.video:
        file = message.video
    elif message.photo:
        file = message.photo[-1]

    file_info = await bot.get_file(file.file_id)
    mime_type, _ = mimetypes.guess_type(file_info.file_path)
    _, file_extension = os.path.splitext(file_info.file_path)
    file_data = (str(time_ns()) + file_extension, await file.download(destination=bytes_io), mime_type)

    note = await note.add_files(file_data)

    await message.answer(
        text="🤖 Можешь прислать мне еще один файл/фото/видео, а я прикреплю его к заметке. Или нажми на кнопку ниже, чтобы сохранить заметку без вложений.",
        reply_markup=scheduled_lesson_add_file_buttons(scheduled_lesson_note=note)
    )


@dp.callback_query_handler(scheduled_lesson_note_callback.filter(), state="*")
async def bot_scheduled_lesson_note_callback(call: CallbackQuery, callback_data: dict):
    state = dp.current_state(user=call.from_user.id)
    await state.reset_state(with_data=True)

    note = await ScheduledLessonNote.get(id=callback_data["scheduled_lesson_note_id"])

    await call.message.edit_text(
        text=note.text,
        reply_markup=scheduled_lesson_note_buttons(scheduled_lesson_note=note,
                                                   for_creator=call.from_user.id == note.created_by)
    )


@dp.callback_query_handler(scheduled_lesson_delete_note_callback.filter(), state="*")
async def bot_scheduled_lesson_delete_note_callback(call: CallbackQuery, callback_data: dict):
    note = await ScheduledLessonNote.get(id=callback_data["scheduled_lesson_note_id"])
    await note.delete()

    return await bot_scheduled_lesson_callback(call=call, callback_data={"scheduled_lesson_id": note.scheduled_lesson})


@dp.callback_query_handler(scheduled_lesson_note_add_file_callback.filter(), state="*")
async def bot_scheduled_lesson_note_add_file_callback(call: CallbackQuery, callback_data: dict):
    note = await ScheduledLessonNote.get(id=callback_data["scheduled_lesson_note_id"])

    state = dp.current_state(user=call.from_user.id)
    await state.update_data(scheduled_lesson_id=note.scheduled_lesson, scheduled_lesson_note_id=note.id, text=note.text)
    await ScheduledLessonNoteState.file.set()

    await call.answer("🤖 Теперь можешь прислать мне файл/фото/видео, а я прикреплю его к заметке.")
