from datetime import datetime, timedelta
from typing import List
from urllib.parse import urlencode

from utils.polyrobot import api_service as APIService
from utils.polyrobot.base import Deserializable
from utils.polyrobot.constants import WEEKDAYS
from utils.polyrobot.file import File


class LessonRoom(Deserializable):
    number: str

    def message_text(self) -> str:
        return self.number


class LessonPlace(Deserializable):
    title: str
    link: str
    rooms: List[LessonRoom]

    ROOMS = "rooms"

    @classmethod
    def deserialize(cls, data: dict):
        data[cls.ROOMS] = [LessonRoom.deserialize(room) for room in data[cls.ROOMS]]
        return super().deserialize(data)

    def message_text(self) -> str:
        if self.link:
            return f"🔗 <a href='{self.link}'>{self.title}</a>"
        else:
            return f"🏫 {self.title}: " + ", ".join(room.message_text() for room in self.rooms)


class LessonTeacher(Deserializable):
    full_name: str

    def message_text(self) -> str:
        return f"<i>{self.full_name}</i>"


class Lesson(Deserializable):
    title: str
    group: str
    type: str
    place: LessonPlace
    teachers: List[LessonTeacher]

    PLACE = "place"
    TEACHERS = "teachers"

    @classmethod
    def deserialize(cls, data: dict):
        data[cls.PLACE] = LessonPlace.deserialize(data[cls.PLACE])
        data[cls.TEACHERS] = [LessonTeacher.deserialize(teacher) for teacher in data[cls.TEACHERS]]
        return super().deserialize(data)

    def message_text(self) -> str:
        return f"{self.place.message_text()}\n<b>{self.title} ({self.type})</b>\n" + \
               ", ".join(teacher.message_text() for teacher in self.teachers)


class ScheduledLesson(Deserializable):
    id: str
    lesson: Lesson
    datetime: datetime

    LESSON = "lesson"
    DATETIME = "datetime"

    TODAY = "today"

    @classmethod
    def deserialize(cls, data: dict):
        data[cls.LESSON] = Lesson.deserialize(data[cls.LESSON])
        data[cls.DATETIME] = datetime.fromisoformat(data[cls.DATETIME])
        return super().deserialize(data)

    @classmethod
    async def get(cls, id: int):
        data = await APIService.get(f"/scheduled-lesson/{id}/")
        return cls.deserialize(data)

    @property
    def time_text(self) -> str:
        from_time = self.datetime.strftime("%H:%M")
        to_time = (self.datetime + timedelta(hours=1, minutes=30)).strftime("%H:%M")
        return f"🕘 {from_time} – {to_time}"

    def message_text(self, with_date: bool = True) -> str:
        if with_date:
            datetime_title = f"📆 <b>{self.datetime.strftime('%d.%m.%Y %H:%M')}</b>\n🎓 <b>{WEEKDAYS[self.datetime.weekday()]}</b>\n\n"
        else:
            datetime_title = self.time_text + "\n"

        return datetime_title + self.lesson.message_text()

    async def notes(self):
        data = await APIService.get(f"/scheduled-lesson/{self.id}/note")
        return [ScheduledLessonNote.deserialize(note) for note in data]


class ScheduledLessonNote(Deserializable):
    id: str
    scheduled_lesson: str
    text: str
    created_by: int
    files: List[File]

    FILES = "files"
    CREATED_BY = "created_by"

    @classmethod
    def deserialize(cls, data: dict):
        data[cls.FILES] = [File.deserialize(file) for file in data[cls.FILES]]
        return super().deserialize(data)

    @classmethod
    async def get(cls, id: str):
        data = await APIService.get(f"/scheduled-lesson-note/{id}/")
        return cls.deserialize(data)

    @classmethod
    async def create(cls, created_by: int, scheduled_lesson_id: str, text: str):
        data = await APIService.post(f"/scheduled-lesson/{scheduled_lesson_id}/add-note/", json={
            "created_by": created_by,
            "scheduled_lesson": scheduled_lesson_id,
            "text": text
        })
        return cls.deserialize(data)

    async def add_files(self, *files: tuple):
        files = await File.upload(*files)

        data = await APIService.post(f"/scheduled-lesson-note/{self.id}/add-file/", json={
            "files": [file.id for file in files]
        })

        return self.deserialize(data)

    async def delete(self):
        await APIService.delete(f"/scheduled-lesson-note/{self.id}/")


class ScheduledLessonNotification(Deserializable):
    id: str
    scheduled_lesson: ScheduledLesson
    telegram_user: int
    notify_at: datetime

    SCHEDULED_LESSON = "scheduled_lesson"
    NOTIFY_AT = "notify_at"

    @classmethod
    def deserialize(cls, data: dict):
        data[cls.SCHEDULED_LESSON] = ScheduledLesson.deserialize(data[cls.SCHEDULED_LESSON])
        data[cls.NOTIFY_AT] = datetime.fromisoformat(data[cls.NOTIFY_AT])
        return super().deserialize(data)

    @classmethod
    async def filter(cls, notify_from: datetime = None, notify_to: datetime = None):
        query_params = {}

        if notify_from:
            query_params['notify_from'] = notify_from.strftime('%Y-%m-%dT%H:%M:%S')
        if notify_to:
            query_params['notify_to'] = notify_to.strftime('%Y-%m-%dT%H:%M:%S')

        url = f"/scheduled-lesson-notification?" + urlencode(query_params)
        return [cls.deserialize(notification) for notification in await APIService.get(url)]
