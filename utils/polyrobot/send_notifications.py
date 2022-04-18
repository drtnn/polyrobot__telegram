import asyncio
import logging
from datetime import datetime, timedelta

from keyboards.inline.schedule import scheduled_lesson_buttons
from loader import bot, tz
from utils.polyrobot.schedule import ScheduledLessonNotification

logger = logging.getLogger(__name__)


async def notify_about_scheduled_lessons(sleep_time: int = 20):
    last_datetime = datetime.now(tz=tz) - timedelta(seconds=sleep_time)

    while True:
        now = datetime.now(tz=tz)

        try:
            notifications = await ScheduledLessonNotification.filter(notify_from=last_datetime, notify_to=now)
        except Exception as e:
            logger.info(f"NotificationsError: {e}")
            await asyncio.sleep(sleep_time)
            continue

        last_datetime = now

        for notification in notifications:
            notification: ScheduledLessonNotification

            notes = await notification.scheduled_lesson.notes()
            try:
                await bot.send_message(chat_id=notification.telegram_user,
                                       text=notification.scheduled_lesson.message_text(),
                                       reply_markup=scheduled_lesson_buttons(scheduled_lesson=notification.scheduled_lesson,
                                                                             notes=notes),
                                       disable_web_page_preview=True)
            except Exception as e:
                logger.info(f"NotificationSendError: {e}")

        await asyncio.sleep(sleep_time)
