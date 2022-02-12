from datetime import date
from typing import List

from utils.polyrobot.constants import WEEKDAYS
from utils.polyrobot.schedule import ScheduledLesson


def generate_one_day_schedule_message_text(date_obj: date, scheduled_lessons: List[ScheduledLesson]) -> str:
    if scheduled_lessons:
        date_title = f"📆 <b>{date_obj.strftime('%d.%m.%Y')}</b>\n🎓 <b>{WEEKDAYS[date_obj.weekday()]}</b>\n\n"
        return date_title + '\n\n'.join(
            [scheduled_lesson.to_message_text(with_date=False) for scheduled_lesson in scheduled_lessons])
    else:
        return f"📆 <b>{date_obj.strftime('%d.%m.%Y')}</b>\n🥳 <b>{WEEKDAYS[date_obj.weekday()]} – выходной!</b>"
