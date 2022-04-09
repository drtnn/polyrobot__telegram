from collections import defaultdict
from datetime import date
from typing import List

from utils.polyrobot.academic_performance import AcademicPerformance
from utils.polyrobot.constants import WEEKDAYS
from utils.polyrobot.schedule import ScheduledLesson


def schedule_message_text(date_obj: date, scheduled_lessons: List[ScheduledLesson]) -> str:
    if scheduled_lessons:
        date_title = f"📆 <b>{date_obj.strftime('%d.%m.%Y')}</b>\n🎓 <b>{WEEKDAYS[date_obj.weekday()]}</b>\n\n"
        return date_title + "\n\n".join(
            scheduled_lesson.message_text(with_date=False) for scheduled_lesson in scheduled_lessons
        )
    else:
        return f"📆 <b>{date_obj.strftime('%d.%m.%Y')}</b>\n🥳 <b>{WEEKDAYS[date_obj.weekday()]} – выходной!</b>"


def performance_semester_message_text() -> str:
    return "🧑🏻‍🏫 <b>Успеваемость</b>\n\nВ данном разделе отображается информация о результатах сдачи зачетно-экзаменационных сессий. Выбери семестр из списка ниже:"


def performance_lesson_message_text(academic_performances: List[AcademicPerformance]) -> str:
    text = "🧑🏻‍🏫 <b>Успеваемость</b>\n\n"
    academic_performance_by_type = defaultdict(list)

    for academic_performance in academic_performances:
        academic_performance_by_type[academic_performance.exam_type].append(academic_performance)

    for exam_type, academic_performances in academic_performance_by_type.items():
        text += (f"<b>{exam_type}</b>\n" + "\n".join(
            f"<b>{academic_performance.name}</b> – {academic_performance.grade}" for academic_performance in
            academic_performances
        ) + "\n\n")
    return text
