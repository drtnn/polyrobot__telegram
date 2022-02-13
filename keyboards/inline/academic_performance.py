from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callback_data import academic_performance_semester, academic_performance_lesson, academic_performance


def select_semester_buttons(semesters_count: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*[
        InlineKeyboardButton(f'{num} семестр', callback_data=academic_performance_semester.new(semester_number=num))
        for num in range(1, semesters_count + 1)
    ])
    return keyboard


def select_lesson_buttons(semester_number: str, id_to_lesson_title: dict) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*[
        InlineKeyboardButton(
            lesson_title, callback_data=academic_performance_lesson.new(semester_number=semester_number, lesson_id=id)
        ) for id, lesson_title in id_to_lesson_title.items()
    ])
    keyboard.add(InlineKeyboardButton("🔙", callback_data=academic_performance.new()))
    return keyboard


def lesson_buttons(semester_number: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🔙", callback_data=academic_performance_semester.new(semester_number=semester_number))
    )
    return keyboard
