from datetime import datetime, date

from utils.polyrobot.base import Deserializable


class AcademicPerformance(Deserializable):
    id: str
    bill_num: str
    bill_type: str
    doc_type: str
    name: str
    exam_date: date
    exam_time: str
    grade: str
    ticket_num: str
    teacher: str
    course: str
    exam_type: str
    chair: str

    EXAM_DATE = "exam_date"

    @classmethod
    def deserialize(cls, data: dict):
        data[cls.EXAM_DATE] = datetime.strptime(data[cls.EXAM_DATE], "%B %d, %Y").date()
        return super().deserialize(data)

    def message_text(self):
        return f"🧑🏻‍🏫 <b>{self.name}</b>\n\n<b>Курс:</b> {self.course}\n<b>Форма аттестации:</b> {self.exam_type}\n<b>Дата проведения:</b> {self.exam_date.strftime('%d.%m.%Y')}\n<b>Оценка:</b> {self.grade}\n\n<b>Преподаватель:</b> <code>{self.teacher}</code>\n<b>Кафедра:</b> <code>{self.chair}</code>"
