from datetime import datetime, timedelta
from typing import List

from utils.polyrobot.base import Deserializable
from utils.polyrobot.constants import WEEKDAYS


class LessonRoom(Deserializable):
    number: str

    def __init__(self, number: str):
        self.number = number

    def to_message_text(self) -> str:
        return self.number


class LessonPlace:
    title: str
    link: str
    rooms: List[LessonRoom]

    ROOMS = "rooms"

    def __init__(self, title: str, link: str = None, rooms: List[LessonRoom] = None):
        self.title = title
        self.link = link
        self.rooms = rooms

    @classmethod
    def deserialize(cls, data: dict):
        data[cls.ROOMS] = [LessonRoom.deserialize(room) for room in data[cls.ROOMS]]
        return cls(**data)

    def to_message_text(self) -> str:
        if self.link:
            return f"🔗 <a href='{self.link}'>{self.title}</a>"
        else:
            return f"🏫 {self.title}: " + ", ".join(room.to_message_text() for room in self.rooms)


class LessonTeacher(Deserializable):
    full_name: str

    def __init__(self, full_name: str):
        self.full_name = full_name

    def to_message_text(self) -> str:
        return f"<i>{self.full_name}</i>"


class Lesson:
    title: str
    group: str
    type: str
    place: LessonPlace
    teachers: List[LessonTeacher]

    PLACE = "place"
    TEACHERS = "teachers"

    def __init__(self, title: str, group: str, type: str, place: LessonPlace, teachers: List[LessonTeacher]):
        self.title = title
        self.group = group
        self.type = type
        self.place = place
        self.teachers = teachers

    @classmethod
    def deserialize(cls, data: dict):
        data[cls.PLACE] = LessonPlace.deserialize(data[cls.PLACE])
        data[cls.TEACHERS] = [LessonTeacher.deserialize(teacher) for teacher in data[cls.TEACHERS]]
        return cls(**data)

    def to_message_text(self) -> str:
        return f"{self.place.to_message_text()}\n<b>{self.title} ({self.type})</b>\n" + \
               ", ".join([teacher.to_message_text() for teacher in self.teachers])


class ScheduledLesson:
    id: str
    lesson: Lesson
    datetime: datetime

    LESSON = "lesson"
    DATETIME = "datetime"

    TODAY = "today"

    def __init__(self, id: str, lesson: Lesson, datetime: datetime):
        self.id = id
        self.lesson = lesson
        self.datetime = datetime

    @classmethod
    def deserialize(cls, data: dict):
        data[cls.LESSON] = Lesson.deserialize(data[cls.LESSON])
        data[cls.DATETIME] = datetime.fromisoformat(data[cls.DATETIME])
        return cls(**data)

    @property
    def time_text(self) -> str:
        from_time = self.datetime.strftime("%H:%M")
        to_time = (self.datetime + timedelta(hours=1, minutes=30)).strftime("%H:%M")
        return f"🕘 {from_time} – {to_time}"

    def to_message_text(self, with_date: bool = True) -> str:
        if with_date:
            datetime_title = f"📆 <b>{self.datetime.strftime('%d.%m.%Y %H:%M')}</b>\n🎓 <b>{WEEKDAYS[self.datetime.weekday()]}</b>\n\n"
        else:
            datetime_title = self.time_text + "\n"

        return datetime_title + self.lesson.to_message_text()
