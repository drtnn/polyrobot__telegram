from datetime import datetime, date
from typing import List

from inflection import camelize

from utils.polyrobot.base import Deserializable


class Payment(Deserializable):
    id: str
    contragent: str
    student: str
    number: str
    name: str
    type: str
    level: str
    dorm_num: str
    dorm_room: str
    file: str
    bill: str
    can_sign: bool
    signed_user: bool
    signed_user_date: str
    signed_user_time: str
    start_date: date
    end_date_plan: date
    end_date_fact: date
    qr_current: str
    qr_total: str
    sum: str
    balance: str
    balance_currdate: str
    last_payment_date: date
    payments: List[dict]
    agreements: List[dict]
    paygraph: List[dict]

    START_DATE = "start_date"
    END_DATE_PLAN = "end_date_plan"
    END_DATE_FACT = "end_date_fact"
    LAST_PAYMENT_DATE = "last_payment_date"

    @classmethod
    def deserialize(cls, data: dict):
        data[cls.START_DATE] = data.pop(camelize(cls.START_DATE, uppercase_first_letter=False))
        data[cls.END_DATE_PLAN] = data.pop(camelize(cls.END_DATE_PLAN, uppercase_first_letter=False))
        data[cls.END_DATE_FACT] = data.pop(camelize(cls.END_DATE_FACT, uppercase_first_letter=False))
        data[cls.LAST_PAYMENT_DATE] = data.pop(camelize(cls.LAST_PAYMENT_DATE, uppercase_first_letter=False))

        data[cls.START_DATE] = datetime.strptime(data[cls.START_DATE], "%B %d, %Y")
        data[cls.END_DATE_PLAN] = datetime.strptime(data[cls.END_DATE_PLAN], "%B %d, %Y")
        if data[cls.END_DATE_FACT]:
            data[cls.END_DATE_FACT] = datetime.strptime(data[cls.END_DATE_FACT], "%B %d, %Y")
        data[cls.LAST_PAYMENT_DATE] = datetime.strptime(data[cls.LAST_PAYMENT_DATE], "%B %d, %Y")
        return super().deserialize(data)

    @property
    def end_date(self):
        return self.end_date_fact if self.end_date_fact else self.end_date_plan

    def message_text(self):
        return "\n\n".join(
            [
                f"💴 {self.type}",
                "\n".join(
                    [
                        f"<b>Номер договора:</b> {self.number}",
                        f"<b>Начало действия договора:</b> {self.start_date.strftime('%d.%m.%Y')}",
                        f"<b>Окончание действия договора:</b> {self.end_date.strftime('%d.%m.%Y')}",
                        f"<b>Сумма к оплате:</b> {self.sum} руб.",
                    ]
                ),
                "\n".join(
                    [
                        f"<b>Долг:</b> {self.balance_currdate} руб.",
                        f"<b>Дата последнего платежа:</b> {self.last_payment_date.strftime('%d.%m.%Y')}",
                        f"<b>К выплате до конца действия договора:</b> {self.balance} руб.",
                    ]
                )
            ]
        )


class Payments(Deserializable):
    education: List[Payment]
    dormitory: List[Payment]

    EDUCATION = "education"
    DORMITORY = "dormitory"

    @classmethod
    def deserialize(cls, data: dict):
        data[cls.EDUCATION] = [Payment.deserialize(payment) for payment in data[cls.EDUCATION]]
        data[cls.DORMITORY] = [Payment.deserialize(payment) for payment in data[cls.DORMITORY]]
        return super().deserialize(data)
