from typing import List

from inflection import camelize
from utils.polyrobot.base import Deserializable


class Profile(Deserializable):
    id: int
    user_status: str
    status: str
    course: str
    name: str
    surname: str
    patronymic: str
    avatar: str
    birthday: str
    sex: str
    code: str
    faculty: str
    group: str
    specialty: str
    specialization: str
    degree_length: str
    education_form: str
    finance: str
    degree_level: str
    enter_year: str
    orders: List[str]

    DEGREE_LENGTH = "degree_length"
    EDUCATION_FORM = "education_form"
    DEGREE_LEVEL = "degree_level"
    ENTER_LEVEL = "enter_year"

    def __init__(self, id: int, user_status: str, status: str, course: str, name: str, surname: str, patronymic: str,
                 avatar: str, birthday: str, sex: str, code: str, faculty: str, group: str, specialty: str,
                 specialization: str, degree_length: str, education_form: str, finance: str, degree_level: str,
                 enter_year: str, orders: List[str], **kwargs):
        self.id = id
        self.user_status = user_status
        self.status = status
        self.course = course
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.avatar = avatar
        self.birthday = birthday
        self.sex = sex
        self.code = code
        self.faculty = faculty
        self.group = group
        self.specialty = specialty
        self.specialization = specialization
        self.degree_length = degree_length
        self.education_form = education_form
        self.finance = finance
        self.degree_level = degree_level
        self.enter_year = enter_year
        self.orders = orders

        for key, value in kwargs:
            setattr(self, key, value)

    @classmethod
    def deserialize(cls, data: dict):
        data[cls.DEGREE_LENGTH] = data.pop(camelize(cls.DEGREE_LENGTH, uppercase_first_letter=False))
        data[cls.EDUCATION_FORM] = data.pop(camelize(cls.EDUCATION_FORM, uppercase_first_letter=False))
        data[cls.DEGREE_LEVEL] = data.pop(camelize(cls.DEGREE_LEVEL, uppercase_first_letter=False))
        data[cls.ENTER_LEVEL] = data.pop(camelize(cls.ENTER_LEVEL, uppercase_first_letter=False))
        return super().deserialize(data)

    def to_message_text(self) -> str:
        return f"👨🏻‍🎓 <b>{self.surname} {self.name} {self.patronymic}</b>\n\n<b>Код студента:</b> {self.code}\n<b>Группа:</b> {self.group}\n<b>Год набора:</b> {self.enter_year}\n<b>Форма обучения:</b> {self.education_form}\n<b>Вид финансирования:</b> {self.finance}\n<b>Уровень образования:</b> {self.degree_level}\n\n<b>Факультет:</b> <code>{self.faculty}</code>\n<b>Специальность:</b> <code>{self.specialty}</code>\n<b>Специализация:</b> <code>{self.specialization}</code>"

    def orders_to_message_text(self) -> str:
        return "\n".join("・ " + order for order in self.orders)
