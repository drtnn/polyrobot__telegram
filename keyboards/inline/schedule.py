from datetime import date, timedelta
from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.polyrobot.constants import WEEKDAYS
from utils.polyrobot.schedule import ScheduledLesson, ScheduledLessonNote
from .callback_data import schedule_callback, scheduled_lesson_callback, scheduled_lesson_note_callback, \
    scheduled_lesson_add_note_callback, scheduled_lesson_delete_note_callback, scheduled_lesson_note_add_file_callback


def schedule_buttons(date_obj: date, scheduled_lessons: List[ScheduledLesson]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    yesterday = date_obj - timedelta(days=1)
    tomorrow = date_obj + timedelta(days=1)

    for scheduled_lesson in scheduled_lessons:
        keyboard.row(
            InlineKeyboardButton(
                text=("π§π»βπ» " if scheduled_lesson.lesson.place.link else "π§π»βπ« ") + scheduled_lesson.lesson.title,
                callback_data=scheduled_lesson_callback.new(scheduled_lesson_id=scheduled_lesson.id)
            )
        )

    keyboard.add(
        InlineKeyboardButton(
            text=f"π {WEEKDAYS[yesterday.weekday()]}",
            callback_data=schedule_callback.new(date=yesterday.isoformat())
        ),
        InlineKeyboardButton(
            text=f"{WEEKDAYS[tomorrow.weekday()]} π",
            callback_data=schedule_callback.new(date=tomorrow.isoformat())
        )
    )
    if date.today() != date_obj:
        keyboard.add(
            InlineKeyboardButton(text="π Π‘Π΅Π³ΠΎΠ΄Π½Ρ", callback_data=schedule_callback.new(date=ScheduledLesson.TODAY))
        )
    return keyboard


def scheduled_lesson_buttons(
        scheduled_lesson: ScheduledLesson, notes: List[ScheduledLessonNote]
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        *[
            InlineKeyboardButton(
                text=note.text[:20] if len(note.text) > 20 else note.text,
                callback_data=scheduled_lesson_note_callback.new(scheduled_lesson_note_id=note.id)
            ) for note in notes
        ]
    )

    keyboard.row(
        InlineKeyboardButton(
            text="βοΈ ΠΠΎΠ±Π°Π²ΠΈΡΡ Π·Π°ΠΌΠ΅ΡΠΊΡ",
            callback_data=scheduled_lesson_add_note_callback.new(scheduled_lesson_id=scheduled_lesson.id)
        )
    )

    keyboard.row(
        InlineKeyboardButton(
            text="π",
            callback_data=schedule_callback.new(date=scheduled_lesson.datetime.date().isoformat())
        )
    )
    return keyboard


def scheduled_lesson_note_buttons(
        scheduled_lesson_note: ScheduledLessonNote, for_creator: bool = False
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    files = scheduled_lesson_note.files
    keyboard.add(*[InlineKeyboardButton(f"Π€Π°ΠΉΠ» β{number + 1}", url=files[number].data) for number in range(len(files))])

    if for_creator:
        keyboard.row(
            InlineKeyboardButton(
                text="β ΠΠΎΠ±Π°Π²ΠΈΡΡ ΡΠ°ΠΉΠ»",
                callback_data=scheduled_lesson_note_add_file_callback.new(
                    scheduled_lesson_note_id=scheduled_lesson_note.id
                )
            )
        )
        keyboard.row(
            InlineKeyboardButton(
                text="β Π£Π΄Π°Π»ΠΈΡΡ Π·Π°ΠΌΠ΅ΡΠΊΡ",
                callback_data=scheduled_lesson_delete_note_callback.new(
                    scheduled_lesson_note_id=scheduled_lesson_note.id
                )
            )
        )

    keyboard.row(
        InlineKeyboardButton(
            text="π",
            callback_data=scheduled_lesson_callback.new(scheduled_lesson_id=scheduled_lesson_note.scheduled_lesson)
        )
    )
    return keyboard


def scheduled_lesson_add_file_buttons(scheduled_lesson_note: ScheduledLessonNote):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            text="βοΈ",
            callback_data=scheduled_lesson_note_callback.new(scheduled_lesson_note_id=scheduled_lesson_note.id)
        )
    )
    return keyboard
