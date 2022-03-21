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

    def __init__(self, id: str, bill_num: str, bill_type: str, doc_type: str, name: str, exam_date: str, exam_time: str,
                 grade: str, ticket_num: str, teacher: str, course: str, exam_type: str, chair: str, **kwargs):
        self.id = id
        self.bill_num = bill_num
        self.bill_type = bill_type
        self.doc_type = doc_type
        self.name = name
        self.exam_date = datetime.strptime(exam_date, "%B %d, %Y").date()
        self.exam_time = exam_time
        self.grade = grade
        self.ticket_num = ticket_num
        self.teacher = teacher
        self.course = course
        self.exam_type = exam_type
        self.chair = chair

        for key, value in kwargs:
            setattr(self, key, value)

    def to_message_text(self):
        return f"🧑🏻‍🏫 <b>{self.name}</b>\n\n<b>Курс:</b> {self.course}\n<b>Форма аттестации:</b> {self.exam_type}\n<b>Дата проведения:</b> {self.exam_date.strftime('%d.%m.%Y')}\n<b>Оценка:</b> {self.grade}\n\n<b>Преподаватель:</b> <code>{self.teacher}</code>\n<b>Кафедра:</b> <code>{self.chair}</code>"
